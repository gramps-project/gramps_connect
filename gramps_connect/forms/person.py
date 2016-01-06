from gramps.gen.lib.person import Person
from gramps.gen.display.name import NameDisplay

nd = NameDisplay().display

from .form import Form

class PersonForm(Form):
    """
    """
    _class = Person
    fields = [
        "primary_name.type",
        "primary_name.title",
        "primary_name.nick",
        "primary_name.call",
        "primary_name.first_name",
        "primary_name.suffix",
        "primary_name.surname_list.0.prefix",
        "primary_name.surname_list.0.surname",
        "primary_name.surname_list.0.origintype",
        "gender",
        "gramps_id",
        "tag_list",
        "private",
    ]

    def describe(self):
        return nd(self.instance)

    def probably_alive(self):
        return True

