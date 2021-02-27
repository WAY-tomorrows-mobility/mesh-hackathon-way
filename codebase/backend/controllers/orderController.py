from flask import Flask, render_template, request, jsonify
from cloudant.database import CouchDatabase

order_key = "order_KEY"


def setup(db):
    global order_key

    orders = db.get(order_key)

    if not orders:
        db.create_document({'_id': order_key, 'orders': []}, )


def post_order(db: CouchDatabase):
    order = request.json['order']
    doc = db.get(order_key)
    orders = doc['orders']
    orders.append(order)

    db[order_key] = doc

    return jsonify(order)


def get_orders(db: CouchDatabase):
    doc = db.get(order_key)
    orders = doc['orders']
    # out = [i.__dict__ for i in orders]
    return jsonify(orders)
