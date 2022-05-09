from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import pandas as pd
import asyncio

#инициализация бота через токен
token = ''
bot = Bot(token=token)
dp = Dispatcher(bot,storage=MemoryStorage())
flag=True
# value - мин размер плотности которые надо рассматривать
# command - режим работы:
# 1-пользователь просто запросил плотности на данный момент(/search)
# 2-пользователь запросил уведомления о новых плотностях=> надо проверять со старыми(/subscribe)
def search_new(value,key):
    sorted_data= pd.read_json('result')
    values=pd.read_json('values')
    previous_data = pd.read_json('previous_data')
    sorted_data_dict={}
    previous_data_dict={}
    result_data={}
    notifications_data={}
    #перенос pandas в словарь
    for x,y in sorted_data.iterrows():
        sorted_data_dict[x]={'bids':y['bids'],'asks':y['asks']}
    for x,y in values.iterrows():
        sorted_data_dict[x]={'bids':sorted_data_dict[x]['bids'],'asks':sorted_data_dict[x]['asks'],'volume':y[0]}
    for x,y in previous_data.iterrows():
        previous_data_dict[x]={'bids':y['bids'],'asks':y['asks']}


    #отбор плотностей подходящих под value*volume
    for ticket in sorted_data_dict:
        bids=[]
        asks=[]
        #Обработка bids
        for bid in sorted_data_dict[ticket]['bids']:
            if float(bid[0])*float(bid[1])>=value*float(sorted_data_dict[ticket]['volume']):
                bids.append(bid)
            else:
                break
        #обработка asks
        for ask in sorted_data_dict[ticket]['asks']:
            if float(ask[0])*float(ask[1])>=value*float(sorted_data_dict[ticket]['volume']):
                asks.append(ask)
            else:
                break
        if bids!=[] or asks!=[]:
            result_data[ticket]={'bids':bids,'asks':asks}

    #второй режим-подписка на рассылку (тут надо делать доп проверку, чтобы не отправлять одни и те же плотности несколько раз)
    if key==2:
        if not(previous_data.empty):
            for ticket in result_data:
                bids=[]
                asks=[]
                if ticket in previous_data_dict:
                    #oбработка bids
                    for bid in result_data[ticket]['bids']:
                        flat_list = [item for sublist in previous_data_dict[ticket]['bids'] for item in sublist]
                        if not(bid[0] in flat_list):
                            bids.append(bid)
                    #обработка asks
                    for ask in result_data[ticket]['asks']:
                        flat_list = [item for sublist in previous_data_dict[ticket]['asks'] for item in sublist]
                        if not(ask[0] in flat_list):
                            bids.append(ask)
                    if bids!=[] or asks!=[]:
                        notifications_data[ticket]={'bids':bids,'asks':asks}
                else:
                    notifications_data[ticket]=result_data[ticket]

        else:
            notifications_data=result_data
    pd.DataFrame(data=result_data.values(),index=result_data.keys()).to_json('previous_data')
    if key==1:
        return result_data
    elif key==2:
        return notifications_data
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id,'Вечер в хату')


# создаём форму и указываем поля
class Form(StatesGroup):
    search = State()
    subscribe= State()

#обработка отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe_command(message: types.Message):
    global flag
    flag=False
    await message.reply('Рассылка плотностей отменена')

#Если чел выбрал режим поиск/подписка но передумал и не хочет вводить value
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


#Обработка команды /search + считывание value через состояния
#=======================================================================================================================
@dp.message_handler(commands=['search'])
async def search_command(message: types.Message):
    print('Запрос на поиск ', message.from_user.username,message.from_user.full_name)
    await Form.search.set()
    await message.reply("Введите размер плотности:")


@dp.message_handler(state=Form.search)
async def data_search(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        value = int(message.text)
        data = search_new(value,1)
        await state.finish()
        if data==[]:
            await message.reply("Подходящих плотностей не найдено")
        else:
            for ticket in data:
                text='++++++++++COIN+++++++++++'+ticket+'\n'
                #обработка bids
                text += '\nLONG\n'
                count=0
                for bid in data[ticket]['bids']:
                    count+=1
                    text+=str(count)+') уровень:'+bid[0]+'\n монет на уровне'+bid[0]+'\n'
                text+='\nSHORT*\n'
                count=0
                for ask in data[ticket]['asks']:
                    count+=1
                    text+=str(count)+') уровень:'+bid[0]+'\n монет на уровне'+bid[0]+'\n'
                    await bot.send_message(message.from_user.id,text)
#===================================================================
#Обработка подписки
#=======================================================================================================================
@dp.message_handler(commands=['subscribe'])
async def subscribe_command(message: types.Message):
    print('Запрос на поиск', message.from_user.id, message.from_user.username,message.from_user.first_name)
    await message.reply("Введите размер плотности:")
    await Form.subscribe.set()

@dp.message_handler(state=Form.subscribe)
async def data_search_subscribe(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        f=True
        value=int(message.text)
        await state.finish()
        while f:
            global flag
            f=flag
            await asyncio.sleep(15)
            data = search_new(value,2)
            if data!=[]:
                for ticket in data:
                    text = '++++++++++COIN+++++++++++' + ticket + '\n'
                    # обработка bids
                    text += '\nLONG\n'
                    count = 0
                    for bid in data[ticket]['bids']:
                        count += 1
                        text += str(count) + ') уровень:' + bid[0] + '\n монет на уровне' + bid[0] + '\n'
                    text += '\nSHORT*\n'
                    count = 0
                    for ask in data[ticket]['asks']:
                        count += 1
                        text += str(count) + ') уровень:' + bid[0] + '\n монет на уровне' + bid[0] + '\n'
                        await bot.send_message(message.from_user.id, text)
#=======================================================================================================================
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)












