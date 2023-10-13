from typing import List, Tuple
import requests
import io
import csv
from cycle_object import cycle_object
from cycle_database import cycle_database

# the sheet_parser provides a number of parsing functions for different formats of google sheets that track workout cycles
# the formats handled are documented in README.md
class sheet_parser:

  # parses gym cycle from gca format file and saves cycle object to storage
  def parse_gym_gca(self, cycle_name: str, google_sheet_id: str, gid: str) -> None:
    # download raw data
    sheet = self._download_sheet(google_sheet_id, gid)

    # parse and add to cycle
    cycle = cycle_object()

    # extract exercises
    num_days = max([len(row)-2 for row in sheet])
    for row in sheet:
      if len(row) < 3:
        # row is too small to contain exercise data
        continue

      exercise_type, exercise_name = self._gca_exercise_name_decode(row[1])

      if exercise_type != "gym":
        # exclude none gym entries
        continue
      
      day_num = num_days-1
      for col_index in range(2,len(row)):
        sets = self._gca_exercise_entry_decode(row[col_index], exercise_type)
        cycle.add_exercise(day_num, exercise_name, sets)
        day_num -= 1

    # save cycle
    cdb = cycle_database()
    cdb.save(cycle_name, cycle)

  # returns a tuple (exercise type, exercise_name) for the given encoded_exercise_name 
  # execise types are ("empty", "gym", "calisthenics", or "accessory")
  def _gca_exercise_name_decode(self, encoded_exercise_name: str) -> Tuple[str, str]:
    if len(encoded_exercise_name) == 0 or encoded_exercise_name[0] == "-":
      return ("empty","")
    
    if encoded_exercise_name == "*" or encoded_exercise_name == "**":
      return ("empty","")
    
    if encoded_exercise_name[0] != "*":
      return ("gym", encoded_exercise_name)
    
    if encoded_exercise_name[1] != "*":
      return ("calisthenics", encoded_exercise_name[1:])
    
    return ("accessory",encoded_exercise_name[2:])
  
  # decodes exercise string to get a list of tuples of (reps, weight)
  def _gca_exercise_entry_decode(self, encoded_str: str, exercise_type: str) -> List[Tuple[int, int]]:
    if exercise_type == "empty":
      raise ValueError(f"exercise type should not be \"empty\" when decoding exercise entry")

    if exercise_type == "gym" or exercise_type == "accessory":
      out = []
      for set_groups in encoded_str.strip().split(","):
        set_group = set_groups.strip().split("x")

        # if there are 3 values -> (sets, reps, weight)
        # if there are 2 values -> (reps, weight) and sets = 1
        # if there are 1 values -> (reps) and sets = 1 and weight = 1
        # if there are 0 values -> no exercise was done
        if len(set_group) == 3:
          sets = self._num_in_str(set_group[0])
          reps = self._num_in_str(set_group[1])
          weight = self._num_in_str(set_group[2])
          out += [(reps, weight) for _ in range(sets)]
        elif len(set_group) == 2:
          reps = self._num_in_str(set_group[0])
          weight = self._num_in_str(set_group[1])
          out += [(reps, weight)]
        elif len(set_group) == 1:
          reps = self._num_in_str(set_group[0])
          weight = 1
          out += [(reps, weight)]

      return out
    
    elif exercise_type == "calisthenics":
      out = []
      for set_groups in encoded_str.strip().split(","):
        set_group = set_groups.strip().split("x")

        # if there are 2 values -> (sets, reps) and sets = 1
        # if there are 1 values -> (reps) and sets = 1
        # if there are 0 values -> no exercise was done
        if len(set_group) == 2:
          sets = self._num_in_str(set_group[0])
          reps = self._num_in_str(set_group[1])
          out += [(reps, 1) for _ in range(sets)]
        elif len(set_group) == 1:
          reps = self._num_in_str(set_group[0])
          out += [(reps, 1)]

      return out
    
    return []
  
  # returns the number within the string, ignoring any non-digit characters
  def _num_in_str(self, s: str) -> int:
    tot = 0
    for c in s:
      if c.isdigit():
        tot *= 10
        tot += int(c)
    return tot
    
  # given the google sheet id and gid, returns the google sheet cells in a list of lists by requesting the google url
  def _download_sheet(self, google_sheet_id: str, gid: str) -> List[List[str]]:
    r = requests.get(f'https://docs.google.com/spreadsheet/ccc?key={google_sheet_id}&output=csv&gid={gid}')
    csv_str = r.content.decode('utf-8')
    csv_file = io.StringIO(csv_str)
    csv_reader = csv.reader(csv_file)
    return [row for row in csv_reader]

if __name__ == "__main__":
  sp = sheet_parser()
  
  with open("./drive_metadata.csv") as file:
    csv_reader = csv.reader(file)

    for i,row in enumerate(csv_reader):
      if i == 0:
        continue

      cycle_name, google_sheet_id, gid, format = row
      if format == "gca":
        sp.parse_gym_gca("gym_"+cycle_name, google_sheet_id, gid)
        print(f"create gym_{cycle_name} cycle object")
      else:
        print(f"format {format} not suppoerted for cycle {cycle_name}")

print("parsing complete")
  