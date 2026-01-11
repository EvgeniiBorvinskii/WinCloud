"""
Network Client - Handles communication with WinCloud server
Includes retry logic, timeout handling, and error recovery
"""
import requests
import time
from typing import Dict, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from common.logger import get_logger
from common.config import Config

logger = get_logger('NetworkClient')


class NetworkClient:
    """
    Network client for WinCloud server communication
    Handles:
    - File upload/download
    - Authentication
    - Connection health checks
    - Automatic retries
    """
    
    def __init__(self):
        self.config = Config()
        self.server_url = self.config.get('server_url', 'https://5.249.160.54:8443')
        self.api_version = 'v1'
        self.session = self._create_session()
        self.auth_token = None
        self.max_retries = 3
        self.timeout = 30
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry strategy"""
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "POST", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Disable SSL verification for now (should use proper certs in production)
        session.verify = False
        
        return session
    
    def check_connection(self) -> bool:
        """
        Check if server is available
        Returns True if server responds, False otherwise
        """
        try:
            url = f"{self.server_url}/api/{self.api_version}/health"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                logger.info("Server connection successful")
                return True
            else:
                logger.warning(f"Server returned status {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to server - connection refused")
            return False
        except requests.exceptions.Timeout:
            logger.error("Server connection timeout")
            return False
        except Exception as e:
            logger.error(f"Server connection check failed: {e}")
            return False
    
    def authenticate(self, user_id: Optional[str] = None) -> Dict:
        """
        Authenticate with server
        In production, this would use proper OAuth/JWT
        """
        try:
            # For now, use simple token-based auth
            # In production: implement proper authentication
            url = f"{self.server_url}/api/{self.api_version}/auth"
            
            payload = {
                'user_id': user_id or self._get_device_id(),
                'client_version': '1.0.0'
            }
            
            response = self.session.post(url, json=payload, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('token')
                logger.info("Authentication successful")
                return {'success': True, 'token': self.auth_token}
            else:
                logger.error(f"Authentication failed: {response.status_code}")
                return {'success': False, 'error': 'Authentication failed'}
                
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return {'success': False, 'error': str(e)}
    
    def upload_archive_cloud_part(
        self,
        data: bytes,
        metadata: Dict,
        chunk_size: int = 5 * 1024 * 1024  # 5MB chunks
    ) -> Dict:
        """
        Upload cloud portion (90%) to server
        Uses chunked upload for large files
        """
        try:
            logger.info(f"Uploading cloud data: {len(data)} bytes")
            
            # Ensure authentication
            if not self.auth_token:
                auth_result = self.authenticate()
                if not auth_result['success']:
                    return {'success': False, 'error': 'Authentication required'}
            
            # Create upload session
            url = f"{self.server_url}/api/{self.api_version}/archives/upload"
            
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/octet-stream'
            }
            
            # For small files, upload directly
            if len(data) < chunk_size:
                response = self.session.post(
                    url,
                    data=data,
                    headers=headers,
                    timeout=self.timeout * 2
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Upload successful: {result.get('archive_id')}")
                    return {
                        'success': True,
                        'cloud_archive_id': result['archive_id'],
                        'file_ids': result.get('file_ids', [])
                    }
                else:
                    logger.error(f"Upload failed: {response.status_code}")
                    return {'success': False, 'error': f'Server error: {response.status_code}'}
            
            # For large files, use chunked upload
            return self._chunked_upload(data, url, headers, chunk_size)
            
        except requests.exceptions.ConnectionError:
            logger.error("Upload failed: Cannot connect to server")
            return {'success': False, 'error': 'Server unavailable'}
        except requests.exceptions.Timeout:
            logger.error("Upload failed: Timeout")
            return {'success': False, 'error': 'Upload timeout'}
        except Exception as e:
            logger.error(f"Upload failed: {e}", exc_info=True)
            return {'success': False, 'error': str(e)}
    
    def _chunked_upload(
        self,
        data: bytes,
        url: str,
        headers: Dict,
        chunk_size: int
    ) -> Dict:
        """Upload large files in chunks"""
        try:
            total_size = len(data)
            uploaded = 0
            chunk_index = 0
            upload_id = None
            
            while uploaded < total_size:
                chunk_start = uploaded
                chunk_end = min(uploaded + chunk_size, total_size)
                chunk_data = data[chunk_start:chunk_end]
                
                # Add chunk headers
                chunk_headers = headers.copy()
                chunk_headers.update({
                    'X-Chunk-Index': str(chunk_index),
                    'X-Total-Size': str(total_size),
                    'X-Chunk-Size': str(len(chunk_data))
                })
                
                if upload_id:
                    chunk_headers['X-Upload-Id'] = upload_id
                
                # Upload chunk
                response = self.session.post(
                    url,
                    data=chunk_data,
                    headers=chunk_headers,
                    timeout=self.timeout * 2
                )
                
                if response.status_code != 200:
                    return {'success': False, 'error': f'Chunk {chunk_index} upload failed'}
                
                result = response.json()
                upload_id = result.get('upload_id')
                
                uploaded = chunk_end
                chunk_index += 1
                
                logger.info(f"Uploaded chunk {chunk_index}: {uploaded}/{total_size} bytes")
            
            # Finalize upload
            finalize_url = f"{url}/finalize/{upload_id}"
            response = self.session.post(finalize_url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'cloud_archive_id': result['archive_id'],
                    'file_ids': result.get('file_ids', [])
                }
            else:
                return {'success': False, 'error': 'Failed to finalize upload'}
                
        except Exception as e:
            logger.error(f"Chunked upload failed: {e}", exc_info=True)
            return {'success': False, 'error': str(e)}
    
    def download_archive_cloud_part(self, archive_id: str) -> Dict:
        """
        Download cloud portion (90%) from server
        """
        try:
            logger.info(f"Downloading cloud data: {archive_id}")
            
            # Ensure authentication
            if not self.auth_token:
                auth_result = self.authenticate()
                if not auth_result['success']:
                    return {'success': False, 'error': 'Authentication required'}
            
            url = f"{self.server_url}/api/{self.api_version}/archives/{archive_id}/download"
            
            headers = {
                'Authorization': f'Bearer {self.auth_token}'
            }
            
            response = self.session.get(
                url,
                headers=headers,
                timeout=self.timeout * 3,
                stream=True
            )
            
            if response.status_code == 200:
                # Download data
                data = b''
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        data += chunk
                
                logger.info(f"Download successful: {len(data)} bytes")
                return {'success': True, 'data': data}
            else:
                logger.error(f"Download failed: {response.status_code}")
                return {'success': False, 'error': f'Server error: {response.status_code}'}
                
        except requests.exceptions.ConnectionError:
            logger.error("Download failed: Cannot connect to server")
            return {'success': False, 'error': 'Server unavailable'}
        except requests.exceptions.Timeout:
            logger.error("Download failed: Timeout")
            return {'success': False, 'error': 'Download timeout'}
        except Exception as e:
            logger.error(f"Download failed: {e}", exc_info=True)
            return {'success': False, 'error': str(e)}
    
    def delete_archive(self, archive_id: str) -> Dict:
        """Delete archive from server"""
        try:
            if not self.auth_token:
                auth_result = self.authenticate()
                if not auth_result['success']:
                    return {'success': False, 'error': 'Authentication required'}
            
            url = f"{self.server_url}/api/{self.api_version}/archives/{archive_id}"
            
            headers = {
                'Authorization': f'Bearer {self.auth_token}'
            }
            
            response = self.session.delete(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                logger.info(f"Archive deleted: {archive_id}")
                return {'success': True}
            else:
                return {'success': False, 'error': f'Delete failed: {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Delete failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _get_device_id(self) -> str:
        """Get unique device identifier"""
        import platform
        import uuid
        
        # Generate device ID based on machine characteristics
        # In production, store this securely
        machine_id = f"{platform.node()}-{uuid.getnode()}"
        return hashlib.sha256(machine_id.encode()).hexdigest()[:16]
    
    def __del__(self):
        """Cleanup session"""
        if hasattr(self, 'session'):
            self.session.close()


import hashlib
