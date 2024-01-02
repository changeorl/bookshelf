#######################################
#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @author: chenzh05
# @Desc: { notion api request body template }
# @Date: 2023/08/09 16:15
#######################################


def tmpl_page_property(property: dict, **kwargs) -> dict:
    _type = property["type"]

    if _type == "checkbox":
        checked = kwargs["checked"] if "checked" in kwargs else None
        data = {
            # "id": property["id"],
            # "type": "checkbox",
            "checkbox": checked,
        }

    if _type == "date":
        start = kwargs["start"] if "start" in kwargs else None
        end = kwargs["end"] if "end" in kwargs else None
        time_zone = kwargs["time_zone"] if "time_zone" in kwargs else None
        data = {
            # "id": property["id"],
            # "type": "date",
            "date": {"start": start, "end": end, "time_zone": time_zone},
        }

    if _type == "multi_select":
        # options = property["multi_select"]["options"]
        # options = [i["name"] for i in range(len(options))]
        options = kwargs["tags"] if "tags" in kwargs else None
        options = [{"name": i} for i in options]
        data = {
            # "id": property["id"],
            # "type": "multi_select",
            "multi_select": options,
        }

    if _type == "title":
        content = kwargs["title"] if "title" in kwargs else None
        link = kwargs["link"] if "link" in kwargs else None
        data = {
            # "id": "title",
            # "type": "title",
            "title": [{"text": {"content": content}}],
        }

    # temp = {}
    # temp[property["name"]] = data
    return data


def tmpl_rich_text(
    content: str,
    link: bool = None,
    bold: bool = False,
    italic: bool = False,
    strikethrough: bool = False,
    underline: bool = False,
    code: bool = False,
    color: str = "default",
):
    tmpl = {
        "type": "text",
        "text": {"content": content, "link": link},
        "annotations": tmpl_annotation(
            bold, italic, strikethrough, underline, code, color
        ),
        "plain_text": content,
        "href": link,
    }

    return tmpl


def tmpl_annotation(
    bold=False,
    italic=False,
    strikethrough=False,
    underline=False,
    code=False,
    color="default",
):
    tmpl = {
        "bold": bold,
        "italic": italic,
        "strikethrough": strikethrough,
        "underline": underline,
        "code": code,
        "color": color,
    }
    return tmpl
