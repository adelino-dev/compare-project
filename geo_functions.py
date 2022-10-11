import googlemaps

API_KEY = '' #google cloud key
gmaps = googlemaps.Client(key = API_KEY) 

testMode = True

if testMode:
  positionTest = {'lat':-9.664039599999999, 'lng':-35.7303309}
  
  import json
  
  with open("_data_test_/stations.json", encoding='utf-8') as stations:
    stationsTest = json.load(stations)

  with open("_data_test_/distances.json", encoding='utf-8') as stations:
    distancesTest = json.load(stations)
   

def get_position(address = None):
  """
  address --> a string with a address
    default: None

  -----
  If addres is None, returns the user's current position, 
  else returns the addres position.

  * position is a tuple (latitude, longitude)
  """
  if testMode:
    position = positionTest
    
  elif address == None:
    position = gmaps.geolocate()['location']

  else:
    position = gmaps.geocode(address)[0]['geometry']['location']

  lat = position['lat']
  lng = position['lng']
  position = (lat, lng)

  return position
  
def compare_distances(position):
  """
  position --> the user's position (latitude and longitude)

  ------------
  Returns a list sorted in ascending order of distance 
  containing tuples with the gas stations names and the distances.
  """
  stations = get_stations(position)
  ids = get_stationsID(stations)
  stationsPositions = get_stationsPositions(stations)

  names = []
  for id in ids:
    name = get_stationName(stations, id)
    names.append(name)

  name_distance = []
  for i in range(len(stations)):
    name = names[i]
    destination = stationsPositions[i]
    distance = get_stationDistance(position, destination)
    name_distance.append((name, distance))
    
  return name_distance
  
def get_stations(position):
  """
  position --> the user's position (latitude and longitude)

  ------------
  Returns a list sorted in ascending order 
  by distances with the google maps 
  results of the nearest gas stations.
  """
  if testMode:
    stations = stationsTest
    
  else:
    stations = gmaps.places_nearby(
      location = position,
      name = "gas station",
      open_now = True,
      rank_by = "distance"
    )

  return stations['results']

def get_stationsID(stations):
  """
  stations --> a list sorted in ascending order by distances containing 
              google maps results of the nearest gas stations.

  ------------
  Returns a list containing the identifiers 
  of the gas stations sorted in ascending order by distances.
  """
  stations_id = []

  for station in stations:
    stations_id.append(station['place_id'])

  return stations_id

def get_stationsPositions(stations):
  """
  stations --> a list sorted in ascending order by distances containing 
              google maps results of the nearest gas stations.

  ------------
  Returns a list containing the latitude and longitude
  of the gas stations sorted in ascending order by distances.
  """
  stations_id = []

  for station in stations:
    position = station['geometry']['location']
    lat = position['lat']
    lng = position['lng']
    stations_id.append((lat, lng))

  return stations_id

def get_stationName(stations, place_id):
  """
  stations --> a list with the google maps 
              results of the gas stations.

  place_id --> the gas station identifier.
  
  ----------
  Return the station name (string).
  """
  for station in stations:
    if station['place_id'] == place_id:
      name = station['name']
      return name

def get_stationDistance(origin, destination):
  """
  origin --> latitude and longitude of the gas station (tuple).
  destination -->  latitude and longitude of destination (tuple).
  ----------

  Returns the distance beetwen the gas station and the origin.
  """
  
  if testMode:
    destination = str(destination[0])+", "+str(destination[1])
    distance = distancesTest[destination]['rows'][0]['elements'][0]['distance']['text']
    
  else:
    distance = gmaps.distance_matrix(origin, destination)['rows'][0]['elements'][0]['distance']['text']
  
  return distance

if __name__ == "__main__":
  position = get_position()
  print("Posição Atual:", position)

  stations = get_stations(position)
  ids = get_stationsID(stations)
  names = []
  positions = get_stationsPositions(stations)
  
  for id in ids:
    name = get_stationName(stations, id)
    names.append(name)

  for i in range(len(stations)):
    name = names[i]
    destination = positions[i]
    distance = get_stationDistance(position, destination)
    print(name, distance)