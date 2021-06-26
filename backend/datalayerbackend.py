import sqlhelper
import numpy as np
import orchestrator
import MLparams

def init():
    try:
        #create tables part is manually right now, If init is done with no tables then we will get an exceptipon.
        dbcon = sqlhelper.connectDB()
        if(sqlhelper.checkTableExists(dbcon, 'featureinfo') == False):
            raise Exception
        print("Inside Init")

        if(sqlhelper.checkEmpty('featureinfo') == False):
            print('Init already done exiting init')
            return

        with open("features.txt") as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            features = {}
            for i in content:
                feature = i.split(",")
                ft_info = addFeature(feature[0],feature[1])
                features[ft_info[0]] = ft_info[1]

        print('Features added successfully')

        with open("places.txt") as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            places = {}
            for i in content:
                place = i.split(",")
                pl_info = addPlace(place[0],place[1])
                places[pl_info[0]] = pl_info[1]

        print('Places added successfully')
        failure_dict = orchestrator.init(places,features)
        print("Could not be added")
        print(failure_dict)
    except Exception as e:
        print(str(e))
        return {'error': str(e)}


def addFeature(feature_name,feature_url):
    try:
        feature_dict = {}
        feature_dict['name'] = feature_name
        feature_dict['image_url'] = feature_url
        insert_dict = sqlhelper.insert("",'featureinfo',feature_dict)
        return [insert_dict['insert_id'],feature_name]
    except Exception as e:
        return {'error': str(e)}


def addPlace(place_name,place_url):
    try:
        place_dict = {}
        place_dict['name'] = place_name
        place_dict['image_url'] = place_url
        insert_dict = sqlhelper.insert("",'placeinfo',place_dict)
        return [insert_dict['insert_id'],place_name]
    except Exception as e:
        print('In exception')
        return {'error': str(e)}

def getPlaces(place_ids):
    try:
        place_info = sqlhelper.selectIds(place_ids,'place_id','placeinfo')
        return [{"place_id":row[0], "name":row[1], "image_url":row[2]} for row in place_info]
    except Exception as e:
        return {'error': str(e)}

def register(username,passwd):
    try:
        element_dict = {}
        element_dict['username'] = username
        element_dict['password'] = passwd
        element_dict['firstlogin'] = 0
        insert_dict = sqlhelper.insert("",'logininfo',element_dict)

        user_dict = {}
        user_dict['user_id'] = insert_dict['insert_id']
        sqlhelper.insert("",'userinfo',user_dict)

        return {'id':user_dict['user_id']}
    except Exception as e:
        return {'error': str(e)}

def login(username,passwd):
    try:
        user_dict = {}
        element_dict = {}
        element_dict['username'] = username
        element_dict['password'] = passwd
        user_info = sqlhelper.select_mulparams(element_dict,'logininfo')

        for row in user_info:
            user_dict['id'] = row[0]
            user_dict['firstlogin'] = row[3]

        return user_dict
    except Exception as e:
        return {'error': str(e)}

def getFeatureList():
    try:
        feature_list = sqlhelper.selectAll("FeatureInfo")
        return [{"feature_id":row[0], "name":row[1], "image_url":row[2]} for row in feature_list]
    except Exception as e:
        return {'error': str(e)}

def passFeatureList(user_id, features):
    try:
        element_dict = {}
        element_dict['Id'] = user_id
        element_dict['firstlogin'] = 1
        sqlhelper.update('Id',element_dict,'logininfo')

        orchestrator.addUser(user_id,features)
    except Exception as e:
        return {'error': str(e)}

def wishListAdd(user_id, place_id):
    try:
        user_info = sqlhelper.select(user_id, 'user_id', 'userinfo')
        for row in user_info:
            wish_list = row[2]

        if wish_list == None or wish_list == '':
            wish_list = str(place_id)
        else:
            wish_list += ',' + str(place_id)

        element_dict = {}
        element_dict['user_id'] = user_id
        element_dict['wish_list'] = wish_list
        sqlhelper.update('user_id',element_dict,'userinfo') 

        orchestrator.updateUserEmbeddings(user_id,place_id)
    except Exception as e:
        return {'error': str(e)}

def wishListRemove(user_id, place_id):
    try:
        user_info = sqlhelper.select(user_id, 'user_id', 'userinfo')
        for row in user_info:
            wish_list = row[2]

        if wish_list.find(',') != -1:
            wish_list = list(wish_list.split(','))
            index = wish_list.index(str(place_id))
            del wish_list[index]
            wish_list = ','.join(wish_list)
        else:
            wish_list = ""
        element_dict = {}
        element_dict['user_id'] = user_id
        element_dict['wish_list'] = wish_list
        sqlhelper.update('user_id',element_dict,'userinfo') 
    except Exception as e:
        return {'error': str(e)}

def wishListGet(user_id):
    try:
        places_dict = {}
        user_info = sqlhelper.select(user_id, 'user_id', 'userinfo')
        for row in user_info:
            wish_list = row[2]       
        
        wish_list = list(wish_list.split(','))
        wish_list = list(map(int, wish_list))

        return getPlaces(wish_list)
    except Exception as e:
        return {'error': str(e)}

def visitedListAdd(user_id, place_id):
    try:
        user_info = sqlhelper.select(user_id, 'user_id', 'userinfo')
        for row in user_info:
            visited_list = row[1]

        if visited_list == None or visited_list == '':
            visited_list = str(place_id)
        else:
            visited_list += ',' + str(place_id)

        element_dict = {}
        element_dict['user_id'] = user_id
        element_dict['visited_list'] = visited_list
        sqlhelper.update('user_id',element_dict,'userinfo') 
    except Exception as e:
        return {'error': str(e)}

def visitedListRemove(user_id, place_id):
    try:
        user_info = sqlhelper.select(user_id, 'user_id', 'userinfo')
        for row in user_info:
            visited_list = row[1]

        if visited_list.find(',') != -1:
            visited_list = list(visited_list.split(','))
            index = visited_list.index(str(place_id))
            del visited_list[index]
            visited_list = ','.join(visited_list)
        else:
            visited_list = ""

        element_dict = {}
        element_dict['user_id'] = user_id
        element_dict['visited_list'] = visited_list
        sqlhelper.update('user_id',element_dict,'userinfo') 
    except Exception as e:
        return {'error': str(e)}

def visitedListGet(user_id):
    try:
        places_dict = {}
        user_info = sqlhelper.select(user_id, 'user_id', 'userinfo')
        for row in user_info:
            visited_list = row[1]       
        
        visited_list = list(visited_list.split(','))
        visited_list = list(map(int, visited_list))

        return getPlaces(visited_list)

    except Exception as e:
        return {'error': str(e)}

def recommend(user_id):
    try:
        places_object = visitedListGet(user_id)
        places_list = [pl['place_id'] for pl in places_object]
        
        recommendations = orchestrator.getRecommendations(user_id, places_list, MLparams.DEFAULT_RECOMMENDATIONS_COUNT)
        # TODO: Remove the visited list from the recommendations
        print(recommendations)
        if recommendations['wish_based']:
            common_list = list(set(recommendations['feature_based']).intersection(recommendations['wish_based']))
            recommendations['wish_based'] = list(set(recommendations['wish_based']) - set(common_list))

        feature_recommendation_ids = recommendations['feature_based']
        wish_recommendations_ids = recommendations['wish_based']

        recommendations_dict = {'feature_based':[],
                                'wish_based':[]}

        recommendations_dict['feature_based'] = getPlaces(feature_recommendation_ids)
        if wish_recommendations_ids:
            recommendations_dict['wish_based'] = getPlaces(wish_recommendations_ids)     
    
        return recommendations_dict
    except Exception as e:
        return {'error': str(e)}

def search(query):
    try:
        places_dict = {}
        place_info = sqlhelper.select_like('name','placeinfo',query)
        return [{"place_id":row[0], "name":row[1], "image_url":row[2]} for row in place_info]
        return places_dict
    except Exception as e:
        return {'error': str(e)}  