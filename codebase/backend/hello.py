# from cloudant.client import Cloudant

from flask import Flask, render_template, request, jsonify
import atexit
import os
import json
from controllers import userController, orderController, adminController
from flask_cors import CORS
import db_Setup

app = Flask(__name__, static_url_path='')
CORS(app)

db = db_Setup.Setup()
orderController.setup(db)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if db_Setup.client:
        return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])


@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    data = {'name': user}
    if db_Setup.client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)


@app.route('/api/user', methods=['POST'])
def post_user():
    return userController.post_user(db)


@app.route('/api/user', methods=['GET'])
def get_all_users():
    return userController.get_all_users(db)


@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    return userController.get_user(db, user_id)


@app.route('/api/order', methods=['POST'])
def post_order():
    return orderController.post_order(db)


@app.route('/api/order', methods=['GET'])
def get_all_orders():
    return orderController.get_orders(db)


@app.route('/admin', methods=['GET'])
def calc_orders():
    return adminController.get_all(db, n=3)


@app.route('/admin/<kluster_n>', methods=['GET'])
def calc_orders_forK(kluster_n):
    return adminController.get_all(db, int(kluster_n))


@atexit.register
def shutdown():
    if db_Setup.client:
        db_Setup.Close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
