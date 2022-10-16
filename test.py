import utils
#from binanceIchimoku import client
from utils import formatForBinance


def formatForBinance_test():
    print(formatForBinance('1.00000', '947.237'))
    assert formatForBinance('1.00000', '947.237') == '947'

def formatForBinance_test2():
    print(formatForBinance('100.2508', '947.237'))
    assert formatForBinance('100.2508', '947.237') == '947.2370'

#def findPump_test():
 #   print(utils.findPump(client))


formatForBinance_test()
formatForBinance_test2()
#findPump_test()
print("Everything passed")
