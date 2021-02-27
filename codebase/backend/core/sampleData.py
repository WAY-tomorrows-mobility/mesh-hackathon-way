from random import randint, random
import copy


def get_data():
    dest = (10, 10)
    startPoint = (0, 0)
    n = 100

    orders = []

    nH = int(n / 2)

    stucture = {"location": "",
                "destiny": "",
                "options": {
                    # Higher values for more importance
                    "ecological": 0.5,
                    "time": 0.1,
                    "comfort": 0.9
                }}

    for j in range(n):
        x_step = randint(0, n)
        y_step = randint(0, n)

        p = (startPoint[0] + x_step, startPoint[1] + y_step)
        new_o = copy.deepcopy(stucture)

        new_o["location"] = p
        new_o["destiny"] = dest
        new_o["options"]["ecological"] = random() + x_step / n
        new_o["options"]["time"] = random()+ y_step / n
        new_o["options"]["comfort"] = random()

        orders.append(new_o)

    return orders
