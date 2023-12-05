import csv

class Election:
    """Class to define the election"""
    
    def __init__(self):
        """Initialize an Election object."""
        
        self.candidates_by_position = {
            "President": [],
            "Vice-President": [],
            "Secretary": [],
            "Treasurer": []
        }

    def add_candidate(self, candidate):
        """Add a candidate to the election.

        :param candidate: A Candidate object to be added to the election.
        """
        position = candidate.position
        self.candidates_by_position[position].append(candidate)

    def vote(self, candidate_index):
        """define candidate vote using index's.

        :param candidate_index: The index of the candidate to vote for.
        """
        if 0 <= candidate_index < len(self.candidates):
            self.candidates[candidate_index].votes += 1
        else:
            print("Invalid candidate index.")

    def remove_candidate(self, candidate_index):
        """Remove a candidate at a specified index.

        :param candidate_index: The index of the candidate to be removed.
        """
        if 0 <= candidate_index < len(self.candidates):
            candidate = self.candidates.pop(candidate_index)
            position = candidate.position
            self.candidates_by_position[position].remove(candidate)
        else:
            print("Invalid candidate index.")

    def remove_candidate_by_name(self, candidate_name):
        """Remove a candidate by their name.

        :param candidate_name: The name of the candidate to be removed.
        :return: True if the candidate was found and removed, False if not.
        """
        for position, candidates in self.candidates_by_position.items():
            for candidate in candidates:
                if candidate.name == candidate_name:
                    self.candidates_by_position[position].remove(candidate)
                    return True
        return False

    def get_candidates_by_position(self):
        """Dictionary of candidates grouped by their positions.

        :return: A dictionary where keys are positions and values are lists of candidates.
        """
        return self.candidates_by_position

    def get_results(self):
        """Election results as a list of strings.

        :return: A list of strings containing the names, votes, and positions of candidates.
        """
        results = []
        for position, candidates in self.candidates_by_position.items():
            for candidate in candidates:
                results.append(f"{candidate.name} - {candidate.votes} votes for {position}")
        return results

    def load_candidates_from_file(self):
        """Load candidates from the CSV file."""
        try:
            with open('candidates.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    position, candidate_name = row
                    candidate = Candidate(candidate_name, position)
                    self.add_candidate(candidate)
        except FileNotFoundError:
            pass

    def save_candidates_to_file(self):
        """Save candidates to the CSV file.
        """
        with open('candidates.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for position, candidates in self.candidates_by_position.items():
                for candidate in candidates:
                    writer.writerow([position, candidate.name])
                    
class Candidate:
    """Candidate for the election"""
    
    def __init__(self, name, position):
        """Initialize a Candidate object.

        :param name: The name of the candidate.
        :param position: The position for which the candidate is running.
        """
        self.name = name
        self.position = position
        self.votes = 0

    def __str__(self):
        """Return name and votes of candidate as a string.

        :return: A formatted string containing the candidate's name and vote count.
        """
        return f"{self.name} - {self.votes}"
