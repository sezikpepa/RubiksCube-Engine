import pygame
import datetime
import pygame
from colors import white, red, yellow, orange, green, blue, grey, black, lime
from typing import Tuple

from rubiks_cube_structures import Rubiks_cube_net
from rubiks_cube_nets import empty_net, pll_corners_solved, solved_cube_net
from opposite_move import opposite_moves
from move_creator import Move_creator

import copy


class Algorithm_helper:
	def __init__(self, x: int, y: int, width: int, height: int, color, algorithm: list, locked: bool = False):
		if not isinstance(x, int):
			raise TypeError(f"ERROR: variable x has to be int -> {x}")
		if not isinstance(y, int):
			raise TypeError(f"ERROR: variable y has to be int -> {y}")
		if not isinstance(width, int):
			raise TypeError(f"ERROR: variable width has to be int -> {width}")
		if not isinstance(height, int):
			raise TypeError(f"ERROR: variable height has to be int -> {height}")
		if not isinstance(algorithm, list):
			raise TypeError(f"ERROR: variable algorithm has to be list -> {algorithm}")
		if not isinstance(locked, bool):
			raise TypeError(f"ERROR: variable algorithm has to be bool -> {locked}")

		if x < 0:
			raise ValueError(f"ERROR: variable x can not be negative -> {x}")
		if y < 0:
			raise ValueError(f"ERROR: variable y can not be negative -> {y}")
		if width < 0:
			raise ValueError(f"ERROR: variable width can not be negative -> {width}")
		if height < 0:
			raise ValueError(f"ERROR: variable height can not be negative -> {height}")

		self.x: int = x
		self.y: int = y
		self.width: int = width
		self.height: int = height
		self.color = color
		self.algorithm: list = algorithm
		self.moves: list = []

		self.locked: bool = locked

		self.ingore_u: bool = False
		self.hide: bool = False

		self.move_creator = Move_creator()


	def reset(self) -> None:
		self.locked = False
		self.algorithm = []
		self.moves = []

	def alg_done_check(self) -> None:
		if self.moves == self.algorithm and len(self.algorithm) > 0:
			self.reset()
	
	def add_move(self, move: str) -> None:
		if not isinstance(move, str):
			raise TypeError(f"ERROR: variable move has to be string -> {move}")
		if not self.algorithm and self.ingore_u and (move == "u" or move == "u2" or move == "u’" or move == "y" or move == "y’") and not self.moves:
			return
		elif self.algorithm and not self.moves and (move == "u" or move == "u2" or move == "u’" or move == "y" or move == "y’"):
			self.reset()
			return

		self.moves.append(move)
		self.check_for_shorter()

	def double_and_normal_shorter(self, normal_move) -> None:
		self.moves = self.moves[:-2]
		if normal_move == "’":			
			self.moves.append(self.move_creator.get_clockwise_move(normal_move))
		else:
			self.moves.append(self.move_creator.get_counter_clockwise_move(normal_move))

	def check_for_shorter(self) -> None:	 #check if wrong moves can be shortened. For example U2 and U’ to U
		changed = True
		while changed:
			changed = False
			if len(self.moves) >= 2:
				if self.moves[-1] == self.moves[-2]:
					if not self.move_creator.is_double(self.moves[-1]):
						changed = True
						new_move = self.move_creator.get_double_move(self.moves[-1])
						self.moves = self.moves[:-2]
						self.moves.append(new_move)
						continue
					
					changed = True
					self.moves = self.moves[:-2]
					continue

				if self.move_creator.is_same_face_move(self.moves[-1], self.moves[-2]):
					changed = True
					if self.move_creator.is_double(self.moves[-1]) and not self.move_creator.is_double(self.moves[-2]):
						almost_last_move = self.moves[-2]
						self.double_and_normal_shorter(almost_last_move)
						continue

					if not self.move_creator.is_double(self.moves[-1]) and self.move_creator.is_double(self.moves[-2]):
						last_move = self.moves[-1]
						self.double_and_normal_shorter(last_move)
	   
	def clicked_check(self, mouse_position: Tuple[int]) -> None:
		if not isinstance(mouse_position, Tuple):
			raise TypeError(f"ERROR: variable mouse_position has to be tuple -> {mouse_position}")
		if len(mouse_position) != 2:
			raise TypeError(f"ERROR: variable mouse_position has to have two elements -> {mouse_position}")
		if not isinstance(mouse_position[0], int):
			raise TypeError(f"ERROR: variable mouse_position can include only ints -> {mouse_position[0]}")
		if not isinstance(mouse_position[1], int):
			raise TypeError(f"ERROR: variable mouse_position can include only ints -> {mouse_position[1]}")
		if mouse_position[0] < 0:
			raise ValueError(f"ERROR: variable mouse_position can include only positive numbers -> {mouse_position[0]}")
		if mouse_position[1] < 0:
			raise ValueError(f"ERROR: variable mouse_position can include only positive numbers -> {mouse_position[1]}")

		if self.x < mouse_position[0] < self.x + self.width and self.y < mouse_position[1] < self.y + self.height:
			if self.hide:
				self.hide = False
			else:
				self.hide = True


	def draw(self, screen) -> None:
		if not isinstance(screen, pygame.Surface):
			raise TypeError(f"ERROR: variable screen has to be pygame.Surface")

		pygame.draw.rect(screen, "black", (self.x, self.y, self.width, self.height))

		if not self.hide:
			pygame.draw.rect(screen, self.color, (self.x + 2, self.y + 2, self.width - 4, self.height - 4))

			length_min = min([len(self.algorithm), len(self.moves)])
			length_max = max([len(self.algorithm), len(self.moves)])
			moves_first = []
			moves_second = []
			mistake_found = False
			for i in range(length_min):
				if not mistake_found:
					move = self.moves[i]
					if move == self.algorithm[i]:
						moves_first.append(move.capitalize())
					else:
						moves_second.append(move.capitalize())
						mistake_found = True

				else:
					move = self.moves[i]
					moves_second.append(move.capitalize())

			if len(self.moves) > len(self.algorithm):
				for element in self.moves[length_min:length_max]:
					moves_second.append(element.capitalize())

			#ALG
			algorithm_for_print = ""
			for element in self.algorithm:
				algorithm_for_print += element.capitalize()
				algorithm_for_print += " "

			font = pygame.font.SysFont(None, 45)
			img = font.render(algorithm_for_print, True, black)
			screen.blit(img, (self.x + 15, self.y + 15))

			#MOVES
			if len(moves_second) > 20:
				moves_second = moves_second[:20]
				moves_first = []
			elif len(moves_first) + len(moves_second) > 20:
				moves_first = moves_first[20 - len(moves_second):20]

			moves_first_print = ""
			for element in moves_first:
				moves_first_print += element
				moves_first_print += " "

			moves_second_print = ""
			for element in moves_second:
				moves_second_print += element
				moves_second_print += " "

			font = pygame.font.SysFont(None, 45)
			img1 = font.render(moves_first_print, True, green)
			  
			font = pygame.font.SysFont(None, 45)
			img2 = font.render(moves_second_print, True, red)

			screen.blit(img1, (self.x + 15, self.y + 55))
			screen.blit(img2, (self.x + 15 + img1.get_size()[0], self.y + 55))



#-----------------------------------------------------------------------------------------------------------------

import unittest

class TestStringMethods(unittest.TestCase):

	def test_algorithm_helper_check_for_shorter(self):
		algorithm_helper = Algorithm_helper(10, 10, 10, 10, "black", [])
		algorithm_helper.add_move("x")
		algorithm_helper.add_move("x")
		algorithm_helper.check_for_shorter()
		self.assertEqual(algorithm_helper.moves, ["x2"])

		algorithm_helper = Algorithm_helper(10, 10, 10, 10, "black", [])
		algorithm_helper.add_move("x")
		algorithm_helper.add_move("y")
		algorithm_helper.check_for_shorter()
		self.assertEqual(algorithm_helper.moves, ["x", "y"])

		algorithm_helper = Algorithm_helper(10, 10, 10, 10, "black", [])
		algorithm_helper.add_move("r2")
		algorithm_helper.add_move("r")
		algorithm_helper.check_for_shorter()
		self.assertEqual(algorithm_helper.moves, ["r’"])

		algorithm_helper = Algorithm_helper(10, 10, 10, 10, "black", [])
		algorithm_helper.add_move("r2")
		algorithm_helper.add_move("r2")
		algorithm_helper.check_for_shorter()
		self.assertEqual(algorithm_helper.moves, [])

		algorithm_helper = Algorithm_helper(10, 10, 10, 10, "black", [])
		algorithm_helper.add_move("r")
		algorithm_helper.add_move("r2")
		algorithm_helper.check_for_shorter()
		self.assertEqual(algorithm_helper.moves, ["r’"])

		algorithm_helper = Algorithm_helper(10, 10, 10, 10, "black", [])
		algorithm_helper.add_move("x2")
		algorithm_helper.add_move("x")
		algorithm_helper.check_for_shorter()
		self.assertEqual(algorithm_helper.moves, ["x’"])

		algorithm_helper = Algorithm_helper(10, 10, 10, 10, "black", [])
		algorithm_helper.add_move("x2")
		algorithm_helper.add_move("y")
		algorithm_helper.check_for_shorter()
		self.assertEqual(algorithm_helper.moves, ["x2", "y"])

	def test_alg_done_check(self):
		algorithm_helper = Algorithm_helper(10, 10, 10, 10, "black", ["x", "r"])
		algorithm_helper.add_move("x")
		algorithm_helper.add_move("r")
		algorithm_helper.alg_done_check()
		self.assertFalse(algorithm_helper.moves)  
		self.assertFalse(algorithm_helper.algorithm)

		algorithm_helper = Algorithm_helper(10, 10, 10, 10, "black", ["x", "r"])
		algorithm_helper.ingore_u = True
		algorithm_helper.add_move("u")
		algorithm_helper.add_move("x")
		algorithm_helper.add_move("r")
		algorithm_helper.alg_done_check()
		self.assertEqual(algorithm_helper.moves, ["x", "r"])  

		algorithm_helper = Algorithm_helper(10, 10, 10, 10, "black", [])
		algorithm_helper.add_move("x")
		algorithm_helper.add_move("r")
		algorithm_helper.alg_done_check()
		self.assertEqual(algorithm_helper.moves, ["x", "r"])  
		

if __name__ == '__main__':
	unittest.main()