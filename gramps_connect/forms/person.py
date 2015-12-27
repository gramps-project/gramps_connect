
from gramps.gen.lib.person import Person
from gramps.gen.display.name import NameDisplay

nd = NameDisplay().display

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

    def render(self, field, action, user, js=None, link=None, *args, **kwargs):
        method = None
        if ":" in field:
            field, function, attr = field.split(":", 2)
            method = getattr(self.database, function)
        data = self.instance.get_field(field)
        if isinstance(data, (list, tuple)):
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
        return retval

    def get(self, field):
        return self.instance.get_field(field)

class PersonForm(Form):
    """
    """
    _class = Person

    def describe(self):
        return nd(self.instance)

    def probably_alive(self):
        return True

