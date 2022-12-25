from __future__ import annotations
import pygame
from typing import Tuple, List
import copy
import random
from colors import white, red, yellow, orange, green, blue, grey, black
from random import randint, choice
from matrix import matrix_multiplication, rotation_x, rotation_z, rotation_y, rotation_x_reverse, rotation_y_reverse, rotation_z_reverse
from matrix import draw_matrix, rotate_for_draw
from matrix import rotation_x_speed, rotation_z_speed, rotation_y_speed, rotation_x_reverse_speed, rotation_y_reverse_speed, rotation_z_reverse_speed
from rubiks_cube_nets import solved_cube_net, cross_on_yellow_net, cross_on_white_net, corners_solved_net, first_two_layers_solved_net, oll_dot_net, oll_solved_net, solved_cube_net_white_up, all_black_net
from algs import pll_algs, sexy_move, oll_corners_algs, rotate_edges_alg, insert_edge_alg, swap_corners_alg, rotate_corner_alg
from itertools import permutations
from opposite_move import opposite_moves
from rubiks_cube_states import Rubiks_cube_states
from advice import Advice

class Helper_for_oll:
	def __init__(self, wrongly_flipped_edges, wrongly_flipped_corners) -> None:
		self.wrongly_flipped_edges = wrongly_flipped_edges
		self.wrongly_flipped_corners = wrongly_flipped_corners

	def two_unflipped_edges(self, wrongly_flipped_edges):
		if "front" in wrongly_flipped_edges and "back" in wrongly_flipped_edges:
			return Advice("DO EDGE ROTATE ALGORITHM", rotate_edges_alg)

		if "left" in wrongly_flipped_edges and "right" in wrongly_flipped_edges:
			return Advice("ROTATE LINE TO RIGHT POSITION", [], ignore_u=True)

		if "front" in wrongly_flipped_edges and "right" in wrongly_flipped_edges:
			return Advice("DO EDGE ROTATE ALGORITHM", rotate_edges_alg)

		return Advice("ROTATE L-SHAPE TO RIGHT POSITION", [], ignore_u=True)

	def all_edges_correct(self):
		if len(self.wrongly_flipped_corners) == 0:
			return Advice("OLL SOLVED. CONGRATULATION", [], done=True)

		if "4" in self.wrongly_flipped_corners:
			return Advice("DO CORNER ROTATE ALG UNTIL IT IS SOLVED", rotate_corner_alg) #there is bug

		return Advice("ROTATE ANOTHER CORNER TO RIGHT SPOT", [], ignore_u=True)

	def no_edges_correct(self):
		return Advice("DO EDGE ROTATE ALGORITHM", rotate_edges_alg)

	def get_advice(self):
		if len(self.wrongly_flipped_edges) == 4:
			return self.no_edges_correct()

		if len(self.wrongly_flipped_edges) == 2:
			return self.two_unflipped_edges(self.wrongly_flipped_edges)

		if len(self.wrongly_flipped_edges) == 0:
			return self.all_edges_correct()

		raise NotImplementedError()





#-----------------------------------------------------------------------------------------------------------------

import unittest

class TestStringMethods(unittest.TestCase):
	def test_two_unflipped_edges_line_right(self):
		helper = Helper_for_oll(["back", "front"], [])
		advice = helper.get_advice()
		test_advice = Advice("DO EDGE ROTATE ALGORITHM", rotate_edges_alg, ignore_u = False, done = False)
		self.assertEqual(advice, test_advice)    

	def test_two_unflipped_edges_line_wrong(self):
		helper = Helper_for_oll(["left", "right"], [])
		advice = helper.get_advice()
		test_advice = Advice("ROTATE LINE TO RIGHT POSITION", [], ignore_u = True, done = False)
		self.assertEqual(advice, test_advice)  

	def test_two_unflipped_edges_l_shape_wrong(self):
		helper = Helper_for_oll(["front", "left"], [])
		advice = helper.get_advice()
		test_advice = Advice("ROTATE L-SHAPE TO RIGHT POSITION", [], ignore_u = True, done = False)
		self.assertEqual(advice, test_advice)  

	def test_two_unflipped_edges_l_shape_right(self):
		helper = Helper_for_oll(["front", "right"], [])
		advice = helper.get_advice()
		test_advice = Advice("DO EDGE ROTATE ALGORITHM", rotate_edges_alg, ignore_u = False, done = False)
		self.assertEqual(advice, test_advice) 
        

if __name__ == '__main__':
    unittest.main()