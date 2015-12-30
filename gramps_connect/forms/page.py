
from .form import Form

class PageForm(Form):
    """
    """
    def __init__(self, database, table, fields, _, 
                 page_size=20, order_by=None, filter=None):
        super().__init__(database, None, _)
        self.table = table
        self.fields = fields
        self.page_size = page_size
        self.order_by = order_by
        self.filter = filter

    def get_page(self, start=0):
        rows = self.database.select(self.table, self.fields, 
                                    self.order_by, self.filter, start, 
                                    limit=self.page_size)
        
