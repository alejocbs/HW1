def init_state():
    """Function to initializice the states. Do not enter a number higher than 10"""
    global tray, bins, to_place
    gripers = False  # gripper to empty state
    execute = True
    robot_location = "home"  # set the robot initial location to home
    # Define and validate how many parts are inside the bins
    while True:
        red, green, blue = input("""How many red/green/blue parts are in the bins?""").split()
        if int(red) > 10 or int(green) > 10 or int(blue) > 10:
            print("Number of parts incorrect. Max number of part per color is 10")
            print("try again")
        else:
            bins = {"red": int(red), "green": int(green), "blue": int(blue)}
            break
    # Define and validate how many parts are already in kit tray
    while True:
        red, green, blue = input("""How many red/green/blue parts are already in the kit tray?""").split()
        if int(red) > 10 or int(green) > 10 or int(blue) > 10:
            print("Number of parts incorrect. Max number of part per color is 10")
            print("try again")
        else:
            tray = {"red": int(red), "green": int(green), "blue": int(blue)}
            break
    # Define and validate how many parts are going to be placed in tray
    while True:
        red, green, blue = input("""How many red/green/blue parts to be placed in the kit tray?""").split()
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


# Check for trip optimizer
def check_two_parts(_tray, _to_place, _key):
    if _to_place % 2 == 0:
        arm = ["left", "right"]
    else:
        arm = ["left"]
    return arm


# Robot actions
def pick(arm: str, empty_gripper: bool, part: str):
    print(f"Pick {part} part with the {arm} arm")
    ud = {part: bins[part] - 1}
    bins.update(ud)
    gripper = True
    return gripper


def place(arm: str, empty_gripper: bool, part: str):
    print("place ", part, " with ", arm, " arm")
    ud = {part: tray[part] + 1}
    tray.update(ud)
    # set gripper to empty
    gripper = False
    return gripper


def move_to_bin(empty_gripper: bool, part: str):
    """Move from home to bin"""
    print("===================================")
    print("Move to bin")
    grip = pick(arm, empty_gripper, part)
    location = "at_bin"
    return location, grip


def move_to_kit_tray(empty_gripper: bool, part: str):
    print("===================================")
    print("Move to kit tray")
    location = "at_tray"
    grip = place(arm, empty_gripper, part)
    return location, grip

