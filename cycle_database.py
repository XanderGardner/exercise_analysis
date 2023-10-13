import pickle
from cycle_object import cycle_object

# cycle_database manages reading and writing cycle_objects to storage using pickle
class cycle_database:

  # saves the given cycle to storage under given cycle_name
  def save(self, cycle_name, cycle) -> None:
    path = f"./cycle_objects/{cycle_name}.pkl"
    with open(path, "wb") as file:
      pickle.dump(cycle, file)

  # returns to cycle from storage for the given cycle_name
  def load(self, cycle_name) -> cycle_object:
    path = f"./cycle_objects/{cycle_name}.pkl"
    with open(path, 'rb') as file:
      return pickle.load(file)
