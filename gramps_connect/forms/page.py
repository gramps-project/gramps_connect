
from gramps.gen.lib.person import Person

from .form import Form

class PageForm(Form):
    """
    """

    def __init__(self, database, table, _):
        self._class = database._tables[table]["class_func"]
        super().__init__(database, None, _)
        self.table = table
        self.filter = filter

        
