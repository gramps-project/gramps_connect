from .handlers import BaseHandler
from ..forms.actionform import ActionForm, Action, Table

import tornado.web

from gramps.gen.utils.grampslocale import GrampsLocale, _

class ActionHandler(BaseHandler):
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
            table = Table()
            action = table.get_item_by_handle(handle)
            self.render("action.html",
                        **self.get_template_dict(tview=_("action detail"),
                                                 page=page,
                                                 search=search,
                                                 form=ActionForm(self.database, _, instance=action),
                                             )
                    )
        else:
            self.render("page_view.html",
                        **self.get_template_dict(tview=_("action view"),
                                                 page=page,
                                                 search=search,
                                                 form=ActionForm(self.database, _, table="Action"),
                                             )
                    )

    @tornado.web.authenticated
    def post(self, handle):
        # Run report here
        self.redirect("/action")
