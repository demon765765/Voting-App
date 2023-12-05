import tkinter as tk
from tkinter import messagebox
import csv
import json

class VoterApp(tk.Tk):
    """The main voter interface"""
    
    def __init__(self, voter_user):
        """Initialize the VoterApp.

        :param voter_user: An object representing the voter user.
        """
        super().__init__()
        self.voter_user = voter_user
        self.title(f"Voter {self.voter_user.login_id}")

        width = 900
        height = 600

        # center position
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

        # listbox frame
        frame = tk.Frame(self)
        frame.pack(expand=True, padx=20, pady=20)
        self.candidates_listboxes = {}
        categories = ["President", "Vice-President", "Secretary", "Treasurer"]
        for category in categories:
            label = tk.Label(frame, text=f"{category} Candidates:")
            label.grid(row=categories.index(category), column=0, sticky="w", pady=(0, 10))
            listbox = tk.Listbox(frame, selectmode=tk.SINGLE, exportselection=False, width=40, height=5)
            listbox.grid(row=categories.index(category), column=1, padx=(10, 0), pady=(0, 10), sticky="w")
            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
            scrollbar.grid(row=categories.index(category), column=2, sticky="ns", pady=(0, 10))
            listbox.config(yscrollcommand=scrollbar.set)
            self.candidates_listboxes[category] = listbox
        self.load_candidates()

        # vote
        self.vote_button = tk.Button(self, text="Vote", command=self.submit_vote)
        self.vote_button.pack(pady=(0, 10))

        # Status Label
        self.status_label = tk.Label(self, text="", fg="green")
        self.status_label.pack()

        # bind and clear
        for listbox in self.candidates_listboxes.values():
            listbox.bind("<FocusIn>", lambda event, category=category: self.clear_status(event, category))

        # bind and update vote button
        for listbox in self.candidates_listboxes.values():
            listbox.bind("<<ListboxSelect>>", self.on_category_select)

    def load_candidates(self):
        """Load candidates from the CSV file to the listboxes."""
        for listbox in self.candidates_listboxes.values():
            listbox.delete(0, tk.END)
        try:
            with open('candidates.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row['Name']
                    position = row['Position']
                    if position in self.candidates_listboxes:
                         self.candidates_listboxes[position].insert(tk.END, name)
        except FileNotFoundError:
            pass
                   
    def on_category_select(self, event):
        """Event handler when category is selected in listbox.

        :param event: The event object.
        """
        self.clear_status(event, "")

    def submit_vote(self):
        """Submit the vote based on the selected candidates."""
        if self.has_voted():
            self.display_status("Voter has already voted.", "red")
        else:
            selected_candidates = {}

            for category, listbox in self.candidates_listboxes.items():
                selected_index = listbox.curselection()
                if selected_index:
                    selected_candidates[category] = listbox.get(selected_index[0])
                else:
                    self.display_status(f"Please select 1 candidate from each category.", "red")
                    return

            message = "Vote submitted successfully!\nSelected Candidates:\n"
            message += "\n".join(f"{category}: {candidate}" for category, candidate in selected_candidates.items())
            self.display_status(message, "green")
            self.save_vote(selected_candidates)
            self.mark_as_voted()

    def has_voted(self):
        """Check if the voter has already voted.

        :return: True if the voter has voted, False otherwise.
        """
        try:
            with open(f'voter_{self.voter_user.login_id}.txt', 'r') as file:
                return file.read() == 'voted'
        except FileNotFoundError:
            return False

    def mark_as_voted(self):
        """Mark voter as voted by creating a TXT file."""
        with open(f'voter_{self.voter_user.login_id}.txt', 'w') as file:
            file.write('voted')

    def save_vote(self, selected_candidates):
        """Save selected candidate votes to the JSON file.

        :param selected_candidates: A dictionary containing selected candidates for each position.
        """
        try:
            if not self.has_headers('votes.json'):
                headers = {"President": [], "Vice-President": [], "Secretary": [], "Treasurer": []}
                with open('votes.json', 'w') as header_file:
                    json.dump(headers, header_file)
            with open('votes.json', 'r') as file:
                votes_data = json.load(file)
            for position, candidate in selected_candidates.items():
                votes_data[position].append(candidate)
            with open('votes.json', 'w') as file:
                json.dump(votes_data, file)
        except Exception as e:
            print(f"Error saving vote: {e}")
            
    def has_headers(self, file_path):
        """Check if CSV file has headers.

        :param file_path: The path to the CSV file.
        :return: True if the file has headers, False otherwise.
        """
        try:
            with open(file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                headers = next(reader, None)
                return headers is not None
        except FileNotFoundError:
            return False

    def display_status(self, message, color):
        """Display a status message in the GUI.

        :param message: The message to display.
        :param color: The color of the message (e.g., "red" or "green").
        """
        self.status_label.config(text=message, fg=color)

    def clear_status(self, event, category):
        """Clear the status label in the GUI.

        :param event: The event object.
        :param category: The category (not used in this method).
        """
        self.status_label.config(text="")
        
if __name__ == "__main__":
    voter_name = "App"
    voter_app = VoterApp(voter_name)
    voter_app.mainloop()
