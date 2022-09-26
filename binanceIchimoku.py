from datetime import time
from time import sleep

from binance import Client
import utils

client = utils.setProfile()
coins = client.get_all_coins_info()

pumpvolume = utils.findPump(client)
print("The coin pairs with a pump in last hours :", pumpvolume)
kijunsen = utils.getKijunsen(pumpvolume)



# Personal account operations
cassa = round(float((client.get_asset_balance("USDT")["free"])))
print("Cassa:" + client.get_asset_balance("USDT")["free"])
# getTot disponibile e diviso per len(pumpVolume)
# crea copia dictionary di pumpvolume[] e kijunsen[]
# if prezzo attuale >*kinjunsen*0.95 allora place kinjunsen order (orderid in lista), altrimenti delete da lista
# when order kinjun è completo place oco order con 5% (oco orderid in lista) delete da lista
# when normal order è canceled delete da lista
currentOrder = []

# for sul pumpvolume
for c in range(len(pumpvolume)):
    # quantity= [usdt/price]
    prezzoatt = client.get_symbol_ticker(symbol=pumpvolume[c])["price"]
    if int(float(client.get_asset_balance("USDT")["free"])) > 50:

        precision = client.get_symbol_info(symbol=pumpvolume[c])["quotePrecision"]-2
        print(precision)
        prezzoatt = "{:0.0{}f}".format(float(prezzoatt), precision)
        print("prezzoatt:" + str(pumpvolume[c]) + " -" + str(prezzoatt))
        if float(kijunsen[c]) > float(prezzoatt) > float(kijunsen[c] * 0.95):
             prezzobuy = prezzoatt
        else:
            kijunsen[c] = "{:0.0{}f}".format(kijunsen[c], precision)
            prezzobuy = kijunsen[c]
        print("prezzobuy:" + str(prezzobuy))

        # order BUY
    quantity = int(0.99 * (float(cassa) / len(pumpvolume)) / float(prezzoatt))
    if float(cassa) / len(pumpvolume) < 50:
        quantity = int(0.99 * 50 / float(prezzoatt))

    currentOrder.insert(c, client.order_limit_buy(symbol=pumpvolume[c],
                                                  quantity=quantity,
                                                  price=str(prezzobuy)))
    # a=a+1
    print(str(currentOrder[c]))

# concludi ordini
timeout = 60 * 60 * 3  # 3h
timeout_start = time()
while len(pumpvolume) > 0 and time() < timeout_start + timeout:
    # mettere una pausa
    # for
    for d in range(len(pumpvolume)):
        if currentOrder[d]["status"] == 'FILLED':
            client.order_oco_sell(symbol=pumpvolume[d],
                                  quantity=currentOrder[d]["executedQty"],
                                  price=str(kijunsen[d] * 1.05),
                                  stopPrice=str(kijunsen[d] * 0.95),
                                  stopLimitPrice=str(kijunsen[d] * 0.95),
                                  stopLimitTimeInForce='FOK')
            del kijunsen[d]
            del pumpvolume[d]
            del currentOrder[d]
    sleep(10)

# delete the orders which in 3h haven't been still FILLED
for y in range(len(currentOrder)):
    client.cancel_order(
        symbol=str(currentOrder[y]["status"]),
        orderId=currentOrder[y]["orderId"]
    )