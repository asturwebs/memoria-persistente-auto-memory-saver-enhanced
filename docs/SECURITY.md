# Security Policy - Persistent Memory (Auto Memory Saver Enhanced)

## 🔒 Supported Versions

| Version | Security Support |
| ------- | ------------------- |
| 2.1.x   | ✅ Yes               |
| 2.0.x   | ✅ Yes               |
| < 2.0   | ❌ No               |

## 🚨 Report Vulnerabilities

If you discover a security vulnerability, please **DO NOT** report it publicly. Instead:

### Responsible Disclosure Process

1. **Private Email**: Send details to pedro@asturwebs.es
2. **Required Information**:
   - Detailed description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Affected version
   - Any known mitigation

3. **Expected Response**:
   - Receipt confirmation: 24-48 hours
   - Initial assessment: 1 week
   - Resolution: According to severity (1-4 weeks)

### Vulnerability Severity

- **Critical**: Remote code execution, unauthorized data access
- **High**: Privilege escalation, authentication bypass
- **Medium**: Information disclosure, DoS
- **Low**: Minor configuration issues

## 🛡️ Security Best Practices

### For Users
- Keep OpenWebUI updated
- Review valve configurations regularly
- Don't share logs containing sensitive information
- Use private mode for sensitive conversations

### For Developers
- Validate all user inputs
- Sanitize data before storing
- Use secure logging (without sensitive data)
- Implement appropriate rate limiting

## 🔐 Privacy Considerations

- Memories are stored locally in OpenWebUI
- No data is sent to external services
- Private mode prevents memory saving
- Logs may contain conversation fragments (configure appropriately)

## 📋 Security Audits

- Regular code review
- Dependency analysis
- Basic penetration testing
- Known vulnerability monitoring

## 🤝 Coordinated Disclosure

We work with security researchers to:
- Validate and reproduce reports
- Develop patches responsibly
- Coordinate public disclosure
- Recognize security contributions

## 📞 Security Contact

- **Email**: pedro@asturwebs.es
- **PGP**: Available upon request
- **Response**: 24-48 hours for critical reports

Thank you for helping keep Auto Memory Saver Enhanced secure! 🙏
