from gramps.gen.lib.family import Family

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

    search_terms = [
        "father", "mother", "id",
    ]

    search_ops = {
        "father_handle.primary_name.surname_list.surname": "NI",
        "father_handle.primary_name.surname_list.surname": "NI",
        }

    default_search_fields = ["father_handle.primary_name.surname_list.0.surname"]

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

    def describe(self):
        return str(self.instance)

