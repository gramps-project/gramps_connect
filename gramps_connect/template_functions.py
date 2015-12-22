from gramps.gen.display.name import NameDisplay

nd = NameDisplay().display

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

def render(name, value, action, javascript=None):
    return value
