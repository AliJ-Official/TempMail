from string import ascii_lowercase, ascii_uppercase, digits
from Modules.UserAgents import user_agents
from datetime import datetime, timezone
from Modules.CoreB import Core, Agent
from random import choice, choices
from requests import get, post
from time import sleep

from windows_toasts import Toast, WindowsToaster, ToastDisplayImage
from webbrowser import open as open_in_browser
from PIL.Image import open as open_image
from CTkListbox import CTkListbox
from tkinterweb import HtmlFrame
from tkinter import PanedWindow
from customtkinter import *

class TempMail:
    """
    Manages temporary email accounts using the mail.tm API.
    """
    def __init__(self) -> None:
        """
        Initializes a new TempMail instance by creating a temporary email account
        and setting its attributes such as id, email, password, and token.
        """
        self.ua = choice(user_agents)

        for key, value in self._create_account().items():
            setattr(self, key, value)

    def _generate_email(self, domain: str = None) -> str:
        """
        Generates a random email address with a random domain or a specified domain.

        If no domain is provided, a random domain is selected from active domains.

        Args:
            domain (str, optional): The domain for the email. If None, a random domain is used.

        Returns:
            str: A randomly generated email address.
        """
        if not domain:
            domain = self._get_domains(True)
        return ''.join(choices(ascii_lowercase, k=10)) + '@' + domain

    def _generate_password(self, length: int = 18) -> str:
        """
        Generates a random password.

        Args:
            length (int, optional): Length of the password. Default is 18 characters.

        Returns:
            str: A randomly generated password.
        """
        return ''.join(choices(ascii_uppercase + ascii_lowercase + digits, k=length))

    def _get_domains(self, random: bool = False):
        """
        Retrieves a list of active domains from the API.

        Args:
            random (bool, optional): If True, returns a single random active domain. Defaults to False.

        Returns:
            list or str: A list of active domains or a single random domain.
        """
        resp = get('https://api.mail.tm/domains')
        domains = []

        for item in resp.json()['hydra:member']:
            if item['isActive']:
                domains.append(item['domain'])
        if random:
            return choice(domains)
        return domains

    def _create_account(self, email: str = None, password: str = None) -> dict:
        """
        Creates a new temporary email account and returns the account's details.

        If no email or password is provided, random ones are generated.

        Args:
            email (str, optional): The email address for the account. Defaults to None.
            password (str, optional): The password for the account. Defaults to None.

        Returns:
            dict: A dictionary containing the account details (id, email, password, token).
        """
        if not email:
            email = self._generate_email()
        if not password:
            password = self._generate_password()
        resp = post(url='https://api.mail.tm/accounts', headers={'User-Agent': self.ua, 'Content-Type': 'application/json'}, data='{"address":"' + email + '","password":"' + password + '"}')
        resp2 = post(url='https://api.mail.tm/token', headers={'User-Agent': self.ua, 'Content-Type': 'application/json'}, data='{"address":"' + email + '","password":"' + password + '"}')
        
        return {
            'id': resp.json()['id'],
            'email': resp.json()['address'],
            'password': password,
            'token': resp2.json()['token']
        }

    def get_messages(self) -> list:
        """
        Fetches the messages for the temporary email account.

        Returns:
            list: A list of Message objects representing the received emails.
        """
        resp = get('https://api.mail.tm/messages', headers={'User-Agent': self.ua, 'Authorization': 'Bearer ' + self.token})
        return [Message(item, self.token, self.ua) for item in resp.json()['hydra:member']]

class Message:
    """
    Represents an email message retrieved from the mail.tm API.
    
    Attributes:
        from_addr (str): Sender's email address.
        from_name (str): Sender's name.
        sent_time (str): Timestamp of when the email was sent.
        subject (str): Subject of the email.
        id (str): Unique identifier for the email message.
        token (str): Authentication token used to access email content.
    """
    def __init__(self, object, token, ua):
        """
        Initializes a Message object using data from the API response.

        Args:
            object (dict): Dictionary containing email details.
            token (str): Authentication token for API access.
            ua (str): User-Agent header to be used in API requests.
        """
        self.ua = ua
        self.from_addr = object['from']['address']
        self.from_name = object['from']['name']
        self.sent_time = object['updatedAt']
        self.subject = object['subject']
        self.id = object['id']
        self.token = token

    @property
    def html(self):
        """
        Retrieves the HTML content of the email by making an authenticated API request.
        
        Returns:
            str: HTML content of the email.
        """
        resp = get('https://api.mail.tm/messages/' + self.id,
                   headers={'User-Agent': self.ua, 'Authorization': 'Bearer ' + self.token})
        return ''.join(resp.json()['html'])

class Icons:
    """
    Stores various icon images to be used within the application.

    Attributes:
        sun (CTkImage): Icon for the sun (day mode).
        moon (CTkImage): Icon for the moon (night mode).
        online (CTkImage): Icon representing an online status.
        offline (CTkImage): Icon representing an offline status.
        regenerate (CTkImage): Icon representing a refresh or regenerate action.
        copy (CTkImage): Icon representing a copy action.
    """
    sun = CTkImage(
            open_image("Icons\\sun.png"), size=(25, 25)
            )
    moon = CTkImage(
            open_image("Icons\\moon.png"), size=(25, 25)
            )
    online = CTkImage(
            open_image("Icons\\online.png"), size=(25, 25)
            )
    offline = CTkImage(
        open_image("Icons\\offline.png"), size=(25, 25)
        )
    regenerate = CTkImage(
            open_image("Icons\\refresh.png"), size=(25, 25)
            )
    copy = CTkImage(
            open_image("Icons\\copy.png"), size=(40, 40)
            )
    
class Window(CTk):
    def __init__(self) -> None:
        super().__init__()

        # Flags and variables
        self.connection_status = self._is_online()  # Track internet connection status
        self.is_generating_email = False  # Prevent multiple email generation requests
        self.inbox = {}  # Store received messages
        self.tm = None  # Temporary email object

        # -- Configure main window --
        self._set_window_geometry()
        self.title("TempMail")
        set_appearance_mode("Dark")
        self.iconbitmap("Icons/email.ico")
        # Config rows and columns weight in master window
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # A protocol for stop the background tasks when user close the GUI window
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Set up font for the application
        self.FONT = lambda size, w: CTkFont("Ubuntu", size, w)

        # -- Configure top frame (UI elements like theme switch and connection status) --
        TopFrame = CTkFrame(self)
        TopFrame.grid(row=0, column=0, sticky=NSEW)
        # Config rows and columns weight in TopFrame
        TopFrame.rowconfigure(1, weight=1)
        TopFrame.columnconfigure((0,1,2), weight=1)
        # Bind right-click on TopFrame button to load the default html
        TopFrame.bind("<Button-1>", 
                lambda event: self._load_default_html()
            )
        
        # Theme toggle button (sun/moon icon)
        self.theme_button = CTkButton(TopFrame, text="",
                                      command=self._change_theme,
                                      fg_color="transparent",
                                      image=Icons.sun,
                                      width=20, height=20,
                                      hover=False
                                     ) 
        self.theme_button.grid(row=0, column=0, sticky=W)

        # Connection status icon (online/offline)
        self.connection_status_icon = CTkLabel(TopFrame, text="",
                                               fg_color="transparent",
                                               image=Icons.online,
                                               width=40, height=40
                                              ) 
        self.connection_status_icon.grid(row=0, column=2, sticky=E)

        # -- Configure inner frame (temporary email address display and actions) --
        InnerFrame = CTkFrame(TopFrame, fg_color="transparent",
                                width=300, height=100
                             )
        InnerFrame.grid(row=0, pady=5, column=1, rowspan=2)
        # Config rows and columns weight in InnerFrame
        InnerFrame.rowconfigure(1, weight=1)

        # Label for temporary email address
        CTkLabel(InnerFrame,
                 text="Temporary Email Address",
                 font=self.FONT(20, "bold"),
                ).grid(row=0, column=0)
        
        # A button to let user to ask another email
        regenerate_button = CTkButton(InnerFrame, text="",
                                      command=self.regenerate_email,
                                      fg_color="transparent",
                                      image=Icons.regenerate,
                                      width=5, height=5,
                                      hover=False
                                     ) 
        regenerate_button.grid(row=0, column=1, sticky=E, padx=5)

        # Email entry field
        # A field for showing the current email to user
        self.email_entry = CTkEntry(InnerFrame, corner_radius=50,
                                    height=50, width=250, state=DISABLED,
                                    font=self.FONT(14, NORMAL)
                                   ) 
        self.email_entry.grid(row=1, column=0)

        # Copy email button (copy to clipboard)
        copy_button = CTkButton(InnerFrame, text="",
                                image=Icons.copy, hover=False,
                                command=self._copy_email,
                                fg_color="transparent",
                                width=5, height=5
                               )
        copy_button.grid(row=1, column=1)

        # -- Configure bottom frame (for inbox and HTML content display) --
        BottomFrame = CTkFrame(self, fg_color="transparent")
        BottomFrame.grid(row=1, column=0, sticky=NSEW, pady=3, padx=2)
        # Config rows and columns weight in BottomFrame
        BottomFrame.rowconfigure(0, weight=1)
        BottomFrame.columnconfigure(1, weight=1)

        # -- Set up PanedWindow (resizable frame for inbox and HTML view) --
        self.PanedWindow = PanedWindow(BottomFrame, orient=HORIZONTAL, 
                                       sashrelief=FLAT, sashwidth=5,
                                       background="#242424"
                                       ) 
        self.PanedWindow.pack(fill=BOTH, expand=True)

        # -- Inbox Frame (displays received email messages) --
        InboxFrame = CTkFrame(self.PanedWindow, border_width=0)
        # A listbox for showing the inbox messages
        self.inbox_list = CTkListbox(InboxFrame, corner_radius=0,
                                     fg_color="transparent",
                                     border_width=0, width=300,
                                     command=self._open_message,
                                    ) 
        self.inbox_list.pack(expand=True, fill=BOTH)
        self.inbox_list.bind("<Button-1>",
                            lambda event: self._load_default_html()
                        )

        # -- HTML Frame (displays email content and default HTML page) --
        self.HtmlFrame = HtmlFrame(self.PanedWindow, vertical_scrollbar=True,
                                   horizontal_scrollbar=False,
                                   messages_enabled=False
                                  ) 
        # Load the default HTML page for first time
        self.HtmlFrame.load_html(default_html) 
        self.is_default_html = True

        # Deactivating the mousewheel
        self.unbind_all("<MouseWheel>") 
        # To Open The Links in Browser
        self.HtmlFrame.on_link_click(lambda url: open_in_browser(url)) 
        
        # Add inbox and HTML frames into the PanedWindow
        self.PanedWindow.add(InboxFrame)
        self.PanedWindow.add(self.HtmlFrame)

        # Initialize background tasks
        background_tasks = [
            Agent(self.update_connection_status),
            Agent(self.update_inbox)
        ]

        self.Core = Core(list_of_agents=background_tasks)
        self.Core.run()
        self.Core.add_task(Agent(self.generate_email))

    def _set_window_geometry(self) -> None:
        """
        Sets the geometry (size and resolution) of the window based on the screen's
        width and height, with a fixed window size at 72% of the screen width and 77%
        of the screen height. The window is also set to be non-resizable.
        """

        # Screen dimensions (width and height)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Constants for the desired window size as a percentage of the screen size
        WIDTH_PERCENTAGE = 0.75
        HEIGHT_PERCENTAGE = 0.77

        # Calculate the window's width and height
        window_width = int(screen_width * WIDTH_PERCENTAGE)
        window_height = int(screen_height * HEIGHT_PERCENTAGE)

        # Calculate the position to center the window
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Set the window size position and make it non-resizable
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.resizable(False, False)

    def _raise_window(self) -> None:
        """
        Brings the window to the front and ensures it has focus. 
        This method is useful for making the window the active, top-most window in the UI.
        
        It does the following:
        - Uses `self.lift()` to bring the window to the front of other windows.
        - Uses `self.focus_force()` to force focus on the window, ensuring it's the active window.
        """
        # Bring the window to the front of other windows
        self.lift()
        
        # Force focus on the window to ensure it's the active window
        self.focus_force()

    def _change_theme(self) -> None:
        """
        Toggles the theme between Light and Dark mode. 
        - If the current theme is Light, it switches to Dark mode, changes the theme button icon to a sun icon, 
        and updates the background color of the PanedWindow.
        - If the current theme is Dark, it switches to Light mode, changes the theme button icon to a moon icon, 
        and updates the background color of the PanedWindow.
        """

        # Check the current appearance mode
        if get_appearance_mode() == "Light":
            # Switch to Dark mode
            set_appearance_mode("Dark")
            
            # Update the theme button icon to represent Light mode (sun icon)
            self.theme_button.configure(image=Icons.sun)
            
            # Set the background color of the PanedWindow to Dark mode color
            self.PanedWindow.configure(background="#242424")

        else:
            # Switch to Light mode
            set_appearance_mode("Light")
            
            # Update the theme button icon to represent Dark mode (moon icon)
            self.theme_button.configure(image=Icons.moon)
            
            # Set the background color of the PanedWindow to Light mode color
            self.PanedWindow.configure(background="#ebebeb")

    def _load_default_html(self) -> None:
        """
        Loads the default HTML content into the HtmlFrame if it is not already loaded.
        This prevents redundant reloads and ensures the default page is displayed.
        """
        if not self.is_default_html:
            self.HtmlFrame.load_html(default_html)
            self.is_default_html = True

    def _is_online(self) -> bool:
        """
        Checks if the device has an active internet connection by sending HTTP requests to two external URLs.
        - The method tries to send GET requests to "https://google.com" and "http://mojeip.net.pl/asdfa/azenv.php".
        - If either request returns a status code of 200 (indicating success), the method returns `True`, indicating the device is connected to the internet.
        - If an exception occurs (e.g., no internet connection), it returns `False`.
        
        Returns:
            bool: True if either of the requests is successful (status code 200), False otherwise.
        """
        
        try:
            # Send GET request to google.com with a timeout of 5 seconds
            r1 = get("https://google.com", timeout=5)
            
            # Send GET request to a second URL with a timeout of 5 seconds
            r2 = get("http://mojeip.net.pl/asdfa/azenv.php", timeout=5)
            
            # Return True if either request is successful (status code 200)
            return r1.status_code == 200 or r2.status_code == 200
        except:
            # If any exception occurs (e.g., no internet), return False
            return False

    def _convert_time(self, iso_time: str) -> str:
        """
        Converts an ISO-formatted date string to a local time string.

        Args:
            iso_date (str): The ISO-formatted date string.

        Returns:
            str: The local time string in "HH:MM:SS" format.
        """
        # fetch the system time zone
        system_timezone = datetime.now(tz=timezone.utc).astimezone().tzinfo 
        # Parse the ISO date string to a datetime object
        time_utc = datetime.fromisoformat(iso_time.replace("Z", "+00:00"))  
        # Convert the UTC time to the system's local time zone
        time_local = time_utc.astimezone(system_timezone)
        # Format the local time as a string and return it
        return time_local.strftime("%H:%M:%S")
    
    def _show_notification(self, on_click: callable, *args) -> None:
        """
        Displays a notification with a custom icon and triggers a callback when clicked.

        Args:
            on_click (callable): Function to call when the notification is clicked.
            *args (str): The text fields to be shown in the notification.
        """
  
        # Create an instance of WindowsToaster to handle displaying notifications.
        frame = WindowsToaster("TempMail")
        
        # Create an instance of the Toast class, which represents the notification.
        notif = Toast()
        
        # Add an image to the notification using the specified path.
        notif.AddImage(ToastDisplayImage.fromPath("Icons\\email.png"))
        
        # Set the action that should occur when the notification is activated (clicked).
        notif.on_activated = lambda event: on_click()  # Calls the on_click callback when clicked.
        
        # Set the text fields for the notification to the provided arguments.
        notif.text_fields = args
        
        # Display the notification using the Windows toaster.
        frame.show_toast(notif)
    
    def _copy_email(self) -> None:
        """
        Copies the current email address to the clipboard.
        Triggered when the user clicks the copy button.
        """
        self.clipboard_clear()
        self.clipboard_append(self.email_entry.get()) 
    
    def update_connection_status(self) -> None:
        """
        Periodically checks the internet connection and updates the status icon.
        """
        while True:
            if self._is_online():
                self.connection_status_icon.configure(image=Icons.online)
                self.connection_status = True
            else:
                self.connection_status_icon.configure(image=Icons.offline)
                self.connection_status = False

            # Check connection and update UI every 4 second
            sleep(4)
    
    def generate_email(self) -> None:
        """
        Generates a new temporary email address and updates the UI.
        Displays notifications when the email is ready or if there is an issue.
        """
        if self.connection_status: 

            self.is_generating_email = True
            self.email_entry.configure(state=NORMAL)
            self.email_entry.delete(0, END)
            self.email_entry.insert(END, "Generating email...")
            self.email_entry.configure(state=DISABLED)

            while True:
                try:
                    # if email generating was Successful
                    self.tm = TempMail()
                    self.email_entry.configure(state=NORMAL)
                    self.email_entry.delete(0, END)
                    self.email_entry.insert(END, self.tm.email)
                    self.is_generating_email = False

                    self._show_notification(self._copy_email,
                                            "Your email is ready!",
                                            self.tm.email,
                                            "Tap to copy"
                                           )
                    self.inbox.clear()
                    self.inbox_list.delete(0, END)
                    break

                except:
                    # if email generatig wasn't Successful
                    self.tm = None
                    sleep(3)
        else:
            # if device wasn't online
            self.tm = None
            self.email_entry.configure(state=NORMAL)
            self.email_entry.delete(0, END)
            self.email_entry.insert(END, "Offline! Can't generate email.")
        
        self.email_entry.configure(state=DISABLED)
    
    def regenerate_email(self) -> None:
        """
        Regenerates the temporary email address by adding it into the tasks-list for Core
        Called when user click on the regenerate button.
        """
        if not self.is_generating_email:
            self.Core.add_task(Agent(self.generate_email))

        self._load_default_html()

    def update_inbox(self) -> None:
        """
        Updates the inbox with new messages and displays them in the UI.
        """
        while True:
            if self.connection_status and self.tm: # if internet was connected and email was created
                messages = self.tm.get_messages() # All received messages

                for msg in messages:
                    header = f"{msg.subject}\n{msg.from_addr} <{self._convert_time(msg.sent_time)}>"

                    if header not in self.inbox: # Prevent duplicate message
                        self.inbox.update({header: msg.html})
                        self.inbox_list.insert(END, header) # Insert into the inbox list in UI

                        self._show_notification(self._raise_window,
                                                "New Message", msg.from_addr, msg.subject)
            # Update inbox every 3 second
            sleep(3)

    def _open_message(self, header) -> None:
        """
        Displays the selected email message in the HTML frame.
        Called when user click on a message in inbox list.

        Args:
            header (str): The header of the selected email message.
        """
        message_content = self.inbox[header]
        self.HtmlFrame.load_html(message_content)
        self.is_default_html = False

    def _on_closing(self) -> None:
        for var in list(globals().keys()):
            if var not in ["__name__", "__file__", "__doc__", "__builtins__"]:
                del globals()[var]
        
        for var in list(locals().keys()):
            if var != "delete_locals":
                del locals()[var]
    
        self.destroy()
        
        from os import _exit
        _exit(1)


if __name__ == "__main__":
    # Load HTML page for using in UI
    try: 
        with open("Index.html", "r") as htm:
            default_html = htm.read()
    except FileNotFoundError:
        default_html = "<html></html>"

    window = Window()  
    window.mainloop()    
