import logging
import math

from ..template_functions import make_button

from gramps.gen.display.name import NameDisplay

nd = NameDisplay().display

class Form(object):
    """
    """
    _class = None
    edit_fields = []
    column_headings = []
    select_fields = []
    env_fields = []
    post_process_functions = {}
    search_terms = {}
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
        total = self.database._tables[self.table]["count_func"]()
        records = self.rows.total
        matching = len(self.rows)
        total_pages = math.ceil(records / self.page_size)
        return ("""<div align="center" style="background-color: lightgray; border: 1px solid black; border-radius:5px; margin: 0px 1px; padding: 1px;">""" +
                make_button("<<", self.make_query(page=1)) +
                " | " +
                make_button("<", self.make_query(page=max(page - 1, 1))) +
                (" | <b>Page</b> %s of %s | " % (page, total_pages)) +
                make_button(">", self.make_query(page=min(page + 1, total_pages))) +
                " | " +
                make_button(">>", self.make_query(page=total_pages)) +
                (" | <b>Showing</b> %s/%s <b>of</b> %s <b>in</b> %.4g seconds" % (matching, records, total, round(self.rows.time, 4))) +
                "</div>")

    def parse(self, search_pair):
        """
        search_pair: field OP value | search_pair OR search_pair
        """
        if " OR " in search_pair: 
            search_pairs = [s.strip() for s in search_pair.split(" OR ")]
            return ["OR", [self.parse(pair) for pair in search_pairs]]
        elif " AND " in search_pair: 
            search_pairs = [s.strip() for s in search_pair.split(" AND ")]
            return ["AND", [self.parse(pair) for pair in search_pairs]]
        elif " LIKE " in search_pair:
            field, term = [s.strip() for s in search_pair.split(" LIKE ", 1)]
            return self.expand_fields(field, "LIKE", term)
        elif "!=" in search_pair:
            field, term = [s.strip() for s in search_pair.split("!=", 1)]
            return self.expand_fields(field, "!=", term)
        elif "=" in search_pair:
            field, term = [s.strip() for s in search_pair.split("=", 1)]
            return self.expand_fields(field, "=", term)
        else: # search all defaults, OR
            or_filter = []
            for field in self.default_search_fields:
                term = search_pair.strip()
                or_filter.append(self.expand_fields(field, "LIKE", term))
            return ["OR", or_filter]

    def expand_fields(self, field, op, term):
        """
        Return (field, op, term) or ["OR", ...]
        """
        # check for named aliases:
        field = self.search_terms.get(field, field)
        term = self.fix_term(term)
        # replace term for common values
        if isinstance(field, (list, tuple)):
            or_filter = []
            for field in field:
                field = self.database._tables[self.table]["class_func"].get_field_alias(field)
                or_filter.append((field, op, term))
            return ["OR", or_filter]
        else:
            field = self.database._tables[self.table]["class_func"].get_field_alias(field)
            return (field, op, term)

    def fix_term(self, term):
        """
        Turn string terms into common values
        """
        term = term.strip()
        if term == "[]":
            term = []
        elif term == "None":
            term = None
        elif term.isdigit():
            term = int(term)
        elif ((term.startswith('"') and term.endswith('"')) or
              (term.startswith("'") and term.endswith("'"))):
            term = term[1:-1]
        return term

    def select(self, page=1, search=None):
        self.page = page - 1
        self.search = search
        self.filter = None
        if search:
            searches = search.split(",") # top-level ANDs
            filter = []
            # get all filter terms:
            for search_pair in searches:
                filter.append(self.parse(search_pair))
            if len(filter) == 1:
                self.filter = filter[0]
            elif len(filter) > 1:
                self.filter = ["AND", filter]
        self.log.info("filter: " + str(self.filter))
        self.rows = self.database.select(self.table,
                                         self.select_fields + self.env_fields,
                                         self.sort, self.page * self.page_size,
                                         limit=self.page_size,
                                         filter=self.filter)
        return ""

    def get_rows(self, page=1):
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
                    data = self.post_process_functions[field_name](data, env)
                if self.link:
                    link = self.link % env
                    data = data if data else "&nbsp;"
                    data = """<a href="%s?page=%s" class="browsecell">%s</a>""" % (link, page, data)
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
        data = self.instance.get_field(field, self.database)
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
        if field in self.post_process_functions:
            retval = self.post_process_functions[field](data, {})
        if link:
            retval = '''<a href="''' +  (link % kwargs) + '''">''' + retval + """</a>"""
        return str(retval)

    def get(self, field):
        return self.instance.get_field(field, self.database)

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

    def get_person_from_handle(self, handle, env):
        if handle:
            person = self.database.get_person_from_handle(handle)
            if person:
                return nd(person)
        return ""

