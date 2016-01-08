from gramps.gen.lib.person import Person
from gramps.gen.display.name import NameDisplay

nd = NameDisplay().display

from .form import Form

class PersonForm(Form):
    """
    """
    _class = Person
    view = "person"
    tview = "People"

    edit_fields = [
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

    link = "/person/%(handle)s"

    select_fields = [
        "gramps_id",
        "primary_name.surname_list.0.surname",
        "primary_name.first_name",
        "gramps_id",
        "gender",
        "birth_ref_index",
        "death_ref_index",
    ]

    env_fields = [
        "handle",
    ]

    sort = True

    def set_post_process_functions(self):
        self.post_process_functions = {
            "gender": self.render_gender,
            "birth_ref_index": self.event_index,
            "death_ref_index": self.event_index,
            #"tag_list": self.get_tag_from_handle:name
        }

    def event_index(self, index):
        return self._("Birth")

    def render_gender(self, gender_code):
        return self._("Male")

    def describe(self):
        return nd(self.instance)

    def probably_alive(self):
        return True
