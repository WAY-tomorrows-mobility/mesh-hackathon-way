from flask import Flask, render_template, request, jsonify


def post_user(db):
    user = request.json['name']
    data = {'name': user}
    if db:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)


def get_all_users(db):
    if db:
        return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])


def get_user(db, user_id):
    if db:
        user = db[user_id]
        if user:
            return jsonify(user)
        else:
            return jsonify({})
    else:
        print('No database')
        return jsonify([])
