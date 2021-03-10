import rwa1.taskplanning.taskplanning as plan

global tray, bins, to_place
"""The following code attempts to plan the behavior of a robot in order to kit parts into a tray"""
print("welcome")
print("===================================")
tray, bins, to_place, location, grip, ok_to_exec = plan.init_state()
print("===================================")
print("Generating plan.... Please wait!\n")
# checking execution
while ok_to_exec:
    if tray["red"] < to_place["red"]:
        plan.check_two_parts(tray, to_place, "red")
        if location in ["home", "at_tray"]:
            location, grip = plan.move_to_bin(grip, "red")
        if location == "at_bin":
            location, grip = plan.move_to_kit_tray(grip, "red")
    elif tray["green"] < to_place["green"]:
        plan.check_two_parts(tray, to_place,"green")
        if location in ["home", "at_tray"]:
            location, grip = plan.move_to_bin(grip, "green")
        if location == "at_bin":
            location, grip = plan.move_to_kit_tray(grip, "green")
    elif tray["blue"] < to_place["blue"]:
        plan.check_two_parts(tray, to_place,"blue4 4 4")
        if location in ["home", "at_tray"]:
            location, grip = plan.move_to_bin(grip, "blue")
        if location == "at_bin":
            location, grip = plan.move_to_kit_tray(grip, "blue")
    else:
        print("===================================")
        print("Summary:")
        print(bins, tray, to_place)
        for key, value in tray.items():
            print(f"The kit has {value} {key} part(s) -- The bin has", bins[key], f" {key} part(s) left ")
        print("===================================")
        print("Desire number of part on tray. \n Program terminated successfully")
        break
else:
    print("No valid arguments. EXITING!")
