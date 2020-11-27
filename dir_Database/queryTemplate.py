
class QueryTemplate:
    """
    Class to interact with databases
    """
    
    def __init__(self, *args):
        pass

    def connect(self):
        pass

    def construct_query(self):
        pass

    def do_query(self):
        pass

    def format_results(self):
        pass

    def output_results(self):
        pass

    def process_format(self):
        """
        Sequence control of the functions 
        - The process_format method is the primary method to be called by an outside
          client. 
        - It ensures each step is executed in order, but it does not care if that step is
          implemented in this class or in a subclass.
        """
        self.connect()
        self.construct_query()
        self.do_query()
        self.format_results()
        self.output_results()
        
        
        
        

        

        