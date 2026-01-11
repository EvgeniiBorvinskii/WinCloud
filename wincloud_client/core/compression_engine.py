"""
Compression Engine - Core module for file compression with 10%/90% split
"""
import os
import io
import json
import time
import hashlib
import threading
from typing import List, Dict, Callable, Optional
import lzma
import zstandard as zstd

from common.logger import get_logger
from wincloud_client.core.network_client import NetworkClient
from common.file_splitter import FileSplitter
from common.crypto import CryptoManager

logger = get_logger('CompressionEngine')


class CompressionEngine:
    """
    Main compression engine that handles:
    1. File compression using LZMA2/Zstandard
    2. Splitting compressed data into 10% local + 90% cloud
    3. Uploading cloud portion to server
    4. Creating local archive with metadata
    """
    
    def __init__(self):
        self.network_client = NetworkClient()
        self.crypto_manager = CryptoManager()
        self.file_splitter = FileSplitter()
        self._cancel_flag = False
        self._lock = threading.Lock()
    
    def create_archive(
        self,
        file_paths: List[str],
        archive_path: str,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Create WinCloud archive (.wca)
        
        Args:
            file_paths: List of files to archive
            archive_path: Output archive path
            progress_callback: Function(progress, status, stats)
        
        Returns:
            Dict with success status and metadata
        """
        self._cancel_flag = False
        start_time = time.time()
        
        try:
            logger.info(f"Creating archive: {archive_path}")
            logger.info(f"Files to compress: {len(file_paths)}")
            
            # Calculate total size
            total_size = sum(os.path.getsize(f) for f in file_paths if os.path.exists(f))
            processed_size = 0
            
            # Prepare archive metadata
            archive_metadata = {
                'version': '1.0',
                'files': [],
                'created': time.time(),
                'total_size': total_size,
                'compression': 'zstd+lzma2'
            }
            
            # Local data buffer (10%)
            local_data = io.BytesIO()
            
            # Cloud data buffer (90%)
            cloud_data = io.BytesIO()
            
            # Process each file
            for idx, file_path in enumerate(file_paths):
                if self._cancel_flag:
                    return {'success': False, 'error': 'Operation cancelled'}
                
                if not os.path.exists(file_path):
                    logger.warning(f"File not found: {file_path}")
                    continue
                
                # Update progress
                if progress_callback:
                    progress = int((processed_size / total_size) * 100) if total_size > 0 else 0
                    speed = processed_size / (time.time() - start_time + 0.001) / (1024 * 1024)
                    
                    progress_callback(
                        progress,
                        f"Compressing: {os.path.basename(file_path)} ({idx + 1}/{len(file_paths)})",
                        {
                            'speed': speed,
                            'processed': processed_size,
                            'remaining': total_size - processed_size
                        }
                    )
                
                # Compress and split file
                result = self._compress_and_split_file(file_path)
                
                if not result['success']:
                    logger.error(f"Failed to compress {file_path}: {result.get('error')}")
                    continue
                
                # Write local part (10%)
                local_data.write(result['local_part'])
                
                # Write cloud part (90%)
                cloud_data.write(result['cloud_part'])
                
                # Add file metadata
                file_metadata = {
                    'name': os.path.basename(file_path),
                    'path': file_path,
                    'size': result['original_size'],
                    'compressed_size': result['compressed_size'],
                    'local_offset': result['local_offset'],
                    'local_size': result['local_size'],
                    'cloud_offset': result['cloud_offset'],
                    'cloud_size': result['cloud_size'],
                    'checksum': result['checksum'],
                    'cloud_id': None  # Will be set after upload
                }
                
                archive_metadata['files'].append(file_metadata)
                processed_size += result['original_size']
            
            # Upload cloud portion
            if progress_callback:
                progress_callback(
                    80,
                    "Uploading to cloud server...",
                    {'speed': 0, 'processed': processed_size, 'remaining': 0}
                )
            
            cloud_upload_result = self._upload_cloud_data(
                cloud_data.getvalue(),
                archive_metadata
            )
            
            if cloud_upload_result['success']:
                # Update metadata with cloud IDs
                for idx, file_meta in enumerate(archive_metadata['files']):
                    file_meta['cloud_id'] = cloud_upload_result['file_ids'][idx]
                
                logger.info(f"Cloud data uploaded successfully: {cloud_upload_result['cloud_archive_id']}")
                archive_metadata['cloud_archive_id'] = cloud_upload_result['cloud_archive_id']
            else:
                logger.warning("Cloud upload failed, archive will be local-only")
                archive_metadata['cloud_archive_id'] = None
                archive_metadata['cloud_error'] = cloud_upload_result.get('error')
            
            # Create final archive file
            if progress_callback:
                progress_callback(
                    95,
                    "Writing archive file...",
                    {'speed': 0, 'processed': processed_size, 'remaining': 0}
                )
            
            self._write_archive_file(
                archive_path,
                archive_metadata,
                local_data.getvalue()
            )
            
            # Calculate compression ratio
            archive_size = os.path.getsize(archive_path)
            compression_ratio = (1 - archive_size / total_size) * 100 if total_size > 0 else 0
            
            # Final progress update
            if progress_callback:
                progress_callback(
                    100,
                    "Archive created successfully!",
                    {
                        'speed': 0,
                        'processed': total_size,
                        'remaining': 0,
                        'compression_ratio': compression_ratio
                    }
                )
            
            elapsed_time = time.time() - start_time
            logger.info(f"Archive created in {elapsed_time:.2f}s")
            logger.info(f"Original size: {total_size / (1024*1024):.2f} MB")
            logger.info(f"Archive size: {archive_size / (1024*1024):.2f} MB")
            logger.info(f"Compression ratio: {compression_ratio:.2f}%")
            
            return {
                'success': True,
                'message': f'Archive created successfully!\n'
                          f'Original: {total_size / (1024*1024):.2f} MB\n'
                          f'Compressed: {archive_size / (1024*1024):.2f} MB\n'
                          f'Ratio: {compression_ratio:.1f}%',
                'archive_path': archive_path,
                'metadata': archive_metadata
            }
            
        except Exception as e:
            logger.error(f"Archive creation failed: {e}", exc_info=True)
            return {'success': False, 'error': str(e)}
    
    def _compress_and_split_file(self, file_path: str) -> Dict:
        """Compress file and split into 10%/90% parts"""
        try:
            # Read file
            with open(file_path, 'rb') as f:
                original_data = f.read()
            
            original_size = len(original_data)
            
            # Calculate checksum
            checksum = hashlib.sha256(original_data).hexdigest()
            
            # Compress using Zstandard (fast) + LZMA2 (high compression)
            # First pass: Zstandard for speed
            compressor = zstd.ZstdCompressor(level=10)
            compressed_zstd = compressor.compress(original_data)
            
            # Second pass: LZMA2 for maximum compression
            compressed_data = lzma.compress(
                compressed_zstd,
                format=lzma.FORMAT_XZ,
                preset=9
            )
            
            compressed_size = len(compressed_data)
            
            # Split: 10% local, 90% cloud
            split_result = self.file_splitter.split_data(
                compressed_data,
                local_percentage=10
            )
            
            return {
                'success': True,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'local_part': split_result['local_part'],
                'cloud_part': split_result['cloud_part'],
                'local_offset': 0,
                'local_size': len(split_result['local_part']),
                'cloud_offset': 0,
                'cloud_size': len(split_result['cloud_part']),
                'checksum': checksum
            }
            
        except Exception as e:
            logger.error(f"File compression failed: {e}", exc_info=True)
            return {'success': False, 'error': str(e)}
    
    def _upload_cloud_data(self, cloud_data: bytes, metadata: Dict) -> Dict:
        """Upload cloud portion to server"""
        try:
            # Encrypt cloud data
            encrypted_data = self.crypto_manager.encrypt_data(cloud_data)
            
            # Upload to server
            result = self.network_client.upload_archive_cloud_part(
                encrypted_data,
                metadata
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Cloud upload failed: {e}", exc_info=True)
            return {'success': False, 'error': str(e)}
    
    def _write_archive_file(self, archive_path: str, metadata: Dict, local_data: bytes):
        """Write final .wca archive file"""
        try:
            with open(archive_path, 'wb') as f:
                # Write magic header
                f.write(b'WCLOUD10')  # Magic number + version
                
                # Write metadata length (4 bytes)
                metadata_json = json.dumps(metadata, indent=2).encode('utf-8')
                metadata_length = len(metadata_json)
                f.write(metadata_length.to_bytes(4, byteorder='little'))
                
                # Write metadata
                f.write(metadata_json)
                
                # Write local data
                f.write(local_data)
            
            logger.info(f"Archive file written: {archive_path}")
            
        except Exception as e:
            logger.error(f"Failed to write archive: {e}", exc_info=True)
            raise
    
    def extract_archive(
        self,
        archive_path: str,
        output_dir: Optional[str] = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Extract WinCloud archive
        
        Args:
            archive_path: Path to .wca archive
            output_dir: Output directory (default: same as archive)
            progress_callback: Function(progress, status, stats)
        
        Returns:
            Dict with success status
        """
        self._cancel_flag = False
        start_time = time.time()
        
        try:
            logger.info(f"Extracting archive: {archive_path}")
            
            # Determine output directory
            if output_dir is None:
                output_dir = os.path.dirname(archive_path)
            
            # Read archive
            metadata, local_data = self._read_archive_file(archive_path)
            
            if not metadata:
                return {'success': False, 'error': 'Invalid archive file'}
            
            total_files = len(metadata['files'])
            
            # Download cloud data
            if progress_callback:
                progress_callback(
                    10,
                    "Downloading from cloud...",
                    {'speed': 0, 'processed': 0, 'remaining': metadata['total_size']}
                )
            
            cloud_data = self._download_cloud_data(metadata)
            
            if not cloud_data['success']:
                return {'success': False, 'error': f"Cloud download failed: {cloud_data.get('error')}"}
            
            # Extract files
            for idx, file_meta in enumerate(metadata['files']):
                if self._cancel_flag:
                    return {'success': False, 'error': 'Operation cancelled'}
                
                # Update progress
                if progress_callback:
                    progress = 20 + int((idx / total_files) * 70)
                    progress_callback(
                        progress,
                        f"Extracting: {file_meta['name']} ({idx + 1}/{total_files})",
                        {'speed': 0, 'processed': idx, 'remaining': total_files - idx}
                    )
                
                # Extract file
                self._extract_file(
                    file_meta,
                    local_data,
                    cloud_data['data'],
                    output_dir
                )
            
            # Final progress
            if progress_callback:
                progress_callback(
                    100,
                    "Extraction completed!",
                    {'speed': 0, 'processed': total_files, 'remaining': 0}
                )
            
            elapsed_time = time.time() - start_time
            logger.info(f"Extraction completed in {elapsed_time:.2f}s")
            
            return {
                'success': True,
                'message': f'Successfully extracted {total_files} file(s) to {output_dir}',
                'output_dir': output_dir
            }
            
        except Exception as e:
            logger.error(f"Extraction failed: {e}", exc_info=True)
            return {'success': False, 'error': str(e)}
    
    def _read_archive_file(self, archive_path: str) -> tuple:
        """Read .wca archive file"""
        try:
            with open(archive_path, 'rb') as f:
                # Read and verify magic header
                magic = f.read(8)
                if not magic.startswith(b'WCLOUD'):
                    raise ValueError("Invalid archive format")
                
                # Read metadata length
                metadata_length = int.from_bytes(f.read(4), byteorder='little')
                
                # Read metadata
                metadata_json = f.read(metadata_length)
                metadata = json.loads(metadata_json.decode('utf-8'))
                
                # Read local data
                local_data = f.read()
            
            return metadata, local_data
            
        except Exception as e:
            logger.error(f"Failed to read archive: {e}", exc_info=True)
            return None, None
    
    def _download_cloud_data(self, metadata: Dict) -> Dict:
        """Download cloud portion from server"""
        try:
            cloud_archive_id = metadata.get('cloud_archive_id')
            
            if not cloud_archive_id:
                return {'success': False, 'error': 'No cloud data available'}
            
            # Download from server
            result = self.network_client.download_archive_cloud_part(cloud_archive_id)
            
            if not result['success']:
                return result
            
            # Decrypt data
            decrypted_data = self.crypto_manager.decrypt_data(result['data'])
            
            return {'success': True, 'data': decrypted_data}
            
        except Exception as e:
            logger.error(f"Cloud download failed: {e}", exc_info=True)
            return {'success': False, 'error': str(e)}
    
    def _extract_file(
        self,
        file_meta: Dict,
        local_data: bytes,
        cloud_data: bytes,
        output_dir: str
    ):
        """Extract single file from archive"""
        try:
            # Get local and cloud parts
            local_offset = file_meta['local_offset']
            local_size = file_meta['local_size']
            cloud_offset = file_meta['cloud_offset']
            cloud_size = file_meta['cloud_size']
            
            local_part = local_data[local_offset:local_offset + local_size]
            cloud_part = cloud_data[cloud_offset:cloud_offset + cloud_size]
            
            # Merge parts
            compressed_data = self.file_splitter.merge_data(local_part, cloud_part)
            
            # Decompress: LZMA2 first
            decompressed_lzma = lzma.decompress(compressed_data)
            
            # Then Zstandard
            decompressor = zstd.ZstdDecompressor()
            original_data = decompressor.decompress(decompressed_lzma)
            
            # Verify checksum
            checksum = hashlib.sha256(original_data).hexdigest()
            if checksum != file_meta['checksum']:
                raise ValueError(f"Checksum mismatch for {file_meta['name']}")
            
            # Write file
            output_path = os.path.join(output_dir, file_meta['name'])
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(original_data)
            
            logger.info(f"Extracted: {file_meta['name']}")
            
        except Exception as e:
            logger.error(f"Failed to extract file: {e}", exc_info=True)
            raise
    
    def cancel_operation(self):
        """Cancel current operation"""
        with self._lock:
            self._cancel_flag = True
        logger.info("Operation cancelled by user")
