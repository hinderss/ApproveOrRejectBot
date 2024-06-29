from aiogram import Router
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from sqlalchemy.exc import SQLAlchemyError

from app import ADMIN_CHAT_ID, db
from app.database.models import User
from app.keyboards.questions import *
from app.scripts.helpers import make_caption


router = Router()


class AdminFeedback(StatesGroup):
    entering_feedback = State()


@router.message(F.document)
async def doc_capture(message: types.message.Message, state: FSMContext):
    language = lang.default_language_code
    try:
        user: User = await db.get_user(message.from_user.id)
        language = user.language
        await state.clear()
        document_id = message.document.file_id
        file_msg = await message.bot.send_document(chat_id=ADMIN_CHAT_ID,
                                                   document=document_id,
                                                   caption=make_caption(message),
                                                   reply_markup=get_accept_keyboard(message.from_user.id,
                                                                                    message.message_id
                                                                                    )
                                                   )
        await db.add_review(document_id, message.from_user.id, message.message_id, file_msg.message_id)
        await db.increment_user_sent(message.from_user.id)
    except SQLAlchemyError:
        await message.answer(lang.get(language, 'db_error'))
    except Exception as e:
        await message.answer(lang.get(language, 'unknown_error'))
        print(f"Unknown error: {e}")


@router.callback_query(F.data.startswith("adminaccept"))
async def callbacks_num(callback: types.CallbackQuery):
    language = lang.default_language_code
    try:
        user: User = await db.get_user(callback.from_user.id)
        language = user.language
        user_id = callback.data.split("?")[1]
        chat_msg_id = int(callback.data.split("?")[2])
        await db.increment_user_accepted(user_id)
        await callback.message.edit_caption(caption=callback.message.caption+"\n\n✅",
                                            reply_markup=get_after_keyboard(user_id, chat_msg_id, language))
        await callback.answer(f"{lang.get(language, 'accepted')}!")
        reviewed_msg = await callback.bot.send_message(user_id,
                                                       text="✅!",
                                                       reply_to_message_id=chat_msg_id)
        await db.add_reviewed(user_id, chat_msg_id, reviewed_msg.message_id, True)
        await callback.answer()
    except SQLAlchemyError:
        await callback.answer(lang.get(language, 'db_error'))
    except Exception as e:
        await callback.answer(lang.get(language, 'unknown_error'))
        print(f"Unknown error: {e}")


@router.callback_query(F.data.startswith("editadminaccept"))
async def edit_admin_accept(callback: types.CallbackQuery):
    language = lang.default_language_code
    try:
        user: User = await db.get_user(callback.from_user.id)
        language = user.language
        user_id = callback.data.split("?")[1]
        chat_msg_id = int(callback.data.split("?")[2])
        reviewed_msg = await db.get_reviewed_msg_id(user_id, chat_msg_id)

        if not await db.get_document_accepted(user_id, chat_msg_id):
            await callback.message.edit_caption(caption=callback.message.caption+"\n\n✅",
                                                reply_markup=get_after_keyboard(user_id, chat_msg_id, language))
            await callback.answer(f"{lang.get(language, 'accepted')}!")
            await callback.bot.edit_message_text(chat_id=user_id,
                                                 message_id=reviewed_msg,
                                                 text="✅!")
            await db.update_accepted(True, user_id, chat_msg_id)
            await db.update_feedback(user_id, chat_msg_id, None)
            await db.increment_user_accepted(user_id)
        else:
            await callback.message.edit_reply_markup(reply_markup=get_after_keyboard(user_id, chat_msg_id, language))
        await callback.answer()
    except SQLAlchemyError:
        await callback.answer(lang.get(language, 'db_error'))
    except Exception as e:
        await callback.answer(lang.get(language, 'unknown_error'))
        print(f"Unknown error: {e}")


@router.callback_query(F.data.startswith("editadminreject"))
async def edit_admin_reject(callback: types.CallbackQuery):
    language = lang.default_language_code
    try:
        user: User = await db.get_user(callback.from_user.id)
        language = user.language
        user_id = callback.data.split("?")[1]
        chat_msg_id = int(callback.data.split("?")[2])

        reviewed_msg = await db.get_reviewed_msg_id(user_id, chat_msg_id)
        try:
            if await db.get_document_accepted(user_id, chat_msg_id):
                await db.update_accepted(False, user_id, chat_msg_id)
                await db.decrement_user_accepted(user_id)
                await callback.message.edit_caption(caption=callback.message.caption + "\n\n❌",
                                                    reply_markup=get_reject_keyboard(user_id, chat_msg_id, language))
                await callback.answer(f"{lang.get(language, 'rejected')}!")
                await callback.bot.edit_message_text(chat_id=user_id,
                                                     message_id=reviewed_msg,
                                                     text="❌!")
            else:
                await callback.message.edit_reply_markup(reply_markup=get_reject_keyboard(user_id,
                                                                                          chat_msg_id,
                                                                                          language))
        except SQLAlchemyError:
            await callback.answer(lang.get(language, 'db_error'))
        await callback.answer()
    except Exception as e:
        await callback.answer(lang.get(language, 'unknown_error'))
        print(f"Unknown error: {e}")


@router.callback_query(F.data.startswith("change"))
async def change(callback: types.CallbackQuery):
    language = lang.default_language_code
    try:
        user: User = await db.get_user(callback.from_user.id)
        language = user.language
        user_id = callback.data.split("?")[1]
        chat_msg_id = int(callback.data.split("?")[2])
        await callback.message.edit_reply_markup(reply_markup=get_accept_keyboard_edit(user_id, chat_msg_id))
    except Exception as e:
        await callback.message.answer(lang.get(language, 'unknown_error'))
        print(f"Unknown error: {e}")


@router.callback_query(F.data.startswith("editfeedback"))
async def edit_feedback(callback: types.CallbackQuery, state: FSMContext):
    language = lang.default_language_code
    try:
        user: User = await db.get_user(callback.from_user.id)
        language = user.language
        user_id = callback.data.split("?")[1]
        chat_msg_id = int(callback.data.split("?")[2])
        await callback.message.edit_reply_markup(reply_markup=get_edit_process_keyboard(user_id, chat_msg_id, language))
        enter_feedback_msg = await callback.bot.send_message(ADMIN_CHAT_ID,
                                                             text=f"{lang.get(language, 'enter_comment')}:",
                                                             reply_to_message_id=callback.message.message_id)
        await state.update_data(user_id=user_id, chat_msg_id=chat_msg_id,
                                admin_msg_id=callback.message.message_id,
                                enter_feedback_msg_id=enter_feedback_msg.message_id,
                                admin_msg_text=callback.message.md_text)
        await state.set_state(AdminFeedback.entering_feedback)
    except Exception as e:
        await callback.message.answer(lang.get(language, 'unknown_error'))
        print(f"Unknown error: {e}")


@router.message(AdminFeedback.entering_feedback)
async def apply_feedback(message: Message, state: FSMContext):
    language = lang.default_language_code
    try:
        user: User = await db.get_user(message.from_user.id)
        language = user.language
        user_data = await state.get_data()
        await message.bot.edit_message_caption(chat_id=ADMIN_CHAT_ID,
                                               message_id=user_data['admin_msg_id'],
                                               caption=f"{user_data['admin_msg_text']} "
                                                       f"\n\n[{message.text}]".replace('\\', ''))
        await message.bot.edit_message_reply_markup(chat_id=ADMIN_CHAT_ID,
                                                    message_id=user_data['admin_msg_id'],
                                                    reply_markup=get_after_keyboard(user_data['user_id'],
                                                                                    user_data['chat_msg_id'],
                                                                                    language
                                                                                    ))
        await message.bot.edit_message_text(chat_id=ADMIN_CHAT_ID,
                                            message_id=user_data['enter_feedback_msg_id'],
                                            text=f"👆{lang.get(language, 'press_to_return')}")
        try:
            await db.update_feedback(user_data['user_id'], user_data['chat_msg_id'], message.text)
            reviewed_msg_id = await db.get_reviewed_msg_id(user_data['user_id'], user_data['chat_msg_id'])

            await message.bot.edit_message_text(chat_id=user_data['user_id'],
                                                message_id=reviewed_msg_id,
                                                text=f"❌\n {message.text}")
            await message.delete()
        except SQLAlchemyError:
            await message.answer(lang.get(language, 'db_error'))
    except Exception as e:
        await message.message.answer(lang.get(language, 'unknown_error'))
        print(f"Unknown error: {e}")
    finally:
        await state.clear()


@router.callback_query(F.data.startswith("adminreject"))
async def callbacks_num(callback: types.CallbackQuery):
    language = lang.default_language_code
    try:
        user: User = await db.get_user(callback.from_user.id)
        language = user.language
        user_id = callback.data.split("?")[1]
        chat_msg_id = int(callback.data.split("?")[2])
        await callback.message.edit_caption(
            caption=callback.message.caption + "\n\n❌", reply_markup=get_reject_keyboard(user_id,
                                                                                         chat_msg_id,
                                                                                         language))
        await callback.answer(f"{lang.get(language, 'rejected')}!")
        reviewed_msg = await callback.bot.send_message(user_id, text="❌!", reply_to_message_id=chat_msg_id)
        await db.add_reviewed(user_id, chat_msg_id, reviewed_msg.message_id, False)
        await callback.answer()
    except Exception as e:
        await callback.message.answer(lang.get(language, 'unknown_error'))
        print(f"Unknown error: {e}")


@router.callback_query(AdminFeedback.entering_feedback, F.data.startswith("canceleditfeedback"))
async def cancel_edit_feedback(callback: types.CallbackQuery, state: FSMContext):
    language = lang.default_language_code
    try:
        user: User = await db.get_user(callback.from_user.id)
        language = user.language
        user_data = await state.get_data()

        user_id = callback.data.split("?")[1]
        chat_msg_id = int(callback.data.split("?")[2])
        await callback.message.bot.edit_message_text(chat_id=ADMIN_CHAT_ID,
                                                     message_id=user_data['enter_feedback_msg_id'],
                                                     text=f"👆{lang.get(language, 'press_to_return')}")
        await callback.message.edit_reply_markup(reply_markup=get_reject_keyboard(user_id, chat_msg_id, language))
        await callback.answer()
    except Exception as e:
        await callback.message.answer(lang.get(language, 'unknown_error'))
        print(f"Unknown error: {e}")
    finally:
        await state.clear()
