from aiogram import types


def validate_username(message: types.message.Message):
    if message.from_user.first_name is None:
        name = f"{message.from_user.last_name}"
    elif message.from_user.last_name is None:
        name = f"{message.from_user.first_name}"
    elif message.from_user.first_name is None and message.from_user.last_name is None:
        name = message.from_user.username
    else:
        name = f"{message.from_user.first_name} {message.from_user.last_name}"
    return name


def make_caption(message: types.message.Message) -> str:
    return f"{validate_username(message)}\n\n {message.md_text}"
