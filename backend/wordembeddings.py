import wikipedia
import nlp_helper
import spacy
import numpy as np
import heapq


# Singleton implementation
# So we don't create the new instance again and again. 
# And Language model has to be defined only once
class WordEmbedder:

    __shared_instance = 'shared'

    @staticmethod
    def getInstance():
  
        """Static Access Method"""
        if WordEmbedder.__shared_instance == 'shared':
            WordEmbedder()
        return WordEmbedder.__shared_instance

    def __init__(self) -> None:

        """virtual private constructor"""
        if WordEmbedder.__shared_instance != 'shared':
            raise Exception ("This class is a singleton class !")
        else:
            # TODO: Try with the transformer model as well 'en_core_web_trf'. 'en_core_web_lg' only uses the semantics, transformer model
            # uses the context as well
            self.language_model = spacy.load('en_core_web_lg')
            
            self.addn_stop_words = ['\n', '.', '-',',']
            for stop_word in self.addn_stop_words:
                self.language_model.vocab[stop_word].is_stop = True

            WordEmbedder.__shared_instance = self

        # returns the places and features word vectors
    def initML(self, places, features):
        try:
            # Create Embeddings for the places
            places_dict = {}
            failure_dict = {}
            for place_id in places:
                place = places[place_id]
                print(place)
                # TODO: Check using the .summary API as well
                try:
                    place_info = wikipedia.page(place).content
                except wikipedia.DisambiguationError as e:
                    failure_dict[place_id] = place
                    continue
                except wikipedia.PageError as e:
                    failure_dict[place_id] = place
                    continue

                place_embedding = nlp_helper.createTextVector(place_info, self.language_model)
                places_dict[place_id] = place_embedding
            
            # Create Embeddings for the features
            features_dict = {}

            for feature_id in features:
                feature = features[feature_id]
                print(feature)
                # TODO: Check using the .summary API as well
                try:
                    feature_info = wikipedia.page(feature).content
                except wikipedia.DisambiguationError as e:
                    failure_dict[feature_id] = feature
                    continue
                except wikipedia.PageError as e:
                    failure_dict[feature_id] = feature
                    continue
                
                feature_embedding = nlp_helper.createTextVector(feature_info, self.language_model)
                features_dict[feature_id] = feature_embedding

            embedding_dict = {'places':places_dict,
                                'features':features_dict,
                                'failures':failure_dict}

            return embedding_dict

        except Exception as e:
            return {'error': str(e)}

    # Calculates the new average of the user embedding
    def updateUserEmbeddings(self, avg_num, user_vector, place_vector):
        try:
            avg_user_vector = avg_num * np.array(user_vector)
            avg_user_vector = np.array([avg_user_vector, place_vector]).sum(axis=0)
            user_embedding = avg_user_vector/(avg_num+1)
            return user_embedding
        except Exception as e:
            return {'error': str(e)}

    # Calculates the user embedding
    def calcUserEmbedding(self, feature_vectors):
        try:
            # Averaging the feature embeddings
            user_embedding = np.array([featVec for featVec in feature_vectors]).mean(axis=0)
            return user_embedding
        except Exception as e:
            return {'error': str(e)}

    def calcFeatureEmbedding(self, feature_name):
        try:
            # TODO: Check using the .summary API as well 
            feature_info = wikipedia.page(feature_name).content
            feature_embedding = nlp_helper.createTextVector(feature_info, self.language_model)
            return feature_embedding
        except Exception as e:
            return {'error': str(e)}

    def calcPlaceEmbedding(self, place_name):
        try:
            # TODO: Check using the .summary API as well 
            place_info = wikipedia.page(place_name).content
            place_embedding = nlp_helper.createTextVector(place_info, self.language_model)
            return place_embedding
        except Exception as e:
            return {'error': str(e)}


    def getRecommendations(self, user_vector, wish_vector, places, visited_places, count):
        try:
            recommended_ft_dict = {}
            recommended_wish_dict = {}
            count = int(count)
            if count == 0:
                return []

            recommendations = {'feature_based':[],
                                'wish_based':[]}

            for place_id in places:
                if place_id in visited_places:
                    continue
                place_vector = places[place_id]
                similarity_ft = nlp_helper.get_cosine_similarity(user_vector, place_vector)
                recommended_ft_dict[place_id] = similarity_ft
                if wish_vector.size > 1:
                    similarity_wish = nlp_helper.get_cosine_similarity(wish_vector, place_vector)
                    recommended_wish_dict[place_id] = similarity_wish

            # return the keys with largest values
            recommendations['feature_based'] =  heapq.nlargest(count, recommended_ft_dict, key=recommended_ft_dict.get)
            if wish_vector.size > 1:
                recommendations['wish_based'] =  heapq.nlargest(count, recommended_wish_dict, key=recommended_wish_dict.get)

            print(recommendations)
            return recommendations
        except Exception as e:
            return {'error': str(e)}