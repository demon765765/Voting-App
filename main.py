import tkinter as tk
from tkinter import messagebox
from admin_app import AdminApp
from voter_app import VoterApp
import csv

class User:
    """Represents a user in the login system."""
   
    def __init__(self, login_id, role):
        """Initializes a User.

        :param login_id: The user's login ID.
        :type login_id: str

        :param role: Role of the user either admin or voter.
        :type role: str
        """
        self.login_id = login_id
        self.role = role

class Admin(User):
    """Represents an admin user."""

    def __init__(self, login_id):
        """Initializes an admin.

        :param login_id: The admin's login ID.
        :type login_id: str
        """
        super().__init__(login_id, "administrator")

class Voter(User):
    """Represents a voter user."""
    
    def __init__(self, login_id):
        """Initializes a Voter.

        :param login_id: The voter's login ID.
        :type login_id: str
        """
        super().__init__(login_id, "voter")

class VoterLoginScreen:
    """UI for the voter login screen."""
    
    def __init__(self, master):
        """Initializes the VoterLoginScreen.

        :param master: The main voter login window.
        :type master: tk.Tk
        """
        self.master = master
        self.master.title("Voter Login")

        width = 300
        height = 200

        # center position
        x = (master.winfo_screenwidth() - width) // 2
        y = (master.winfo_screenheight() - height) // 2

        self.master.geometry(f"{width}x{height}+{x}+{y}")

        # widgets
        self.label_name = tk.Label(master, text="Name:")
        self.label_name.pack()

        self.entry_name = tk.Entry(master)
        self.entry_name.pack()

        self.label_voter_id = tk.Label(master, text="Voter ID:")
        self.label_voter_id.pack()

        self.entry_voter_id = tk.Entry(master)
        self.entry_voter_id.pack()

        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack()
        
        self.master.bind('<Return>', lambda event=None: self.login())

    def login(self):
        """Handles the login process for voters."""
        name = self.entry_name.get()
        voter_id = self.entry_voter_id.get()
        if self.verify_voter(name, voter_id):
            voter_user = Voter(name)
            self.master.destroy()
            voter_app = VoterApp(voter_user)
            voter_app.mainloop()
        else:
            messagebox.showerror("Error", "Invalid Name or Voter ID")

    def verify_voter(self, name, voter_id):
        """Verifies the voter credentials.

        :param name: The voter's name.
        :type name: str

        :param voter_id: The voter's ID.
        :type voter_id: str

        :return: True if the credentials are valid, False if not.
        :rtype: bool
        """
        with open("voters.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["Name"] == name and row["VoterID"] == voter_id:
                    return True
        return False

    def run(self):
        """Runs the VoterLoginScreen."""
        self.master.mainloop()
        
class AdminLoginScreen:
    """UI for the admin login screen."""
    
    def __init__(self, master):
        """Initializes the AdminLoginScreen.

        :param master: The main admin login window.
        :type master: tk.Tk
        """
        self.master = master
        self.master.title("Admin Login")

        width = 300
        height = 200

        # center position
        x = (master.winfo_screenwidth() - width) // 2
        y = (master.winfo_screenheight() - height) // 2

        self.master.geometry(f"{width}x{height}+{x}+{y}")

        # widgets
        self.label_name = tk.Label(master, text="Admin Name:")
        self.label_name.pack()

        self.entry_name = tk.Entry(master)
        self.entry_name.pack()

        self.label_admin_name = tk.Label(master, text="Admin Password:")
        self.label_admin_name.pack()

        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.pack()

        self.login_admin_button = tk.Button(master, text="Login", command=self.login_admin)
        self.login_admin_button.pack()
        
        self.master.bind('<Return>', lambda event=None: self.login_admin())
        
        """ Admin Login Credentials."""
        admin_credentials = {"admin": "adminpass"}  # admin login
        
    def login_admin(self):
        """Handles the login process for admin."""
        username = self.entry_name.get()
        password = self.entry_password.get()
        if username == "admin" and password == "adminpass":
            admin_user = Admin(username)
            self.master.destroy()
            admin_app = AdminApp(admin_user)
            admin_app.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid admin credentials")

    def run(self):
        """Runs the AdminLoginScreen."""
        self.master.mainloop()

class LoginScreen:
    """UI for the main login screen."""
    
    def __init__(self, master):
        """Initializes the LoginScreen.

        :param master: The main login window.
        :type master: tk.Tk
        """
        self.master = master
        self.admin_login = None
        self.master.title("Login")

        width = 300
        height = 200

        # center position
        x = (master.winfo_screenwidth() - width) // 2
        y = (master.winfo_screenheight() - height) // 2

        self.master.geometry(f"{width}x{height}+{x}+{y}")

        self.voter_button = tk.Button(master, text="Voter Login", command=self.open_voter_login)
        self.voter_button.pack(side=tk.LEFT, padx=30)

        self.admin_button = tk.Button(master, text="Admin Login", command=self.open_admin_login)
        self.admin_button.pack(side=tk.RIGHT, padx=30)

        # admin login
        self.admin_credentials = {"admin": "adminpass"}

        self.entry_username = tk.Entry(master)
        self.entry_password = tk.Entry(master, show="*")

    def open_voter_login(self):
        """Opens the voter login screen."""
        self.master.withdraw()
        voter_login_screen = VoterLoginScreen(tk.Toplevel(self.master))
        voter_login_screen.run()

    def open_admin_login(self):
        """Opens the admin login screen."""
        self.master.withdraw()
        admin_login_screen = AdminLoginScreen(tk.Toplevel(self.master))
        admin_login_screen.run()

if __name__ == "__main__":
    root = tk.Tk()
    login_screen = LoginScreen(root)
    root.mainloop()
