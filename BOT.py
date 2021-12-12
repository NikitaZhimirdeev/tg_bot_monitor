import asyncio
import os
import sys
from craate_bot import dp, bot
from aiogram import Bot, Dispatcher, executor, types
import add_delete
import parser_website

# Идексация того, что бот начал работу
async def on_startup(_):
    print('Бот вышел в сеть')

# Команда запуска бота
@dp.message_handler(commands=['start', 'help'])
async def START(message: types.Message):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    # Сбор всех id пользователей, которые активировали бота

    if 'users.txt' not in os.listdir(dir_path):
        with open(os.path.join(dir_path, 'users.txt'), 'a') as f:
            pass

    with open(os.path.join(dir_path, 'users.txt'), 'r') as f:
        users = ''.join(f.readlines()).strip().split('\n')
    # Проверка, если пользователя нет в списке активировавших, то записываем его туда
    if not (str(message.from_user.id) in users):
        with open(os.path.join(dir_path, 'users.txt'), 'a') as f:
            f.write(f'{message.from_user.id}\n')
    await message.answer('Чтобы начать мониторинг введите команду /RUN, чтобы просмотреть, добавить или удалить ключевые слова войдите в панель администратора при помощи команды /admin')

# @dp.message_handler(commands='RUN')
async def PARSER_WHILE():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    # print('Бот вышел в сеть')
    error_ind = 0
    while True:
        try:
            keywords = parser_website.read_keywords()
            mozhaysk, vos_mo, pavpos = parser_website.main()

            # Открываем список пользователей, которые активировали бота
            if 'users.txt' not in os.listdir(dir_path):
                with open(os.path.join(dir_path, 'users.txt'), 'a') as f:
                    pass

            with open(os.path.join(dir_path, 'users.txt'), 'r') as f:
                users = ''.join(f.readlines()).strip().split('\n')

            if 'filtr.txt' not in os.listdir(dir_path):
                with open(os.path.join(dir_path, 'filtr.txt'), 'a') as f:
                    pass

            NEW_DATA = {}
            filtr_read = parser_website.read_filtr()

            for key, val in mozhaysk.items():
                if key.strip() not in filtr_read:
                    NEW_DATA[key] = val
                    # print(f'{key} - {val}')
                    # parser_website.write_filtr(key)
            ALL = {**vos_mo, **pavpos}
            for key, val in ALL.items():
                for words in keywords:
                    if words in key:
                        if not (key.strip() in filtr_read):
                            # print(f'{words} - {key}')
                            # print(f'{key} - {val}')
                            # write_filtr(key)
                            NEW_DATA[key] = val
            # print(f'NEW_DATA - {NEW_DATA}')
            if NEW_DATA == {}:
                for user in users:
                    try:
                        await bot.send_message(chat_id=user, text = 'Новых документов нет')
                    except:
                        pass
            else:
                for key, val in NEW_DATA.items():
                    parser_website.write_filtr(key)
                    for user in users:
                        # await bot.send_message(chat_id=user, text=MS)
                        try:
                            await bot.send_message(chat_id=user, text = f'{key}\n{val}')
                        except:
                            pass


            await asyncio.sleep(85800) # 85800 Время сна, если необходимо изменить частоту проперки, то необходимо имменить число, время в секундах
            sys.exit()
        except SystemExit:
            # print('sysEXIT')
            sys.exit()
        except:
            error_ind += 1
            if error_ind < 20:
                # print('sleep')
                await asyncio.sleep(60)
            else:
                # print('sysEXIT SLEEP')
                sys.exit()
#////////////////////////////////////////////////////////////////
@dp.message_handler(commands='RUN')
async def PARSER(message: types.Message):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    # print('Бот вышел в сеть')
    # while True:
    # try:
    keywords = parser_website.read_keywords()
    mozhaysk, vos_mo, pavpos = parser_website.main()

    # Открываем список пользователей, которые активировали бота
    if 'users.txt' not in os.listdir(dir_path):
        with open(os.path.join(dir_path, 'users.txt'), 'a') as f:
            pass

    with open(os.path.join(dir_path, 'users.txt'), 'r') as f:
        users = ''.join(f.readlines()).strip().split('\n')

    if 'filtr.txt' not in os.listdir(dir_path):
        with open(os.path.join(dir_path, 'filtr.txt'), 'a') as f:
            pass

    NEW_DATA = {}
    filtr_read = parser_website.read_filtr()

    for key, val in mozhaysk.items():
        if key.strip() not in filtr_read:
            NEW_DATA[key] = val
            # print(f'{key} - {val}')
            # parser_website.write_filtr(key)
    ALL = {**vos_mo, **pavpos}
    for key, val in ALL.items():
        for words in keywords:
            if words in key:
                if not (key.strip() in filtr_read):
                    # print(f'{words} - {key}')
                    # print(f'{key} - {val}')
                    # write_filtr(key)
                    NEW_DATA[key] = val
    # print(f'NEW_DATA - {NEW_DATA}')
    if NEW_DATA == {}:
        for user in users:
            try:
                await bot.send_message(chat_id=user, text='Новых документов нет')
            except:
                pass
    else:
        for key, val in NEW_DATA.items():
            parser_website.write_filtr(key)
            for user in users:
                # await bot.send_message(chat_id=user, text=MS)
                try:
                    await bot.send_message(chat_id=user, text=f'{key}\n{val}')
                except:
                    pass


        # await asyncio.sleep(15) # Время сна, если необходимо изменить частоту проперки, то необходимо имменить число, время в секундах
    # except:
    #     print('sleep')
    #     await asyncio.sleep(60)


add_delete.register_handlers_admin(dp)


# Запуска бота
loop = asyncio.get_event_loop()
loop.create_task(PARSER_WHILE())
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
# loop = asyncio.get_event_loop()
# loop.create_task(PARSER_WHILE())

#P http://www.admmozhaysk.ru/docs/doc/no928-62-ot-30.01.2018-ob-utverzhdenii-pravil-zemlepolzovaniya-i-zastrojki-territorii-chasti-territor-148791
#S http://www.admmozhaysk.ru/docs/doc/no928-62-ot-30.01.2018-ob-utverzhdenii-pravil-zemlepolzovaniya-i-zastrojki-territorii-chasti-territor-148791