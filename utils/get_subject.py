import pandas as pd
import os

with open(os.path.join(os.getcwd(),'subjects.txt')) as fl:
          subjects = fl.readlines()
          subjects = [x.strip() for x in subjects]

subject = subjects[int(os.environ.get("SLURM_ARRAY_TASK_ID"))]

exit(subject)
