from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity

def removeStopWords(text, language_model):
    document = language_model(text)
    token_list = []
    for token in document:
        token_list.append(token.text)

    # Create list of word tokens after removing stopwords
    filtered_sentence =[] 

    for word in token_list:
        lexeme = language_model.vocab[word]
        if lexeme.is_stop == False:
            filtered_sentence.append(word)
    
    return ' '.join(filtered_sentence)


def createTextVector(text, language_model):
    #document = language_model(text)
    filtered_string = removeStopWords(text, language_model)
    
    textDoc = language_model(filtered_string)
    textVector = textDoc.vector.reshape(1,-1)
    
    return textVector


def get_cosine_similarity(feature_vec_1, feature_vec_2):    
    return cosine_similarity(feature_vec_1.reshape(1, -1), feature_vec_2.reshape(1, -1))[0][0]