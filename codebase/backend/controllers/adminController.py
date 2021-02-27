from flask import Flask, render_template, request, jsonify
from cloudant.database import CouchDatabase
import core.entry as core

from .orderController import order_key


def get_all(db, n:int):
    doc = db.get(order_key)

    orders = doc['orders']
    doc['orders'] = []
    db[order_key] = doc

    result = core.start(orders, n, draw=False)

    return jsonify(result)
