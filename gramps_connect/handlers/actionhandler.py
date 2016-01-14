from .handlers import BaseHandler
from ..forms.action import ActionForm

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
        self.render("page_view.html",
                    **self.get_template_dict(tview=_("person view"),
                                             page=page,
                                             search=search,
                                             form=ActionForm(self.database, _),
                                         )
                )

def process_report_run(request, handle):
    """
    Run a report or export.
    """
    # can also use URL with %0A as newline and "=" is "=":
    # http://localhost:8000/report/ex_gpkg/run?options=off=gpkg%0Ax=10
    from gramps.webapp.reports import import_file, export_file, download
    from gramps.cli.plug import run_report
    import traceback
    if request.user.is_authenticated():
        profile = request.user.profile
        report = Report.objects.get(handle=handle)
        args = {"off": "html"} # basic defaults
        # override from given defaults in table:
        if report.options:
            for pair in str(report.options).split("\\n"):
                if "=" in pair:
                    key, value = [x.strip() for x in pair.split("=", 1)]
                    if key and value:
                        args[key] = value
        # override from options on webpage:
        if "options" in request.GET:
            options = str(request.GET.get("options"))
            if options:
                for pair in options.split("\n"): # from webpage
                    if "=" in pair:
                        key, value = [x.strip() for x in pair.split("=", 1)]
                        if key and value:
                            args[key] = value
        #############################################################################
        if report.report_type == "report":
            filename = "/tmp/%s-%s-%s.%s" % (str(profile.user.username), str(handle), timestamp(), args["off"])
            run_report(db, handle, of=filename, **args)
            mimetype = 'application/%s' % args["off"]
        elif report.report_type == "export":
            filename = "/tmp/%s-%s-%s.%s" % (str(profile.user.username), str(handle), timestamp(), args["off"])
            export_file(db, filename, gramps.cli.user.User()) # callback
            mimetype = 'text/plain'
        elif report.report_type == "import":
            filename = download(args["i"], "/tmp/%s-%s-%s.%s" % (str(profile.user.username),
                                                                 str(handle),
                                                                 timestamp(),
                                                                 args["iff"]))
            if filename is not None:
                if True: # run in background, with error handling
                    import threading
                    def background():
                        try:
                            import_file(db, filename, gramps.cli.user.User()) # callback
                        except:
                            make_message(request, "import_file failed: " + traceback.format_exc())
                    threading.Thread(target=background).start()
                    make_message(request, "Your data is now being imported...")
                    return redirect("/report/")
                else:
                    success = import_file(db, filename, gramps.cli.user.User()) # callback
                    if not success:
                        make_message(request, "Failed to load imported.")
                    return redirect("/report/")
            else:
                make_message(request, "No filename was provided or found.")
                return redirect("/report/")
        else:
            make_message(request, "Invalid report type '%s'" % report.report_type)
            return redirect("/report/")
        # need to wait for the file to exist:
        start = time.time()
        while not os.path.exists(filename):
            # but let's not wait forever:
            if time.time() - start > 10: # after 10 seconds, give up!
                context = RequestContext(request)
                make_message(request, "Failed: '%s' is not found" % filename)
                return redirect("/report/")
            time.sleep(1)
        # FIXME: the following should go into a queue for later presentation
        # like a jobs-result queue
        if filename.endswith(".html"):
            # just give it, perhaps in a new tab
            from django.http import HttpResponse
            response = HttpResponse(content_type="text/html")
            for line in open(filename, mode="rb"):
                response.write(line)
            return response
        else:
            return send_file(request, filename, mimetype)
    # If failure, just fail for now:
    context = RequestContext(request)
    context["message"] = "You need to be logged in to run reports."
    return render_to_response("main_page.html", context)
