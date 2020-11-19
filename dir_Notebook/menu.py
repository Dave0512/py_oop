import sys
from notebook import Notebook, Note

class Menu:
    """
    Display a menu and respond to choices when run.
    """
    def __init__(self):
        """
        Initiate the Menu class with attributes notebook and choices
        """
        self.notebook = Notebook()
        self.choices = {
             "1": self.show_notes
            ,"2": self.search_notes
            ,"3": self.add_note
            ,"4": self.modify_note
            ,"5": self.quit
        }
        
    def display_menu(self):
        """
        Show Menu Options to the User
        """
        print("""
        Notebook Menu 
        
        1. Show all notes
        2. Search Notes
        3. Add note
        4. Modify Note
        5. Quit
        """)

    def run(self):
        """
        Display ther menu and respond to choices
        """
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice) 
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def show_notes(self,notes=Note):
        """
        Show all notes
        """
        if not notes:
            notes = self.notebook.notes
        for note in notes:
            print("{0}: {1}\n{2}".format(
                note.id, note.tags, note.memo
            ))

    def search_notes(self):
        """
        Show filtered note
        """
        filter = input("Search for: ")
        notes = self.notebook.search(filter)
        self.show_notes(notes)
