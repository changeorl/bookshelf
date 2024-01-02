from services import *
from utils import *


def delete_tags():
    tags_stay = list()
    tags_delete = list()
    tags = get_tags_db(Config.db_fleeto)

    prompt = f"{bold_italic('enter')} for skip, {bold_italic('d')} for deletion, {bold_italic('q')} for quit"
    divider = '-' * len(prompt)

    print(prompt + '\n' + divider)
    for t in tags:
        flag = input(f"keep tag `{t}`? ")
        if flag == 'd':
            tags_delete.append(t)
            continue
        if flag == 'q':
            exit()
        tags_stay.append(t)

    flag_confirm = input(f"{divider}\ndelete tags {tags_delete}, confirm? [d/q]:  ")
    if flag_confirm == 'd':
        update_tags_db(Config.db_fleeto, tags_stay)
        print(divider + '\n' + 'done.')
    else:
        print(divider + '\n' + 'abort.')
        exit()


if __name__ == "__main__":
    delete_tags()
