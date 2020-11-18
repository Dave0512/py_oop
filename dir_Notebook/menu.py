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
        
