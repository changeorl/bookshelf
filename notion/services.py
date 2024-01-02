from apis import *


def new_fleeto(_content: str,
               _name: str = 'new note',
               _tags: list = ['python api'],
               _icon: str = 'Notion'):
    # db_id
    parent = dict(database_id=Config.db_quick_note)

    # properties: name,tags
    tags = dict(
        multi_select=[dict(name=t) for t in _tags]
    )
    name = dict(
        title=[
            dict(
                text=dict(content=_name)
            )
        ]
    )
    properties = dict(Name=name, Tags=tags)

    # children: [paragraph]
    paragraph = dict(
        object="block",
        type="paragraph",
        paragraph=dict(
            rich_text=[
                dict(
                    type="text",
                    text=dict(content=_content)
                )
            ]
        )
    )
    children = [paragraph]

    # icon
    icon = dict(
        type="external",
        external=dict(url=f"https://cdn.simpleicons.org/{_icon}/white")
    )

    # api sent
    res = page_create(parent=parent, properties=properties, children=children, icon=icon)
    jprint(res.json())

    # error response
    error = """
    {
        "object": "error",
        "status": 400,
        "code": "validation_error",
        "message": "body failed validation. Fix one:\nbody.icon.emoji should be defined, instead was `undefined`.\nbody.icon.type should be `\"external\"` or `undefined`, instead was `\"externaeel\"`.",
        "request_id": "ac26ca48-5fee-4ffe-8cb3-b8cc59e72994"
    }
    """
    # success response
    success = """
    {
        "object": "page",
        "id": "efbc9c79-2499-4d8f-9388-d4713b52d9e8",
        "created_time": "2023-10-31T02:53:00.000Z",
        "last_edited_time": "2023-10-31T02:53:00.000Z",
        "created_by": {
            "object": "user",
            "id": "5b02b983-2356-4012-b7ff-bea7da21ef08"
        },
        "last_edited_by": {
            "object": "user",
            "id": "5b02b983-2356-4012-b7ff-bea7da21ef08"
        },
        "cover": null,
        "icon": {
            "type": "external",
            "external": {
                "url": "https://cdn.simpleicons.org/Notion/white"
            }
        },
        "parent": {
            "type": "database_id",
            "database_id": "5bc1dbd4-8652-44dc-9149-722c9ab999af"
        },
        "archived": false,
        "properties": {
            "Tags": {
                "id": "j%3C%3A%3F",
                "type": "multi_select",
                "multi_select": [
                    {
                        "id": "fa4567ce-b4de-4dd7-8519-87ec4d290e02",
                        "name": "flomo",
                        "color": "blue"
                    },
                    {
                        "id": "22a612dc-40c0-4873-8e41-6b338867b3a7",
                        "name": "whisper",
                        "color": "purple"
                    }
                ]
            },
            "Created time": {
                "id": "y%7C_m",
                "type": "created_time",
                "created_time": "2023-10-31T02:53:00.000Z"
            },
            "Name": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": "1111111",
                            "link": null
                        },
                        "annotations": {
                            "bold": false,
                            "italic": false,
                            "strikethrough": false,
                            "underline": false,
                            "code": false,
                            "color": "default"
                        },
                        "plain_text": "1111111",
                        "href": null
                    }
                ]
            }
        },
        "url": "https://www.notion.so/1111111-efbc9c7924994d8f9388d4713b52d9e8",
        "public_url": null,
        "request_id": "9ad24d79-f380-403a-b49c-d3364bf1bb9b"
    }
    """


def get_tags_db(_db_id: str, print_tags: bool = False):
    res = database_retireve(_db_id)
    title = res.json()["title"][0]["text"]["content"]
    tags = [
        x["name"]
        for x in
        res.json()["properties"]["Tags"]["multi_select"]["options"]
    ]
    if print_tags:
        print(f"`{title}`")
        print(f"{'-' * (len(title) + 4)}")
        for t in tags:
            print(t)
    return tags


def update_tags_db(_db_id: str, _tags: list):
    print("updating tags...")
    # properties: name,tags
    tags = dict(
        multi_select=dict(
            options=[
                dict(name=t) for t in _tags
            ]
        )
    )
    properties = dict(Tags=tags)
    res = database_update(_db_id, properties=properties)
    print(res.json())
