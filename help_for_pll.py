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
from algs import pll_algs, sexy_move, oll_corners_algs, rotate_edges_alg, insert_edge_alg, swap_corners_alg, rotate_corner_alg, swap_edges_alg
from itertools import permutations
from opposite_move import opposite_moves
from rubiks_cube_states import Rubiks_cube_states
from advice import Advice

class Helper_for_pll:
	def __init__(self, adjacent_corners_position, line_positions) -> None:
		self.adjacent_corners_positions = adjacent_corners_position
		self.line_positions = line_positions

	def no_adjacent_corners(self):
		return Advice("DO ALGORITHM TO SWAP CORNERS", swap_corners_alg)

	def adjacent_corners(self):
		if self.adjacent_corners_positions[0] != "back":
			return Advice("ROTATE ADJACENT CORNERS TO BACK", [], ignore_u=True)
		else:
			return Advice("DO ALGORITHM TO SWAP CORNERS", swap_corners_alg)

	def line(self):
		if len(self.line_positions) == 1:
			if self.line_positions[0] != "front":
				return Advice("ROTATE STRIP TO FRONT", [], ignore_u=True)

			return Advice("DO EDGE SWITCH ALGORITHM", swap_edges_alg)

		elif len(self.line_positions) == 4:
			#todo auf
			if(True == True):
				return Advice("SOLVED. GONGRATULATION", [], done=True)
			else:
				return Advice("ALIGN LAST LAYER", [], ignore_u=True)

		return Advice("DO EDGE SWITCH ALGORITHM", swap_edges_alg)

	def get_advice(self):

		if len(self.adjacent_corners_positions) == 1:
			return self.adjacent_corners()

		elif len(self.adjacent_corners_positions) == 0:
			return self.no_adjacent_corners()

		else:
			return self.line()