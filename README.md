# WinCloud - Cloud-Based File Archiver

![WinCloud Logo](assets/wincloud2.png)

## Overview

WinCloud is an innovative file archiving solution that combines local compression with cloud storage optimization. Unlike traditional archivers, WinCloud uses a hybrid approach where 10% of the compressed file is stored locally, while 90% is securely stored on our cloud infrastructure.

## Key Features

- **Hybrid Compression**: Advanced compression algorithm with local + cloud storage
- **Fast Performance**: Optimized for millions of concurrent users
- **WinRAR-like Interface**: Familiar and intuitive GUI
- **Secure Storage**: End-to-end encryption for cloud-stored data
- **Real-time Progress**: Detailed statistics and progress tracking
- **Offline Mode**: Graceful handling of server unavailability
- **Multi-threading**: Parallel processing for maximum speed

## How It Works

1. **Compression Phase**:
   - Files are compressed using industry-standard algorithms (LZMA2)
   - Compressed data is split: 10% local, 90% cloud
   - Cloud portion is encrypted and uploaded securely
   - Local archive contains metadata and recovery information

2. **Extraction Phase**:
   - Local 10% is read from archive
   - Cloud 90% is downloaded and decrypted
   - Data streams are merged and decompressed
   - Original files are restored

## Architecture

```
WinCloud/
├── wincloud_client/       # Client application (GUI + Logic)
├── wincloud_server/       # Server infrastructure (NOT PUBLIC)
├── common/               # Shared utilities and protocols
├── assets/               # Images, icons, resources
└── docs/                # Documentation
```

## Technology Stack

- **Frontend**: PyQt6 (Cross-platform GUI)
- **Compression**: LZMA2, Zstandard
- **Networking**: HTTPS REST API with gRPC for streaming
- **Security**: AES-256 encryption, RSA key exchange
- **Database**: PostgreSQL for metadata
- **Cache**: Redis for session management

## Installation

### Client

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python wincloud_client/main.py
```

### Building Executable

```bash
pyinstaller --onefile --windowed --icon=assets/wincloud.ico wincloud_client/main.py
```

## Security Notice

⚠️ **Server Code Not Included**: For security reasons, the server implementation is not published in this repository. Only the client code and public APIs are available.

## System Requirements

- **OS**: Windows 10/11 (64-bit)
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 100MB for application
- **Network**: Stable internet connection (1 Mbps+)

## Privacy & Data Protection

- All cloud data is encrypted before transmission
- Zero-knowledge architecture: server cannot read your files
- User authentication with secure token management
- GDPR and data protection compliant

## Performance

- Compression speed: Up to 100 MB/s (hardware dependent)
- Upload speed: Network limited, multi-threaded
- Supports files up to 50 GB
- Optimized for SSD storage

## Roadmap

- [ ] Linux and macOS support
- [ ] Mobile applications (iOS/Android)
- [ ] Browser extension
- [ ] Team collaboration features
- [ ] API for developers

## License

Proprietary - All rights reserved

## Contact

For support and inquiries: [Your Contact Information]

---

**Note**: This is a public-facing repository containing only the client-side implementation. Server infrastructure details are confidential.
