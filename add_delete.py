from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from craate_bot import dp, bot
import admin_kb
import os
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class FSMADMIN_ADD(StatesGroup):
    add = State()

class FSMADMIN_DEL(StatesGroup):
    delete = State()

# @dp.message_handler(commands='admin', state=None)
async def admin(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=admin_kb.button_case_admin)

# @dp.message_handler(commands='Добавить', state=None)
async def cm_start(message: types.Message):
    await FSMADMIN_ADD.add.set()
    await message.reply('введите ключевые слова через запятую\nНапример: Генеральный план, ГП, Сервитут\nДля отмены добавления введите "отмена"')

# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')

# @dp.message_handler(state=FSMADMIN_ADD.add)
async def add(message: types.Message, state: FSMContext):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    print(os.path.join(dir_path, 'keywords.txt'))
    with open(os.path.join(dir_path, 'keywords.txt'), 'a', encoding='utf-8') as f:
        for k in message.text.split(','):
            f.write(f'{k.strip()}\n')
    await state.finish()
    await message.reply('Ключевые слова добавлены')

# @dp.message_handler(commands='Посмотреть')
async def read_key_word(message: types.Message):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    if 'keywords.txt' not in os.listdir(dir_path):
        with open(os.path.join(dir_path, 'keywords.txt'), 'a', encoding='utf-8') as f:
            f.write('')
        await message.reply('Нет ключевых слов')
    else:
        with open(os.path.join(dir_path, 'keywords.txt'), 'r', encoding='utf-8') as f:
            keyword = ''.join(f.readlines()).strip().split('\n')
        MS = ''
        for word in keyword:
            MS += f'{word}\n'
        # print(f'MS - "{MS}"')
        if MS.strip() == '':
            await message.reply('Нет ключевых слов')
        else:
            await message.reply(MS)

@dp.message_handler(commands='Удалить', state=None)
async def start_delete_key_word(message: types.Message):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    if 'keywords.txt' not in os.listdir(dir_path):
        with open(os.path.join(dir_path, 'keywords.txt'), 'a', encoding='utf-8') as f:
            f.write('')
        await message.reply('Нет ключевых слов')
    else:
        with open(os.path.join(dir_path, 'keywords.txt'), 'r', encoding='utf-8') as f:
            keyword = ''.join(f.readlines()).strip().split('\n')
        if len(keyword) == 0:
            await message.reply('Нет ключевых слов')
        else:
            MS = ''
            for word in keyword:
                MS += f'{word}\n'
            if MS.strip() == '':
                await message.reply('Нет ключевых слов')
            else:
                await FSMADMIN_DEL.delete.set()
                await message.reply(f'{MS}\n Напишите ключевые слова которые необходимо удалить через запятую\nНапример: Генеральный план, ГП, Сервитут\nДля отмены удаления введите "отмена"')

@dp.message_handler(state=FSMADMIN_DEL.delete)
async def delete(message: types.Message, state: FSMContext):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    del_word = message.text.split(',')
    with open(os.path.join(dir_path, 'keywords.txt'), 'r', encoding='utf-8') as f:
        keyword = ''.join(f.readlines()).strip().split('\n')
    error = []
    for word in del_word:
        if word.strip() in keyword:
            keyword.remove(word.strip())
        else:
            error.append(word.strip())

    MS = ''
    with open(os.path.join(dir_path, 'keywords.txt'), 'w', encoding='utf-8') as f:
        for word in keyword:
            f.write(f'{word}\n')
            MS += f'{word}\n'
    await message.answer(f'Текущий список ключевых слов\n{MS}')

    if len(error) != 0:
        MS_er = ''
        for er in error:
            MS_er += f'{er}\n'
        await message.answer(f'Данные слова не получилось удалить: {MS_er}')
    await state.finish()

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin, commands=['admin'])
    dp.register_message_handler(cm_start, commands='Добавить', state=None)
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(add, state=FSMADMIN_ADD.add )
    dp.register_message_handler(read_key_word, commands='Посмотреть')