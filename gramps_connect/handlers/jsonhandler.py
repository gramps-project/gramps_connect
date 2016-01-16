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

import tornado.web
import simplejson

from .handlers import BaseHandler

class JsonHandler(BaseHandler):
    """
    Process an Ajax/Json query request.
    """
    @tornado.web.authenticated
    def get(self):
        field = self.get_argument("field", None)
        query = self.get_argument("q", "").strip()
        page = int(self.get_argument("p", "1"))
        size = int(self.get_argument("s", "10"))
        if field in ["mother", "father"]:
            table = "Person"
            fields = ["primary_name.first_name", 
                      "primary_name.surname_list.0.surname", 
                      "gender", 
                      "handle"]
            sort = True
            if "," in query:
                surname, given = [s.strip() for s in query.split(",", 1)]
                filter = ["OR", [("primary_name.surname_list.0.surname", "LIKE", "%s%%" % surname),
                                 ("primary_name.first_name", "LIKE", "%s%%" % given),
                             ]]
            elif query:
                filter = ("primary_name.surname_list.0.surname", "LIKE", "%s%%" % query)
            else:
                filter = None
            # UNKNOWN = 2, MALE = 1, FEMALE = 0
            if field == "mother":
                if filter:
                    filter = ["AND", [filter, ("gender", "IN", [0, 2])]]
                else:
                    filter = ("gender", "=", 0)
            elif field == "father":
                if filter:
                    filter = ["AND", [filter, ("gender", "IN", [1, 2])]]
                else:
                    filter = ("gender", "=", 1)
            return_fields = ['primary_name.surname_list.0.surname',
                             'primary_name.first_name']
            return_delim = ", "
        elif field == "person":
            q, order, terms = build_person_query(request, query)
            matches = Name.objects.filter(q).order_by(*order)
            class_type = gramps.gen.lib.Person
            handle_expr = "match.person.handle"
        elif field == "place":
            q, order, terms = build_place_query(request, query)
            matches = Place.objects.filter(q).order_by(*order)
            class_type = gramps.gen.lib.Place
            handle_expr = "match.handle"
        else:
            raise Exception("""Invalid field: '%s'; Example: /json/?field=mother&q=Smith&p=1&size=10""" % field)
        ## ------------
        self.log.info("json filter: " + str(filter))
        rows = self.database.select(table, fields, sort, (page - 1) * size, 
                                    size, filter=filter)
        response_data = {"results": [], "total": rows.total}
        for row in rows:
            obj = self.database.get_from_name_and_handle(table, 
                                                         row["handle"])
            if obj:
                name = return_delim.join([obj.get_field(f) for f in return_fields])
                response_data["results"].append({"id": obj.handle, 
                                                 "name": name})
        self.set_header('Content-Type', 'application/json')
        self.write(simplejson.dumps(response_data))
