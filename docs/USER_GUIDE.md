# WinCloud User Guide

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Creating Archives](#creating-archives)
4. [Extracting Archives](#extracting-archives)
5. [Settings](#settings)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## Installation

### System Requirements

- **OS**: Windows 10 or 11 (64-bit)
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 100MB for application
- **Network**: Stable internet connection (1 Mbps+)

### Installation Steps

1. Download WinCloud installer from [releases](https://github.com/EvgeniiBorvinskii/WinCloud/releases)
2. Run `WinCloud-Setup.exe`
3. Follow installation wizard
4. Launch WinCloud from Start Menu

### First Run

On first launch, WinCloud will:
- Create configuration folder in `C:\Users\YourName\.wincloud`
- Generate encryption key
- Check server connection
- Show main window

---

## Getting Started

### Main Window Overview

```
┌─────────────────────────────────────────────┐
│ File | Commands | Tools | Help              │  Menu Bar
├─────────────────────────────────────────────┤
│ [Add Files] [Add Folder] [Create] [Extract]│  Toolbar
├─────────────────────────────────────────────┤
│                                             │
│  Files to Archive:                          │
│  ┌───────────────────────────────────────┐ │
│  │ Name         Size      Type      Path  │ │
│  │ document.pdf 10.5 MB   PDF       ...   │ │
│  │ image.jpg    2.3 MB    JPEG      ...   │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  Operation Progress:                        │
│  ┌───────────────────────────────────────┐ │
│  │ Progress: ████████░░ 80%              │ │
│  │ Status: Uploading to cloud...         │ │
│  │ Speed: 5.2 MB/s | Processed: 50 MB   │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  Status: Ready                              │  Status Bar
└─────────────────────────────────────────────┘
```

---

## Creating Archives

### Method 1: Add Files

1. Click **"Add Files"** button or press `Ctrl+O`
2. Select one or more files
3. Click **"Create Archive"** or press `Ctrl+A`
4. Choose save location
5. Wait for compression and upload
6. See success message with statistics

### Method 2: Add Folder

1. Click **"Add Folder"** button
2. Select folder to archive
3. All files in folder will be added
4. Click **"Create Archive"**
5. Follow steps above

### Archive Process

1. **Compression**: Files are compressed using advanced algorithms
2. **Splitting**: Data is split (10% local, 90% cloud)
3. **Encryption**: Cloud portion is encrypted
4. **Upload**: Encrypted data uploaded to server
5. **Finalization**: Local `.wca` file created

### Progress Information

During archiving, you'll see:
- **Progress Bar**: Overall completion percentage
- **Current File**: File being processed
- **Speed**: Compression/upload speed in MB/s
- **Processed**: Amount of data processed
- **Remaining**: Estimated remaining data
- **Compression Ratio**: Space savings percentage

### Example

```
Original files: 100 MB
After compression: 45 MB (55% compression)
Local archive size: 4.5 MB (10%)
Cloud storage: 40.5 MB (90%)
Total savings: 95.5 MB (95.5%)
```

---

## Extracting Archives

### Basic Extraction

1. Click **"Extract Archive"** or press `Ctrl+E`
2. Select `.wca` archive file
3. Extraction starts automatically
4. Files are restored to original location (or chosen folder)

### Extraction Process

1. **Reading**: Local archive is read
2. **Downloading**: Cloud portion downloaded from server
3. **Decryption**: Cloud data is decrypted
4. **Merging**: Local and cloud parts combined
5. **Decompression**: Data is decompressed
6. **Verification**: Checksums verified
7. **Writing**: Files written to disk

### Offline Mode

If server is unavailable:
- Warning message will be shown
- Cannot extract archives requiring cloud data
- Can still create local-only archives (future feature)

---

## Settings

### Accessing Settings

Menu: **Tools** → **Settings**

### Available Options

#### General
- **Language**: Interface language (English, Russian, etc.)
- **Theme**: Light or Dark mode
- **Auto-update**: Check for updates on startup

#### Compression
- **Compression Level**: 1-9 (9 = maximum)
- **Split Ratio**: Local/Cloud percentage
- **Algorithm**: Zstandard, LZMA2, or both

#### Network
- **Server URL**: Cloud server address
- **Timeout**: Network timeout (seconds)
- **Max Retries**: Retry attempts on failure
- **Chunk Size**: Upload chunk size (MB)

#### Security
- **Encryption**: Enable/disable encryption
- **Key Management**: View/regenerate encryption key
- **Auto-logout**: Automatic session timeout

#### Advanced
- **Log Level**: Logging verbosity
- **Temp Directory**: Temporary files location
- **Cache Size**: Maximum cache size

---

## Troubleshooting

### Server Connection Failed

**Symptoms**: "Could not connect to cloud server" error

**Solutions**:
1. Check internet connection
2. Verify server is accessible: https://5.249.160.54:8443/api/v1/health
3. Check firewall settings
4. Try again later (server may be under maintenance)

### Compression Failed

**Symptoms**: Error during archive creation

**Solutions**:
1. Check if files are accessible (not locked by another program)
2. Ensure enough disk space for temporary files
3. Try with fewer/smaller files
4. Check logs: `C:\Users\YourName\.wincloud\logs`

### Extraction Failed

**Symptoms**: Cannot extract archive

**Solutions**:
1. Verify archive file is not corrupted
2. Check if cloud data is still available on server
3. Ensure enough disk space for extracted files
4. Try re-downloading archive if possible

### Checksum Mismatch

**Symptoms**: "Checksum verification failed" error

**Solutions**:
1. Archive may be corrupted
2. Try extracting again
3. If persists, cloud data may be corrupted (contact support)

### Slow Performance

**Symptoms**: Very slow compression or upload

**Solutions**:
1. Close other programs using CPU/network
2. Try with smaller files first
3. Check network speed
4. Lower compression level in settings
5. Upgrade hardware (more RAM/faster CPU)

---

## FAQ

### Q: Is my data safe?
**A**: Yes! All cloud data is encrypted with AES-256 before upload. Only you have the encryption key.

### Q: What happens if I lose my encryption key?
**A**: Unfortunately, encrypted data cannot be recovered without the key. Keep backups of your `.wincloud` folder.

### Q: Can I use WinCloud offline?
**A**: You can create archives offline, but extraction requires downloading from cloud server.

### Q: What file types are supported?
**A**: All file types! WinCloud archives any file.

### Q: Is there a file size limit?
**A**: Maximum file size is 50GB per archive.

### Q: Can I archive folders with subdirectories?
**A**: Yes! All subdirectories and files are included.

### Q: How long is cloud data stored?
**A**: Indefinitely, unless you delete the archive or your account.

### Q: Can I share archives?
**A**: Currently, you can share the `.wca` file, but the recipient needs access to the cloud portion (same account).

### Q: Does WinCloud work on Mac/Linux?
**A**: Not yet. Windows only for now. Mac/Linux support is planned.

### Q: How do I uninstall?
**A**: Use Windows "Add or Remove Programs". User data in `.wincloud` folder can be deleted manually.

### Q: Is WinCloud free?
**A**: Current version is free. Future plans may include premium features.

### Q: How is WinCloud different from WinRAR?
**A**: WinCloud uses hybrid cloud storage for better space efficiency. WinRAR is local-only.

---

## Getting Help

### Support Channels

- **GitHub Issues**: https://github.com/EvgeniiBorvinskii/WinCloud/issues
- **Documentation**: https://github.com/EvgeniiBorvinskii/WinCloud/tree/main/docs
- **Email**: [Your Support Email]

### Before Asking for Help

1. Check this user guide
2. Search existing GitHub issues
3. Check log files for error messages
4. Try reproducing the issue

### Reporting Bugs

Include:
- WinCloud version
- Windows version
- Steps to reproduce
- Error messages
- Log files (if applicable)

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Add Files |
| `Ctrl+A` | Create Archive |
| `Ctrl+E` | Extract Archive |
| `Ctrl+Q` | Exit |
| `F1` | Help |

---

## Advanced Usage

### Command Line (Future)

```bash
wincloud create archive.wca file1.txt file2.txt
wincloud extract archive.wca
wincloud list archive.wca
```

### Batch Processing (Future)

Create multiple archives:
```bash
for file in *.zip; do
    wincloud create "$file.wca" "$file"
done
```

---

## Tips & Tricks

1. **Organize Files**: Archive related files together
2. **Use Folders**: Archive entire project folders
3. **Verify Extractions**: Always check extracted files
4. **Keep Local Copies**: Keep `.wca` files safe
5. **Monitor Progress**: Watch statistics for performance insights
6. **Regular Backups**: Back up important archives
7. **Clean Up**: Delete old archives from server to save space

---

## Version Information

**Current Version**: 1.0.0  
**Release Date**: January 11, 2026  
**Documentation Version**: 1.0  

---

*For more information, visit: https://github.com/EvgeniiBorvinskii/WinCloud*
