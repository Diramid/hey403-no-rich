<h1 align="center">
  🌐 Hey 403 - CLI Edition
  <br>
  <sub>⚡ DNS Accessibility Testing Tool ⚡</sub>
</h1>

<div align="center">

[![Stars](https://img.shields.io/github/stars/Diramid/hey-403-cli?logo=starship&color=gold)](https://github.com/Diramid/hey403/stargazers)
[![Forks](https://img.shields.io/github/forks/Diramid/hey-403-cli?logo=git&color=9cf)](https://github.com/Diramid/hey403/forks)
[![Issues](https://img.shields.io/github/issues/Diramid/hey-403-cli?logo=openbugbounty&color=red)](https://github.com/Diramid/hey403/issues)
[![License](https://img.shields.io/github/license/Diramid/hey-403-cli?logo=open-source-initiative&color=green)](https://github.com/Diramid/hey403/blob/main/LICENSE)

</div>

## 📖 Table of Contents
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🔧 Usage Examples](#-usage-examples)
- [🤝 Contributing](#-contributing)
- [⚖️ License](#️-license)

## 🌟 About Hey 403
**Hey 403 - CLI Edition** is a powerful command-line utility designed to diagnose domain accessibility issues across multiple DNS providers. This tool helps developers, network administrators, and security professionals quickly identify:

- Geo-restrictions and censorship blocks 🚫
- DNS resolution inconsistencies 🌍
- Server response variations 🔄
- Potential connectivity issues 🔍

### Key Capabilities
- Test domain accessibility through **15+ global DNS servers**
- Detect **403 Forbidden** and other HTTP errors
- Compare DNS resolution times ⏱️
- Identify regional blocking patterns 🗺️
- Generate machine-readable reports 📊

### Why Use Hey 403?
- 🚦 **Instant Diagnostics**: Verify domain accessibility in seconds
- 🌐 **Global Perspective**: Test against worldwide DNS providers
- 🔧 **Troubleshooting Made Easy**: Pinpoint DNS-related issues quickly
- 📈 **Performance Metrics**: Measure response times across providers

## ✨ Features
| **Feature**         | **Description**                          |
|----------------------|------------------------------------------|
| 🚪 CLI First        | Terminal-native interface                |
| 🌍 15+ Built-in DNS | Preconfigured DNS servers                |
| ⚡ Parallel Testing  | Concurrent DNS checks                    |
| 🎨 Colorful Output  | Rich text formatting                     |

## 🚀 Quick Start
```bash
# Install the package
pip install hey403

# Run the main command
hey403 --help
```

## 🔧 Usage Examples
```bash
# Test a single domain
hey403 example.com

```
## 🤝 Contributing
1. Fork the repository
2. Set up the development environment:
   ```bash
   git clone https://github.com/Diramid/hey-403-cli.git
   cd hey-403-cli
   pip install -e .[dev]
   ```
3. Run tests:
   ```bash
   pytest tests/ -v
   ```
4. Commit and push your changes:
   ```bash
   git checkout -b feature/amazing-feature
   git commit -m 'Add amazing feature'
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

## ⚖️ License
Distributed under MIT License. See [LICENSE](https://github.com/Diramid/hey403/blob/main/LICENSE) for details.

---

> **Note** 📢  
> Always use this tool responsibly and in compliance with local laws and regulations.  
> Unauthorized access to computer systems is strictly prohibited.
