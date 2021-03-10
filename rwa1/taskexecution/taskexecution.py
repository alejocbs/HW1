import rwa1.taskplanning.taskplanning as plan
from time import sleep
from tqdm import tqdm

"""The following code attempts to plan the behavior of a robot in order to kit parts into a tray"""
print("welcome")
print("If no input is read program will run default values")
print("===================================")
tray, bins, to_place, location, grip, ok_to_exec = plan.init_state()
print("===================================")
print("Generating plan.... Please wait!\n")
for i in tqdm(range(10)): # nice  loading bar
    sleep(0.5)
#  offline planning execution
plan.plan(tray,bins,to_place,location,grip,ok_to_exec)
