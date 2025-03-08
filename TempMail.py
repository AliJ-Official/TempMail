from string import ascii_lowercase, ascii_uppercase, digits
from Modules.UserAgents import user_agents
from datetime import datetime, timezone
from Modules.Core import Agent, Core
from random import choice, choices
from requests import get, post
from time import sleep
from os import _exit

from windows_toasts import Toast, WindowsToaster, ToastDisplayImage
from webbrowser import open as open_in_browser
from PIL.Image import open as open_image
from CTkListbox import CTkListbox
from tkinterweb import HtmlFrame
from tkinter import PanedWindow
from customtkinter import *


class TempMail:
    """
    A class to manage temporary email accounts using the mail.tm API.

    Attributes:
        id (str): The ID of the temporary email account.
        email (str): The email address of the temporary email account.
        password (str): The password for the temporary email account.
        token (str): The authentication token for the temporary email account.
    """

    def __init__(self, ua: str) -> None:
        """
        Initialize a new TempMail instance by creating a temporary email account
        and setting its attributes.
        """
        self.ua = ua

        for key, value in self._create_account().items():
            setattr(self, key, value)

    def __str__(self) -> str:
        """
        Return a string representation of the TempMail instance.

        Returns:
            str: A string representation of the instance.
        """
        return f'<id: {self.id} email: {self.email}>'

    def _generate_email(self, domain: str = None) -> str:
        """
        Generate a random email address.

        Args:
            domain (str, optional): The domain part of the email address.
            If not provided, a random active domain will be used.

        Returns:
            str: A randomly generated email address.
        """
        if not domain:
            domain = self._get_domains(True)
        return ''.join(choices(ascii_lowercase, k=10)) + '@' + domain

    def _generate_password(self, length: int = 18) -> str:
        """
        Generate a random password.

        Args:
            length (int, optional): The length of the password. Defaults to 18.

        Returns:
            str: A randomly generated password.
        """
        return ''.join(choices(ascii_uppercase + ascii_lowercase + digits, k=length))

    def _get_domains(self, random: bool = False):
        """
        Get a list of active domains from the API.

        Args:
            random (bool, optional): If True, returns a single random domain.
            Defaults to False.

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
        Create a temporary email account and return its details.

        Args:
            email (str, optional): The email address for the account.
            If not provided, a random email will be generated.
            password (str, optional): The password for the account.
            If not provided, a random password will be generated.

        Returns:
            dict: A dictionary containing the account details.
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
        Get a list of messages for the temporary email account.

        Returns:
            list: A list of Message objects representing the messages.
        """
        resp = get('https://api.mail.tm/messages', headers={'User-Agent': self.ua, 'Authorization': 'Bearer ' + self.token})
        return [Message(item, self.token, self.ua) for item in resp.json()['hydra:member']]

class Message:
    """
    A class to represent an email message retrieved from the mail.tm API.

    Attributes:
        from_addr (str): The sender's email address.
        from_name (str): The sender's name.
        sent_time (str): The time when the email was sent.
        subject (str): The subject of the email.
        id (str): The unique identifier of the email message.
        token (str): The authentication token for accessing the email content.
    """

    def __init__(self, object: dict, token: str, ua: str):
        """
        Initialize a new Message instance with details from a dictionary.

        Args:
            object (dict): A dictionary containing the email message details.
            token (str): The authentication token for accessing the email content.
        """
        self.ua = ua

        self.from_addr = object['from']['address']
        self.from_name = object['from']['name']
        self.sent_time = object['updatedAt']
        self.subject = object['subject']
        self.id = object['id']
        self.token = token

    @property
    def html(self) -> str:
        """
        Property to retrieve the HTML content of the email message.

        Returns:
            str: The HTML content of the email message.
        """
        # Make a GET request to the mail.tm API to retrieve the email content
        resp = get('https://api.mail.tm/messages/' + self.id,
                   headers={'User-Agent': self.ua, 'Authorization': 'Bearer ' + self.token})
        # Return the HTML content from the API response
        return ''.join(resp.json()['html'])

class Master(CTk):
    def __init__(self) -> None:
        super().__init__()

        # This flag prevents user requests to generate another email at same time
        self.is_generatig_email = False
        # A flag for showing the connection status
        self.connection_status = self._check_connection()
        # A container for carrying the Received messages and them content
        self.msgs_content = {}
        # A variable that gonne overwrite during the program and store the curent generated email
        self.tm = None 

        # --Config the master window--
        self._set_geometry()
        self.title("TempMail")
        set_appearance_mode("Dark")
        self.iconbitmap("Icons\\email.ico")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # A protocol for stop the background tasks when user close the GUI window
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Define Font for program
        self.FONT = lambda size, w: CTkFont("Ubuntu", size, w)

        # --Config TopFrame--
        TopFrame = CTkFrame(self)
        TopFrame.grid(row=0, column=0, sticky=NSEW)
        TopFrame.rowconfigure(1, weight=1)
        TopFrame.columnconfigure((0,1,2), weight=1)
        TopFrame.bind("<Button-1>", lambda event: self.HtmlFrame.load_html(default_html))

        self.sun_icon = CTkImage( # Load sun_icon for light theme
            open_image("Icons\\sun.png"), size=(25, 25)
            )
        self.moon_icon = CTkImage( # Load moon-icon for dark theme
            open_image("Icons\\moon.png"), size=(25, 25)
            )
        # Config Theme Button
        self.theme_button = CTkButton(TopFrame, text="",
                                        fg_color="transparent",
                                        image=self.sun_icon,
                                        width=20, height=20,
                                        command=self._change_theme,
                                        hover=False
                                        ) # A button to let user change the theme(light|dark)
        self.theme_button.grid(row=0, column=0, sticky=W)

        self.online_icon = CTkImage( # Load online-icon for connection status
            open_image("Icons\\online.png"), size=(25, 25)
            )
        self.offline_icon = CTkImage( # Load offline-icon for connection status
            open_image("Icons\\offline.png"), size=(25, 25)
            )
        # Config connection status 
        self.connection_status_icon = CTkLabel(TopFrame, text="",
                                           fg_color="transparent",
                                           image=self.online_icon,
                                           width=40, height=40
                                           ) # A lable for showing the connection status to user
        self.connection_status_icon.grid(row=0, column=2, sticky=E)

        # --Initialize EmailFrame--
        EmailFrame = CTkFrame(TopFrame, fg_color="transparent",
                                   width=300, height=100)
        EmailFrame.grid(row=0, pady=5, column=1, rowspan=2)
        EmailFrame.rowconfigure(1, weight=1)

        # A fixed lable for guid the user 
        CTkLabel(EmailFrame,
                text="Temporary Email Address", font=self.FONT(20, "bold"),
                ).grid(row=0, column=0)
        
        regenerate_icon = CTkImage( # Load icon for regenerate-email button
            open_image("Icons\\refresh.png"), size=(25, 25)
            )
        # Config Regenerate Button
        regenerate_button = CTkButton(EmailFrame, text="",
                                      fg_color="transparent",
                                      image=regenerate_icon,
                                      width=5, height=5,
                                      command=self.regenerate_email,
                                      hover=True
                                      ) # A button to let user to ask another email
        regenerate_button.grid(row=0, column=1, sticky=E, padx=5)

        # Email Entry 
        self.email_entry = CTkEntry(EmailFrame, corner_radius=50,
                                    height=50, width=250, state=DISABLED
                                    ) # A field for showing the current email to user
        self.email_entry.grid(row=1, column=0)
     
        copy_icon = CTkImage( # Load icon for copy button
            open_image("Icons\\copy.png"), size=(40, 40)
            )
        # Config copy button
        copy_button = CTkButton(EmailFrame, text="",
                                    fg_color="transparent",
                                    image=copy_icon, hover=True,
                                    command=self._copy_email,
                                    width=5, height=5
                                    ) # A button to copy the current email into the clipboard
        copy_button.grid(row=1, column=1)

        # --Initialize BottomFrame--
        BottomFrame = CTkFrame(self, fg_color="transparent")
        BottomFrame.grid(row=1, column=0, sticky=NSEW, pady=3, padx=2)
        BottomFrame.rowconfigure(0, weight=1)
        BottomFrame.columnconfigure(1, weight=1)

        # --Initialize PanedWindow--
        self.PanedWindow = PanedWindow(BottomFrame, orient=HORIZONTAL, 
                                       sashrelief=FLAT, sashwidth=5,
                                       background="#242424"
                                       ) # A resizable frame for user convenience in manage the InboxFrame and HtmlFrame
        self.PanedWindow.pack(fill=BOTH, expand=True)

        # --Initialize InboxFrame--
        InboxFrame = CTkFrame(self.PanedWindow, border_width=0)
        
        self.inbox_list = CTkListbox(InboxFrame, corner_radius=0,
                                    fg_color="transparent",
                                    border_width=0, width=300,
                                    command=self._open_messages,
                                    ) # A listbox for showing the inbox messages
        self.inbox_list.pack(expand=True, fill=BOTH)
        self.inbox_list.bind("<Button-1>", lambda event: self.HtmlFrame.load_html(default_html))

        # --Initialize HtmlFrame-- 
        self.HtmlFrame = HtmlFrame(self.PanedWindow, vertical_scrollbar=True,
                                    horizontal_scrollbar=False,
                                    messages_enabled=False
                                ) # A frame that gonna show the messages content and default HTML page in self
    
        self.HtmlFrame.load_html(default_html) # Load the default HTML page for first time
        self.unbind_all("<MouseWheel>") # Deactivating the mousewheel
        self.HtmlFrame.on_link_click(lambda url: open_in_browser(url)) # To Open The Links in Browser
        
        # Add two(InboxFrame, self.HtmlFrame) into the PanedWindow(resizable window)
        self.PanedWindow.add(InboxFrame)
        self.PanedWindow.add(self.HtmlFrame)

        # --Initialize background tasks--
        tasks = [ # A task list for running them Asynchronous
            Agent(self.update_connection_status),
            Agent(self.update_inbox),
        ]
        
        # Instance of the Core Class to Handle the Asynchronous tasks
        self.core = Core(list_of_agents=tasks) 
        self.core.run()
        self.core.add_task(Agent(self.generate_email)) # Disposable task (call for one time)

    def _set_geometry(self) -> None:
        """
        Fetch the screen size and set the program master window geometry accordingly.
        """
        sc_width = self.winfo_screenwidth()
        sc_height = self.winfo_screenheight()

        window_width = int(sc_width*0.72)
        window_height = int(sc_height*0.77)

        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)

    def raise_window(self) -> None:
        self.lift()  # Bring the Tkinter window to the front
        self.focus_force() # Force focus on the window to make sure it's the active window

    def _change_theme(self) -> None:
        """
        Change the theme.
        called when user click on the change theme button.
        """
        if get_appearance_mode() == "Light":
            set_appearance_mode("Dark")
            self.theme_button.configure(image=self.sun_icon)
            self.PanedWindow.configure(background="#242424")
        else:
            set_appearance_mode("Light")
            self.theme_button.configure(image=self.moon_icon)
            self.PanedWindow.configure(background="#ebebeb")
        
    def _copy_email(self) -> None:
        """
        Copies the current email address to the clipboard.
        Called when user click on the copy button.
        """
        self.clipboard_clear()
        self.clipboard_append(self.email_entry.get())  

    def update_connection_status(self) -> None:
        """
        Check the connection status using self._check_connection and updates the UI accordingly.
        """
        while True:
            if self._check_connection():
                self.connection_status_icon.configure(image=self.online_icon)
                self.connection_status = True
            else:
                self.connection_status_icon.configure(image=self.offline_icon)
                self.connection_status = False

            # Check connection and update UI every 5 second
            sleep(5)

    def _check_connection(self) -> bool:
        """
        Checks the internet connection status.
        """
        try:
            r1 = get("https://google.com", timeout=5)
            r2 = get("http://mojeip.net.pl/asdfa/azenv.php", timeout=5)
            return r1.status_code == 200 or r2.status_code == 200
        except:
            return False
        
    def _convert_time(self, iso_date: str) -> str:
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
        time_utc = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))  
        # Convert the UTC time to the system's local time zone
        time_local = time_utc.astimezone(system_timezone)
        # Format the local time as a string and return it
        return time_local.strftime("%H:%M:%S")

    def generate_email(self) -> None:
        """
        Generates a new temporary email address and updates the UI.
        """
        if self.connection_status:
            ua = choice(user_agents) # choose an user_agent randomly every time 

            self.is_generatig_email = True
            while True:
                try:
                    # if email generating was Successful
                    self.tm = TempMail(ua)
                    self.email_entry.configure(state=NORMAL)
                    self.email_entry.delete(0, END)
                    self.email_entry.insert(END, self.tm.email)
                    self.is_generatig_email = False

                    self._show_notification(self._copy_email,
                                                "Your email is ready!",
                                                self.tm.email,
                                                "Tap to copy"
                                            )
                    self.msgs_content.clear()
                    self.inbox_list.delete(0, END)
                    break

                except:
                    # if email generatig wasn't Successful
                    self.tm = None
                    self.email_entry.configure(state=NORMAL)
                    self.email_entry.delete(0, END)
                    self.email_entry.insert(END, "Generating your email...")
                    sleep(3)
        else:
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
        if not self.is_generatig_email:
            self.core.add_task(Agent(self.generate_email))

    def _show_notification(self, on_click, *args) -> None:  
        """
        Displays a notification with the specified message and triggers a callback when clicked.

        This function creates a notification with a custom icon and text fields, then displays
        it using a Windows toaster. When the notification is activated (clicked), the provided
        `on_click` callback function is executed.

        Parameters:
        on_click (function): A callback function to be executed when the notification is clicked.
        *args (str): A variable number of text fields to be included in the notification's content.

        Returns:
        None

        Example:
        _show_notification(lambda: print("Notification clicked"), "You have a new email!")
        """
  
        # Create an instance of WindowsToaster to handle displaying notifications.
        notif_frame = WindowsToaster("TempMail")
        
        # Create an instance of the Toast class, which represents the notification.
        notif = Toast()
        
        # Add an image to the notification using the specified path.
        notif.AddImage(ToastDisplayImage.fromPath("Icons\\email.png"))
        
        # Set the action that should occur when the notification is activated (clicked).
        notif.on_activated = lambda event: on_click()  # Calls the on_click callback when clicked.
        
        # Set the text fields for the notification to the provided arguments.
        notif.text_fields = args
        
        # Display the notification using the Windows toaster.
        notif_frame.show_toast(notif)
      
    def update_inbox(self) -> None:
        """
        Updates the inbox with new messages and displays them in the UI.
        """
        while True:
            if self.connection_status and self.tm: # if internet was connected and email was created
                all_messages = self.tm.get_messages() # All received messages

                for msg in all_messages:
                    header = f"{msg.subject}\n{msg.from_name} | {msg.from_addr} <{self._convert_time(msg.sent_time)}>"

                    if header not in self.msgs_content: # Prevent duplicate message
                        self._show_notification(self.raise_window, 
                                                "New Message", msg.from_addr, msg.subject)

                        self.msgs_content.update({header: msg.html})
                        self.inbox_list.insert(END, header) # Insert into the inbox list in UI

            # Update inbox every 5 second
            sleep(3)

    def _open_messages(self, header) -> None:
        """
        Displays the selected email message in the HTML frame.
        Called when user click on a message in inbox list.

        Args:
            header (str): The header of the selected email message.
        """
        html = self.msgs_content[header]
        self.HtmlFrame.load_html(html)

    def _on_closing(self) -> None:
        self.destroy()
        _exit(0)


if __name__ == "__main__":
    try: # Load the HTML page and HtmlFrame in Program gonna use it
        with open("Index.html", "r") as htm:
            default_html = htm.read()
    except FileNotFoundError:
        default_html = "<html></html>"

    program = Master()
    program.mainloop()
