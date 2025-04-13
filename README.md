<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./Icons/TempMail.ico">
    <img src="./Icons/TempMail.ico">
  </picture>
</p>

**TempMail** is a Python-based GUI program designed to provide users with temporary email addresses and inbox management. Built with simplicity and anonymity in mind, it leverages the **mail.tm API** to create disposable email accounts, making it perfect for signing up on websites or services without revealing your personal email.

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
![](Screenshots/DarkTheme.PNG)

![](Screenshots/LightTheme.PNG)

---
## 📂 Project Structure

```
📂 TempMail/
├── 📂 Icons/             # Contains all UI icons and images
├── 📂 Modules/           
│   ├── 📄 __init__.py     # Python import modules manager
│   ├── 📄 TempMail_API.py # Handles application backend 
│   └── 📄 CoreB.py        # Core functionality module
├── 📂 Screenshots         # Contains UI Screenshots
├── 📄 AutoInstaller.bat  # AutoInstaller script for Windows
├── 📄 HomePage.html       # HomePage HTML file for UI
├── 📄 LICENSE  
├── 📄 README.md           # Project documentation
├── 📄 TempMail.py         # GUI application script
└── 📄 requirements.txt    # Lists all required dependencies
```
---
## 🛠️ Installation

### 🔹 Automatic Installation (Recommended)

1. Clone the repository using this command:
   ```bash
   git clone https://github.com/AliJ-Official/TempMail.git
   ```

- If you don't have git installed on your system, you can download the zip file from this [link](https://codeload.github.com/AliJ-Official/TempMail/zip/refs/heads/main) and follow the steps below.

2. Navigate to the TempMail directory.

3. Ensure you have an active internet connection and run the **AutoInstaller.bat** script.

5. Follow the on-screen instructions to select your Python version and complete the installation. You can run the program immediately.

---

### 🔹 Manual Installation

1. Clone the repository using this command:
   ```bash
   git clone https://github.com/AliJ-Official/TempMail.git
   ```
- If you don't have git installed on your system, you can download the zip file from this [link](https://codeload.github.com/AliJ-Official/TempMail/zip/refs/heads/main) and follow the steps below.


2. Navigate to the TempMail directory.

3. Open powershell or cmd in TempMail directory.

4. Create and activate a Virtual Environment (recommended):
   ```bash
   python -m venv .venv
   .venv/Scripts/activate.bat
   ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the program:
   ```bash
   python TempMail.py
   ```

- To deactivate the Virtual Environment:
   ```bash
   deactivate
   ```

- Alternatively, you can run the program without activating the Virtual Environment:
   ```bash
   .venv/Scripts/python.exe TempMail.py
   ```

---

## 🚧 Limitations

- **Third-Party Dependency**: TempMail relies on the [mail.tm API](https://mail.tm). If the API is down or unavailable, the program will not function as expected.
- **Notifications Blocked**: TempMail uses system notifications to alert users about new emails and other events. If notifications are blocked in your Windows settings, these features will not work. 

    ### How to Enable Notifications in Windows:
   1. Open the **Settings** app on your Windows system.
   2. Navigate to **System** > **Notifications & actions**.
   3. Ensure the **Get notifications from apps and other senders** option is turned **On**.
   4. Ensure that **Focus Assist** is turned off or configured to allow notifications.

   By enabling notifications, you can ensure a better user experience with real-time alerts.
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
