from gramps.gen.lib.person import Person
from gramps.gen.display.name import NameDisplay

nd = NameDisplay().display

from .forms import Form

class PersonForm(Form):
    """
    """
    _class = Person
    view = "person"
    tview = "People"

    # Fields for editor:
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

    # URL for page view rows:
    link = "/person/%(handle)s"

    # Search fields to use if not specified:
    default_search_fields = [
        "primary_name.surname_list.0.surname",
        "primary_name.first_name",
        # FIXME: add alternate names
    ]

    # Search fields, list is OR
    search_terms = {
        "surname": "surname", 
        "given": "given", 
        "id": "gramps_id", 
        "gender": "gender", 
        "birth": "birth", 
        "death": "death",
    }

    # Fields for page view; width sum = 95%:
    select_fields = [
        ("primary_name.surname_list.0.surname", 25),
        ("primary_name.first_name", 20),
        ("gramps_id", 10),
        ("gender", 10),
        ("birth_ref_index", 15),
        ("death_ref_index", 15),
    ]

    # Other fields needed to select:
    env_fields = [
        "handle",
        "event_ref_list",
    ]

    # Does the interator support a sort_handles flag?
    sort = True

    def set_post_process_functions(self):
        self.post_process_functions = {
            "gender": self.render_gender,
            "birth_ref_index": self.event_index,
            "death_ref_index": self.event_index,
            #"tag_list": self.get_tag_from_handle:name
        }

    def event_index(self, index, env):
        if 0 <= index < len(env["event_ref_list"]):
            event_ref = env["event_ref_list"][index]
            if event_ref.ref:
                event = self.database.get_event_from_handle(event_ref.ref)
                if event:
                    return event.date
        return ""

    def render_gender(self, gender_code, env):
        return ["Female", "Male", "Unknown"][gender_code]

    def describe(self):
        return nd(self.instance)

    def probably_alive(self):
        return True
