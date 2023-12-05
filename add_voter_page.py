import tkinter as tk
from tkinter import messagebox
import csv

class AddVoterPage(tk.Toplevel):
    """Represents the Add Voter Page in the admin app."""

    def __init__(self, admin_app):
        """Initializes the AddVoterPage.

        :param admin_app: The parent admin app.
        :type admin_app: AdminApp
        """
        super().__init__()

        self.admin_app = admin_app
        self.title("Add Voter Page")
        
        width = 755
        height = 600

        # center position
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2

        # geometry
        self.geometry(f"{width}x{height}+{x}+{y}")

        # frame for listbox
        frame = tk.Frame(self)
        frame.pack(expand=True)

        # voter names and IDs
        self.voter_listbox = tk.Listbox(frame, selectmode=tk.SINGLE, width=50, height=10)
        self.voter_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=(10, 0))

        # adjust frame
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, y=90)

        # voter name
        self.label_new_name = tk.Label(self, text="Voter Name:")
        self.label_new_name.pack(pady=(10, 0))
        self.entry_new_name = tk.Entry(self)
        self.entry_new_name.pack(pady=(0, 10))

        # new voter ID
        self.label_new_id = tk.Label(self, text="Numeric Voter ID:")
        self.label_new_id.pack(pady=(10, 0))
        self.entry_new_id = tk.Entry(self)
        self.entry_new_id.pack(pady=(0, 10))

        # add voter button
        self.add_voter_button = tk.Button(self, text="Add Voter", command=self.add_voter)
        self.add_voter_button.pack(pady=(0, 10))
        
        # delete voter
        self.delete_voter_button = tk.Button(self, text="Delete Voter", command=self.delete_voter)
        self.delete_voter_button.pack(pady=(0, 10))

        # save voter list
        self.save_list_button = tk.Button(self, text="Save Voter List", command=self.save_voter_list)
        self.save_list_button.pack(pady=(0, 10))

        # status label
        self.status_label = tk.Label(self, text="", fg="green")
        self.status_label.pack()

        # admin page
        self.admin_page_button = tk.Button(self, text="Admin Page", command=self.return_to_admin_page)
        self.admin_page_button.pack(pady=(10, 0))

        # bind and clear
        self.entry_new_name.bind("<FocusIn>", lambda event: self.clear_status())
        self.entry_new_id.bind("<FocusIn>", lambda event: self.clear_status())

        # validate voter ID
        validate_id = self.register(self.validate_voter_id)
        self.entry_new_id.config(validate="key", validatecommand=(validate_id, "%P"))

        # load voters
        self.load_voters()

    def validate_voter_id(self, new_value):
        """Validates the format of the voter ID.

        :param new_value: a new value entered in the voter ID entry.
        :type new_value: str

        :return: True if the new value is a digit or an empty string, False if not.
        :rtype: bool
        """
        return new_value.isdigit() or new_value == ""

    def add_voter(self):
        """Adds a new voter to the list."""
        name = self.entry_new_name.get()
        voter_id = self.entry_new_id.get()

        if name and voter_id:
            if not self.is_duplicate_voter_id(voter_id):
                voter_info = f"{name} - {voter_id}"
                self.voter_listbox.insert(tk.END, voter_info)
                self.entry_new_name.delete(0, tk.END)
                self.entry_new_id.delete(0, tk.END)
                self.display_status(f"Voter {name} added successfully!", "green")
            else:
                self.display_status("Voter ID must be unique.", "red")
        else:
            self.display_status("Name and ID are required fields.", "red")

    def is_duplicate_voter_id(self, voter_id):
        """Checks if a voter ID already exists in the list.

        :param voter_id: The voter ID to check.
        :type voter_id: str

        :return: True if the voter ID is a duplicate, False if not.
        :rtype: bool
        """
        return any(voter_id in item for item in self.voter_listbox.get(0, tk.END))
    
    def delete_voter(self):
        """Deletes the selected voter from the list."""
        selected_index = self.voter_listbox.curselection()
        if selected_index:
            voter_info = self.voter_listbox.get(selected_index)
            voter_id = voter_info.split(" - ")[1]
            if voter_id in [item.split(" - ")[1] for item in self.voter_listbox.get(0, tk.END)]:
                self.voter_listbox.delete(selected_index)
                self.display_status(f"Voter {voter_info} deleted successfully!", "green")
            else:
                self.display_status(f"{voter_info} not found for deletion.", "red")
        else:
            self.display_status("No voter selected for deletion.", "red")

    def save_voter_list(self):
        """Saves the current voter list to a CSV file."""
        try:
            current_voters = [item.split(" - ") for item in self.voter_listbox.get(0, tk.END)]
            with open('voters.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'VoterID'])
                for name, voter_id in current_voters:
                    writer.writerow([name, voter_id])
            self.display_status("Voter list saved successfully!", "green")
        except PermissionError:
            self.display_status("Must close open list file to save!", "red")

    def load_voters(self):
        """Loads the voter list from a CSV file."""
        try:
            with open('voters.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader, None)
                voters_data = []
                for row in reader:
                    if len(row) >= 2:
                        voter_info = f"{row[0]} - {row[1]}"
                        voters_data.append(voter_info)
                for voter_info in voters_data:
                    self.voter_listbox.insert(tk.END, voter_info)
        except FileNotFoundError:
            pass

    def return_to_admin_page(self):
        """Returns to the Admin Page."""
        self.destroy()
        self.admin_app.root.deiconify()

    def display_status(self, message, color):
        """Displays a status message.

        :param message: The message to display.
        :type message: str

        :param color: Message text color red or green.
        :type color: str
        """
        self.status_label.config(text=message, fg=color)

    def clear_status(self):
        """Clears the label."""
        self.status_label.config(text="")

    def run(self):
        """Runs the AddVoterPage."""
        self.mainloop()

if __name__ == "__main__":
    admin_app = AdminApp(None)
    add_voter_page = AddVoterPage(admin_app)
    add_voter_page.run()
