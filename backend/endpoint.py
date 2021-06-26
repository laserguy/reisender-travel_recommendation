from flask import Flask
from flask import request
from flask_restful import Resource, Api, reqparse
app = Flask(__name__)
api = Api(app)

import orchestrator


# The Init should be called only once
# It will be a post request, as backend will have to send info (places list<name><id> dict) to the ML model
# And backend also need to send the feature list (<feature_id><feature_name> dict)
# Returns the list of features/places for which wiki was disambiguous(could not inserted into the database)
class Init(Resource):
    def post(self):
        try:
            
            data = request.get_json()
            #print(data['places'])
            
            places = {}
            features={}

            for pl_dict in data['places']:
                places[pl_dict['id']] = pl_dict['place_name']

            for ft_dict in data['features']:
                features[ft_dict['id']] = ft_dict['feature_name']

            return  orchestrator.init(places, features)

        except Exception as e:
            return {'error': str(e)}

# class for the recommendation
# call with <user_id><count>   # give the count of recommendations required
class Recommend(Resource):
    def get(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', required=True)
            parser.add_argument('count', required=True)

            args = parser.parse_args()
            user_id = args['user_id']
            count = args['count']

            return orchestrator.getRecommendations(user_id,count)

        except Exception as e:
            return {'error': str(e)}
    
class Users(Resource):
    # updateUserEmbeddings
    # parameters = <user_id><place_id>
    def put(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', required=True)
            parser.add_argument('place_id', required=True)

            args = parser.parse_args()
            user_id = args['user_id']
            place_id = args['place_id']

            print(orchestrator.updateUserEmbeddings(user_id, place_id))

        except Exception as e:
            return {'error': str(e)}
    # addUser 
    # parameters = <user_id><feature_ids>
    def post(self):
        try:
            data = request.get_json()
            for user in data['user']:
                user_id = user['id']
                feature_ids = user['feature_ids']

            orchestrator.addUser(user_id, feature_ids)

        except Exception as e:
            return {'error': str(e)}
    # removeUser
    # parameters = <user_id>
    def delete(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', required=True)

            args = parser.parse_args()
            user_id = args['user_id']

            orchestrator.removeUser(user_id)

        except Exception as e:
            return {'error': str(e)}
    

class Feature(Resource):
    # addFeature
    # parameters = <feature_id><feature_name>
    def put(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('feature_id', required=True)
            parser.add_argument('feature_name', required=True)

            args = parser.parse_args()
            feature_id = args['feature_id']
            feature_name = args['feature_name']

            orchestrator.addFeature(feature_id, feature_name)

        except Exception as e:
            return {'error': str(e)}
    # removeFeature
    # parameters = <feature_id>
    def delete(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('feature_id', required=True)

            args = parser.parse_args()
            feature_id = args['feature_id']

            orchestrator.removeFeature(feature_id)

        except Exception as e:
            return {'error': str(e)}

class Place(Resource):
    # addPlace
    # parameters = <place_id><place_name>
    def put(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('place_id', required=True)
            parser.add_argument('place_name', required=True)

            args = parser.parse_args()
            place_id = args['place_id']
            place_name = args['place_name']

            orchestrator.addPlace(place_id, place_name)

        except Exception as e:
            return {'error': str(e)}
    # removePlace
    # parameters = <place_id>
    def delete(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('place_id', required=True)

            args = parser.parse_args()
            place_id = args['place_id']

            orchestrator.removePlace(place_id)

        except Exception as e:
            return {'error': str(e)}

api.add_resource(Init, '/init')  # init is the entry point to set up the DB first time (server startup)
api.add_resource(Recommend, '/getRecommendations')
api.add_resource(Users, '/users')
# These two are for adding more features and places and won't be called due to user's activity
api.add_resource(Feature, '/feature')
api.add_resource(Place, '/place')


if __name__ == '__main__':
    app.run()  # run our Flask app