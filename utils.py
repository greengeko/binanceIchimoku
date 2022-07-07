from binance import Client
import re

api_key = 'insert'
api_secret = 'insert'


def my_max(sequence):
    if not sequence:
        raise ValueError('empty sequence')
    maximum = sequence[0]
    for item in sequence:
        if item > maximum:
            maximum = item
    return maximum


def my_min(sequence):
    if not sequence:
        raise ValueError('empty sequence')
    minimum = sequence[0]
    for item in sequence:
        if item < minimum:
            minimum = item
    return minimum


def setProfile():
    client = Client(api_key, api_secret)
    return client


def findPump(client):
    pairs = []
    tickers = client.get_all_tickers()
    for i in range(len(tickers)):
        if re.fullmatch(".*USDT$", tickers[i]["symbol"]):  # or (re.fullmatch(".*BTC$",tickers[i]["symbol"]))
            pairs.append(tickers[i]["symbol"])

    pumpvolume = []
    pos = 0
    for i in pairs:
        # print(i)
        daticoin = client.get_historical_klines(i, Client.KLINE_INTERVAL_1HOUR, "6 hour ago UTC")
        for y in range(len(daticoin) - 1):
            if (5 * (float(daticoin[y][5])) < (float(daticoin[y + 1][5]))) and 1.10 * (float(daticoin[y][2])) < (
            float(daticoin[y + 1][2])):
                if int(y + 2) != len(daticoin): #??
                    pumpvolume.insert(pos, i)
                    pos = pos + 1
                print(str(i) + " " + str(5 - int(y + 2)) + "h fa")
    return pumpvolume
