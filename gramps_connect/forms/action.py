from .form import Form, Column, Row

class ActionForm(Form):
    """
    """
    _class = None
    view = "action"
    tview = "Action"
    table = "Action"

    # URL for page view rows:
    link = "/action/%(id)s"

    # Search fields to use if not specified:
    default_search_fields = [
        "name"
    ]

    # Search fields, list is OR
    search_terms = {
    }

    # Fields for page view:
    select_fields = [
        ("name", 95),
    ]

    # Other fields needed to select:
    env_fields = [
        "id"
    ]

    # Does the interator support a sort_handles flag?
    sort = True

    def set_post_process_functions(self):
        self.post_process_functions = {
        }

    def describe(self):
        return self.instance

    def get_column_labels(self):
        return Row([Column("#", self.count_width), Column("Action", 95)])

    def select(self, page=1, search=None):
        self.search = search
        self.page = page - 1
        class Actions(list):
            total = 2
            time = 0.0
        actions = Actions()
        actions.append({"name": "Name1", "details": "xxx", "id": "ID1"})
        actions.append({"name": "Name2", "details": "yy", "id": "ID2"})
        self.rows = actions

    def get_get_table_count(self):
        return 2
