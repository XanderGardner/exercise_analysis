from typing import List, Tuple

# a cycle object represents a series of workouts completed in one "workout cycle"
# days are 0 indexed
# each day has multiple exercises
# each exercise on a day has multiple sets
# each set has a certain number of reps for a given weight

class cycle_object:

  # initialize an empty cycle object
  def __init__(self):
    self.num_days = 0 # number of days in this cycle
    self.exercises = {} # store workouts for each day for a given exercise key
  
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
  
  # returns a list of the exercise names in this cycle
  def exercise_names(self) -> List[str]:
    return list(self.exercises.keys())

  # return the total volume for a given day and exercise
  def get_volume(self, day: int, exercise_name: str) -> int:
    self._validate_day(day)
    self._validate_exercise_name(exercise_name)

    reps_and_weights = self.exercises[exercise_name][day]
    return sum([rep * weight for rep,weight in reps_and_weights])

  # return an ascending list of volumes for a given day and exercise
  def get_volume_list(self, day: int, exercise_name: str) -> int:
    self._validate_day(day)
    self._validate_exercise_name(exercise_name)

    reps_and_weights = self.exercises[exercise_name][day]
    volumes = [rep * weight for rep,weight in reps_and_weights]
    volumes.sort()
    return volumes
  
  # the length of the cycle is the number of days in the cycle
  def __len__(self):
    return self.num_days
  
  def __str__(self):
    return f"cycle_object({self.exercises})"

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

  assert(cycle.get_volume(0, "front squat") == 1000)
  assert(cycle.get_volume(1, "hack squat") == 1000)
  assert(len(cycle) == 2)

  print(cycle)

  print("tests complete")
