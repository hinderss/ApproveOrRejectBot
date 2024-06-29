from aiogram import types
from app import lang


def get_accept_keyboard(user_id, message_id):
    buttons = [
        [
            types.InlineKeyboardButton(text="✅", callback_data=f"adminaccept?{user_id}?{message_id}"),
            types.InlineKeyboardButton(text="❌", callback_data=f"adminreject?{user_id}?{message_id}")
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def select_language():
    avl = lang.available_languages()
    paired_list = [[avl[i], avl[i + 1]] for i in range(0, len(avl) - 1, 2)]
    if len(avl) % 2 != 0:
        paired_list.append([avl[-1]])

    buttons = []
    for i in paired_list:
        row = []
        for j in i:
            row.append(
                types.InlineKeyboardButton(text=f"{lang.language_by_code(j)}", callback_data=f"language?{j}")
            )
        buttons.append(row)

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def vipe_markup(language):
    buttons = [
        [
            types.InlineKeyboardButton(text=f"{lang.get(language, 'reset')}🧹", callback_data=f"vipeaccept"),
            types.InlineKeyboardButton(text=f"{lang.get(language, 'cancel')}✖️", callback_data=f"vipereject")
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_accept_keyboard_edit(user_id, message_id):
    buttons = [
        [
            types.InlineKeyboardButton(text="✏️✅", callback_data=f"editadminaccept?{user_id}?{message_id}"),
            types.InlineKeyboardButton(text="✏️❌", callback_data=f"editadminreject?{user_id}?{message_id}")
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_after_keyboard(user_id, message_id, language):
    buttons = [
        [
            types.InlineKeyboardButton(text=f"✏️{lang.get(language, 'edit_choice')}",
                                       callback_data=f"change?{user_id}?{message_id}"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_reject_keyboard(user_id, message_id, language):
    buttons = [
        [
            types.InlineKeyboardButton(text=f"✏️{lang.get(language, 'edit_choice')}",
                                       callback_data=f"change?{user_id}?{message_id}")
        ],
        [
            types.InlineKeyboardButton(text=f"🗒{lang.get(language, 'add_comment')}",
                                       callback_data=f"editfeedback?{user_id}?{message_id}")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_edit_process_keyboard(user_id, message_id, language):
    buttons = [[types.InlineKeyboardButton(text=f"{lang.get(language, 'editing_press_to_cancel')}",
                                           callback_data=f"canceleditfeedback?{user_id}?{message_id}")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
