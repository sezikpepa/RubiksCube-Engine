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
from move_creator import Move_creator
from help_for_oll import Helper_for_oll
from help_for_pll import Helper_for_pll
from advice import Advice
from parts_solved import Parts_solved
from timer import Timer
from algorithm_helper import Algorithm_helper


from project_settings import speed, shift, net_scale, scale, net_x, net_y, fps, cube_position, window_width, window_height, window_caption



class Program_handler:
	def __init__(self) -> None:

		pygame.init()
		pygame.display.set_caption(window_caption)
		self.screen = pygame.display.set_mode((window_width, window_height))
		self.clock = pygame.time.Clock()

		self.rubiks_cube_player = Rubiks_cube(shift, net_scale, net_x, net_y)

		#BUTTONS
		self.cross_practice_button = Button(250, 620, 350, 40, blue, "CROSS PRACTICE", 50)
		self.first_layer_practice_button = Button(250, 670, 350, 40, tyrkis, "FIRST LAYER PRACTICE", 50)
		self.second_layer_practice_button = Button(250, 720, 350, 40, violet, "SECOND LAYER PRACTICE", 50)
		self.oll_practice_button = Button(250, 770, 350, 40, pink, "OLL PRACTICE", 50)
		self.pll_practice_button = Button(250, 820, 350, 40, dark_green, "PLL PRACTICE", 50)
		self.shuffle_button = Button(250, 870, 350, 40, bage, "SHUFFLE", 50)
		self.reset_button = Button(250, 920, 350, 40, red, "RESET", 50)

		self.insert_own_button = Button(1350, 920, 350, 40, blue, "INSERT OWN", 50)
		self.confirm_insert_button = Button(1350, 870, 350, 40, green, "CONFIRM", 50)

		#TIMER
		self.timer = Timer(1300, 150)

		#MOVE CREATOR
		self.move_creator = Move_creator()

		#INSERTER
		self.net_inserter = Net_inserter(1385, 450, 40, 1400, 820, net_scale=30)

		#EVENT HANDLER
		self.event_handler = Event_Handler()

		self.keep_inserter_shown: bool = False

		self.algorithm_helper = Algorithm_helper(800, 840, 500, 100, white, [])
		self.info_window = Info_window(700, 100, 600, 50, white, "", False)

		self.parts_solved_info = Parts_solved(1320, 400)

		self.run = True

	def check_inputs(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.run = False

			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.process_mouse_inputs()

			elif event.type == pygame.KEYDOWN:
				self.process_keyboard_inputs(event)

	def process_keyboard_inputs(self, event):
		if not self.rubiks_cube_player.user_moves_blocked:
			print(pygame.key.get_mods(), pygame.KMOD_CTRL, pygame.KMOD_SHIFT)
			try:
				move = self.move_creator.get_move(event, pygame.key.get_mods(), pygame.KMOD_CTRL, pygame.KMOD_SHIFT)
			except KeyError:
				return

			self.rubiks_cube_player.add_move(move)
			if not self.algorithm_helper.locked and self.rubiks_cube_player.mode != Rubiks_cube_states.NOTHING:
				self.algorithm_helper.add_move(move)


	def process_mouse_inputs(self):
		mouse_position = pygame.mouse.get_pos()
		if self.reset_button.clicked_check(mouse_position):
			self.reset()

		elif self.cross_practice_button.clicked_check(mouse_position):
			self.rubiks_cube_player = Rubiks_cube(shift, net_scale, net_x, net_y, mode=Rubiks_cube_states.CROSS)
			self.insert_own_button.keep_pressed = False

		elif self.first_layer_practice_button.clicked_check(mouse_position):
			self.rubiks_cube_player = Rubiks_cube(shift, net_scale, net_x, net_y, mode=Rubiks_cube_states.FIRST_LAYER)
			self.insert_own_button.keep_pressed = False

		elif self.second_layer_practice_button.clicked_check(mouse_position):
			self.rubiks_cube_player = Rubiks_cube(shift, net_scale, net_x, net_y, mode=Rubiks_cube_states.SECOND_LAYER)
			self.insert_own_button.keep_pressed = False

		elif self.oll_practice_button.clicked_check(mouse_position):
			self.rubiks_cube_player = Rubiks_cube(shift, net_scale, net_x, net_y, mode=Rubiks_cube_states.OLL)
			self.algorithm_helper.reset()
			self.info_window.reset()
			self.insert_own_button.keep_pressed = False

		elif self.pll_practice_button.clicked_check(mouse_position):
			self.rubiks_cube_player = Rubiks_cube(shift, net_scale, net_x, net_y, mode=Rubiks_cube_states.PLL)
			self.algorithm_helper.reset()
			self.info_window.reset()
			self.insert_own_button.keep_pressed = False

		elif self.shuffle_button.clicked_check(mouse_position):
			self.rubiks_cube_player = Rubiks_cube(shift, net_scale, net_x, net_y)
			self.rubiks_cube_player.new_scramble()
			self.rubiks_cube_player.scrambling = True
			self.algorithm_helper.reset()
			self.info_window.reset()
			self.timer.reset()
			self.insert_own_button.keep_pressed = False

		if self.insert_own_button.clicked_check(mouse_position) and not self.insert_own_button.keep_pressed and not self.rubiks_cube_player.shuffled:
			self.insert_own_button.keep_pressed = True
			self.insert_own_button.text = "CLOSE"
		
		elif self.insert_own_button.clicked_check(mouse_position) and self.insert_own_button.keep_pressed:
			self.insert_own_button.keep_pressed = False
			self.insert_own_button.text = "INSERT OWN"
		
		if self.confirm_insert_button.clicked_check(mouse_position):
			if self.net_inserter.check_validity() and not self.rubiks_cube_player.shuffled:
				self.reset()

				self.rubiks_cube_player = Rubiks_cube(shift, net_scale, net_x, net_y, mode=Rubiks_cube_states.NOTHING)
				self.rubiks_cube_player.insert_own_net(self.net_inserter.net)
				self.rubiks_cube_player.shuffled = True
			else:
				self.net_inserter.show_invalid_state()
			
		self.algorithm_helper.clicked_check(mouse_position)
		self.info_window.clicked_check(mouse_position)
		self.net_inserter.color_input(mouse_position)
		self.net_inserter.box_clicked(mouse_position)

	def reset(self):
		self.rubiks_cube_player.reset_waiting = True
		self.algorithm_helper.reset()
		self.info_window.reset()
		self.timer.reset()
		self.net_inserter.reset()
		self.insert_own_button.keep_pressed = False
		self.insert_own_button.text = "INSERT OWN"

	def draw(self):
		self.rubiks_cube_player.draw(self.screen, scale, cube_position)

		if self.insert_own_button.keep_pressed:
			self.net_inserter.draw(self.screen)
			self.confirm_insert_button.draw(self.screen)

		if self.rubiks_cube_player.mode == Rubiks_cube_states.OLL or self.rubiks_cube_player.mode == Rubiks_cube_states.PLL:
			self.algorithm_helper.draw(self.screen)

		if self.rubiks_cube_player.mode != Rubiks_cube_states.NOTHING:
			self.info_window.draw(self.screen)

		if self.rubiks_cube_player.shuffled and self.rubiks_cube_player.mode == Rubiks_cube_states.NOTHING:
			self.parts_solved_info.draw(self.screen)
		
		if self.rubiks_cube_player.mode == Rubiks_cube_states.NOTHING and self.rubiks_cube_player.shuffled:
			self.timer.draw(self.screen)

		self.draw_buttons()

		pygame.display.update()


	def draw_buttons(self):
		self.reset_button.draw(self.screen)
		self.cross_practice_button.draw(self.screen)
		self.shuffle_button.draw(self.screen)
		self.first_layer_practice_button.draw(self.screen)
		self.second_layer_practice_button.draw(self.screen)
		self.oll_practice_button.draw(self.screen)
		self.pll_practice_button.draw(self.screen)

		if not self.rubiks_cube_player.shuffled:
			self.insert_own_button.draw(self.screen)

	def parts_solved_info_things(self):
		if self.rubiks_cube_player.net.solved_check() and self.rubiks_cube_player.shuffled and not self.rubiks_cube_player.scrambling:
			self.parts_solved_info.pll_solved(str(self.timer))

		elif self.rubiks_cube_player.net.oll_check() and self.rubiks_cube_player.shuffled and not self.rubiks_cube_player.scrambling:
			self.parts_solved_info.oll_solved(str(self.timer))

		elif self.rubiks_cube_player.net.second_layer_check() and self.rubiks_cube_player.shuffled and not self.rubiks_cube_player.scrambling:
			self.parts_solved_info.first_two_layers_solved(str(self.timer))

		elif self.rubiks_cube_player.net.first_layer_check() and self.rubiks_cube_player.shuffled and not self.rubiks_cube_player.scrambling:
			self.parts_solved_info.first_layer_solved(str(self.timer))

		elif self.rubiks_cube_player.net.white_cross_check() and self.rubiks_cube_player.shuffled and not self.rubiks_cube_player.scrambling:
			self.parts_solved_info.cross_solved(str(self.timer))

	def reset_screen(self):
		self.screen.fill(grey)

	def set_things_after_advice(self, advice):
		self.algorithm_helper.ingore_u = advice.ignore_u
		self.info_window.text = advice.message
		self.algorithm_helper.algorithm = advice.alg

		if(advice.done == True):
			self.rubiks_cube_player.user_moves_blocked = True

	def work(self):
		while self.run:
			self.clock.tick(fps)
			self.reset_screen()

			self.check_inputs()
			self.parts_solved_info_things()
				
			#CUBE THINGS
			if self.rubiks_cube_player.reset_waiting and not self.rubiks_cube_player.move_in_progress:
				self.rubiks_cube_player = Rubiks_cube(shift, net_scale, net_x, net_y)

			if not self.rubiks_cube_player.scrambling:
				self.rubiks_cube_player.do_next_move()
			else:
				self.rubiks_cube_player.scramble()

			
			if self.rubiks_cube_player.net.solved_check():
				self.timer.stop() #BUG
				self.rubiks_cube_player.user_moves_blocked = True

			if self.rubiks_cube_player.mode == Rubiks_cube_states.NOTHING and self.rubiks_cube_player.shuffled:
				self.timer.start()

			#INFO WINDOW
			if self.rubiks_cube_player.mode == Rubiks_cube_states.PLL and not self.rubiks_cube_player.scrambling:
				#CORNERS
				if not (self.algorithm_helper.moves or self.rubiks_cube_player.moves_buffer):
					adjacent_corners_positions = self.rubiks_cube_player.net.mode_five_hinter_corners()
					line_positions = self.rubiks_cube_player.net.mode_five_hinter_edges()
					pll_helper = Helper_for_pll(adjacent_corners_positions, line_positions)
					advice = pll_helper.get_advice()

					self.set_things_after_advice(advice)

					

			elif self.rubiks_cube_player.mode == Rubiks_cube_states.OLL and not self.rubiks_cube_player.scrambling:
				if not (self.algorithm_helper.moves or self.rubiks_cube_player.moves_buffer):
					wrongly_flipped_edges = self.rubiks_cube_player.net.mode_four_hinter_edges()
					wrongly_flipped_corners = self.rubiks_cube_player.net.mode_four_hinter_corners()
					helper_for_oll = Helper_for_oll(wrongly_flipped_edges, wrongly_flipped_corners)
					advice = helper_for_oll.get_advice()

					self.set_things_after_advice(advice)				
					

			elif self.rubiks_cube_player.mode == Rubiks_cube_states.CROSS and not self.rubiks_cube_player.scrambling:
				if not self.rubiks_cube_player.moves_buffer and self.rubiks_cube_player.net.white_cross_check():
					self.info_window.text = "DONE. CONGRATULATION"
					self.rubiks_cube_player.user_moves_blocked = True

			elif self.rubiks_cube_player.mode == Rubiks_cube_states.FIRST_LAYER and not self.rubiks_cube_player.scrambling:
				if not self.rubiks_cube_player.moves_buffer and self.rubiks_cube_player.net.white_cross_check() and self.rubiks_cube_player.net.first_layer_check():
					self.info_window.text = "DONE. CONGRATULATION"
					self.rubiks_cube_player.user_moves_blocked = True

			elif self.rubiks_cube_player.mode == Rubiks_cube_states.SECOND_LAYER and not self.rubiks_cube_player.scrambling:
				if not self.rubiks_cube_player.moves_buffer and self.rubiks_cube_player.net.white_cross_check() and self.rubiks_cube_player.net.first_layer_check() and self.rubiks_cube_player.net.second_layer_check():
					self.info_window.text = "DONE. CONGRATULATION"
					self.rubiks_cube_player.user_moves_blocked = True
			
			
			#ALGORITHM HELPER
			self.algorithm_helper.alg_done_check()

			self.draw()
			
			
		pygame.quit()