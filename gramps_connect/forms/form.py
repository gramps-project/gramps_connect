

class Form(object):
    """
    """
    def __init__(self, database, instance, _):
        # scheme is a map from FIELD to Python Type, list[Gramps objects], or Handle
        self.database = database
        self.schema = self._class.get_schema()
        self.instance = instance
        self._ = _

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

