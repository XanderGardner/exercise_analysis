from typing import List, Tuple
from scipy.stats import zscore

# a cycle object represents a series of workouts completed in one "workout cycle"
# days are 0 indexed
# each day has multiple exercises
# each exercise on a day has multiple sets
# each set has a certain number of reps for a given weight

class cycle_object:

  # initialize an empty cycle object
  def __init__(self):
    self.num_days = 0 # number of days in this cycle
    self.exercises = {} # for a given exercise key stores for each day a list of tuples of reps and weight
  
  ########
  # volume by day analysis functions
  ########

  # for all exercises return a tuple of the list of days and a parallel list of zscored volumes for each set
  def get_zscore_volumes(self, exercise_name: str = None) -> Tuple[List[int],List[int]]:
    if exercise_name is not None:
      self._validate_exercise_name(exercise_name)

      days,vols = self.get_volumes(exercise_name)
      zscores = zscore(vols).tolist()
      return (days,zscores)

    else:

      # get volumes for all exercises if exercise name not provided
      out_days = []
      out_vols = []
      for exercise_name in self.exercise_names():
        days,vols = self.get_zscore_volumes(exercise_name)
        out_days += days
        out_vols += vols
      return (out_days, out_vols)

  # for a given exercise return a tuple of the list of days and a parallel list of volumes
  def get_volumes(self, exercise_name: str) -> Tuple[List[int],List[int]]:
    self._validate_exercise_name(exercise_name)

    volumes = []
    days = []
    for day in range(self.num_days):
      volume = self.get_volume(day, exercise_name)
      if volume is not None:
        volumes += [volume]
        days += [day]
    return (days ,volumes)

  # return the total volume for a given day and exercise
  def get_volume(self, day: int, exercise_name: str) -> int:
    self._validate_day(day)
    self._validate_exercise_name(exercise_name)

    reps_and_weights = self.exercises[exercise_name][day]
    return sum([rep * weight for rep,weight in reps_and_weights]) if len(reps_and_weights) > 0 else None
  
  ########
  # volume by set and day analysis functions
  ########

  # for all exercises return a tuple of the list of days and a parallel list of zscored volumes for each set
  def get_zscore_set_volumes(self, exercise_name: str = None) -> Tuple[List[int],List[int]]:
    if exercise_name is not None:
      self._validate_exercise_name(exercise_name)

      days,vols = self.get_set_volumes(exercise_name)
      zscores = zscore(vols).tolist()
      return (days,zscores)

    else:

      # get volumes for all exercises if exercise name not provided
      out_days = []
      out_vols = []
      for exercise_name in self.exercise_names():
        days,vols = self.get_zscore_set_volumes(exercise_name)
        out_days += days
        out_vols += vols
      return (out_days, out_vols)

  
  # for a given exercise return a tuple of the list of days and a parallel list of volumes for each set
  # there may be repeat days since sets may be on the same day
  def get_set_volumes(self, exercise_name: str) -> Tuple[List[int],List[int]]:
    self._validate_exercise_name(exercise_name)

    volumes = []
    days = []
    for day in range(self.num_days):
      day_volumes = self.get_set_volumes_on_day(day, exercise_name)
      if len(day_volumes) > 0:
        volumes += day_volumes
        days += [day for _ in range(len(day_volumes))]
    return (days ,volumes)

  # return an ascending list of volumes (one for each set) for a given day and exercise
  def get_set_volumes_on_day(self, day: int, exercise_name: str) -> List[int]:
    self._validate_day(day)
    self._validate_exercise_name(exercise_name)

    reps_and_weights = self.exercises[exercise_name][day]
    volumes = [rep * weight for rep,weight in reps_and_weights]
    volumes.sort()
    return volumes
  
  ########
  # basic get functions
  ########

  # returns a list of the exercise names in this cycle
  def exercise_names(self) -> List[str]:
    return list(self.exercises.keys())
  
  # returns a list of the days [0,1,...,num_days-1]
  def get_days_list(self) -> List[int]:
    return list(range(self.num_days))
  
  # the length of the cycle is the number of days in the cycle
  def __len__(self):
    return self.num_days
  
  def __str__(self):
    return f"cycle_object({self.exercises})"
  
  ########
  # setter functions
  ########

  # add given list of exercise sets to cycle object, expanding days and exercises if need
  def add_exercise(self, day: int, exercise_name: str, sets: List[Tuple[int, int]]) -> None:
    for reps, weight in sets:
      self.add_exercise_set(day, exercise_name, reps, weight)
  
  # add given exercise set to cycle object, expanding days and exercises if needed
  def add_exercise_set(self, day: int, exercise_name: str, reps: int, weight: int) -> None:
    # exapand exercise days
    if day >= self.num_days:
      extra_days = day - self.num_days + 1
      for exercise in self.exercises.keys():
        self.exercises[exercise] += [[] for _ in range(extra_days)]
      self.num_days = day + 1

    # expand exercise names
    if exercise_name not in self.exercises:
      self.exercises[exercise_name] = [[] for _ in range(self.num_days)]
    
    self.exercises[exercise_name][day] += [[reps, weight]]
  
  ########
  # input validation functions
  ########

  # validate day input
  def _validate_day(self, day: int) -> None:
    if day < 0 or day >= self.num_days:
      raise ValueError(f"input day should be an int 0 to {self.num_days-1} but was given {day}")
  
  # validate exercise_name input
  def _validate_exercise_name(self, exercise_name: str) -> None:
    if exercise_name not in self.exercises:
      raise ValueError(f"input exercise_name \"{exercise_name}\" is not in this cycle object")

if __name__ == "__main__":
  cycle = cycle_object()
  cycle.add_exercise_set(0, "front squat", 5, 100)
  cycle.add_exercise_set(0, "front squat", 5, 100)
  cycle.add_exercise_set(0, "pushups", 5, 160)
  cycle.add_exercise_set(1,"pushups", 6, 160)
  cycle.add_exercise(1, "hack squat", [(5,100),(5,100)])

  assert("pushups" in cycle.exercise_names())
  assert("front squat" in cycle.exercise_names())
  assert(len(cycle) == 2)

  print(cycle)

  print("tests complete")
