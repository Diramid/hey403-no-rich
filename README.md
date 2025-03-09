<h1 align="center">
  🌐 Hey403 No Rich
  <br>
  <sub>⚡ Core DNS Accessibility Testing Library ⚡</sub>
</h1>

<div align="center">

[![Stars](https://img.shields.io/github/stars/Diramid/hey403-no-rich?logo=starship&color=gold)](https://github.com/Diramid/hey403-no-rich/stargazers)
[![Forks](https://img.shields.io/github/forks/Diramid/hey403-no-rich?logo=git&color=9cf)](https://github.com/Diramid/hey403-no-rich/forks)
[![Issues](https://img.shields.io/github/issues/Diramid/hey403-no-rich?logo=github&color=red)](https://github.com/Diramid/hey403-no-rich/issues)
[![License](https://img.shields.io/github/license/Diramid/hey403-no-rich?logo=open-source-initiative&color=green)](https://github.com/Diramid/hey403-no-rich/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/hey403-no-rich?logo=pypi&color=blue)](https://pypi.org/project/hey403-no-rich/)

</div>

---

## 📖 What is Hey403 No Rich?
**Hey403 No Rich** is a lightweight, dependency-minimal Python library for testing DNS accessibility. Stripped of CLI fluff and `rich` formatting, it’s built as a core module for developers to integrate into their own applications. Diagnose domain issues programmatically with ease.

### Why Hey403 No Rich?
- ⚡ **Fast & Lean**: No UI overhead—just pure DNS testing logic.
- 🌐 **Global DNS**: Leverage 15+ DNS providers for comprehensive checks.
- 🔧 **Embeddable**: Perfect for embedding in scripts, tools, or larger systems.
- 📏 **Minimal Footprint**: Fewer dependencies, more flexibility.

---

## ✨ Features
| Feature             | Description                              |
|---------------------|------------------------------------------|
| 🌍 **15+ DNS**      | Test with top global DNS providers.      |
| ⚡ **Parallel Tests**| Concurrent DNS resolution for speed.    |
| 🔍 **Error Detection**| Catch 403s, blocks, and timeouts.       |
| 🔧 **DNS Control**  | Manage system DNS programmatically.      |
| 📦 **No Rich**      | No `rich` dependency—raw, simple output. |

---

## 🚀 Get Started
1. **Install it**:
   ```bash
   pip install hey403-no-rich
   ```
2. **Use it in your code**:
   ```python
   from hey403_no_rich import DNSResolver

   resolver = DNSResolver()
   results = resolver.test_dns("example.com")
   print(results)
   ```

---

## 🔧 Usage Examples
### Test a Domain
```python
from hey403_no_rich import DNSResolver

resolver = DNSResolver()
results = resolver.test_dns("example.com", dns_list=["8.8.8.8", "1.1.1.1"])
for dns, status, time in results:
    print(f"DNS: {dns}, Status: {status}, Time: {time}")
```

### Set System DNS
```python
from hey403_no_rich import DNSManager

manager = DNSManager()
manager.set_dns("8.8.8.8", alternative="8.8.4.4")
```

### Get Current DNS
```python
from hey403_no_rich import DNSManager

manager = DNSManager()
current = manager.get_current_dns()
print(f"Current DNS: {current}")
```

---

## 🤝 Contributing
Want to make it better? Jump in!
1. Fork it 🍴
2. Set up your env:
   ```bash
   git clone https://github.com/Diramid/hey403-no-rich.git
   cd hey403-no-rich
   pip install -e .[dev]
   ```
3. Test it:
   ```bash
   pytest tests/ -v
   ```
4. Push & PR:
   ```bash
   git checkout -b feature/awesome
   git commit -m "Add awesome feature"
   git push origin feature/awesome
   ```
5. Open a PR on [GitHub](https://github.com/Diramid/hey403-no-rich/pulls)

See [Contributing Guide](CONTRIBUTING.md) for details.

---

## ⚖️ License
Open-source under the [MIT License](LICENSE). Use it, tweak it, integrate it—legally!

---

## 🌟 Support Us
- ⭐ Star us on [GitHub](https://github.com/Diramid/hey403-no-rich)!
- 🐛 Report bugs at [Issues](https://github.com/Diramid/hey403-no-rich/issues).
- 💬 Share how you’re using it—we’d love to hear!

---

> **Note** 📢  
> Built for developers, by developers. Use responsibly and respect local laws.
