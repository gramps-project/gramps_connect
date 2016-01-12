from gramps.gen.lib.family import Family

from .form import Form

class FamilyForm(Form):
    """
    """
    _class = Family
    view = "family"
    tview = "Family"

    # Fields for editor:
    edit_fields = [
    ]

    # URL for page view rows:
    link = "/family/%(handle)s"

    # Fields for page view:
    select_fields = [
        "gramps_id",
        "father_handle",
        "mother_handle",
        "type.string",
    ]

    # Search fields, list is OR:
    search_terms = {
        "father": ["father_surname", "father_given"], 
        "mother": ["mother_surname", "mother_given"], 
        "id": "gramps_id",
    }

    # Search fields to use if not specified:
    default_search_fields = [
        "father_handle.primary_name.surname_list.0.surname",
        "father_handle.primary_name.first_name",
        "mother_handle.primary_name.surname_list.0.surname",
        "mother_handle.primary_name.first_name",
    ]

    # Other fields needed to select:
    env_fields = [
        "handle",
    ]

    # Does the interator support a sort_handles flag?
    sort = False

    def set_post_process_functions(self):
        self.post_process_functions = {
            "father_handle": self.get_person_from_handle,
            "mother_handle": self.get_person_from_handle,
            #"tag_list": self.get_tag_from_handle:name
        }

    def describe(self):
        return str(self.instance)

