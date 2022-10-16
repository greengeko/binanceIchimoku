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
        if re.fullmatch(".*BTC$", tickers[i]["symbol"]):  # or (re.fullmatch(".*USDT$",tickers[i]["symbol"]))
            pairs.append(tickers[i]["symbol"])

    pumpvolume = []
    pos = 0
    for i in pairs:
        #:return: list of OHLCV values, useful:
        # 1:Open, 2:High, 3:Low, 4:Close, 5:Volume
        daticoin = client.get_historical_klines(i, Client.KLINE_INTERVAL_1HOUR, "4 hour ago UTC")
        for y in range(len(daticoin) - 1):  # TODO:xk -1?
            # Volume at least 5times greater than the h before && at least 10% higher max than the h before
            # && the tail high is not greater than candle closure more than 5%
            #&& the tail is not longer than the candle itself
            if 5 * float(daticoin[y][5]) < float(daticoin[y + 1][5]) and 1.10 * float(daticoin[y][2]) < float(
                    daticoin[y + 1][2]) and float(daticoin[y+1][2])-float(daticoin[y+1][4]) < float(daticoin[y+1][4])-float(daticoin[y+1][1]) :
                if int(y + 2) != len(daticoin) and i not in pumpvolume:  # discard the duplicates
                    pumpvolume.insert(pos, i)
                    pos = pos + 1
                print(str(i) + " " + str(4 - int(y + 2)) + "h ago")
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
            maxlistprov.insert(a, float(coindata[a][2]))  # high
            minlistprov.insert(a, float(coindata[a][3]))  # low
        minlist.insert(s, my_min(minlistprov))
        maxlist.insert(s, my_max(maxlistprov))
        s = s + 1
    print("maxlist: ")
    print(maxlist)
    print("minlist: ")
    print(minlist)
    # kijunsen=max+min/2
    for b in range(len(maxlist)):
        kij = float(maxlist[b]) + float(minlist[b])
        kij = convert_scientific_to_decimal(kij / 2)
        kijunsen.insert(b, kij)
    print("kijunsen: ")
    print(kijunsen)
    return kijunsen


def formatForBinance(number, newNumber):
    #delete extra zeros
    while number[-1] == '0':
        number = number[0:-1]
    #fix the decimal part
    digits = number[::-1].find('.')
    newNumber = f"{newNumber}"
    digitsNew = newNumber[::-1].find('.')
    if digitsNew > digits:
        newNumber = newNumber[0:-(digitsNew - digits)]
    if digitsNew < digits:
        newNumber = newNumber.ljust(digits-digitsNew + len(newNumber), '0')
    #delete the point if not necessary
    if newNumber[-1]=='.':
        newNumber = newNumber[0:-1]

    return f"{newNumber}"


def convert_scientific_to_decimal(num):
    if 'e' in str(num):
        return "{:.15f}".format(float(str(num)))
    else:
        return str(num)


def clean(client,currentOrder):
    for y in range(len(currentOrder)):
        client.cancel_order(
            symbol=str(currentOrder[y]["status"]),
            orderId=currentOrder[y]["orderId"]
        )
