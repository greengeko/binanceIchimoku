import utils
from utils import formatForBinance

client = utils.setProfile()
def formatForBinance_test():
    print(formatForBinance('1.00000', '947.237'))
    assert formatForBinance('1.00000', '947.237') == '947'

def formatForBinance_test2():
    print(formatForBinance('100.2508', '947.237'))
    assert formatForBinance('100.2508', '947.237') == '947.2370'

def precision_test(client):
    precision = client.get_symbol_info(symbol='ADABTC')["filters"][0]["tickSize"]
    print('precision:', precision)

#def findPump_test():
 #   print(utils.findPump(client))


#formatForBinance_test()
#formatForBinance_test2()
precision_test(client)
#findPump_test()
print("Everything passed")
