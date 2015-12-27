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

from gramps.plugins.lib.libhtml import Html
from gramps.gen.lib import *
from gramps.gen.lib.struct import Struct

def make_button(text, url, **kwargs):
    if "icon" in kwargs:
        if kwargs["icon"] == "+":
            img_src = "/images/add.png"
        elif kwargs["icon"] == "?":
            img_src = "/images/text-editor.png"
        elif kwargs["icon"] == "-":
            img_src = "/images/gtk-remove.png"
        else:
            raise Exception("invalid icon: %s" % kwargs["icon"])
        return ("""<img height="22" width="22" alt="%(text)s" title="%(text)s" 
     src="%(img_src)s" onmouseover="buttonOver(this)" onmouseout="buttonOut(this)" 
     onclick="document.location.href='%(url)s'" 
     style="background-color: lightgray; border: 1px solid lightgray; border-radius:5px; margin: 0px 1px; padding: 1px;" />
""") % {"url": url % kwargs, 
        "img_src": img_src,
        "text": text}
    else:
        return """<a href="%(url)s">%(text)s</a>""" % {"url": url % kwargs, 
                                                       "text": text}

def nbsp(string):
    """
    """
    if string:
        return string
    else:
        return "&nbsp;"

class Table(object):
    """
    >>> table = Table("css_id")
    >>> table.columns("Col1", "Col2", "Col3")
    >>> table.row("1", "2", "3")
    >>> table.row("4", "5", "6")
    >>> table.get_html()
    """
    def __init__(self, form, id):
        self.id = id # css id
        self.form = form
        self.column_widths = None
        self.columns = []
        self.rows = []

    def set_columns(self, *args):
        self.columns = args

    def append_row(self, *args):
        self.rows.append(list(map(nbsp, args)))

    def get_html(self, style=None, tab_height=200):
        ## Hack of levels of nbsp
        html = Html('div',
                    class_="content",
                    id=self.id,
                    style=("overflow: auto; height:%spx; background-color: #f4f0ec;" % 
                           tab_height) if not style else style)
        table = Html("table", width="95%", cellspacing="0")
        rowhtml = Html("tr")
        for (name, width) in self.columns:
            cell = Html("th", class_="TableHeaderCell", width=("%s%%" % width), colspan="1")
            cell += name
            rowhtml += cell
        table += rowhtml
        for row in self.rows:
            rowhtml = Html("tr")
            cell = Html("td", class_="TableDataCell", width=("%s%%" % self.columns[0][1]), colspan="1")
            div = Html("div", style="background-color: lightgray; padding: 2px 0px 0px 2px")
            div += Html("img", height="22", width="22", 
                        alt="Delete row", title="Delete row", 
                        src="/images/gtk-remove.png", 
                        onmouseover="buttonOver(this)", onmouseout="buttonOut(this)", 
                        onclick="document.location.href='/person/b2cfa6ca1e174b1f63d/remove/eventref/1'", 
                        style="background-color: lightgray; border: 1px solid lightgray; border-radius:5px; margin: 0px 1px; padding: 1px;")
            div += Html("img", height="22", width="22", 
                        alt="Move row up", title="Move row up", 
                        src="/images/up.png", 
                        onmouseover="buttonOver(this)", onmouseout="buttonOut(this)", 
                        onclick="document.location.href='/person/b2cfa6ca1e174b1f63d/up/eventref/1'", 
                        style="background-color: lightgray; border: 1px solid lightgray; border-radius:5px; margin: 0px 1px; padding: 1px;")
            div += Html("img", height="22", width="22", 
                        alt="Move row down", title="Move row down", 
                        src="/images/down.png", 
                        onmouseover="buttonOver(this)", onmouseout="buttonOut(this)", 
                        onclick="document.location.href='/person/b2cfa6ca1e174b1f63d/down/eventref/1'", 
                        style="background-color: lightgray; border: 1px solid lightgray; border-radius:5px; margin: 0px 1px; padding: 1px;")
            cell += div
            rowhtml += cell
            for count in range(1, len(self.columns)):
                cell = Html("td", class_="TableDataCell", width=("%s%%" % self.columns[count][1]), colspan="1")
                cell += row[count - 1]
                rowhtml += cell
            table += rowhtml
        html += table
        return str(html).replace("&amp;nbsp;", "&nbsp;")

def event_table(form, user, action, url, **kwargs):
    retval = ""
    has_data = False
    cssid = "tab-events"
    table = Table(form, "event_table")
    event = Event()
    eventref = EventRef()
    table.set_columns(
        ("",                                      11),
        (event.get_label("description", form._),  19),
        (event.get_label("type", form._),         10),
        (event.get_label("gramps_id", form._),     7),
        (event.get_label("date", form._),         20),
        (event.get_label("place", form._),        23),
        (eventref.get_label("role", form._),      10),
    )
    s = Struct.wrap(form.instance, form.database)
    count = 0
    for event_ref in s.event_ref_list: # eventrefs
        table.append_row(event_ref.ref.description, 
                         event_ref.ref.type.string, 
                         event_ref.ref.gramps_id, 
                         event_ref.ref.date.from_struct(), 
                         event_ref.ref.place.name.value, 
                         event_ref.role.string)
        has_data = True
        count += 1
    retval += """<div style="background-color: lightgray; padding: 2px 0px 0px 2px"/>"""
    retval += """<style>#event_table .TableHead {
	padding: 0.000cm 0.000cm 0.000cm 0.000cm;
	border-top:thin solid #000000; border-bottom:thin solid #000000;
	border-left:none; border-right:none;
}
#event_table .TableHeaderCell {
	padding: 0.100cm 0.100cm 0.100cm 0.100cm;
	border-top:none; border-bottom:thin solid #000000;
	border-left:none; border-right:thin solid #000000;
}
#event_table .TableDataCell {
	padding: 0.100cm 0.100cm 0.100cm 0.100cm;
	border-top:none; border-bottom:thin solid #000000;
	border-left:none; border-right:thin solid #000000;
}
#event_table .Header2 {
	font-size: 10pt;
	text-align: left; text-indent: 0.00cm;
	margin-right: 0.00cm; margin-left: 0.00cm;
	margin-top: 0.00cm; margin-bottom: 0.00cm;
	border-top:none; border-bottom:none;
	border-left:none; border-right:none;
	font-weight:bold; 
}
#event_table .Header3 {
	font-size: 10pt;
	text-align: left; text-indent: 0.00cm;
	margin-right: 0.00cm; margin-left: 0.00cm;
	margin-top: 0.00cm; margin-bottom: 0.00cm;
	border-top:none; border-bottom:none;
	border-left:none; border-right:none;
	font-style:italic; font-weight:bold; 
}
#event_table .Header1 {
	font-size: 12pt;
	text-align: left; text-indent: 0.00cm;
	margin-right: 0.00cm; margin-left: 0.00cm;
	margin-top: 0.00cm; margin-bottom: 0.00cm;
	border-top:none; border-bottom:none;
	border-left:none; border-right:none;
	font-weight:bold; 
}
#event_table .Title {
	font-size: 14pt;
	text-align: left; text-indent: 0.00cm;
	margin-right: 0.00cm; margin-left: 0.00cm;
	margin-top: 0.00cm; margin-bottom: 0.00cm;
	border-top:none; border-bottom:none;
	border-left:none; border-right:none;
	font-weight:bold; 
}
#event_table .Normal {
	font-size: 12pt;
	text-align: left; text-indent: 0.00cm;
	margin-right: 0.00cm; margin-left: 0.00cm;
	margin-top: 0.00cm; margin-bottom: 0.00cm;
	border-top:none; border-bottom:none;
	border-left:none; border-right:none;
	
}</style>"""
    if action == "view":
        retval += make_button(form._("Add New Event"), (url % kwargs), icon="+") # .replace("$act", "add"))
        retval += make_button(form._("Add Existing Event"), (url % kwargs), icon="$") # .replace("$act", "share"))
    else:
        retval += """<div style="height: 26px;"></div>""" # to keep tabs same height
    retval += """</div>"""
    retval += table.get_html()
    #if act == "view":
        #count = 1
        #retval = retval.replace("{{", """<div style="background-color: lightgray; padding: 2px 0px 0px 2px">""")
        #retval = retval.replace("}}", """</div>""")
        #for (djevent, event_ref) in event_list:
        #    item = form.instance.__class__.__name__.lower()
        #    retval = retval.replace("[[x%d]]" % count, make_button("x", "/%s/%s/remove/eventref/%d" % (item, form.instance.handle, count)))
        #    retval = retval.replace("[[^%d]]" % count, make_button("^", "/%s/%s/up/eventref/%d" % (item, form.instance.handle, count)))
        #    retval = retval.replace("[[v%d]]" % count, make_button("v", "/%s/%s/down/eventref/%d" % (item, form.instance.handle, count)))
        #    count += 1
    if has_data:
        retval += """ <SCRIPT LANGUAGE="JavaScript">setHasData("%s", 1)</SCRIPT>\n""" % cssid
    return retval
    
