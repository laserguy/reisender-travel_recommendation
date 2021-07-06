from geosky import geo_plug

#geo_plug.all_CountryNames()
#geo_plug.all_Country_StateNames()
#geo_plug.all_State_CityNames(name)# name == 'all' or stae name
places = geo_plug.all_State_CityNames()


import json
import requests

wiki_string = "https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles="
reisender_url = "https://vscode.anor.gq/api/places"
places_json = json.loads(places)

for country_places in places_json:
    #country_places = places_json[key]
    for place_name in country_places:
        wiki_place = wiki_string + place_name
        try:
            request = requests.get(wiki_place)
            var = request.json()
            value = list(var['query']['pages'])[0]
            fetch_url = var['query']['pages'][value]['original']['source']
        except Exception as e:
            continue
        
        place_dict = {'name':place_name,
                     'url':fetch_url}
        print(place_dict)
        try:
            response = requests.post(reisender_url,json=place_dict)
        except Exception as e:
            print(str(e))
            continue
        print(response)
        