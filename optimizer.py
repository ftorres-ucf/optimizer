#!/usr/bin/python3.7
from datetime import datetime
from datetime import time
import subprocess

file_path = "../RT_FRB/controller.py"

opt_param = [
    # Digifil
    {
        "line": 454, 
        "change_pos": 3,
        "starting_param": 1,
        "current_param": 1,
        "param_step" : 1,
        "max_val" : 64
    },
    # Candmaker
    {
        "line": 529,
        "change_pos": 5,
        "starting_param": 1,
        "current_param": 1,
        "param_step" : 1,
        "max_val" : 64
    }
]

hour_limits = [time(12,0,0), time(2,0,0)]



quit = False
run = False

#  Create general purpose loop that loops through each iteration
while not quit:
    now = datetime.now()

    if hour_limits[1].hour < hour_limits[0].hour:
        if now.hour >= hour_limits[0].hour or now.hour <= hour_limits[1].hour:
            run = True
        else:
            run = False
    else:
        if now.hour >= hour_limits[0] and now.hour <= hour_limits[1].hour:
            run = True
        else:
            run = False

    if run:
        

        lines = []
        with open(file_path) as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            
            # Change all parameters needed
            for param_settings in opt_param:
                    for line in lines:
                        index = lines.index(line)
                        if index == param_settings["line"] - 1:
                            split = line.split(",")
                            split[param_settings["change_pos"]] = " " + str(param_settings["current_param"])
                            line = ",".join(split)
                            lines[index] = line

        # Write to file
        with open(file_path, 'w') as file:
            for line in lines:
                file.write("%s\n" % line)


        # Run file 
        # subprocess.call("./" + file_path,shell=True)
        print("Called process")
                
                
        # Save Results

        # Change the current param
        for param_settings in opt_param:
            param_index = opt_param.index(param_settings)
            if param_index == 0:
                param_settings["current_param"] += param_settings["param_step"]

            else:
                if opt_param[param_index - 1]["current_param"] == opt_param[param_index - 1]["max_val"]:
                    # Reset last index's parameters
                    opt_param[param_index - 1]["current_param"] = opt_param[param_index - 1]["starting_param"]

                    # Add step to the current index's current parameter
                    opt_param[param_index]["current_param"] += opt_param[param_index]["param_step"]


        input(opt_param)
        # Check for quit condition
        if opt_param[-1]["current_param"] == opt_param[-1]["max_value"]:
            quit = True
        # Next iteration

