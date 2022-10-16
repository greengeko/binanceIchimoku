import utils
from datetime import time as time_
from time import sleep

client = utils.setProfile()
coins = client.get_all_coins_info()

pumpvolume = utils.findPump(client)
if len(pumpvolume) == 0:
    print("Oh no, no pumps in the last hours :'( ")
    exit(0)
else:
    print("The coin pairs with a pump in last hours :", pumpvolume)

kijunsen = utils.getKijunsen(client, pumpvolume)

# Personal account operations
print("Cassa: " + client.get_asset_balance("BTC")["free"])

# TODO: creare uno schema
# getTot disponibile e diviso per len(pumpVolume)
# if prezzo attuale >*kinjunsen*0.95 allora place kinjunsen order (orderid in lista), altrimenti delete da lista
# when order kinjun è completo place oco order con 5% (oco orderid in lista) delete da lista
# when normal order è canceled delete da lista
currentOrder = []

# for sul pumpvolume
for c in range(len(pumpvolume)):
    # quantity= [coin/price]
    prezzoatt = client.get_symbol_ticker(symbol=pumpvolume[c])["price"]
    if float(client.get_asset_balance("BTC")["free"]) > 0.002:  # around $40
        print("prezzoatt:" + str(pumpvolume[c]) + " -" + str(prezzoatt))
        if float(kijunsen[c]) > float(prezzoatt) > float(kijunsen[c]) * 0.96:
            prezzobuy = prezzoatt
        elif float(prezzoatt) > float(kijunsen[c]) * 0.96 :
            prezzobuy = utils.formatForBinance(str(prezzoatt), str(kijunsen[c])) # meglio con ticksize
        else : break
        print("prezzobuy:" + str(prezzobuy))

        # order BUY
        stepsize = client.get_symbol_info(symbol=pumpvolume[c])["filters"][2]["stepSize"]
        print("stepsize " + str(stepsize))
        quantity = utils.formatForBinance(stepsize, (0.002 / float(prezzoatt)))
        print(str(quantity))
        try:
            currentOrder.insert(c, client.order_limit_buy(symbol=pumpvolume[c],
                                                          quantity=quantity,
                                                          price=str(prezzobuy)))
        except IOError as err:
            print("Order error: {0}".format(err))
        print(str(currentOrder[c]))

# oco orders

#startTime = time_.time()

while len(pumpvolume) > 0 :#and time_.time() - startTime < 10800:

    for d in range(len(pumpvolume)):
        if currentOrder[d]["status"] == 'FILLED':
            try:
                client.order_oco_sell(symbol=pumpvolume[d],
                                      quantity=currentOrder[d]["executedQty"],
                                      price=utils.formatForBinance(currentOrder[d]["price"], str(kijunsen[d] * 1.04)),
                                      stopPrice=utils.formatForBinance(currentOrder[d]["price"],
                                                                       str(kijunsen[d] * 0.96)),
                                      stopLimitPrice=utils.formatForBinance(currentOrder[d]["price"],
                                                                            str(kijunsen[d] * 0.96)),
                                      stopLimitTimeInForce='FOK')
            except IOError as err:
                print("OCO order error: {0}".format(err))
            del kijunsen[d]
            del pumpvolume[d]
            del currentOrder[d]
    sleep(300)

    # delete the orders which in 3h haven't been still FILLED
utils.clean(client, currentOrder)
