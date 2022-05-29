from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from operator import itemgetter
import re
import timer
api_key='insertyourapikey'
api_secret='insertyourapisecret'
client = Client(api_key, api_secret)

coins = client.get_all_coins_info()

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
  api_key='insertApiKeyHere'
  api_secret='insertApiSecretHere'
  client = Client(api_key, api_secret)
  coins = client.get_all_coins_info()
  #all pairs
  tickers=client.get_all_tickers()
  pairs=[]
  for i in range(len(tickers)):
    if ((re.fullmatch(".*USDT$",tickers[i]["symbol"])) ): #or (re.fullmatch(".*BTC$",tickers[i]["symbol"]))
      pairs.append(tickers[i]["symbol"])


#all pairs
tickers=client.get_all_tickers()
pairs=[]
for i in range(len(tickers)):
  if ((re.fullmatch(".*USDT$",tickers[i]["symbol"])) ): #or (re.fullmatch(".*BTC$",tickers[i]["symbol"]))
    pairs.append(tickers[i]["symbol"])


#print(pairs)
while(True):
  pumpvolume=[]
  pos=0
  for i in pairs:
    #print(i)
    daticoin=client.get_historical_klines(i, Client.KLINE_INTERVAL_1HOUR, "6 hour ago UTC")
    #print(client.get_historical_klines(i, Client.KLINE_INTERVAL_1HOUR, "1 day ago UTC"))
    for y in range(len(daticoin)-1):
      if (5*(float(daticoin[y][5]))<(float(daticoin[y+1][5]))) and 1.10*(float(daticoin[y][2]))<(float(daticoin[y+1][2]))  : 
         if int(y+2)!=len(daticoin):
          pumpvolume.insert(pos,i)
          pos=pos+1
         print(str(i) +" "+str(5-int(y+2)) + "h fa" )
      
print(pumpvolume)

#roba per calcolo kijunsen
  kijunsen=[]
  daticoin2=[]

  maxlist=[]

  minlist=[]

  s=0
  for i in pumpvolume:
    #print(i)
    #print(client.get_ticker(26))
    daticoin2=client.get_historical_klines(i, Client.KLINE_INTERVAL_1HOUR, "26 hour ago UTC")
    print(daticoin2)
    s=len(daticoin2)
    maxlistprov=[]
    minlistprov=[]
    for a in range(len(daticoin2)):
      maxlistprov.insert(a,daticoin2[a][2])
      minlistprov.insert(a,daticoin2[a][3])
    minlist.insert(s, my_min(minlistprov))
    maxlist.insert(s, my_max(maxlistprov))
    s=s-1
  print(maxlist) 
  print(minlist)
  for b in range(len(pumpvolume)):
    kij=float(maxlist[b])+float(minlist[b])
  #pari dispari
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

  # kijunsen=max+min/2

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
  
    currentOrder.insert(a,client.order_limit_buy(symbol=pumpvolume[c], 
      quantity=int(0.99*(float(cassa)/len(pumpvolume))/float(prezzoatt)), 
      price=str(prezzobuy)))
    a=a+1
    print(str(currentOrder[c]))
  
  timeout = 60*60*3
  timeout_start = time.time()
  while len(pumpvolume)>0 and time.time() < timeout_start + timeout:
    
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

  for y in range(len(currentOrder)):
    client.cancel_order(
        symbol=str(currentOrder[y]["status"]),
        orderId=currentOrder[y]["orderId"]           
    )   
