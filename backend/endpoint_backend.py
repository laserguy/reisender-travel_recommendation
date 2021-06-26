from flask.wrappers import Response
import datalayerbackend
from flask import Flask, request, jsonify

app = Flask(__name__)
datalayerbackend.init()

@app.route("/api/users/register", methods=['POST'])
def register():
    data = request.get_json()
    u = datalayerbackend.register(data['username'],data['password'])
    return jsonify(u)


@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()
    u = datalayerbackend.login(data['username'],data['password'])
    return jsonify(u)


@app.route('/api/users/features', methods=['POST', 'GET'])
def features():
    if request.method == 'POST':
        data = request.get_json()
        datalayerbackend.passFeatureList(data['user_id'], data['features'])
        return jsonify({})

    features = datalayerbackend.getFeatureList()
    return jsonify(features)


@app.route('/api/users/wishlist', methods=['GET', 'DELETE', 'PUT'])
def wishlist():
    if request.method == "GET":
        data = request.args.get('user_id')
        wl = datalayerbackend.wishListGet(data)
        return jsonify(wl)

    if request.method == "DELETE":
        data = request.args
        datalayerbackend.wishListRemove(data['user_id'], data['place_id'])
        return Response(status=200)

    if request.method == "PUT":
        data = request.get_json()
        wl = datalayerbackend.wishListAdd(data['user_id'], data['place_id'])
        return jsonify(wl)

    return Response(jsonify({"error": 'unknown method'}), status=400)


@app.route('/api/users/visited', methods=['GET', 'DELETE', 'PUT'])
def visited():
    if request.method == "GET":
        data = request.args.get('user_id')
        wl = datalayerbackend.visitedListGet(data)
        return jsonify(wl)

    if request.method == "DELETE":
        data = request.args
        datalayerbackend.visitedListRemove(data['user_id'], data['place_id'])
        return Response(status=200)

    if request.method == "PUT":
        data = request.get_json()
        wl = datalayerbackend.visitedListAdd(data['user_id'], data['place_id'])
        return jsonify({})

    return Response(jsonify({"error": 'unknown method'}), status=400)


@app.route('/api/users/recommend/<user_id>', methods=['GET'])
def recommend(user_id):
    places = datalayerbackend.recommend(user_id)
    return jsonify(places)


@app.route('/api/search', methods=['GET'])
def search():
    q = request.args.get('q')
    places = datalayerbackend.search(q)
    return jsonify(places)


if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app
