![Program Icon](Icons/email.png)

# TempMail

**TempMail** is a Python-based GUI program that provides temporary email addresses and inbox management. It uses the **mail.tm API** to create disposable email accounts.

## ✨ Features

- **Temporary Email Generation** – Create disposable email addresses for anonymous use.
- **Inbox Management** – View and read messages in your temporary inbox.
- **Connection Status Monitoring** – Monitor internet connectivity in real-time.
- **Theme Switching** – Toggle between dark and light UI themes.

---

## 📋 Requirements

Ensure the following are installed:

![Python Icon](Icons/python.png) **Python 3.10-3.12.7** (Python 3.13+ is not supported)

### Required Python Packages:
- `Pillow`
- `requests`
- `CTkListbox`
- `tkinterweb`
- `customtkinter`

Dependencies are listed in `requirements.txt`.

---

## 🚀 Installation

### 🔹 Automatic Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/AliJ-Programming/TempMail.git
    ```

2. Open CMD in TempMail directory.

3. Ensure an internet connection & Run the installation script:
    ```bash
    Auto_Installer.bat
    ```

4. Select the Python version and wait for the installation to complete. You can activate the Virtual Environment immediately or manually later.

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

### 🔹 Manual Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/AliJ-Programming/TempMail.git
    ```

2. Open CMD in TempMail directory.

3. Create and activate a Virtual Environment (recommended):
    ```bash
    python -m venv .venv
    .venv/Scripts/activate.bat
    ```

4. Install dependencies:
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

## 📖 How to Use

- A **temporary email address** is generated and displayed upon launch.
- **Regenerate** a new email by clicking the refresh icon.
- **Copy** the email address using the copy button.
- Click an email in the inbox to **view its contents**.

### 🛠 Key Actions

- **Generate Email** – Automatically created at startup or upon request.
- **Check Inbox** – Inbox updates automatically.
- **Open Messages** – Click an email to view its full content.
- **Regenerate Email** – Generate a new email at any time.
---

## 🚧 Limitations

- **Third-Party Dependency** – Relies on the [mail.tm API](https://mail.tm), subject to its availability.

---

## 🏗 Project Structure

```
📂TempMail/
├── 📂Icons/            # UI icons and images
├── 📂Modules/          # Helper classes and modules
│   ├──📄__init__.py     # Python import modules manager
│   ├──📄 UserAgents.py  # User-agent handling module
│   └──📄 CoreB.py        # Core functionality module
├──📄 Auto_Installer.bat # Auto-installer for Windows
├──📄 Index.html         # HTML file used in the UI
├──📄 README.md          # Project documentation
├──📄 requirements.txt   # Required dependencies
└──📄 TempMail.py        # Main application script
```

---

## 🤝 Contributing

Want to contribute? Follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make your changes and commit them.
4. Open a pull request.

---

## 🙏 Acknowledgments  
This project includes code from [CoreB](https://github.com/mmji-programming/CoreB.git), licensed under the MIT License.  
CoreB is a lightweight and efficient concurrency management library that provides threading controllers, task execution, and queue management.  
In this program, CoreB is used for managing background tasks, ensuring smooth and efficient asynchronous execution.  

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

--- 

**Thanks for using TempMail!** If you encounter issues or have suggestions, feel free to open an issue or contribute.
