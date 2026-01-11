# Contributing to WinCloud

Thank you for your interest in contributing to WinCloud!

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the project goals

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Screenshots if applicable

### Suggesting Features

1. Check if the feature has been suggested
2. Create a new issue explaining:
   - The problem it solves
   - How it should work
   - Example use cases

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/EvgeniiBorvinskii/WinCloud.git
cd WinCloud

# Install dependencies
pip install -r requirements.txt

# Run the application
python wincloud_client/main.py
```

## Coding Standards

### Python Style Guide

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions and classes
- Maximum line length: 100 characters

### Git Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Add detailed description if needed

Example:
```
Add file compression optimization

- Implement multi-threading for large files
- Reduce memory usage by 30%
- Add progress callback for better UX
```

## Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=wincloud_client tests/
```

## Documentation

- Update README.md for user-facing changes
- Update docs/ for architectural changes
- Add comments for complex logic

## Questions?

Feel free to open an issue for questions or discussions!

## License

By contributing, you agree that your contributions will be licensed under the project's license.
