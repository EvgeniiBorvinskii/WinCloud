# Changelog

All notable changes to WinCloud will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-11

### Added
- Initial release of WinCloud
- WinRAR-like graphical user interface
- Hybrid compression (10% local, 90% cloud)
- Two-stage compression (Zstandard + LZMA2)
- AES-256-GCM encryption for cloud data
- Chunked upload for large files
- Real-time progress tracking with statistics
- Automatic retry on network failures
- Offline mode with graceful degradation
- SHA-256 checksum verification
- Multi-threaded compression engine
- REST API for cloud storage
- Comprehensive error handling
- Detailed logging system
- Configuration management

### Security
- End-to-end encryption
- Token-based authentication
- Secure key storage
- Input validation and sanitization

### Documentation
- README with quick start guide
- Architecture documentation
- API documentation
- Deployment guide
- Contributing guidelines
- Security policy

## [Unreleased]

### Planned Features
- Linux and macOS support
- Mobile applications (iOS/Android)
- Browser extension
- Team collaboration features
- Public API for developers
- Automatic updates
- Two-factor authentication
- Advanced compression options
- Archive encryption with password
- File preview in archives
- Drag-and-drop support
- Context menu integration
- Archive repair tool
- Batch operations
- Schedule archiving

### Known Issues
- SSL certificate warnings (self-signed)
- Large memory usage for files >10GB
- GUI freezes on very slow connections (will add timeout)

---

## Version History

### Version Format
- **Major.Minor.Patch** (e.g., 1.0.0)
- **Major**: Breaking changes
- **Minor**: New features (backward compatible)
- **Patch**: Bug fixes (backward compatible)

### Release Notes Location
- GitHub Releases: https://github.com/EvgeniiBorvinskii/WinCloud/releases
- Website: [Coming Soon]

---

For detailed commit history, see: https://github.com/EvgeniiBorvinskii/WinCloud/commits/main
