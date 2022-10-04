from utils import aggiusta


def aggiusta_test():
    print(aggiusta('0.045000', '0.239930300379'))
    assert aggiusta('0.045000', '0.239930300379')=='0.239'


if __name__ == "__main__":
    aggiusta_test()
    print("Everything passed")
