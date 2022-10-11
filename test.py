import utils
from binanceIchimoku import client
from utils import formatForBinance


def formatForBinance_test():
    print(formatForBinance('0.24100000', '0.237'))
    assert formatForBinance('0.24100000', '0.237') == '0.237'


def findPump_test():
    print(utils.findPump(client))


if __name__ == "__main__":
    formatForBinance_test()
    findPump_test()
    print("Everything passed")
