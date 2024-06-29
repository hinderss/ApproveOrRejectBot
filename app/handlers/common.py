from typing import List

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.filters import Command
from aiogram.enums import ParseMode

from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app import db
from app.database.models import User
from app.keyboards.questions import *
from app.scripts.helpers import validate_username
from app.filters.admin_filter import AdminFilter

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    language = lang.get_language_code(message.from_user.language_code)
    try:
        await db.add_user(message.from_user.id, validate_username(message), language)
    except SQLAlchemyError:
        await message.answer(lang.get(language, 'db_error'))
    else:
        await message.answer(f"{lang.get(language, 'welcome')}, {hbold(message.from_user.full_name)}!")


@router.message(Command("lang"))
async def command_lang_handler(message: Message) -> None:
    try:
        user: User = await db.get_user(message.from_user.id)
        language = user.language
    except SQLAlchemyError:
        language = lang.default_language_code
    await message.answer(text=f"{lang.get(language, 'choose_language_prompt')}:", reply_markup=select_language())


@router.callback_query(F.data.startswith("language"))
async def callbacks_language(callback: types.CallbackQuery):
    language = lang.default_language_code
    try:
        new_language = callback.data.split("?")[1]
        await db.update_language(callback.from_user.id, new_language)
        await callback.message.answer(f"{lang.get(new_language, 'language_changed')}.")
    except SQLAlchemyError:
        await callback.answer(lang.get(language, 'db_error'))
    except Exception as e:
        await callback.message.answer(lang.get(language, 'unknown_error'))
        print(f"Unknown error: {e}")
    finally:
        await callback.message.delete()


@router.message(Command("help"))
async def command_lang_handler(message: Message) -> None:
    try:
        user: User = await db.get_user(message.from_user.id)
        language = user.language
    except SQLAlchemyError:
        language = lang.default_language_code
    await message.answer(text=f"{lang.get(language, 'help_content')}", parse_mode=ParseMode.MARKDOWN_V2)


@router.message(Command("stat"))
async def statistics(message: Message) -> None:
    language = lang.default_language_code
    try:
        user: User = await db.get_user(message.from_user.id)
        language = user.language
        await message.answer(f"👤{lang.get(language, 'statistics')}:\n"
                             f"{lang.get(language, 'sent')}: {user.sent}\n"
                             f"{lang.get(language, 'accepted')}: {user.accepted}")
    except NoResultFound:
        await message.answer(lang.get(language, 'user_not_found'))
    except SQLAlchemyError:
        await message.answer(lang.get(language, 'db_error'))
    except Exception as e:
        await message.answer(lang.get(language, 'unknown_error'))
        print(f"Unknown error: {e}")


@router.message(AdminFilter(), Command("adminstat"))
async def admin_statistics(message: Message) -> None:
    language = lang.default_language_code
    try:
        user: User = await db.get_user(message.from_user.id)
        language = user.language
        users: List[User] = await db.get_users()
        msg_text = ""
        for user in users:
            msg_text += (f"👤{user.name}:\n"
                         f"{lang.get(language, 'sent')}: {user.sent}\n"
                         f"{lang.get(language, 'accepted')}: {user.accepted}\n\n")
        await message.answer(msg_text)
    except SQLAlchemyError:
        await message.answer(lang.get(language, 'db_error'))
    except Exception as e:
        await message.answer(lang.get(language, 'unknown_error'))
        print(f"Unknown error: {e}")


@router.message(AdminFilter(), Command("vipe"))
async def vipe(message: Message) -> None:
    try:
        user: User = await db.get_user(message.from_user.id)
        language = user.language
    except SQLAlchemyError:
        language = lang.default_language_code
    await message.answer(text=f"{lang.get(language, 'reset_stats_confirm')}?", reply_markup=vipe_markup(language))


@router.callback_query(AdminFilter(), F.data.startswith("vipeaccept"))
async def callbacks_num(callback: types.CallbackQuery):
    language = lang.default_language_code
    try:
        user: User = await db.get_user(callback.from_user.id)
        language = user.language
        await db.clear_tables_zero_users()
        await callback.message.answer(f"{lang.get(language, 'stats_reset_success')}.")
    except SQLAlchemyError:
        await callback.answer(lang.get(language, 'db_error'))
        await callback.message.answer(f"{lang.get(language, 'stats_reset_failed')}.")
    except Exception as e:
        await callback.message.answer(f"{lang.get(language, 'stats_reset_failed')}.")
        print(f"Unknown error: {e}")
    finally:
        await callback.message.delete()


@router.callback_query(AdminFilter(), F.data.startswith("vipereject"))
async def callbacks_num(callback: types.CallbackQuery):
    await callback.message.delete()
