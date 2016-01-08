from gramps.gen.lib.family import Family
from gramps.gen.display.name import NameDisplay

nd = NameDisplay().display

from .form import Form

class FamilyForm(Form):
    """
    """
    _class = Family
    view = "family"
    tview = "Family"

    edit_fields = [
    ]

    link = "/family/%(handle)s"

    select_fields = [
        "gramps_id",
        "father_handle",
        "mother_handle",
        "type.string",
    ]

    env_fields = [
        "handle",
    ]

    sort = False

    def set_post_process_functions(self):
        self.post_process_functions = {
            "father_handle": self.get_person_from_handle,
            "mother_handle": self.get_person_from_handle,
            #"tag_list": self.get_tag_from_handle:name
        }

    def get_person_from_handle(self, handle, env):
        person = self.database.get_person_from_handle(handle)
        if person:
            return nd(person)
        else:
            return "&nbsp;"

    def describe(self):
        return str(self.instance)

    def get_search_terms(self):
        return "father, mother, id, type, surnames, father.name.first_name, mother.name.first_name, tag, public, private"
