#!/usr/bin/env python

###############
# This little script shows how to initialize communication with ALE and
# send commands to move left and right in Breakout game.
# Author: Ardi Tampuu
###############

import os
import random

# create FIFO pipes
os.system("mkfifo ale_fifo_out")
os.system("mkfifo ale_fifo_in")

# launch ALE with appropriate commands in the background
os.system('./ale -game_controller fifo_named -run_length_encoding false -display_screen true -use_starting_actions true wizard_of_wor_2player.bin &')

#oppen communication with pipes
fin  = open('ale_fifo_out')
fout = open('ale_fifo_in', 'w')

input = fin.readline()
print input
size = input[:-1].split("-")  # saves the image sizes (160*210) for breakout


# first thing we send to ALE is the output options - we want to get only image data (hence the zeros)
fout.write("1,0,0,1\n")
fout.flush()  # send the lines written to pipe

game_over = 0
while not game_over:
    img, episode_info = fin.readline()[:-2].split(":")
    episode_info = episode_info.split(",")

    reward = float(episode_info[1]) # reward obtained this timestep
    game_over = int(episode_info[0]) # sends 1 if episode ended this timestep  
    if reward > 0:
        print "Got", reward, "points"

    player_a_action = random.randint(0,17)
    player_b_action = random.randint(18,35)
    fout.write(str(player_a_action) + "," + str(player_b_action) + "\n")
    fout.flush()

fin.close()
fout.close()

