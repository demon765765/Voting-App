import tkinter as tk
from tkinter import ttk
import csv
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from add_voter_page import AddVoterPage
from election import Election
import json

class Candidate:
    """Represents a candidate in the election."""
    
    def __init__(self, name, position):
        """Initializes a Candidate.

        :param name: Candidate name.
        :type name: str

        :param position: Candidate position.
        :type position: str
        """
        self.name = name
        self.position = position

class AdminApp(tk.Tk):
    """Admin user interface."""
    
    def __init__(self, admin_user):
        """Initializes the AdminApp.

        :param admin_user: The admin user for the app.
        :type admin_user: Admin
        """
        super().__init__()

        self.admin_user = admin_user
        self.title(f"Admin {self.admin_user.login_id}")
        self.root = tk.Tk()
        self.root.title("Admin Page")

        width = 755
        height = 600

        # center position
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.election = Election()

        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0, padx=10, pady=10)

        # candidates elements
        self.positions = ["President", "Vice-President", "Secretary", "Treasurer"]
        self.candidates_listboxes = {}

        for i, position in enumerate(self.positions):
            label = tk.Label(frame, text=f"{position} List:")
            label.grid(row=0, column=i)

            listbox_width = 30
            listbox_height = 10
            candidates_listbox = tk.Listbox(frame, selectmode=tk.SINGLE, width=listbox_width, height=listbox_height)
            candidates_listbox.grid(row=1, column=i)
            self.candidates_listboxes[position] = candidates_listbox

        self.candidates_dict = {}
        self.load_candidates() 

        # candidate
        self.label_name = tk.Label(frame, text="Candidate Name:")
        self.label_name.grid(row=2, column=0, pady=(10, 0), sticky='e', columnspan=2) 
        self.entry_name = tk.Entry(frame)
        self.entry_name.grid(row=2, column=2, pady=(10, 0), sticky='w', columnspan=2)  

        # position
        self.label_position = tk.Label(frame, text="Candidate Position:")
        self.label_position.grid(row=3, column=0, pady=(10, 0), sticky='e', columnspan=2) 

        position_options = ["", "President", "Vice-President", "Secretary", "Treasurer"]
        self.selected_position = tk.StringVar(frame)
        self.selected_position.set(position_options[0])
        self.position_dropdown = tk.OptionMenu(frame, self.selected_position, *position_options)
        self.position_dropdown.grid(row=3, column=2, pady=(10, 0), sticky='w', columnspan=2)  

        # add candidate
        self.add_candidate_button = tk.Button(frame, text="Add Candidate", command=self.add_candidate)
        self.add_candidate_button.grid(row=4, column=0, columnspan=4, pady=(20, 0))

        # delete candidate
        self.delete_candidate_button = tk.Button(frame, text="Delete Candidate", command=self.delete_candidate)
        self.delete_candidate_button.grid(row=5, column=0, columnspan=4, pady=(10, 0))

        # display messages
        self.message_label = tk.Label(self.root, text="", fg="green")
        self.message_label.grid(row=7, column=0, columnspan=4)

        # save list
        self.save_list_button = tk.Button(frame, text="Save Candidate List", command=self.save_candidates)
        self.save_list_button.grid(row=7, column=0, columnspan=4, pady=(10, 0))

        # add voter
        self.add_voter_page_button = tk.Button(frame, text="Voter Page", command=self.open_add_voter_page)
        self.add_voter_page_button.grid(row=8, column=0, columnspan=4, pady=(10, 0))
        
        self.show_results_button = tk.Button(self, text="Show Voting Results", command=self.show_results)
        self.show_results_button.pack(pady=(0, 10))

        # bind and clear
        self.entry_name.bind("<FocusIn>", lambda event: self.clear_message_and_selection())
        self.position_dropdown.bind("<Button-1>", lambda event: self.clear_message_and_selection())
               
    def show_results(self):
        """Displays the voting results in a separate window."""
        votes = self.load_votes()
        results_window = ResultsWindow(self, votes)
        self.wait_window(results_window)

    def open_add_voter_page(self):
        """Opens the AddVoterPage for adding new voters."""
        self.root.withdraw()
        add_voter_page = AddVoterPage(self) 
        add_voter_page.mainloop()
        
    def add_candidate(self):
        """Adds a candidate to the list."""
        name = self.entry_name.get()
        position = self.selected_position.get()
        if name and position:
            candidate = Candidate(name, position)
            if position not in self.candidates_dict:
                self.candidates_dict[position] = []
            self.candidates_dict[position].append(candidate)
            self.refresh_candidates_listboxes()
            self.display_message(f"Candidate {name} added successfully for {position}!", "green")
            self.entry_name.delete(0, tk.END)
            self.selected_position.set("")
        else:
            self.display_message("Name and Position are required fields.", "red")


    def delete_candidate(self):
        """Deletes the selected candidate from the list."""
        selected_listbox = None
        for position, listbox in self.candidates_listboxes.items():
            if listbox == self.root.focus_get():
                selected_listbox = listbox
                break
        if selected_listbox:
            selected_index = selected_listbox.curselection()
            if selected_index:
                candidate_name = selected_listbox.get(selected_index)
                position = [pos for pos, lb in self.candidates_listboxes.items() if lb == selected_listbox][0]
                if candidate_name in [candidate.name for candidate in self.candidates_dict.get(position, [])]:
                    self.candidates_dict[position] = [candidate for candidate in self.candidates_dict.get(position, []) if candidate.name != candidate_name]
                    selected_listbox.delete(selected_index)
                    self.display_message(f"{candidate_name} deleted successfully!", "green")
                else:
                    self.display_message(f"{candidate_name} not found for deletion.", "red")
            else:
                self.display_message("No candidate selected for deletion.", "red")
        else:
            self.display_message("No candidate list selected for deletion.", "red")

    def load_candidates(self):
        """Loads candidate data from CSV file."""
        try:
            with open('candidates.csv', 'r') as file:
                reader = csv.reader(file)
                candidates_data = {}
                next(reader, None)
                for row in reader:
                    if len(row) >= 2:
                        name, position = row[:2]
                        if position not in candidates_data:
                            candidates_data[position] = []
                        candidate = Candidate(name, position)
                        candidates_data[position].append(candidate)
                self.candidates_dict = candidates_data
                self.refresh_candidates_listboxes()
        except FileNotFoundError:
            pass

    def refresh_candidates_listboxes(self):
        """Refreshes the listboxes with the current data."""
        for listbox in self.candidates_listboxes.values():
            listbox.delete(0, tk.END)
        for position, candidates in self.candidates_dict.items():
            for candidate in candidates:
                self.candidates_listboxes[position].insert(tk.END, candidate.name)

    def save_candidates(self):
        """Saves the candidate data to CSV file."""
        with open('candidates.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Position"])
            for candidates in self.candidates_dict.values():
                for candidate in candidates:
                    writer.writerow([candidate.name, candidate.position])
        self.display_message("Candidate list saved successfully!", "green")

    def clear_message_and_selection(self):
        """Clears the displayed message and selection in listboxes."""
        self.message_label.config(text="")
        for listbox in self.candidates_listboxes.values():
            listbox.selection_clear(0, tk.END)

    def display_message(self, message, color):
        """Displays a message in red or green.

        :param message: Message to be displayed.
        :type message: str

        :param color: Color of the message text.
        :type color: str
        """
        self.message_label.config(text=message, fg=color)
        
    def load_votes(self):
        """Loads voting data from a JSON file.

        :return: A dictionary containing voting data.
        :rtype: dict
        """
        try:
            with open('votes.json', 'r') as json_file:
                votes_data = json.load(json_file)
            return votes_data
        except FileNotFoundError:
            return None
    
class ResultsWindow(tk.Toplevel):
    """Window to display voting results."""

    def __init__(self, admin_app, votes):
        """Initializes the ResultsWindow.

        :param admin_app: The main AdminApp window.
        :type admin_app: AdminApp

        :param votes: The voting data to be displayed.
        :type votes: dict
        """
        super().__init__(admin_app)
        self.title("Voting Results")
        self.admin_app = admin_app
        self.votes = votes
        self.create_bar_graphs()

    def create_bar_graphs(self):
        """Creates bar graphs for each position from the voting data."""
        votes = self.admin_app.load_votes()
        if votes:
            for position, candidates in votes.items():
                candidate_counts = Counter(candidates)
                self.create_single_bar_graph(position, candidate_counts)
        else:
            print("No voting data available. Unable to create bar graphs.")
        
    def create_single_bar_graph(self, position, candidate_counts):
        """Creates a single bar graph for each position.

        :param position: The position for which the graph is created.
        :type position: str

        :param candidate_counts: A Counter object containing candidate counts.
        :type candidate_counts: Counter
        """
        fig, ax = plt.subplots(figsize=(4.5, 2.5))
        candidates = list(candidate_counts.keys())
        counts = list(candidate_counts.values())
        ax.bar(candidates, counts)
        ax.set_xlabel("Candidates")
        ax.set_ylabel("Number of Votes")
        ax.set_title(f"Voting Results for {position}")
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def create_widgets(self):
        """Creates the widgets for the ResultsWindow."""
        self.label = tk.Label(self, text="Voting Results")
        self.label.pack(pady=15)
        votes = self.load_votes()
        self.create_bar_graphs(votes)
        self.close_button = tk.Button(self, text="Close", command=self.master.destroy)
        self.close_button.pack(pady=10)
        
if __name__ == "__main__":
    admin_user = Admin("Admin")
    admin_app = AdminApp(admin_user)
    admin_app.mainloop()

