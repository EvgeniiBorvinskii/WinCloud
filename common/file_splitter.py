"""
File Splitter - Splits data into local (10%) and cloud (90%) parts
"""
from typing import Dict
import io

class FileSplitter:
    """
    Handles splitting and merging of file data
    Default: 10% local, 90% cloud
    """
    
    def split_data(
        self,
        data: bytes,
        local_percentage: int = 10
    ) -> Dict:
        """
        Split data into local and cloud parts
        
        Args:
            data: Data to split
            local_percentage: Percentage to keep locally (default 10)
        
        Returns:
            Dict with 'local_part' and 'cloud_part'
        """
        if not isinstance(data, bytes):
            raise TypeError("Data must be bytes")
        
        if not 0 <= local_percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100")
        
        total_size = len(data)
        
        # Calculate split point
        local_size = int(total_size * (local_percentage / 100.0))
        
        # Ensure at least some data in each part (if file is large enough)
        if total_size > 100:
            local_size = max(1, local_size)
            local_size = min(total_size - 1, local_size)
        
        # Split data
        local_part = data[:local_size]
        cloud_part = data[local_size:]
        
        return {
            'local_part': local_part,
            'cloud_part': cloud_part,
            'local_size': len(local_part),
            'cloud_size': len(cloud_part),
            'total_size': total_size
        }
    
    def merge_data(
        self,
        local_part: bytes,
        cloud_part: bytes
    ) -> bytes:
        """
        Merge local and cloud parts back together
        
        Args:
            local_part: Local part (10%)
            cloud_part: Cloud part (90%)
        
        Returns:
            Complete merged data
        """
        if not isinstance(local_part, bytes) or not isinstance(cloud_part, bytes):
            raise TypeError("Parts must be bytes")
        
        # Simple concatenation
        return local_part + cloud_part
    
    def calculate_split_sizes(
        self,
        total_size: int,
        local_percentage: int = 10
    ) -> Dict:
        """
        Calculate split sizes without actually splitting
        
        Args:
            total_size: Total size in bytes
            local_percentage: Percentage for local
        
        Returns:
            Dict with size information
        """
        local_size = int(total_size * (local_percentage / 100.0))
        cloud_size = total_size - local_size
        
        return {
            'total_size': total_size,
            'local_size': local_size,
            'cloud_size': cloud_size,
            'local_percentage': (local_size / total_size * 100) if total_size > 0 else 0,
            'cloud_percentage': (cloud_size / total_size * 100) if total_size > 0 else 0
        }
