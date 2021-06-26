import wordembeddings
import datalayer


def init(places, features):
    try:
        Embedder = wordembeddings.WordEmbedder.getInstance()
        embedding_dict = Embedder.initML(places,features)
        pl_dict = embedding_dict['places']
        ft_dict = embedding_dict['features']
        fl_dict = embedding_dict['failures']

        DL_dict = {}
        DL_dict['places'] = pl_dict
        DL_dict['features'] = ft_dict
        datalayer.initDL(DL_dict)
        return fl_dict     #return the places/features for which we got disambugity error
    except Exception as e:
        return {'error': str(e)}

def getRecommendations(user_id, visited_places, count):
    try:
        user_info = datalayer.getUser(user_id)
        user_vector = user_info['word_vector']
        wish_vector = user_info['wish_vector'] 
        places = datalayer.getAllPlaces()
        Embedder = wordembeddings.WordEmbedder.getInstance()
        recommended_places = Embedder.getRecommendations(user_vector, wish_vector, places, visited_places, count)
        return recommended_places
    except Exception as e:
        return {'error': str(e)}


def updateUserEmbeddings(user_id, place_id):
    try:
        user_info = datalayer.getUser(user_id)
        user_vector = user_info['word_vector']
        avg_num = user_info['avg_num']
        place_vector = datalayer.getPlace(place_id)
        Embedder = wordembeddings.WordEmbedder.getInstance()

        wish_embedding = Embedder.updateUserEmbeddings(avg_num, user_vector, place_vector)
        datalayer.updateUser(user_id, avg_num, wish_embedding)
    except Exception as e:
        return {'error': str(e)}

def addUser(user_id, feature_ids):
    try:
        feat_count = len(feature_ids)
        feature_vectors= datalayer.getFeatures(feature_ids)
        Embedder = wordembeddings.WordEmbedder.getInstance()
        user_embedding = Embedder.calcUserEmbedding(feature_vectors)
        print(user_embedding)
        datalayer.addUser(user_id,feat_count, user_embedding)
    except Exception as e:
        return {'error': str(e)}

def removeUser(user_id):
    try:
        datalayer.removeUser(user_id)
    except Exception as e:
        return {'error': str(e)}

def addFeature(feature_id, feature_name):
    try:
        Embedder = wordembeddings.WordEmbedder.getInstance()
        feature_embedding = Embedder.calcFeatureEmbedding(feature_name)
        datalayer.addFeature(feature_id, feature_embedding)
    except Exception as e:
        return {'error': str(e)}

def removeFeature(feature_id):
    try:
        datalayer.removeFeature(feature_id)
    except Exception as e:
        return {'error': str(e)}

def addPlace(place_id, place_name):
    try:
        Embedder = wordembeddings.WordEmbedder.getInstance()
        place_embedding = Embedder.calcPlaceEmbedding(place_name)
        datalayer.addPlace(place_id, place_embedding)
    except Exception as e:
        return {'error': str(e)}

def removePlace(place_id):
    try:
        datalayer.removePlace(place_id)
    except Exception as e:
        return {'error': str(e)}