from string import ascii_lowercase, ascii_uppercase, digits
from datetime import datetime, timezone
from random import choice, choices
from requests import get, post
from bs4 import BeautifulSoup

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.1.0; Nexus 6P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A705FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.62",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/17.0 Chrome/108.0.5304.141 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/22.11.4.110 Yowser/2.5 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36 OPR/62.0.2254.130116",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/18.19041"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/55.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; rv:41.0) Gecko/20100101 Firefox/41.0",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; Trident/7.0; AS; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36 Edge/16.16299",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; Trident/7.0; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Linux; Android 8.1.0; Pixel 2 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36 Edge/18.18363",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; Trident/7.0; AS; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; Trident/7.0; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; Trident/7.0; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; Trident/7.0; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; Trident/7.0; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; Trident/7.0; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; Trident/7.0; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; Trident/7.0; AS; TSTB; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36 Edg/59.0.3071.115",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36 Edg/60.0.3112.113",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36 Edg/60.0.3112.113",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36 Edg/61.0.3163.100",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.1462.54 Safari/537.36 Edg/108.0.1462.54",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0",
    "Mozilla/5.0 (Linux; Android 11; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36 OPR/62.0.2254.130116",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/18.19041",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/17.0 Chrome/108.0.5304.141 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 10; en-US; vivo 1906 Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 UCBrowser/13.4.0.1288 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/22.11.4.110 Yowser/2.5 Safari/537.36"
]

class TempMail:
    """
    Manages temporary email accounts using the mail.tm API.
    """
    def __init__(self) -> None:
        """
        Initializes a new TempMail instance by creating a temporary email account
        and setting its attributes such as id, email, password, and token.
        """
        self.ua = choice(USER_AGENTS)

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
        self.sent_time = self._convert_time(object['updatedAt'])
        self.subject = object['subject']
        self.id = object['id']
        self.token = token

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

    def _edit_html(self, html: str) -> str:
        """
        Cleans an HTML string to make it compatible with tkinterweb.HtmlFrame.
        - Removes unsupported tags or attributes.
        - Replaces <table> with <div> for layout.
        - Removes external resources like tracking pixels or scripts.
        - Simplifies CSS styles.

        Args:
            html_content (str): The input HTML content as a string.

        Returns:
            str: The cleaned HTML content as a string.
        """
        # Parse the HTML content
        soup = BeautifulSoup(html, "html.parser")
        
        # Remove unsupported tags (e.g., <script>, <iframe>, <style> if needed)
        for tag in soup.find_all(["script", "iframe", "noscript"]):
            tag.decompose()  # Remove the tag completely

        # Remove external resources (e.g., tracking pixels)
        for img in soup.find_all("img"):
            if "tracking" in img.get("src", "") or img.get("src", "").startswith("http"):
                img.decompose()  # Remove the tag
            else:
                # Ensure local images are preserved
                img["src"] = img.get("src", "")

        # Replace <table> with <div> for layout
        for table in soup.find_all("table"):
            table.name = "div"
            for tr in table.find_all("tr"):
                tr.name = "div"
            for td in table.find_all("td"):
                td.name = "div"

        # Simplify inline styles
        for tag in soup.find_all(True):  # Find all tags
            if "style" in tag.attrs:
                # Remove unsupported or complex styles
                tag.attrs["style"] = tag.attrs["style"].replace("center top no-repeat", "background: center top;")
                tag.attrs["style"] = tag.attrs["style"].replace("position: absolute;", "")  # Example cleanup

        # Return the cleaned HTML as a string
        return str(soup)
    
    @property
    def html(self):
        """
        Retrieves the HTML content of the email by making an authenticated API request.
        
        Returns:
            str: HTML content of the email.
        """
        resp = get('https://api.mail.tm/messages/' + self.id,
                   headers={'User-Agent': self.ua, 'Authorization': 'Bearer ' + self.token})
        return self._edit_html(''.join(resp.json()['html']))
