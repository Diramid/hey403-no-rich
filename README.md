
<h1 align="center">
  🌐 Hey 403 - CLI Edition
  <br>
  <sub>⚡ DNS Accessibility Testing Tool ⚡</sub>
</h1>

<div align="center">

[![Stars](https://img.shields.io/github/stars/Diramid/hey-403-cli?logo=starship&color=gold)](https://github.com/Diramid/hey-403-cli/stargazers)
[![Forks](https://img.shields.io/github/forks/Diramid/hey-403-cli?logo=git&color=9cf)](https://github.com/Diramid/hey-403-cli/forks)
[![Issues](https://img.shields.io/github/issues/Diramid/hey-403-cli?logo=openbugbounty&color=red)](https://github.com/Diramid/hey-403-cli/issues)
[![License](https://img.shields.io/github/license/Diramid/hey-403-cli?logo=open-source-initiative&color=green)](https://github.com/Diramid/hey-403-cli/blob/main/LICENSE)

</div>

## 📖 Table of Contents
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🔧 Usage Examples](#-usage-examples)
- [🤝 Contributing](#-contributing)
- [⚖️ License](#️-license)

## ✨ Features
| **Feature**         | **Description**                          |
|----------------------|------------------------------------------|
| 🚪 CLI First        | Terminal-native interface                |
| 🌍 15+ Built-in DNS | Preconfigured DNS servers                |
| ⚡ Parallel Testing  | Concurrent DNS checks                    |
| 🎨 Colorful Output  | Rich text formatting                     |
| 📁 Multi-Format Export | CSV/JSON support                       |

## 🚀 Quick Start
```bash
# Clone & Install
git clone https://github.com/Diramid/hey-403-cli.git
cd hey-403-cli
pipenv install --deploy

# Basic Usage
pipenv run python hey403.py --url https://example.com
```

## 🔧 Usage Examples
```bash
# Single Domain Test
python hey403.py --url https://example.com

# Custom DNS Check
python hey403.py --url https://example.com --dns 1.1.1.1

# Batch Testing
python hey403.py --input urls.txt --output results.csv
```

## 🤝 Contributing
```bash
1. Fork the repository
2. Create your feature branch:
   git checkout -b feature/amazing-feature
3. Commit changes:
   git commit -m 'Add amazing feature'
4. Push to branch:
   git push origin feature/amazing-feature
5. Open a Pull Request
```

## ⚖️ License
Distributed under MIT License. See `LICENSE` for details.

---
