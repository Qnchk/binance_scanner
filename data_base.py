import websocket,json
import multiprocessing
import pandas as pd
import time
#просто функция которая выгружает в список data инфу по монете ticket
def search(mini_pool,data):
    for ticket in mini_pool:
        symbol = ticket
        levels = '20'
        interval='5m'
        ws = websocket.WebSocket()
        #big orders search
        socket2= f'wss://stream.binance.com:9443/ws/{symbol}@depth{levels}@100ms'
        ws.connect(socket2)
        json_message = json.loads(ws.recv())
        ws.close()
        bids = json_message['bids']
        asks = json_message['asks']
        bids.sort(key=lambda x:float(x[1]),reverse=True)
        asks.sort(key=lambda x:float(x[1]),reverse=True)
        data[ticket]= {'bids':bids,'asks':asks}

def processesed():
    while True:
        start_time = time.time()
        file = open('data.txt')
        pool = list(file.read().split())
        data = multiprocessing.Manager().dict() #список для многопотока
        processes = []
        mini_pool1=[]
        mini_pool2=[]
        mini_pool3=[]
        mini_pool4=[]
        mini_pool5=[]
        mini_pool6=[]
        mini_pool7=[]
        mini_pool8=[]
        mini_pool9=[]
        mini_pool10=[]
        mini_pool11=[]
        mini_pool12=[]
        mini_pool13=[]
        mini_pool14=[]
        mini_pool15=[]
        mini_pool16=[]
        mini_pool17=[]
        mini_pool18=[]
        mini_pool19=[]
        mini_pool20=[]
        mini_pool21=[]
        mini_pool22=[]
        mini_pool23=[]
        mini_pool24=[]
        mini_pool25=[]
        mini_pool26=[]
        for i in range(5):
            mini_pool1.append(pool[26*i].lower())
            mini_pool2.append(pool[26*i+1].lower())
            mini_pool3.append(pool[26*i+2].lower())
            mini_pool4.append(pool[26*i+3].lower())
            mini_pool5.append(pool[26*i+4].lower())
            mini_pool6.append(pool[26*i+5].lower())
            mini_pool7.append(pool[26*i+6].lower())
            mini_pool8.append(pool[26*i+7].lower())
            mini_pool9.append(pool[26*i+8].lower())
            mini_pool10.append(pool[26*i+9].lower())
            mini_pool11.append(pool[26*i+10].lower())
            mini_pool12.append(pool[26*i+11].lower())
            mini_pool13.append(pool[26*i+12].lower())
            mini_pool14.append(pool[26*i+13].lower())
            mini_pool15.append(pool[26*i+14].lower())
            mini_pool16.append(pool[26*i+15].lower())
            mini_pool17.append(pool[26*i+16].lower())
            mini_pool18.append(pool[26*i+17].lower())
            mini_pool19.append(pool[26*i+18].lower())
            mini_pool20.append(pool[26*i+19].lower())
            mini_pool21.append(pool[26*i+20].lower())
            mini_pool22.append(pool[26*i+21].lower())
            mini_pool23.append(pool[26*i+22].lower())
            mini_pool24.append(pool[26*i+23].lower())
            mini_pool25.append(pool[26*i+24].lower())
            mini_pool26.append(pool[26*i+25].lower())

        p1 =multiprocessing.Process(target=search,args=(mini_pool1,data))
        p2 =multiprocessing.Process(target=search,args=(mini_pool2,data))
        p3 =multiprocessing.Process(target=search,args=(mini_pool3,data))
        p4 =multiprocessing.Process(target=search,args=(mini_pool4,data))
        p5 =multiprocessing.Process(target=search,args=(mini_pool5,data))
        p6 =multiprocessing.Process(target=search,args=(mini_pool6,data))
        p7 =multiprocessing.Process(target=search,args=(mini_pool7,data))
        p8 =multiprocessing.Process(target=search,args=(mini_pool8,data))
        p9 =multiprocessing.Process(target=search,args=(mini_pool9,data))
        p10 =multiprocessing.Process(target=search,args=(mini_pool10,data))
        p11 =multiprocessing.Process(target=search,args=(mini_pool11,data))
        p12 =multiprocessing.Process(target=search,args=(mini_pool12,data))
        p13 =multiprocessing.Process(target=search,args=(mini_pool13,data))
        p14 =multiprocessing.Process(target=search,args=(mini_pool14,data))
        p15 =multiprocessing.Process(target=search,args=(mini_pool15,data))
        p16 =multiprocessing.Process(target=search,args=(mini_pool16,data))
        p17 =multiprocessing.Process(target=search,args=(mini_pool17,data))
        p18 =multiprocessing.Process(target=search,args=(mini_pool18,data))
        p19 =multiprocessing.Process(target=search,args=(mini_pool19,data))
        p20 =multiprocessing.Process(target=search,args=(mini_pool20,data))
        p21 =multiprocessing.Process(target=search,args=(mini_pool21,data))
        p22 =multiprocessing.Process(target=search,args=(mini_pool22,data))
        p23 =multiprocessing.Process(target=search,args=(mini_pool23,data))
        p24 =multiprocessing.Process(target=search,args=(mini_pool24,data))
        p25 =multiprocessing.Process(target=search,args=(mini_pool25,data))
        p26 =multiprocessing.Process(target=search,args=(mini_pool26,data))
        processes.append(p1)
        processes.append(p2)
        processes.append(p3)
        processes.append(p4)
        processes.append(p5)
        processes.append(p6)
        processes.append(p7)
        processes.append(p8)
        processes.append(p9)
        processes.append(p10)
        processes.append(p11)
        processes.append(p12)
        processes.append(p13)
        processes.append(p14)
        processes.append(p15)
        processes.append(p16)
        processes.append(p17)
        processes.append(p18)
        processes.append(p19)
        processes.append(p20)
        processes.append(p21)
        processes.append(p22)
        processes.append(p23)
        processes.append(p24)
        processes.append(p25)
        processes.append(p26)
        for p in processes:
            p.start()
        #ожидаем завершения потоков
        for p in processes:
            p.join()
        #обрабатываем полученные данные и записываем в json файл
        data_frame = pd.DataFrame(data=data.values(),index=data.keys())
        print(data_frame)
        data_frame.to_json('result')
        print(time.time() - start_time)


if __name__ == '__main__':
    processesed()



