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

## Python imports
import os
import base64
import uuid

## Tornado imports
import tornado.ioloop
from tornado.web import Application, url, StaticFileHandler
from tornado.options import define, options
import tornado.log

## Gramps imports
import gramps.gen.const # initializes locale
from gramps.gen.dbstate import DbState
from gramps.gen.utils.file import media_path_full

## Gramps Connect imports
from gramps_connect.handlers import *

## Command-line configuration options:
define("hostname", default="localhost", 
       help="Name of host Gramps Connect server is running on", type=str)
define("port", default=8000, 
       help="Run Gramps Connect server on the given port", type=int)
define("database", default=None, 
       help="The Gramps Family Tree to serve", type=str)
define("debug", default=False, 
       help="Tornado debug", type=bool)
define("xsrf", default=True, 
       help="Use xsrf cookie", type=bool)
define("base_dir", default=None, 
       help="Base directory (where static, templates, etc. are)", type=str)
define("home_dir", default=None,
       help="Home directory for media", type=str)

class GrampsConnect(Application):
    """
    Main Gramps Connect webapp class
    """
    def __init__(self, options, settings=None):
        self.options = options
        if settings is None:
            settings = self.default_settings()
        super().__init__([
            url(r"/", MainHandler, name="main"),
            url(r'/login', LoginHandler, name="login"),
            url(r'/logout', LogoutHandler, name="logout"),
            url(r'/person/(.*)', PersonHandler, name="person"),
            url(r'/imageserver/(.*)', ImageHandler, 
                {"HOMEDIR": self.options.home_dir,
                 "PORT": self.options.port,
                 "HOSTNAME": self.options.hostname,
                 "GET_IMAGE_FN": self.get_image_path_from_handle},
                name="imageserver", 
            ),
            url(r"/styles/(.*)", StaticFileHandler, 
                {'path': gramps.gen.const.DATA_DIR}),
            url(r"/images/(.*)", StaticFileHandler, 
                {'path': gramps.gen.const.IMAGE_DIR}),
        ], **settings)
        if self.options.database is None:
            raise Exception("Need to specify Gramps Family Tree name with --database='NAME'")
        else:
            self.database = DbState().open_database(self.options.database)

    def default_settings(self):
        """
        """
        if self.options.base_dir is None:
            self.options.base_dir = os.path.dirname(__file__)
        if self.options.home_dir is None:
            self.options.home_dir = os.path.expanduser("~/.gramps/")
        return {
            "cookie_secret": base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            "login_url":     "/login",
            'template_path': os.path.join(self.options.base_dir, "templates"),
            'static_path':   os.path.join(self.options.base_dir, "static"),
            'debug':         self.options.debug,
            "xsrf_cookies":  self.options.xsrf,
        }

    def get_image_path_from_handle(self, identifier):
        """
        Given an image handle, return the full path/filename.
        """
        media = self.database.get_object_from_handle(identifier)
        if media:
            return media_path_full(self.database, media.get_path())
        return ""

if __name__ == "__main__":
    tornado.options.parse_command_line()
    tornado.log.logging.info("Gramps Connect starting...")
    GrampsConnect(options).listen(options.port)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.log.logging.info("Gramps Connect shutting down...")
