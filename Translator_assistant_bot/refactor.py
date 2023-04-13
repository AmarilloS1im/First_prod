# region Imports
import os
import uuid
import csv
import openpyxl
import shutil
import emoji
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


# endregion


# region Class Dictionary
class Dictionary:
    def __init__(self):
        self.__main_dict = None
        self.__custom_dict = None

    @property
    def main_dict(self):
        my_dict = []
        with open(rf"dummy\main_dict.csv") as r_file:
            file_reader = csv.reader(r_file, delimiter=";")
            for row in file_reader:
                tmp_dict = [row[0], row[1]]
                my_dict.append(tmp_dict)
        self.__main_dict = list(sorted(my_dict, key=lambda item: len(item[0]), reverse=True))
        return self.__main_dict

    def set_custom_dict(self, value):
        my_dict = []
        with open(rf"dummy/{value}", 'r', encoding='utf-8-sig') as r_file:
            file_reader = csv.reader(r_file, delimiter=";")
            for row in file_reader:
                tmp_dict = [row[0], row[1]]
                my_dict.append(tmp_dict)
        self.__custom_dict = list(sorted(my_dict, key=lambda item: len(item[0]), reverse=True))

    def get_custom_dict(self):
        return self.__custom_dict


# endregion


# region Translation Block
def translate_info_from_doc(file_name, user_dict):
    def translate_str(str_from_data_file, user_dict):
        print(str_from_data_file)
        out_list = []
        list_to_translate = str_from_data_file.split('\n')
        print(list_to_translate)
        origin_list = str_from_data_file.split('\n')[:]
        if len(list_to_translate) <= 1:
            for j in range(len(user_dict)):
                list_to_translate[0] = list_to_translate[0].replace(user_dict[j][0], user_dict[j][1])
            if list_to_translate != origin_list:
                list_to_translate[0] = origin_list[0] + " / " + list_to_translate[0]
                out_list.append(list_to_translate[0])
            else:
                out_list.append(origin_list[0])
        else:
            for i in range(len(list_to_translate)):
                for j in range(len(user_dict)):
                    list_to_translate[i] = list_to_translate[i].replace(user_dict[j][0], user_dict[j][1])
                if list_to_translate != origin_list:
                    list_to_translate[i] = origin_list[i].lstrip() + " / " + list_to_translate[i]
                    out_list.append(list_to_translate[i])
                else:
                    out_list.append(origin_list[i])
        print(out_list)
        out_list = '\n'.join(out_list)
        print(out_list)
        return out_list

    uuid_name = str(uuid.uuid4())
    uuid_dict = {}
    if uuid_name in uuid_dict.keys():
        uuid_name = str(uuid.uuid4())
    else:
        uuid_dict[uuid_name] = file_name
    extension = file_name.split('.')[-1]
    shutil.copy(rf"dummy\{file_name}", rf"dummy\{uuid_name}.{extension}")
    book = openpyxl.open(rf"dummy\{uuid_name}.{extension}", read_only=False, data_only=True)
    sheet = book.active
    for row in range(2, sheet.max_row):
        for cell in range(1, sheet.max_column):
            if isinstance(sheet[row][cell].value, str):
                sheet[row][cell].value = translate_str(sheet[row][cell].value, user_dict)
            else:
                pass
    book.save(rf"dummy\__Translated__{uuid_dict[uuid_name]}")
    book.close()
    return rf"dummy\__Translated__{uuid_dict[uuid_name]}"


# endregion


# region Bot block
# region Initialize bot and dispatcher
bot = Bot(token=os.getenv('API_TOKEN'))

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)


class FSMAdmin(StatesGroup):
    file_to_translate = State()
    add_custom_dict = State()


# endregion


# region Make buttons
translate_button = types.InlineKeyboardButton('ПЕРЕВЕСТИ', callback_data='translate_button')
add_new_words_button = types.InlineKeyboardButton('ДОБАВИТЬ НОВЫЙ СЛОВАРЬ', callback_data='add_to_dict')
help_button = types.InlineKeyboardButton('ПОМОЩЬ', callback_data='help')
markup_start_screen = types.InlineKeyboardMarkup(row_width=2)
markup_start_screen.add(translate_button, add_new_words_button, help_button)

button_back = types.InlineKeyboardButton('НАЗАД', callback_data='back')
markup_back = types.InlineKeyboardMarkup(row_width=1)
markup_back.add(button_back)

markup_dicts = types.InlineKeyboardMarkup(row_width=1)
main_dict_button = types.InlineKeyboardButton('СКАЧАТЬ БАЗОВЫЙ СЛОВАРЬ', callback_data='main_dict')
custom_dict_button = types.InlineKeyboardButton('ЗАГРУЗИТЬ ПОЛЬЗОВАТЕЛЬСКИЙ СЛОВАРЬ', callback_data='set_custom_dict')
restore_main_dict_button = types.InlineKeyboardButton('УДАЛИТЬ ПОЛЬЗОВАТЕЛЬСКИЙ СЛОВОВАРЬ',
                                                      callback_data='restore_main_dict')
markup_dicts.add(main_dict_button, custom_dict_button, restore_main_dict_button, help_button, button_back)

markup_next_doc = types.InlineKeyboardMarkup(row_width=1)
next_doc_button = types.InlineKeyboardButton('ПЕРЕВЕСТИ СЛЕДУЮЩИЙ ДОКУМЕНТ', callback_data='next_doc')
markup_next_doc.add(next_doc_button, button_back)


# endregion


# region START SCREEN
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_nikname = message.from_user.username
    user_full_name = message.from_user.full_name
    print(f'{user_id}-----{user_full_name} {user_nikname}')
    await message.reply(
        f"Привет {user_full_name}\nЯ Translator's assistant bot\nЧтобы перевести документ нажми кнопку ПЕРЕВЕСТИ\n"
        f"Чтобы добавить новые слова в словарь нажми кнопку ДОБАВИТЬ НОВЫЙ СЛОВАРЬ\n"
        f"Для получения более подробной информации нажми кнопку ПОМОЩЬ",
        reply_markup=markup_start_screen)


# endregion

# region TRANSLATE BUTTON ACTION
@dp.callback_query_handler(text='translate_button')
async def callback_translate(callback: types.CallbackQuery):
    await FSMAdmin.file_to_translate.set()
    await callback.message.answer(f"ЧТОБЫ ЗАГРУЗИТЕ ДОКУМЕНТ, КОТОРЫЙ НУЖНО ПЕРЕВЕСТИ\n"
                                  f"НАЖМИТЕ НА {emoji.emojize(':paperclip:')}", reply_markup=markup_back)


# endregion


# region MESSGE HENDLER TRANSLATE
@dp.message_handler(content_types=types.ContentType.ANY, state=FSMAdmin.file_to_translate)
async def load_on_server_file_to_translate(message: types.Message, state: FSMContext):
    if message.content_type != 'document':
        await FSMAdmin.file_to_translate.set()
        await message.answer('Я умею перводить только Excel файлы, загрузите файл с раширениме .xls или .xlsx',
                             reply_markup=markup_back)
    else:
        user_file = message.document.file_name
        user_unique_id = message.from_user.id
        user_file_extantion = '.' + message.document.file_name.split('.')[-1]
        if user_file_extantion != '.xlsx' and user_file_extantion != '.xls':
            await FSMAdmin.file_to_translate.set()
            await message.answer('Документ должен быть в формате .xls или .xlsx', reply_markup=markup_back)
        else:
            await message.document.download(destination_file=rf"dummy\{user_file}")
            await message.answer('БОТ НАЧАЛ ПЕРВОД ДОКУМЕНТА, ОЖИДАЙТЕ')
            user_dict = Dictionary()
            if rf"{user_unique_id}.csv" in os.listdir('dummy/'):
                user_dict.set_custom_dict(rf"{user_unique_id}.csv")
                user_dict = user_dict.get_custom_dict()
                translated_doc = translate_info_from_doc(user_file, user_dict)
            else:
                user_dict = user_dict.main_dict
                translated_doc = translate_info_from_doc(user_file, user_dict)
            reply_translate_doc = open(translated_doc, 'rb')
            await message.answer('ФАЙЛ ПЕРВЕДЕН И ГОТОВ К СКАЧИВАНИЮ')
            await message.reply_document(reply_translate_doc, reply_markup=markup_next_doc)

            if translated_doc in os.listdir(f'dummy'):
                os.remove(rf"dummy\{translated_doc}")
            await state.finish()


# endregion


# region NEXT DOC BUTTON ACTION
@dp.callback_query_handler(text='next_doc')
async def callback_next_doc_translate(callback: types.CallbackQuery):
    await FSMAdmin.file_to_translate.set()
    await callback.message.answer(f"ЧТОБЫ ЗАГРУЗИТЕ ДОКУМЕНТ, КОТОРЫЙ НУЖНО ПЕРЕВЕСТИ\n"
                                  f"НАЖМИТЕ НА {emoji.emojize(':paperclip:')}", reply_markup=markup_back)


# endregion


# region ADD TO DICT BUTTON ACTION
@dp.callback_query_handler(text='add_to_dict')
async def add_to_dict(callback: types.CallbackQuery):
    await callback.message.answer(
        'Чтобы добавить пользовательский словарь, загрузите файл с новыми словами в формате .CSV\n'
        'Для корректной загрузки словаря, см. справку в разделе "ПОМОЩЬ"', reply_markup=markup_dicts)


# endregion


# region SET CUSTOM DICT BUTTON ACTION
@dp.callback_query_handler(text='set_custom_dict')
async def set_custom_dicts(callback: types.CallbackQuery):
    await callback.message.answer(f"ЧТОБЫ ЗАГРУЗИТЕ ПОЛЬЗОВАТЕЛЬСКИЙ СЛОВАРЬ,"
                                  f"НАЖМИТЕ НА {emoji.emojize(':paperclip:')}", reply_markup=markup_back)
    await FSMAdmin.add_custom_dict.set()


# endregion


# region SEND MAIN DICTTO USER BUTTON ACTION
@dp.callback_query_handler(text='main_dict')
async def upload_main_dict_to_user(callback: types.CallbackQuery):
    reply_main_dict = open(r"dummy\main_dict.csv", 'rb')
    await callback.message.reply_document(reply_main_dict)
    await callback.answer('Базовый словарь получен')


# endregion


# region RESRTORE MAIN DICT BUTTON ACTION
@dp.callback_query_handler(text='restore_main_dict')
async def restore_dict(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    try:
        os.remove(rf"dummy\{user_id}.csv")
        await callback.message.answer('ПОЛЬЗОВАТЕЛЬСКИЙ СЛОВАРЬ УДАЛЕН, БАЗОВЫЙ СЛОВАРЬ ВОССТАНОВЛЕН')
    except:
        await callback.message.answer('У ВАС НЕТ ДЕЙСТВУЮЩЕГО ПОЛЬЗОВАТЕЛЬСКОГО СЛОВАРЯ')


# endregion


# region MESSAGE HENDLER SET CUSTOM DICT
@dp.message_handler(content_types=ContentType.ANY, state=FSMAdmin.add_custom_dict)
async def load_on_server_dict(message: types.Message, state: FSMContext):
    if message.content_type != 'document':
        await FSMAdmin.add_custom_dict.set()
        await message.answer('Словарем может быть только файл в формате .csv', reply_markup=markup_back)
    else:
        user_id = message.from_user.id
        user_dict_name = message.document.file_name
        user_dict_extension = '.' + user_dict_name.split('.')[-1]
        if user_dict_extension != '.csv':
            await FSMAdmin.add_custom_dict.set()
            await message.answer('Файл должен иметь расширение .csv', reply_markup=markup_back)
        else:
            src = rf"dummy\{user_id}{user_dict_extension}"
            await message.document.download(destination_file=src)
            await message.answer('ВАШ СЛОВАРЬ УСПЕШНО ДОБАВЛЕН,МОЖЕТЕ НАЧАТЬ ПЕРВОД ДОКУМЕНТА')
            await state.finish()


# endregion


# region HELP BUTTON ACTION
@dp.callback_query_handler(text='help')
async def callback_help(callback: types.CallbackQuery):
    await callback.message.reply(
        'Чтобы добавить пользовательский словарь, загрузите файл с новыми словами в формате .CSV\n'
        'СОЗДАЙТЕ ПУСТОЙ ФАЛЙ В ФОРМАТЕ .TXT\nПОСЛЕ СОЗДАНИЯ ПЕРЕИМЕНУЙТЕ ЕГО ТАК, КАК ВАМ УДОБНО И ПОМЕНЯЙТЕ '
        'РАСШИРЕНИЕ ФАЙЛА НА .CSV\n'
        'Далее откройте файл и добавьте в колонку A "слово", в колонку B "перевод".\n'
        'Количество пар(слово ; перевод) не ограниченно. ДОБАВЛЯЙТЕ КАЖДУ НОВУЮ ПАРУ СТРОЧКОЙ НИЖЕ.\n\n'
        '\t\t\t\t\t\t\t\tВНИМАНИЕ!    ATTENTION!     ACHTUNG!    \n\n'
        'ВАШ СЛОВАРЬ ДОЛЖЕН ИМЕТЬ КОДИРОВКУ "utf-8 со спецификацией"\n\n'
        'Когда ваш словарь будет готов, загрузите его с помощью кнопки ДОБАВИТЬ '
        'НОВЫЙ СЛОВАРЬ-->ЗАГРУЗИТЬ ПОЛЬЗОВАТЕЛЬСКИЙ СЛОВАРЬ"\n'
        'Вы также можете расширить базовый словарь путем добавления в него своих слов.\n'
        'Для этого в разделе ДОБАВИТЬ НОВЫЙ СЛОВАРЬ нажмите кнопку СКАЧАТЬ БАЗОВЫЙ СЛОВАРЬ\n\n'
        'Сохраните его себе на компьютер, добавьте в него необходимые вам слова,'
        ' после этого загрузите этот файл нажав на кноку '
        'ДОБАВИТЬ НОВЫЙ СЛОВАРЬ-->ЗАГРУЗИТЬ ПОЛЬЗОВАТЕЛЬСКИЙ СЛОВАРЬ\n'
        'После этого можете приступать к перводу\n'
        'ВНИМАНИЕ!\nПри нажатии на кнопку УДАЛИТЬ ПОЛЬЗОВАТЕЛЬСКИЙ СЛОВОВАРЬ, ваш словарь будет полностью удален\n'
        'Весь дальнейший первод будет идти на основание базового словаря ',
        reply_markup=markup_back)


# endregion


# region BACK BUTTON ACTION
@dp.callback_query_handler(text='back', state=[FSMAdmin.add_custom_dict, FSMAdmin.file_to_translate, None])
async def callback_back_button(callback: types.CallbackQuery, state: FSMContext):
    user_full_name = callback.from_user.full_name
    await state.finish()
    await callback.message.reply(
        f'Привет {user_full_name}\nЯ DocTranslatorBot\nЧтобы перевести документ нажми кнопку ПЕРЕВЕСТИ\n'
        f'Чтобы добавить новые слова в словарь нажми кнопку ДОБАВИТЬ НОВЫЕ СЛОВА.',
        reply_markup=markup_start_screen)


# endregion
# endregion


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
