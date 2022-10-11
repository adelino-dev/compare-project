from geo_functions import *
from prices_functions import *
from datetime import datetime

def print_stations():
  """
  ----
  Print the names of the stations listed in the 
  order given with their respective distances and 
  total prices on the side.
  """
  now = datetime.now()
  print("Data/Hora atual:", now)

  position = get_position()
  print("Posição Atual:", position)
  print("----------------------------------")
  print("\nPostos mais próximos:\n")

  stations = compare_distances(position)
  for station in stations:
    name = station[0]
    distance = station[1]
    print(distance, "|", name)
    print("-----------------------------------------------------")
    
if __name__ == "__main__":
  print_stations()