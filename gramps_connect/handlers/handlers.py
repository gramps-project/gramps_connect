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
import logging

from gramps.gen.utils.grampslocale import GrampsLocale, _
from gramps.gen.utils.id import create_id
from gramps.gen.lib import Person, Surname, Family
from gramps.gen.const import VERSION

from ..forms import PersonForm, FamilyForm

template_functions = {}
exec("from gramps_connect.template_functions import *",
     globals(), template_functions)

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(".Handler")
        self.database = None
        self.sitename = None
        self.opts = None
        for name in ["database", "sitename", "opts"]:
            if name in kwargs:
                setattr(self, name, kwargs[name])
                del kwargs[name]
        super().__init__(*args, **kwargs)
        self._ = _

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def set_language(self, language):
        if language == GrampsLocale.DEFAULT_TRANSLATION_STR:
            language = None
        locale = GrampsLocale(lang=language)
        self._ = locale.translation.gettext

    def get_template_dict(self, **kwargs):
        dict = {
            "database": self.database,
            "menu": [],
            "action": "view",
            "user": self.current_user,
            "sitename": self.sitename,
            "opts": self.opts,
            "css_theme": "Web_Mainz.css",
            "gramps_version": VERSION,
            "messages": [],
            "_": self._,
            "next": self.get_argument("next", None),
        }
        dict.update(template_functions)
        dict.update(kwargs)
        return dict

    def get_form(self, table):
        """
        Return the proper form, give a table name.
        """
        if table == "person":
            form = PersonForm
        elif table == "family":
            form = FamilyForm
        else:
            raise Exception("invalid form")
        return form

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html', **self.get_template_dict())

class LoginHandler(BaseHandler):
    def get(self):
        self.set_language("fr_FR.UTF-8")
        self.render('login.html',
                    **self.get_template_dict())
    def post(self):
        getusername = self.get_argument("username")
        getpassword = self.get_argument("password")
        # TODO : Check data from DB
        if "demo" == getusername and "demo" == getpassword:
            self.set_secure_cookie("user", self.get_argument("username"))
            self.redirect(self.get_argument("next",
                                            self.reverse_url("main")))
        else:
            wrong = self.get_secure_cookie("wrong")
            if not wrong:
                wrong = 0
            self.set_secure_cookie("wrong", str(int(wrong)+1))
            self.write('Something Wrong With Your Data <a href="/login">Back</a> '+str(wrong))

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next",
                                        self.reverse_url("main")))

class PersonHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, path=""):
        """
        HANDLE
        HANDLE/edit|delete
        /add
        b2cfa6ca1e174b1f63d/remove/eventref/1
        """
        page = int(self.get_argument("page", 1))
        search = self.get_argument("search", "")
        if "/" in path:
            handle, action= path.split("/", 1)
        else:
            handle, action = path, "view"
        if handle:
            if handle == "add":
                person = Person()
                person.primary_name.surname_list.append(Surname())
                action = "edit"
            else:
                person = self.database.get_person_from_handle(handle)
            if person:
                person.probably_alive = True
                self.render("person.html",
                            **self.get_template_dict(tview=_("person detail"),
                                                     action=action,
                                                     form=PersonForm(self.database, _, instance=person),
                                                     logform=None))
                return
            else:
                self.clear()
                self.set_status(404)
                self.finish("<html><body>No such person</body></html>")
                return
        self.render("page_view.html",
                    **self.get_template_dict(tview=_("person view"),
                                             page=page,
                                             search=search,
                                             form=PersonForm(self.database, _, table="Person"),
                                         )
                )

    @tornado.web.authenticated
    def post(self, path):
        if "/" in path:
            handle, action = path.split("/")
        else:
            handle, action = path, "view"
        if handle == "add":
            person = Person()
            person.primary_name.surname_list.append(Surname())
            person.handle = handle = create_id()
        else:
            person = self.database.get_person_from_handle(handle)
        form = PersonForm(self.database, _, instance=person)
        form.save(handler=self)
        self.redirect("/person/%(handle)s" % {"handle": handle})

class FamilyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, path=""):
        """
        HANDLE
        HANDLE/edit|delete
        /add
        b2cfa6ca1e174b1f63d/remove/eventref/1
        """
        page = int(self.get_argument("page", 1))
        search = self.get_argument("search", "")
        if "/" in path:
            handle, action= path.split("/", 1)
        else:
            handle, action = path, "view"
        if handle:
            if handle == "add":
                family = Family()
                action = "edit"
            else:
                family = self.database.get_family_from_handle(handle)
            if family:
                self.render("family.html",
                            **self.get_template_dict(tview=_("family detail"),
                                                     action=action,
                                                     form=FamilyForm(self.database, _, instance=family),
                                                     logform=None))
                return
            else:
                self.clear()
                self.set_status(404)
                self.finish("<html><body>No such family</body></html>")
                return
        self.render("page_view.html",
                    **self.get_template_dict(tview=_("family view"),
                                             page=page,
                                             search=search,
                                             form=FamilyForm(self.database, _, table="Family"),
                                         )
                )

    @tornado.web.authenticated
    def post(self, path):
        if "/" in path:
            handle, action = path.split("/")
        else:
            handle, action = path, "view"
        if handle == "add":
            family = Family()
            family.handle = handle = create_id()
        else:
            family = self.database.get_family_from_handle(handle)
        form = FamilyForm(self.database, _, instance=family)
        form.save(handler=self)
        self.redirect("/family/%(handle)s" % {"handle": handle})
