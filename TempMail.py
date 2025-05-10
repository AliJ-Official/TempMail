from windows_toasts import Toast, WindowsToaster, ToastDisplayImage
from webbrowser import open as open_in_browser
from PIL.Image import open as open_image
from CTkListbox import CTkListbox
from tkinterweb import HtmlFrame
from tkinter import PanedWindow
from customtkinter import *

from Modules.TempMail_API import TempMail
from Modules.CoreB import Core, Agent
from requests import get
from time import sleep


class Icons:
    """
    Stores various icon images to be used within the application.

    Attributes:
        sun (CTkImage): Light mode toggle icon (25x25px).
        moon (CTkImage): Dark mode toggle icon (25x25px).
        online (CTkImage): Connection active status indicator (25x25px).
        offline (CTkImage): Connection inactive status indicator (25x25px).
        regenerate (CTkImage): Refresh/reload action icon (25x25px).
        copy (CTkImage): Copy to clipboard action icon (40x40px).
        tempmail_ico (str): Path to the application's .ico file for window icons.
        tempmail_png (str): Path to the application's .PNG logo file.
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
    tempmail_ico = "Icons\\TempMail.ico"
    tempmail_png = "Icons\\TempMail.png"


class TempMailGUI(CTk):
    def __init__(self) -> None:
        """
        Initializes the TempMailGUI class and sets up the master application window, 
        user interface components, and background tasks.
        """
        super().__init__()

        # Initialize variables and flags
        self.__connection_status: bool = self._is_online() 
        self.__is_generating_email: bool = False # Flag to prevent multiple email generations
        self.__is_on_homepage: bool = False # Flag to check if the homepage is loaded
        self.__is_tasks_running: bool = True # Flag to handle the background tasks
        self.__homepage: str = None # HTML content for the homepage
        self.__tempmail: TempMail = None # Temporary email object
        self.__inbox: dict = {} # Dictionary to store inbox messages

        # Initialize master window
        self.title("TempMail")
        self._set_window_geometry()
        set_appearance_mode("Dark")
        self.iconbitmap(Icons.tempmail_ico)  
        # Configure rows and columns weight of master window
        self.rowconfigure(1, weight=1)  
        self.columnconfigure(0, weight=1)
        
        # Set up font for the application
        self.FONT = lambda size, w: CTkFont("Roboto", size, w)

        # A protocol to handle the window close event to clean up resources.
        self.protocol("WM_DELETE_WINDOW", self._on_closing)  

        # Initialize ToolBarFrame 
        ToolBarFrame = CTkFrame(self)
        ToolBarFrame.grid(row=0, column=0, sticky=NSEW)

        # Configure rows and columns weight of ToolBarFrame
        ToolBarFrame.rowconfigure(1, weight=1)
        ToolBarFrame.columnconfigure((0,1,2), weight=1)

        # Bind right-click on TopFrame to load the homepage
        ToolBarFrame.bind(
            "<Button-1>", 
            lambda event: self._click_on_free_space()
            )
        
        # Define switch-theme button (light/dark mode)
        self.switch_theme_button = CTkButton(ToolBarFrame, fg_color="transparent",
                                            text="", width=20, height=20,
                                            image=Icons.sun, hover=False,
                                            command=self._switch_theme
                                            ) 
        self.switch_theme_button.grid(row=0, column=0, sticky=W)

        # Define connection-status-ico lable (online/offline)
        self.connection_status_ico = CTkLabel(ToolBarFrame, fg_color="transparent",
                                               text="", width=40, height=40,
                                               image=Icons.online
                                              ) 
        self.connection_status_ico.grid(row=0, column=2, sticky=E)

        # Initialize InnerFrame (a frame within the ToolBarFrame)
        InnerFrame = CTkFrame(ToolBarFrame, fg_color="transparent",
                              width=300, height=100
                             )
        InnerFrame.grid(row=0, pady=5, column=1, rowspan=2)

        # Configure row weight of InnerFrame
        InnerFrame.rowconfigure(1, weight=1)

        # A fixed label
        CTkLabel(InnerFrame, font=self.FONT(20, "bold"),
                 text="Temporary Email Address",
                ).grid(row=0, column=0)
    
        # Define regenerate-email button (let user to ask another email)
        regenerate_button = CTkButton(InnerFrame, fg_color="transparent",
                                      text="", width=5, height=5,
                                      command=self._regenerate_email,
                                      image=Icons.regenerate, hover=False
                                     ) 
        regenerate_button.grid(row=0, column=1, sticky=E, padx=5)

        # Initialize Email entry field (to display the temprary email address)
        self.email_entry = CTkEntry(InnerFrame, corner_radius=50,
                                    height=50, width=250, state=DISABLED,
                                    font=self.FONT(14, NORMAL)
                                   ) 
        self.email_entry.grid(row=1, column=0)

        # Define copy-email button (copy email address in clipboard)
        copy_button = CTkButton(InnerFrame, fg_color="transparent",
                                text="", width=5, height=5,
                                command=self._copy_in_clipboard,
                                image=Icons.copy, hover=False
                               )
        copy_button.grid(row=1, column=1)

        # Initialize PanedWindow (resizable frame for inbox-list and HTML-frame view)
        self.PanedWindow = PanedWindow(self, orient=HORIZONTAL, 
                                       sashrelief=FLAT, sashwidth=5,
                                       background="#242424"
                                       ) 
        self.PanedWindow.grid(row=1, column=0, sticky=NSEW, pady=3, padx=2)

        # Initialize InboxFrame (inbox_list carrier)
        InboxFrame = CTkFrame(self.PanedWindow, border_width=0)

        # A listbox for showing the inbox messages
        self.inbox_list = CTkListbox(InboxFrame, corner_radius=0,
                                     fg_color="transparent",
                                     border_width=0, width=290,
                                     command=self._open_mails,
                                    ) 
        self.inbox_list.pack(expand=True, fill=BOTH)

        # Bind right-click on 
        self.inbox_list.bind(
            "<Button-1>",
            lambda event: self._click_on_free_space()
            )
        
        LableFrame = CTkFrame(InboxFrame, border_width=0,
                               fg_color="transparent")
        LableFrame.pack(fill=BOTH)

        CTkLabel(LableFrame, text="Inbox",
                 font=self.FONT(27, "bold")
                ).grid(row=0, column=0, sticky=W, padx=6)
        
        self.inbox_counter_lbl = CTkLabel(LableFrame, text="0 Messages",
                                            font=self.FONT(15, "normal"),
                                           )
        self.inbox_counter_lbl.grid(row=0, column=1, sticky=W)

        # Initialize HTMLFrame (displays homepage and mails content)
        self.HtmlFrame = HtmlFrame(self.PanedWindow, vertical_scrollbar="auto",
                                   horizontal_scrollbar="auto",
                                   messages_enabled=False
                                  ) 
        # Bind To Open The Links in Browser
        self.HtmlFrame.on_link_click(lambda url: open_in_browser(url))
        # Deactivating the mousewheel
        self.HtmlFrame.unbind_all("<MouseWheel>")

        # Add InboxFrame and HTML-frame into PanedWindow
        self.PanedWindow.add(InboxFrame)
        self.PanedWindow.add(self.HtmlFrame)

        try:
            # Try to load homepage from HTML file
            with open("HomePage.html", "r") as html:
                self.__homepage = html.read()

        except FileNotFoundError:
            # If HTML file is not found, set a default 404 error message
            self.__homepage = """
            <html>
                <body style="background-color: #001f3f;">
                    <h1 style="color: #FFFFFF;">404 HomePage Not Found ;(</h1>
                </body>
            </html>
            """

        # Load homepage for first time
        self._load_homepage()

        # Initialize background tasks
        background_tasks = [
            Agent(self.update_connection_status),
            Agent(self.update_inbox)
        ]

        # Initialize the Core class with the list of background tasks
        self.Core = Core(list_of_agents=background_tasks)
        # Run the background tasks
        self.Core.run()
        # one time task
        self.Core.add_task(Agent(self.generate_email)) 
    
    def _set_window_geometry(self) -> None:
        """
        Sets the geometry (size and resolution) of the window based on the screen's
        width and height, with a fixed window size at 77% of the screen width and 75%
        of the screen height. The window is also set to be non-resizable.
        """

        # Screen dimensions (width and height)
        SCREEN_WIDTH = self.winfo_screenwidth()
        SCREEN_HEIGHT = self.winfo_screenheight()

        # Calculate the window's width and height
        MASTER_WIDTH = int(SCREEN_WIDTH * 0.85)
        MASTER_HEIGHT = int(SCREEN_HEIGHT * 0.85)

        # Calculate the position to center the window
        X = (SCREEN_WIDTH - MASTER_WIDTH) // 2
        Y = (SCREEN_HEIGHT - MASTER_HEIGHT) // 2

        # Set the window size position and make it non-resizable
        self.geometry(f"{MASTER_WIDTH}x{MASTER_HEIGHT}+{X}+{Y}")

        # Remove useless variables
        del SCREEN_WIDTH, SCREEN_HEIGHT, MASTER_WIDTH, MASTER_HEIGHT, X, Y
    
    def _raise_window(self) -> None:
        """
        Brings the window to the front and ensures it has focus.
        And loads the new message content in the HtmlFrame.
        """
        # Bring the window to the front of other windows
        self.lift()
        
        # Force focus on the window to ensure it's the active window
        self.focus_force()
        
        # loads the new message content in the HtmlFrame.
        self.inbox_list.activate(END)

    def _notification_popup(self, on_click: callable, *args) -> None:
        """
        Displays a notification with a custom icon and triggers a callback when clicked.

        Args:
            on_click (callable): Function to call when the notification is clicked.
            *args (str): The text fields to be shown in the notification.
        """

        # Create a WindowsToaster instance for displaying notifications
        toaster = WindowsToaster("TempMail")
        # Create a Toast instance for the notification
        notification = Toast()
        # Set icon notification
        notification.AddImage(ToastDisplayImage.fromPath(Icons.tempmail_png))
        # Define the callback function to be called when the notification is clicked
        notification.on_activated = lambda event: on_click()
        # Set content of the notification
        notification.text_fields = args
        # Show the notification
        toaster.show_toast(notification)

        del toaster, notification

    def _switch_theme(self) -> None:
        """
        Switch theme between Light and Dark mode. 
        - If the current theme is Light, it switches to Dark mode,
            changes the theme button icon to a sun icon, 
            and updates the background color of the PanedWindow.
        - If the current theme is Dark, it switches to Light mode,
            changes the theme button icon to a moon icon, 
            and updates the background color of the PanedWindow.
        """
        match get_appearance_mode():

            case "Light":
                # Switch to Dark mode
                set_appearance_mode("Dark")
                # Update switch-theme button icon to represent Light mode (sun icon)
                self.switch_theme_button.configure(image=Icons.sun)
                # Update background color of the PanedWindow to Dark mode color
                self.PanedWindow.configure(background="#242424")
            
            case "Dark":
                # Switch to Light mode
                set_appearance_mode("Light")
                # Update switch-theme button icon to represent Dark mode (moon icon)
                self.switch_theme_button.configure(image=Icons.moon)
                # Update background color of the PanedWindow to Light mode color
                self.PanedWindow.configure(background="#ffffff")

    def _copy_in_clipboard(self) -> None:
        """
        Copies the current email address to the clipboard.
        Triggered when the user clicks the copy button.
        """
        self.clipboard_clear()
        self.clipboard_append(self.email_entry.get()) 
            
    def _load_homepage(self) -> None:
        """
        Loads homepage HTML content into the HtmlFrame if it is not already loaded.
        This prevents redundant reloads and ensures the default page is displayed.
        """
        if not self.__is_on_homepage:
            self.HtmlFrame.load_html(self.__homepage)
            self.__is_on_homepage = True

    def _click_on_free_space(self) -> None:
        """
        Handles the event when the user clicks on free space in the application.

        - Loads the homepage content into the HtmlFrame.
        - Attempts to deactivate the currently selected item in the inbox list.
        If no item is selected, it silently handles the TypeError exception.
        """
        # Load the homepage content into the HtmlFrame
        self._load_homepage()

        try:
            # Attempt to deactivate the currently selected item in the inbox list
            self.inbox_list.deactivate(self.inbox_list.curselection())
        except TypeError:
            # Silently handle the exception if no item is selected
            ...
    
    def _reset_to_default(self) -> None:
        """
        Resets the application to its default state.

        - Loads the homepage content into the HtmlFrame.
        - Clears all messages from the inbox list in the UI.
        - Resets the inbox message counter to "0 Messages".
        - Clears the internal inbox dictionary that stores email messages.
        """
        # Load the homepage content into the HtmlFrame
        self._load_homepage()

        # Clear the internal inbox dictionary
        self.__inbox.clear()

        # Clear the inbox list in the UI
        self.inbox_list.delete(0, END)
        
        # Reset the inbox message counter in the UI
        self.inbox_counter_lbl.configure(text=f"0 Messages")

    def _is_online(self) -> bool:
        """
        Check internet connectivity by attempting to connect to multiple reliable websites.

        This method attempts to make HTTP requests to a predefined list of high-availability websites.
        If any of the websites responds with a 200 OK status code, the device is considered online.

        Returns:
            bool: 
                - True if any of the test URLs is reachable (device is online)
                - False if all test URLs failed to respond (device may be offline)
        """
        urls = (
            "https://www.cloudflare.com",
            "https://www.google.com",
            "https://github.com",
        )
        
        for url in urls:
            try:
                response = get(url, timeout=5)
                if response.status_code == 200:
                    return True
            except:
                continue  # If this URL fails, try the next one
        
        # If we've tried all URLs and none succeeded
        return False

    def update_connection_status(self) -> None:
        """
        Periodically checks the internet connection and updates the connection-status icon.
        """
        while self.__is_tasks_running:
            if self._is_online():
                # If online, update the connection-status icon to online icon
                self.connection_status_ico.configure(image=Icons.online)
                self.__connection_status = True

                if not (self.__tempmail or self.__is_generating_email):
                    self.Core.add_task(Agent(self.generate_email))

            else:
                # If offline, update the connection-status icon to offline icon
                self.connection_status_ico.configure(image=Icons.offline)
                self.__connection_status = False

            # Update connection status every 3 second
            sleep(3)

    def generate_email(self) -> None:
        """
        Generates a new temporary email address and updates the UI.
        Displays notifications when the email is ready or if there is an issue.
        """

        # if device was online
        if self.__connection_status:

            self.__is_generating_email = True

            self.email_entry.configure(state=NORMAL)
            self.email_entry.delete(0, END)
            self.email_entry.insert(END, "Generating email...")
            self.email_entry.configure(state=DISABLED)

            while self.__is_tasks_running:
                try:
                    # Attempt to generate a temporary email address
                    self.__tempmail = TempMail()
                    # Insert the generated email address into the entry field
                    self.email_entry.configure(state=NORMAL)
                    self.email_entry.delete(0, END)
                    self.email_entry.insert(END, self.__tempmail.email)

                    # Display a notification to inform the user
                    self._notification_popup(self._copy_in_clipboard,
                                            "Your email is ready!",
                                            self.__tempmail.email,
                                            "Tap to copy"
                                           )
                    
                    self._reset_to_default()
                    self.__is_generating_email = False

                    break

                except:
                    # if email generatig wasn't Successful
                    self.__tempmail = None
                    
                    if not self.__connection_status:
                        self.__is_generating_email = False

                        self.email_entry.configure(state=NORMAL)
                        self.email_entry.delete(0, END)
                        self.email_entry.insert(END, "Offline! Can't generate email.")
                        self.email_entry.configure(state=DISABLED)

                        break       
                    
                    # Wait 3 seconds before retrying
                    sleep(3)

        else:
            # if device wasn't online
            self.__tempmail = None
            self.__is_generating_email = False

            self.email_entry.configure(state=NORMAL)
            self.email_entry.delete(0, END)
            self.email_entry.insert(END, "Offline! Can't generate email.")

        self.email_entry.configure(state=DISABLED)

    def _regenerate_email(self) -> None:
        """
        Regenerates the temporary email address by adding it into the tasks-list for Core
        Called when user click on the regenerate button.
        """
        if not self.__is_generating_email:
            self.Core.add_task(Agent(self.generate_email))
   
    def update_inbox(self) -> None:
        """
        Periodically updates the inbox with new messages and displays them in the UI.

        - Checks if the device is online and a temporary email address has been created.
        - Retrieves all received messages from the temporary email service.
        - Prevents duplicate messages by checking if the message header already exists in the inbox dictionary.
        - Adds new messages to the internal inbox dictionary and displays them in the inbox list in the UI.
        - Updates the inbox message counter in the UI to reflect the total number of messages.
        - Displays a notification when a new message arrives, allowing the user to bring the program window to the front and view the message.

        This method runs continuously in a loop and updates the inbox every 3 seconds.
        """
        while self.__is_tasks_running:
            # Check if the device is online and a temporary email address has been created
            if self.__connection_status and self.__tempmail:

                # Retrieve all received messages
                mails = self.__tempmail.get_messages()

                for mail in mails:
                    # Create a unique header for the message
                    header = f"{mail.subject}\n{mail.from_addr} <{mail.sent_time}>"

                    # Prevent duplicate messages by checking if the header already exists
                    if header not in self.__inbox:

                        # Add the new message to the internal inbox dictionary
                        self.__inbox.update({header: mail.html})

                        # Insert the message header into the inbox list in the UI
                        self.inbox_list.insert(END, header)

                        # Update the inbox message counter in the UI
                        self.inbox_counter_lbl.configure(text=f"{len(self.__inbox)} Messages")

                        # Display a notification for the new message
                        self._notification_popup(
                            self._raise_window,
                            "New Message",
                            mail.from_addr,
                            mail.subject
                        )

            # Wait for 3 seconds before checking for new messages again
            sleep(3)

    def _open_mails(self, header: str) -> None:
        """
        Displays the selected email message in the HTML frame.
        Called when user click on a message in inbox list.

        Args:
            header (str): The header of the selected email message.
        """
        mail_html = self.__inbox[header]
        self.HtmlFrame.load_html(mail_html)
        self.__is_on_homepage = False
    
    def _on_closing(self):

        popup = CTkToplevel(self)
        popup.title("TempMail")

        SCREEN_WIDTH = self.winfo_screenwidth()
        SCREEN_HEIGHT = self.winfo_screenheight()
        
        # Calculate centered position with scaling
        X = int(((SCREEN_WIDTH / 2) - (280 / 2)) * self._get_window_scaling())  # Horizontally centered
        Y = int(((SCREEN_HEIGHT / 2) - (130 / 1.5)) * self._get_window_scaling())  # Vertically adjusted upward

        popup.geometry(f"280x130+{X}+{Y}")
        popup.resizable(False, False)
        popup.update_idletasks()  # Ensure the geometry is updated

        # Set the popup icon
        popup.after(200, lambda: popup.iconbitmap(Icons.tempmail_ico))

        # Add a label with the confirmation message
        CTkLabel(
            popup,
            text="Quit TempMail?",
            font=self.FONT(16, "bold"),
            anchor="center"
        ).pack(pady=20)

        # Define the Quit button action
        def quit_program():
            self.__is_tasks_running = False  # Stop background tasks
            
            for var in list(globals().keys()):
                if var not in ["__name__", "__file__", "__doc__", "__builtins__"]:
                    del globals()[var]
        
            for var in list(locals().keys()):
                if var != "delete_locals":
                    del locals()[var]

            popup.destroy()  # Close the popup
            self.destroy()  # Close the main application

            from sys import exit as _exit
            _exit(0)

        # Add Quit and Cancel buttons
        button_frame = CTkFrame(popup, fg_color="transparent")
        button_frame.pack(pady=10, fill="x", expand=True)

        CTkButton(
            button_frame,
            text="Quit",
            command=quit_program,
            width=100
        ).pack(side="left", padx=20)

        CTkButton(
            button_frame,
            text="Cancel",
            command=popup.destroy,  # Close the popup
            fg_color="gray",
            hover_color="#666666",
            width=100
        ).pack(side="right", padx=20)

        # Prevent interaction with the main window while the popup is open
        popup.transient(self)
        popup.grab_set()
        self.wait_window(popup)


if __name__ == '__main__':
    app = TempMailGUI()
    app.mainloop()    
