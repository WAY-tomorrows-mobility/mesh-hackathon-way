class Order(object):
    location = ()
    destiny = ()
    options = {
        # Higher values for more importance
        "ecological": 0.5,
        "time": 0.1,
        "comfort": 0.9
    }
