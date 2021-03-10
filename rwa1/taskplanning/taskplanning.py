def init_state():
    """Function to initializice the states. Do not enter a number higher than 10"""
    global tray, bins, to_place
    gripers = False  # gripper to empty state
    execute = True
    robot_location = "home"  # set the robot initial location to home
    # Define and validate how many parts are inside the bins if no number is enter by default 10 10 10
    while True:
        red, green, blue = (input("""How many red/green/blue parts are in the bins?""") or "10 10 10").split()
        if int(red) > 10 or int(green) > 10 or int(blue) > 10:
            print("Number of parts incorrect. Max number of part per color is 10")
            print("try again")
        else:
            bins = {"red": int(red), "green": int(green), "blue": int(blue)}
            break
    # Define and validate how many parts are already in kit tray
    while True:
        red, green, blue = (input("""How many red/green/blue parts are already in the kit tray?""") or "1 1 1").split()
        if int(red) > 10 or int(green) > 10 or int(blue) > 10:
            print("Number of parts incorrect. Max number of part per color is 10")
            print("try again")
        else:
            tray = {"red": int(red), "green": int(green), "blue": int(blue)}
            break
    # Define and validate how many parts are going to be placed in tray
    while True:
        red, green, blue = (input("""How many red/green/blue parts to be placed in the kit tray?""") or "10 10 10").split()
        if (int(red) - tray["red"]) > bins["red"]:  # Compare wanted red  parts
            print("Not enough parts for kitting: ", red, "needed, ", bins["red"], "available.")
            execute = False
        if (int(green) - tray["green"]) > bins["green"]:  # Compare wanted green  parts
            print("Not enough parts for kitting: ", green, "needed, ", bins["green"], "available.")
            execute = False
        if (int(blue) - tray["blue"]) > bins["blue"]:  # Compare wanted blue  parts
            print("Not enough parts for kitting: ", blue, "needed, ", bins["blue"], "available.")
            execute = False
        else:
            to_place = {"red": int(red), "green": int(green), "blue": int(blue)}
            break
    return tray, bins, to_place, robot_location, gripers, execute

_place = []
_pick = []

# Check for trip optimizer
def check_two_parts(_tray, _to_place,_key):
    """Check if two arms can be used"""
    global arm, count
    if (_to_place[_key]-_tray[_key]) >1:
        arm = ["left", "right"]
        count=2
    else:
        arm = ["left"]
        count=1
    return arm


# Robot actions
# pick parts from trays
def pick(arm: str, empty_gripper: bool, part: str):
    for i in range(count): # function to pick two parts if arms are available
        print(f"Pick {part} part with the {arm[i]} arm")
        _pick.append([part, arm[i]])
        ud = {part: bins[part] - 1}
        bins.update(ud)  # update parts in bins
        gripper = True
    return gripper

# place command for robot arm
def place(arm: str, empty_gripper: bool, part: str):
    for i in range(count):
        print("place ", part, " with ", arm[i], " arm")
        _place.append([part, arm[i]])      # safe the offline planning
        ud = {part: tray[part] + 1}
        tray.update(ud)  #update tray values
    # set gripper to empty
    gripper = False
    return gripper

#move the arm to bin
def move_to_bin(empty_gripper: bool, part: str):
    """Move from home to bin"""
    print("===================================")
    print("Move to bin")
    grip = pick(arm, empty_gripper, part)
    location = "at_bin"  # set the gripper to bin active status
    return location, grip

# move the arm to kit
def move_to_kit_tray(empty_gripper: bool, part: str):
    print("===================================")
    print("Move to kit tray")
    location = "at_tray"
    grip = place(arm, empty_gripper, part)
    return location, grip

def plan(tray, bins, to_place,location,grip,ok_to_exec):
    while ok_to_exec:# check for valid inputs
        if tray["red"] < to_place["red"]: #check number of red parts
            check_two_parts(tray, to_place, "red")
            if location in ["home", "at_tray"]:
                location, grip = move_to_bin(grip, "red")
            if location == "at_bin":
                location, grip = move_to_kit_tray(grip, "red")
        elif tray["green"] < to_place["green"]:
            check_two_parts(tray, to_place,"green")
            if location in ["home", "at_tray"]:
                location, grip = move_to_bin(grip, "green")
            if location == "at_bin":
                location, grip = move_to_kit_tray(grip, "green")
        elif tray["blue"] < to_place["blue"]:
            check_two_parts(tray, to_place,"blue")
            if location in ["home", "at_tray"]:
                location, grip = move_to_bin(grip, "blue")
            if location == "at_bin":
                location, grip = move_to_kit_tray(grip, "blue")
        else:
            #print a summary of the tray, bins and parts
            print("===================================")
            print("Summary:")
            print(bins, tray, to_place)
            for key, value in tray.items():
                print(f"The tray has {value} {key} part(s) -- The bin has", bins[key], f" {key} part(s) left ")
            print("===================================")
            print("Desire number of part on tray. \n Program terminated successfully")
            #print(_place, _pick) # offline plan!!!
            break

    else:
        print("No valid arguments. EXITING!")
