import datetime

# store the next available id for all new notes
last_id = 0

class Note:
    """
    Represent a note in a notebook. Match against a
    string in searches and staore tags for each note.
    """
    def __init__(self,memo,tags=''):
        """
        Initialize a note with memo and optional 
        space-seperated tags.
        Automatically set the note's creation date
        and a unique id.
        """
        self.memo = memo
        self.tags = tags
        self.creation_date = datetime.date.today()
        global last_id
        last_id += 1
        self.id = last_id 

    def match(self,filter):
        """
        Determine if this note matches the filter text. 
        Return true if it matches. False otherwise.
        Search is case sensitive an matches both text and tags
        """
        return filter in self.memo or filter in self.tags