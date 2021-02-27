from core import sampleData
import core.entry as core

if __name__ == '__main__':
    orders = sampleData.get_data()

    print(core.start(orders, 4, draw=True))
