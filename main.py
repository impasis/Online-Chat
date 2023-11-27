from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from pywebio.session import run_js, run_async

import asyncio


def check(name):
    if name in users:
        return "Your name is taken!"
    elif name == "":
        return "Write a name"


def check_message(message):
    if message == "":
        return "Write a message"


async def main():
    def logout():
        run_js('window.location.reload()')
        users.discard(username)

    put_markdown("## Bobogram 2.0")

    box = output()
    put_scrollable(box, height=300, keep_bottom=True)

    username = await input("Your Name", required=True, validate=check)
    users.add(username)

    run_async(enum_messages(username, box))

    messages.append((username, "join the group!"))
    box.append(put_markdown(f"`NF`: `{username}` join the group!"))
    put_button("Log out", onclick=logout)

    while True:
        message = await input(placeholder="Write a message...", validate=check_message)

        messages.append((username, message))
        box.append(put_markdown(f"`{username}`: {message}"))


async def enum_messages(username, box):
    global messages

    while True:
        i = len(messages)
        await asyncio.sleep(1)

        for el in messages[i:]:
            if el[0] != username:
                box.append(put_markdown(f"`{el[0]}`: {el[1]}"))

        if len(messages) >= 1000:
            messages = messages[500:]


messages = []
users = set()

if __name__ == "__main__":
    start_server(main, debug=True, port=8080, cdn=False)
