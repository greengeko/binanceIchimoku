from binance import Client
import re

import api

api_key = api.api_key  # 'insert here'
api_secret = api.api_secret  # 'insert here'


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
                    float(daticoin[y + 1][2]) and float(daticoin[y][4]) < 1.50 * float(daticoin[y][2])):
                if int(y + 2) != len(daticoin) and i not in pumpvolume:  # ??
                    pumpvolume.insert(pos, i)
                    pos = pos + 1
                print(str(i) + " " + str(6 - int(y + 2)) + "h fa")
    return pumpvolume


def getKijunsen(client, pumpvolume):
    kijunsen = []
    maxlist = []
    minlist = []
    s = 0
    for i in pumpvolume:
        coindata = client.get_historical_klines(i, Client.KLINE_INTERVAL_1HOUR, "26 hour ago UTC")
        # print(coindata)
    maxlistprov = []
    minlistprov = []
    for a in range(len(coindata)):
        maxlistprov.insert(a, coindata[a][2])  # high
        minlistprov.insert(a, coindata[a][3])  # low
    minlist.insert(s, my_min(minlistprov))
    maxlist.insert(s, my_max(maxlistprov))
    s = s + 1
    print(maxlist)
    print(minlist)
    # kijunsen=max+min/2
    # risolvere problema arrotondamenti
    for b in range(len(pumpvolume)):
        kij = float(maxlist[b]) + float(minlist[b])
        kijunsen.insert(b, kij / 2)
    print(kijunsen)
    return kijunsen
