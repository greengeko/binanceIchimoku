from datetime import time

from binance import Client
import utils

client = utils.setProfile()
coins = client.get_all_coins_info()

pumpvolume=utils.findPump(client)
      
print(pumpvolume)

#roba per calcolo kijunsen
kijunsen=[]
#daticoin2=[]
maxlist=[]
minlist=[]
s=0

for i in pumpvolume:
  coindata=client.get_historical_klines(i, Client.KLINE_INTERVAL_1HOUR, "26 hour ago UTC")
    # print(coindata)
  s=len(coindata)
  maxlistprov=[]
  minlistprov=[]

  for a in range(len(coindata)):
    maxlistprov.insert(a,coindata[a][2])
    minlistprov.insert(a,coindata[a][3])
  minlist.insert(s, utils.my_min(minlistprov))
  maxlist.insert(s, utils.my_max(maxlistprov)) #s??
  #s=s-1

  print(maxlist)
  print(minlist)

# kijunsen=max+min/2
#risolvere problema arrotondamenti
for b in range(len(pumpvolume)):
  kij=float(maxlist[b])+float(minlist[b])
  kijunsen.insert(b,kij/2)
 # print(len(str(kijunsen[b]))-1)
  kijunStringa=str(kijunsen[b])
  print(kijunStringa)
  print(kijunStringa[len(str(kijunsen[b]))-1])
  if(kijunStringa[len(str(kijunsen[b]))-1]=='5'):
      string_list = list(kijunStringa)
      string_list[len(str(kijunsen[b]))-1] = "0"
      kijunStringa = "".join(string_list)
      kijunsen[b]=float(kijunStringa)
   # kijunsen.insert(b,float(kijunStringa))
  print(kijunsen)  


#Personal account operations
cassa=round(float((client.get_asset_balance("USDT")["free"])))
print(client.get_asset_balance("USDT")["free"])
print("Cassa:"+str(cassa))
#getTot disponibile e diviso per len(pumpVolume)
#crea copia dictionary di pumpvolume[] e kijunsen[]
#if prezzo attuale >*kinjunsen*0.95 allora place kinjunsen order (orderid in lista), altrimenti delete da lista
#when order kinjun è completo place oco order con 5% (oco orderid in lista) delete da lista
#when normal order è canceled delete da lista
currentOrder=[]
  
#for sul pumpvolume
a=0
for c in range(len(pumpvolume)):
# quantity= [usdt/price]
  prezzoatt=client.get_symbol_ticker(symbol=pumpvolume[c])["price"]
  print("prezzoatt:"+str(pumpvolume[c])+" -"+str(prezzoatt))
  if float(prezzoatt)<float(kijunsen[c]) and float(prezzoatt)>float(kijunsen[c]*0.95) :
    prezzobuy=prezzoatt
  else:
    prezzobuy=kijunsen[c]
  print("prezzobuy:"+str(prezzobuy))

    #order BUY
    #sostituire a con c
  currentOrder.insert(a,client.order_limit_buy(symbol=pumpvolume[c],
  quantity=int(0.99*(float(cassa)/len(pumpvolume))/float(prezzoatt)),
  price=str(prezzobuy)))
  a=a+1
  print(str(currentOrder[c]))

#concludi ordini
timeout = 60*60*3 #3h
timeout_start = time.time()
while len(pumpvolume)>0 and time.time() < timeout_start + timeout:
#mettere una pausa
#for
  for d in range(len(pumpvolume)):
    if ((currentOrder[d]["status"]=='FILLED')):
      client.order_oco_sell(symbol=pumpvolume[d],
        quantity=currentOrder[d]["executedQty"],
        price=str(kijunsen[d]*1.05),
        stopPrice=str(kijunsen[d]*0.95),
        stopLimitPrice=str(kijunsen[d]*0.95),
        stopLimitTimeInForce='FOK')
      del kijunsen[d]
      del pumpvolume[d]
      del currentOrder[d]

#delete the orders which in 3h haven't been still FILLED
for y in range(len(currentOrder)):
  client.cancel_order(
  symbol=str(currentOrder[y]["status"]),
  orderId=currentOrder[y]["orderId"]
  )
