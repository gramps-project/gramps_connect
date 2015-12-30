
from gramps.gen.lib.person import Person

from .form import Form

class PageForm(Form):
    """
    """
    _class = Person

    def __init__(self, database, table, fields, _, 
                 page_size=20, sort=False, filter=None):
        super().__init__(database, None, _)
        self.table = table
        self.fields = fields
        self.page_size = page_size
        self.sort = sort
        self.filter = filter

    def get_page(self, start=0):
        rows = self.database.select(self.table, self.fields, 
                                    self.sort, start, 
                                    limit=self.page_size,
                                    filter=self.filter)
        return rows
        
