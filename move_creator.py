import pygame
import os
import math
from typing import List
from typing import Tuple
import copy
import time

from rubiks_cube_structures import Square_on_cube, Rubiks_cube_net, Cube, Rubiks_cube
from colors import white, red, yellow, orange, green, blue, grey, black, lime, bage, tyrkis, violet, pink, dark_green
from keyboard_press_translator import keyboard_press_translator
from algs import swap_corners_alg, swap_edges_alg, rotate_edges_alg, rotate_corner_alg
from event_handler import Event_Handler
from rubiks_cube_states import Rubiks_cube_states


from project_settings import speed, shift, net_scale, scale, net_x, net_y, fps, cube_position, window_width, window_height, window_caption



class Move_creator:
	def __init__(self) -> None:
		pass

	def get_move(self, event, mods, ctrl, shift):
		basic_move = keyboard_press_translator[event.key]
		if mods & ctrl:
			return self.get_counter_clockwise_move(basic_move)

		if mods & shift:
			return self.get_double_move(basic_move)

		return basic_move

	def get_counter_clockwise_move(self, move):
		return f"{move}’"

	def get_double_move(self, move):
		return f"{move}2"

	def get_clockwise_move(self, move):
		return move[:-1]

	def is_double(self, move): #not tested
		return move[-1] == "2"

	def is_clockwise(self, move): #not tested
		return move[-1] != "’"

	def is_counter_clockwise(self, move): #not tested
		return move[-1] == "’"

	def is_same_face_move(self, move1, move2): #not tested
		return move1[0] == move2[0]



#-----------------------------------------------------------------------------------------------------------------

import unittest

class TestStringMethods(unittest.TestCase):
	def test_get_counter_clockwise_move(self):
		move_creator = Move_creator()
		result = move_creator.get_counter_clockwise_move("f")
		self.assertEqual("f’", result)     

	def test_get_double_move(self):
		move_creator = Move_creator()
		result = move_creator.get_double_move("f")
		self.assertEqual("f2", result)

	#TODO
	#def test_get_move(self):
		#move_creator = Move_creator()
		#result = move_creator.get_move(4096, 192, 3)
		#self.assertEqual("f’", result)   
        

if __name__ == '__main__':
    unittest.main()

