# Quick Start Guide

## For End Users

### Installation

1. Download latest release from [GitHub Releases](https://github.com/EvgeniiBorvinskii/WinCloud/releases)
2. Run installer
3. Launch WinCloud

### Creating Your First Archive

1. Click **"Add Files"**
2. Select files to archive
3. Click **"Create Archive"**
4. Choose where to save
5. Wait for completion

### Extracting an Archive

1. Click **"Extract Archive"**
2. Select `.cloud` file
3. Files will be extracted automatically

That's it! See [User Guide](docs/USER_GUIDE.md) for more details.

---

## For Developers

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/EvgeniiBorvinskii/WinCloud.git
cd WinCloud

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run application
python wincloud_client/main.py
```

### Project Structure

```
WinCloud/
├── wincloud_client/     # Client application (PUBLIC)
│   ├── main.py         # Entry point
│   ├── gui/            # PyQt6 interface
│   └── core/           # Compression, network
├── common/             # Shared utilities (PUBLIC)
│   ├── config.py
│   ├── crypto.py
│   ├── logger.py
│   └── file_splitter.py
├── assets/             # Images, icons (PUBLIC)
├── docs/               # Documentation (PUBLIC)
├── wincloud_server/    # Server code (NOT PUBLIC)
├── requirements.txt    # Python dependencies
├── build.ps1           # Build script
└── README.md          # This file
```

### Building Executable

```powershell
# Windows PowerShell
.\build.ps1
```

The executable will be created in `dist/WinCloud.exe`

### Running Tests

```bash
pytest tests/ -v
pytest --cov=wincloud_client tests/
```

---

## For Server Administrators

### Server Deployment

**⚠️ SERVER CODE IS NOT PUBLIC**

The server deployment is handled separately. Contact the development team for:
- Server access
- Deployment scripts
- Configuration details

Server location: `5.249.160.54:/srv/WinCloud`

See [wincloud_server/DEPLOYMENT.md](wincloud_server/DEPLOYMENT.md) for details (if you have access).

---

## Configuration

### Client Configuration

Config file: `C:\Users\YourName\.wincloud\config.json`

```json
{
  "server_url": "https://5.249.160.54:8443",
  "compression_level": 9,
  "split_ratio": {
    "local": 10,
    "cloud": 90
  },
  "encryption": {
    "enabled": true
  }
}
```

### Logs

Logs location: `C:\Users\YourName\.wincloud\logs\`

View latest log:
```powershell
Get-Content "$env:USERPROFILE\.wincloud\logs\wincloud_$(Get-Date -Format 'yyyyMMdd').log" -Tail 50
```

---

## Common Issues

### "Cannot connect to server"

- Check internet connection
- Verify server is running: https://5.249.160.54:8443/api/v1/health
- Check firewall settings

### "Import Error: No module named 'PyQt6'"

```bash
pip install PyQt6
```

### "Permission denied" when running

Run terminal as Administrator or check file permissions.

---

## Getting Help

- **Issues**: https://github.com/EvgeniiBorvinskii/WinCloud/issues
- **Discussions**: https://github.com/EvgeniiBorvinskii/WinCloud/discussions
- **Documentation**: See `docs/` folder

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License - See [LICENSE](LICENSE) for details.

**Note**: Server code is proprietary and not included in this repository.
