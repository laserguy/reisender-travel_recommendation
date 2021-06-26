import sqlhelper
import numpy as np

def initDL(embedding_dict):
    try:
        print("Inside data layer")
        places_dict = embedding_dict['places']
        features_dict = embedding_dict['features']

        #create tables part is manually right now, If init is done with no tables then we will get an exceptipon.
        dbcon = sqlhelper.connectDB()
        if(sqlhelper.checkTableExists(dbcon, 'user_embeddings') == False):
            raise Exception

        # dbcon object is passed in case of it is called from initDL, if it gets called outside this function, then "" (empty string)
        # has to be passed
        for key in places_dict:
            addPlaceInternal(dbcon, key,places_dict[key])
        for key in features_dict:
            addFeatureInternal(dbcon, key,features_dict[key])

        dbcon.commit()
        dbcon.close()
    except Exception as e:
            return {'error': str(e)}

def addUser(user_id,feat_count,user_embedding):
   try:
       element_dict = {}
       element_dict['user_id'] = user_id
       element_dict['avg_num'] = feat_count
       element_dict['word_vector'] = sqlhelper.serializedata(user_embedding)
       sqlhelper.insert("",'user_embeddings',element_dict)
   except Exception as e:
        return {'error': str(e)}

def getUser(user_id):
    try:
       user_info = sqlhelper.select(user_id, 'user_id', 'user_embeddings')
       for row in user_info:
           id = row[0]
           avg_num = row[1]
           word_vector = sqlhelper.deserializedata(row[2])
           if row[3] == None or row[3] == '':
               wish_vector = np.array(['0'])
           else:
               wish_vector = sqlhelper.deserializedata(row[3])
        
       if int(user_id) == int(id):
            return {'user_id':user_id, 'avg_num':avg_num, 'word_vector': word_vector, 'wish_vector': wish_vector}
       else:
           raise Exception
    except Exception as e:
        print("In exception here")
        return {'error': str(e)}

def updateUser(user_id, avg_num, wish_embedding):
   try:
       element_dict = {}
       element_dict['user_id'] = user_id
       element_dict['avg_num'] = avg_num + 1
       element_dict['wish_vector'] = sqlhelper.serializedata(wish_embedding)
       sqlhelper.update('user_id',element_dict,'user_embeddings')
   except Exception as e:
        return {'error': str(e)}

def removeUser(user_id):
   try:
       sqlhelper.delete(user_id, 'user_id','user_embeddings')
   except Exception as e:
        return {'error': str(e)}  

def addPlace(place_id, place_embedding):
    try:
       addPlaceInternal("", place_id, place_embedding)
    except Exception as e:
        return {'error': str(e)}

def addPlaceInternal(dbcon, place_id, place_embedding):
   try:
       print(place_id)
       element_dict = {}
       element_dict['place_id'] = place_id

       element_dict['word_vector'] = sqlhelper.serializedata(place_embedding)
       sqlhelper.insert(dbcon,'place_embeddings',element_dict)
   except Exception as e:
        return {'error': str(e)}

def getPlace(place_id):
    try:
       place_info = sqlhelper.select(place_id, 'place_id', 'place_embeddings')
       for row in place_info:
           id = row[0]
           word_vector = sqlhelper.deserializedata(row[1])

       if int(place_id) == int(id):
            return word_vector
       else:
           raise Exception
    except Exception as e:
        return {'error': str(e)}

def getAllPlaces():
    try:
        places_dict = {}
        places_info = sqlhelper.selectAll('place_embeddings')
        for row in places_info:
            id = row[0]
            word_vector = sqlhelper.deserializedata(row[1])
            places_dict[id] = word_vector

        return places_dict
    except Exception as e:
        return {'error': str(e)}

def removePlace(place_id):
   try:
       sqlhelper.delete(place_id, 'place_id','place_embeddings')
   except Exception as e:
        return {'error': str(e)}  

def addFeature(feature_id, feature_embedding):
    try:
       addFeatureInternal("", feature_id, feature_embedding)
    except Exception as e:
        return {'error': str(e)}

def addFeatureInternal(dbcon, feature_id, feature_embedding):
   try:
       print(feature_id)
       element_dict = {}
       element_dict['feature_id'] = feature_id

       element_dict['word_vector'] = sqlhelper.serializedata(feature_embedding)
       sqlhelper.insert(dbcon,'feature_embeddings',element_dict)
   except Exception as e:
        return {'error': str(e)}

def getFeatures(feature_ids):
    try:
        feature_list = []
        feature_info = sqlhelper.selectIds(feature_ids, 'feature_id', 'feature_embeddings')
        for row in feature_info:
            id = row[0]
            word_vector = sqlhelper.deserializedata(row[1])
            feature_list.append(word_vector)

        return feature_list
    except Exception as e:
        return {'error': str(e)}

def removeFeature(feature_id):
   try:
       sqlhelper.delete(feature_id, 'feature_id','feature_embeddings')
   except Exception as e:
        return {'error': str(e)} 