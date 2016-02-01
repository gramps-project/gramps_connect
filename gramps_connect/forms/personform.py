#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (c) 2015 Gramps Development Team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

# Gramps imports:
from gramps.gen.lib.person import Person
from gramps.gen.display.name import NameDisplay

# Gramps Connect imports:
from .forms import Form

# Globals:
nd = NameDisplay().display

class PersonForm(Form):
    """
    A form for listing, viewing, and editing a Person object.
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

    order_by = [("surname", "ASC"), ("given", "ASC")]

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

    def set_post_process_functions(self):
        """
        Set the post_process_functions dictionary.
        """
        self.post_process_functions = {
            "gender": self.render_gender,
            "birth_ref_index": self.event_index,
            "death_ref_index": self.event_index,
            #"tag_list": self.get_tag_from_handle:name
        }

    def event_index(self, index, env):
        """
        Used for revent_ref_index lookups.
        """
        if 0 <= index < len(env["event_ref_list"]):
            event_ref = env["event_ref_list"][index]
            if event_ref.ref:
                event = self.database.get_event_from_handle(event_ref.ref)
                if event:
                    return event.date
        return ""

    def render_gender(self, gender_code, env):
        """
        Text for gender codes.
        """
        return [self._("Female"), self._("Male"), self._("Unknown")][gender_code]

    def describe(self):
        """
        Textual description of this instance.
        """
        return nd(self.instance)

    def probably_alive(self):
        """
        Placeholder for a probably_alive value.
        """
        return True
