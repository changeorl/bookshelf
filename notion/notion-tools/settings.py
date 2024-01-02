from datetime import datetime
import os

class INFO(object):
    token = 'secret_s6zhSzRMCv1s9zf9rwPLbd6SVc5H9656QCGyWgd4s1F'
    endpoint = 'https://api.notion.com/v1'
    # https://api.notion.com/v1/users

    user_id = '5b02b983-2356-4012-b7ff-bea7da21ef08'
    workspace_name = 'Jo\'s Notion'

class TIME(object):
    now = datetime.now().strftime('%H%M%S')
    today = datetime.now().strftime('%Y-%m-%d')


class PATH(object):
    output = os.path.join(os.getcwd(), 'output')
    if not os.path.exists(output):
        os.makedirs(output)
    output_today = os.path.join(output, TIME.today)
    if not os.path.exists(output_today):
        os.makedirs(output_today)

class DATABASE(object):
    inbox = '48de1468a76942dc9c93128fc56babb1'
    daily_paper = '35935e06e5624c338b37966ab09fda10'
    book = '61abd05763c84033a98f577e7e92ad16'
    gitpaper = '08a9b64c5d344a72967cd3bfdf8f8368'
    # https://www.notion.so/08a9b64c5d344a72967cd3bfdf8f8368?v=29fc8c612979471e9af168cf48e2287e&pvs=4
    # https://www.notion.so/48de1468a76942dc9c93128fc56babb1?v=693dff4dfdae4ad382d9c43316aaeac4&pvs=4
    

class TEST(object):
    # res.json()['results']
    database = ""