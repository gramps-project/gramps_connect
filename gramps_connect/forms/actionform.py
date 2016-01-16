import time

from .forms import Form, Column, Row

from gramps.cli.plug import BasePluginManager

class Action():
    def __init__(self, name, ptype, handle):
        self.name = name
        self.ptype = ptype
        self.handle = handle

    @classmethod
    def get_schema(cls):
        return {
            "handle": str,
            "name": str,
            "ptype": str,
        }

    @classmethod
    def get_field_alias(cls, field):
        return field

    def get_field(self, field, db=None, ignore_errors=False):
        if field == "handle":
            return self.handle
        elif field == "name":
            return self.name
        elif field == "ptype":
            return self.ptype

class Table(object):
    _class = Action
    count = 0
    _cache = None
    _cache_map = {}

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.get_items() # build cache
    
    def get_function_dict(self):
        return {
            "class_func": self.get_class(), 
            "count_func": self.get_count, 
            "commit_func": self.commit,
            "handle_func": self.get_item_by_handle,
            "handles_func": self.get_items,
        }

    def get_class(self):
        return self._class

    def get_item_by_handle(self, handle):
        print(handle)
        return Action(*self._cache_map[handle])

    def get_items(self, sort_handles=False):
        if self._cache is None:
            self._cache_map = {}
            pmgr = BasePluginManager.get_instance()
            cl_list = []
            for reg_action in ["get_reg_reports", 
                               "get_reg_exporters", 
                               "get_reg_importers"]:
                cl_list += getattr(pmgr, reg_action)()
            self._cache = sorted([(pdata.name, self.plugtype(pdata.ptype), pdata.id) 
                                  for pdata in cl_list])
            self.count = len(self._cache)
            for items in self._cache:
                self._cache_map[items[2]] = items
        return [x[2] for x in self._cache]

    def plugtype(self, ptype):
        if ptype == 0:
            return "Report"
        elif ptype == 2:
            return "Tool"
        elif ptype == 3:
            return "Import"
        elif ptype == 4:
            return "Export"
        else:
            raise Exception("Not supported")

    def get_count(self):
        return self.count

    def commit(self):
        pass

class ActionForm(Form):
    """
    """
    _class = Action
    view = "action"
    tview = "Action"
    table = "Action"

    # URL for page view rows:
    link = "/action/%(handle)s"

    # Search fields to use if not specified:
    default_search_fields = [
        "name",
        "ptype"
    ]

    # Search fields, list is OR
    search_terms = {
        "name": "name",
        "action": "ptype",
    }

    # Fields for page view:
    select_fields = [
        ("name", 50),
        ("ptype", 45),
    ]

    # Other fields needed to select:
    env_fields = [
        "handle"
    ]

    # Does the interator support a sort_handles flag?
    sort = True

    def __init__(self, database, _, instance=None, table=None):
        database._tables["Action"] = Table().get_function_dict()
        super().__init__(database, _, instance=instance, table=table)

    def set_post_process_functions(self):
        self.post_process_functions = {
        }

    def get_column_labels(self):
        return Row([
            Column("#", self.count_width), 
            Column("Name", 50),
            Column("Action", 50),
        ])

    def get_table_count(self):
        return self.database._tables[self.table]["count_func"]()

    def get_field_value(self, pid, key):
        options_dict, options_help = self.get_plugin_options(pid)
        return options_dict[key]

    def get_fields(self, pid):
        options_dict, options_help = self.get_plugin_options(pid)
        return options_help

    def get_plugin_options(self, pid):
        """
        Get the default options and help for this plugin.
        """
        pmgr = BasePluginManager.get_instance()
        pdata = pmgr.get_plugin(pid)
        if hasattr(pdata, "optionclass") and pdata.optionclass:
            mod = pmgr.load_plugin(pdata)
            optionclass = getattr(mod, pdata.optionclass)
            optioninstance = optionclass("Name", self.database)
            optioninstance.load_previous_values()
            return optioninstance.options_dict, optioninstance.options_help
        else:
            return {}, {}

    def describe(self):
        action = self.database._tables["Action"]["handle_func"](self.instance.handle)
        return action.name

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
