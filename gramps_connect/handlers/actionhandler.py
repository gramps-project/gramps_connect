from .handlers import BaseHandler
from ..forms.actionform import ActionForm

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
            self.render("action.html",
                        **self.get_template_dict(tview=_("action detail"),
                                                 page=page,
                                                 search=search,
                                                 form=ActionForm(self.database, _, id=handle),
                                             )
                    )
        else:
            self.render("page_view.html",
                        **self.get_template_dict(tview=_("action view"),
                                                 page=page,
                                                 search=search,
                                                 form=ActionForm(self.database, _),
                                             )
                    )

