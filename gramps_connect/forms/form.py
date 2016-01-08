import logging
import math

from ..template_functions import make_button

class Form(object):
    """
    """
    _class = None
    edit_fields = []
    column_headings = []
    select_fields = []
    env_fields = []
    post_process_functions = {}
    link = None
    filter = None
    page_size = 25
    sort = False

    def __init__(self, database, _, instance=None, table=None):
        # scheme is a map from FIELD to Python Type, list[Gramps objects], or Handle
        if table:
            self._class = database._tables[table]["class_func"]
        self.table = table
        self.filter = None
        self.database = database
        self.schema = self._class.get_schema()
        self.instance = instance
        self._ = _
        self.log = logging.getLogger(".Form")
        self.set_post_process_functions()

    def set_post_process_functions(self):
        pass

    def get_search_terms(self):
        return ""

    def get_column_count(self):
        return len(self.select_fields) + 1

    def make_query(self, **kwargs):
        kwargs.update({"search": self.search})
        query = ""
        for kw in kwargs:
            if kwargs[kw]:
                if query == "":
                    query += "?"
                else:
                    query += "&"
                query += "%s=%s" % (kw, kwargs[kw])
        return query

    def get_page_controls(self, page):
        ## FIXME: records should be number total of matching
        records = self.database._tables[self.table]["count_func"]()
        matching = len(self.rows)
        total_pages = math.ceil(records / self.page_size)
        return ("<p>" +
                make_button("<<", self.make_query(page=1)) +
                " | " +
                make_button("<", self.make_query(page=max(page - 1, 1))) +
                (" | <b>Page</b> %s of %s | " % (page, total_pages)) +
                make_button(">", self.make_query(page=min(page + 1, total_pages))) +
                " | " +
                make_button(">>", self.make_query(page=total_pages)) +
                (" | <b>Showing</b>: %s/%s " % (matching, records)) +
                "</p>")

    def select(self, page=1, search=None):
        ## FIXME: select should check all, and then show subportion
        self.page = page - 1
        self.search = search
        ## FIXME: parse search to filter:
        ## self.filter = {"primary_name.surname_list.0.surname": ("LIKE", "Blank")}
        self.rows = list(self.database.select(self.table,
                                         self.select_fields + self.env_fields,
                                         self.sort, self.page * self.page_size,
                                         limit=self.page_size,
                                         filter=self.filter))
        return ""

    def get_rows(self):
        retval = []
        count = (self.page * self.page_size) + 1
        for row in self.rows:
            retval_row = [count]
            env = {}
            for field_name in self.env_fields:
                data = row[field_name]
                env[field_name] = data
            for field_name in self.select_fields:
                data = row[field_name]
                if field_name in self.post_process_functions:
                    data = self.post_process_functions[field_name](data)
                if self.link:
                    link = self.link % env
                    data = """<a href="%s" class="browsecell">%s</a>""" % (link, data)
                retval_row.append(data)
            retval.append(retval_row)
            count += 1
        return retval

    def get_column_labels(self):
        headings = ["#"]
        for field in self.select_fields:
            headings.append(self._class.get_label(field, self._))
        return headings

    def describe(self):
        raise Exception("not implemented")

    def get_label(self, field):
        return self.instance.get_label(field, self._)

    def render(self, field, user, action, js=None, link=None, **kwargs):
        data = self.instance.get_field(field)
        if isinstance(data, (list, tuple)):
            if action == "view":
                retval = ""
                for item in data:
                    if retval:
                        retval += ", "
                    retval += item
            else:
                ## a list of handles
                retval = """<select multiple="multiple" name="%s" id="id_%s" style="width: 100%%">""" % (field, field)
                count = 1
                for item in data:
                    retval += """<option value="%d" selected="selected">%s</option>""" % (count, item)
                    count += 1
                retval += "</select>"
        else:
            retval = data
            if action in ["edit", "add"]:
                id = js if js else "id_" + field
                dict = {"id": id, "name": field, "value": retval}
                retval = """<input id="%(id)s" type="text" name="%(name)s" value="%(value)s" style="display:table-cell; width:100%%">""" % dict
        return str(retval)

    def get(self, field):
        return self.instance.get_field(field)

    def save(self, handler):
        # go thorough fields and save values
        for field in self.edit_fields:
            try:
                value = handler.get_argument(field)
            except:
                self.log.warning("field '%s' not found in form" % field)
                continue
            self.instance.set_field(field, value)
        transaction = self.database.get_transaction_class()
        commit = self.database._tables[self._class.__name__]["commit_func"]
        with transaction("Gramps Connect", self.database) as trans:
            commit(self.instance, trans)
