import pygame
import os
import math
from typing import List
from typing import Tuple
import copy
import time

from rubiks_cube_structures import Square_on_cube, Rubiks_cube_net, Cube, Rubiks_cube
from colors import white, red, yellow, orange, green, blue, grey, black, lime, bage, tyrkis, violet, pink, dark_green
from utilities import Button, Net_inserter, Info_window
from keyboard_press_translator import keyboard_press_translator
from algs import swap_corners_alg, swap_edges_alg, rotate_edges_alg, rotate_corner_alg
from event_handler import Event_Handler
from rubiks_cube_states import Rubiks_cube_states
from program_handler import Program_handler
from move_creator import Move_creator

from project_settings import speed, shift, net_scale, scale, net_x, net_y, fps, cube_position, window_width, window_height, window_caption

#SETTINGS
#os.environ["SDL_VIDEO_CENTERED"] = '1'

if __name__ == "__main__":
	program = Program_handler()
	program.work()