from typing import List
import pickle
from cycle_object import cycle_object
import os

STORAGE_PATH_PREFIX = "./cycle_storage/" # path to storage of pickle objects
STORAGE_SUFFIX = ".pkl" # pickle object file type suffix

# cycle_database manages reading and writing cycle_objects to storage using pickle
class cycle_database:

  # saves the given cycle to storage under given cycle_name
  def save(self, cycle_name, cycle) -> None:
    path = STORAGE_PATH_PREFIX + cycle_name + STORAGE_SUFFIX
    with open(path, "wb") as file:
      pickle.dump(cycle, file)

  # returns to cycle from storage for the given cycle_name
  def load(self, cycle_name) -> cycle_object:
    path = STORAGE_PATH_PREFIX + cycle_name + STORAGE_SUFFIX
    with open(path, 'rb') as file:
      return pickle.load(file)
    
  # returns a list of cycle names currently stored
  def cycles_available(self) -> List[str]:
    file_names = os.listdir(STORAGE_PATH_PREFIX)
    cycle_names = [file_name[:-len(STORAGE_SUFFIX)] for file_name in file_names]
    return cycle_names

if __name__ == "__main__":
  db = cycle_database()
  db.cycles_available()
