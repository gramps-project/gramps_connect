import logging

class Form(object):
    """
    """
    def __init__(self, database, instance, _):
        # scheme is a map from FIELD to Python Type, list[Gramps objects], or Handle
        self.database = database
        self.schema = self._class.get_schema()
        self.instance = instance
        self._ = _
        self.columns = []
        self.link = None
        self.log = logging.getLogger(".Form")

    def set_row_link(self, link):
        self.link = link

    def set_column_headings(self, *columns):
        self.columns = columns

    def get_field_name(self, field_post):
        if ":" in field_post:
            return field_post.split(":", 1)[0]
        else:
            return field_post

    def get_post_process(self, field_post):
        if ":" in field_post:
            return field_post.split(":", 1)[1]
        else:
            return None

    def select(self, fields, page_size=20, sort=False, filter=None):
        # Fields are ordered:
        self.fields = list(map(self.get_field_name, fields))
        self.post_process = {k: v for k,v in zip(map(self.get_field_name, fields), 
                                                 map(self.get_post_process, fields))}
        self.page_size = page_size
        self.sort = sort
        self.filter = filter

    def process(self, data, function, env):
        retval = ""
        if function == "gender":
            retval = self._("Male")
        elif function == "event_index":
            ## FIXME: how to get this type of data in a SQL join?
            retval = self._("Birth")
        else:
            raise Exception()
        if self.link:
            link = self.link % env
            retval = """<a href="%s">%s</a>""" % (link, retval)
        return retval

    def get_page(self, start=0):
        rows = self.database.select(self.table, self.fields, 
                                    self.sort, start, 
                                    limit=self.page_size,
                                    filter=self.filter)
        retval = []
        for row in rows:
            retval_row = []
            for field_name in self.fields:
                data = row[field_name]
                if self.post_process[field_name]:
                    retval_row.append(self.process(data, self.post_process[field_name], row))
                else:
                    retval_row.append(data)
            retval.append(retval_row)
        return retval

    def get_columns(self):
        headings = []
        for field in self.columns:
            headings.append(self._class.get_label(field, self._))
        return headings

    def describe(self):
        raise Exception("not implemented")

    def get_label(self, field):
        method = None
        if ":" in field:
            field, function, attr = field.split(":", 2)
            method = getattr(self.database, function)
        label = self.instance.get_label(field, self._)
        if method:
            obj = method(label)
            label = getattr(obj, attr)
        return label

    def render(self, field, user, action, js=None, link=None, size=None,
               **kwargs):
        method = None
        if ":" in field:
            field, function, attr = field.split(":", 2)
            method = getattr(self.database, function)
        data = self.instance.get_field(field)
        if isinstance(data, (list, tuple)):
            if action == "view":
                retval = ""
                for item in data:
                    if method:
                        obj = method(item)
                        item = getattr(obj, attr)
                    if retval:
                        retval += ", "
                    retval += item
            else:
                ## a list of handles
                retval = """<select multiple="multiple" name="%s" id="id_%s" style="width: 100%%">""" % (field, field)
                count = 1
                for item in data:
                    if method:
                        obj = method(item)
                        item = getattr(obj, attr)
                    retval += """<option value="%d" selected="selected">%s</option>""" % (count, item)
                    count += 1
                retval += "</select>"
        else:
            retval = data
            if method:
                obj = method(retval)
                retval = getattr(obj, attr)
            if action in ["edit", "add"]:
                id = js if js else "id_" + field
                dict = {"id": id, "name": field, "size": "15", "value": retval}
                retval = """<input id="%(id)s" type="text" name="%(name)s" size="%(size)s" value="%(value)s">""" % dict
        return str(retval)

    def get(self, field):
        return self.instance.get_field(field)

    def save(self, handler):
        # go thorough fields and save values
        for field in self.fields:
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
