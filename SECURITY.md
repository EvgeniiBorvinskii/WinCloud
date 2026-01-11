# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: [Your Security Email]

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information:

- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

## Security Features

### Client-Side Security

1. **Encryption**: All cloud data is encrypted with AES-256-GCM before upload
2. **Key Storage**: Master key stored in user's home directory with restricted permissions
3. **SSL/TLS**: All network communication uses HTTPS
4. **Checksum Verification**: SHA-256 checksums verify file integrity

### Server-Side Security

1. **Authentication**: Token-based authentication for all API requests
2. **Input Validation**: All inputs are validated and sanitized
3. **Rate Limiting**: Protection against abuse and DDoS
4. **Isolated Storage**: User data isolated in separate directories
5. **Database Security**: Prepared statements prevent SQL injection

## Best Practices for Users

1. **Keep Software Updated**: Always use the latest version
2. **Secure Your Key**: Never share your encryption key
3. **Use Strong Passwords**: If using password-based encryption
4. **Verify Downloads**: Check file checksums after extraction
5. **Secure Network**: Use trusted networks for uploads/downloads

## Known Limitations

1. **SSL Certificate**: Currently uses self-signed certificate (warning expected)
2. **Password Recovery**: Lost encryption keys cannot be recovered
3. **Cloud Dependency**: Archives require cloud access for extraction

## Future Security Enhancements

- [ ] Two-factor authentication
- [ ] End-to-end encrypted sharing
- [ ] Audit logging
- [ ] Advanced threat protection
- [ ] Regular security audits

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine affected versions
2. Audit code to find similar problems
3. Prepare fixes for all supported versions
4. Release patches as soon as possible

Thank you for helping keep WinCloud secure!
