<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./Icons/email.ico">
    <img src="./Icons/email.ico">
  </picture>
</p>

**TempMail** is a Python-based GUI application designed to provide users with temporary email addresses and inbox management. Built with simplicity and anonymity in mind, it leverages the **mail.tm API** to create disposable email accounts, making it perfect for signing up on websites or services without revealing your personal email.

---

## ✨ Key Features

- **Disposable Email Addresses** – Instantly generate temporary email addresses for anonymous use.
- **Inbox Management** – View and read emails in your temporary inbox with ease.
- **Real-Time Notifications** – Get notified when a new email arrives. Click the notification to bring the program window to the top.
- **Email Ready Notification** – Receive a notification when your temporary email is ready. Click it to copy the email address to your clipboard instantly.
- **Real-Time Connectivity Monitoring** – Stay informed about your internet connection status.
- **Theme Support** – Switch between **light** and **dark** themes for a personalized experience.

---
## 📸 Screenshots
![](Screenshots/Dark-Theme.png)

![](Screenshots/Light-Theme.png)
---

## 📂 Project Structure

```
📂 TempMail/
├── 📂 Icons/            # Contains all UI icons and images
├── 📂 Modules/          # Contains helper classes and modules
│   ├── 📄 __init__.py   # Python import modules manager
│   ├── 📄 UserAgents.py # Handles user-agent strings
│   └── 📄 CoreB.py      # Core functionality module
├── 📄 Auto_Installer.bat # Auto-installer script for Windows
├── 📄 Index.html        # HTML file used in the UI
├── 📄 README.md         # Project documentation
├── 📄 requirements.txt  # Lists all required dependencies
└── 📄 TempMail.py       # Main application script
```
---
## 🛠️ Installation

### 🔹 Automatic Installation (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/AliJ-Programming/TempMail.git
   ```

2. Navigate to the project directory:
   ```bash
   cd TempMail
   ```

3. Ensure you have an active internet connection and run the installation script:
   ```bash
   Auto_Installer.bat
   ```

4. Follow the on-screen instructions to select your Python version and complete the installation. You can activate the Virtual Environment immediately or manually later.

5. Activate the Virtual Environment:
   ```bash
   .venv/Scripts/activate.bat
   ```

6. Run the program:
   ```bash
   python TempMail.py
   ```

7. Alternatively, run the program without activating the Virtual Environment:
   ```bash
   .venv/Scripts/python.exe TempMail.py
   ```

- To deactivate the Virtual Environment:
   ```bash
   deactivate
   ```

---

### 🔹 Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AliJ-Programming/TempMail.git
   ```

2. Navigate to the project directory:
   ```bash
   cd TempMail
   ```

3. Create and activate a Virtual Environment (recommended):
   ```bash
   python -m venv .venv
   .venv/Scripts/activate.bat
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the program:
   ```bash
   python TempMail.py
   ```

6. Alternatively, run the program without activating the Virtual Environment:
   ```bash
   .venv/Scripts/python.exe TempMail.py
   ```

- To deactivate the Virtual Environment:
   ```bash
   deactivate
   ```

---

## 🚧 Limitations

- **Third-Party Dependency**: TempMail relies on the [mail.tm API](https://mail.tm). If the API is down or unavailable, the program will not function as expected.

---

## 🤝 Contributing

We welcome contributions! If you'd like to contribute to TempMail, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Push your branch and open a pull request.

Please ensure your code follows the project's style and includes appropriate documentation.

---

## 🙏 Acknowledgments

This project includes code from [CoreB](https://github.com/mmji-programming/CoreB.git), licensed under the MIT License.  
CoreB is a lightweight and efficient concurrency management library that provides threading controllers, task execution, and queue management.  
In this program, CoreB is used for managing background tasks, ensuring smooth and efficient asynchronous execution.

---

## 📜 License

TempMail is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

**Thank you for using TempMail!** If you encounter any issues or have suggestions for improvement, feel free to open an issue or contribute to the project.

---
