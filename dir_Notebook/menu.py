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