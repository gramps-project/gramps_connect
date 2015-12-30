
from gramps.gen.lib.person import Person
from gramps.gen.display.name import NameDisplay

nd = NameDisplay().display

from .form import Form

class PersonForm(Form):
    """
    """
    _class = Person

    def describe(self):
        return nd(self.instance)

    def probably_alive(self):
        return True

