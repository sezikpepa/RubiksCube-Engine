import pygame
import datetime
import pygame
from colors import white, red, yellow, orange, green, blue, grey, black, lime
from typing import Tuple

from rubiks_cube_structures import Rubiks_cube_net
from rubiks_cube_nets import empty_net, pll_corners_solved, solved_cube_net
from opposite_move import opposite_moves

import copy


class Timer():
	def __init__(self, x: int, y: int) -> None:
		if not isinstance(x, int):
			raise TypeError(f"ERROR: variable x has to be int -> {x}")
		if not isinstance(y, int):
			raise TypeError(f"ERROR: variable y has to be int -> {y}")
		if x < 0:
			raise ValueError(f"ERROR: variable x has to be positive number -> {x}")
		if y < 0:
			raise ValueError(f"ERROR: variable y has to be positive number -> {y}")

		self.utc_start: datetime.datetime = None
		self.time_since: datetime.datetime = None
		self.final_time: datetime.datetime = None
		self.x: int = x
		self.y: int = y

	def reset(self) -> None:
		self.utc_start = None
		self.final_time = None

	def start(self) -> None:
		if not self.utc_start:
			self.utc_start = datetime.datetime.utcnow()

	def stop(self) -> None:
		if self.utc_start:
			self.final_time = datetime.datetime.utcnow()

	def current_timer_time(self) -> datetime.timedelta:
		if self.final_time:
			return self.final_time - self.utc_start
		now = datetime.datetime.utcnow()
		return now - self.utc_start

	def get_time_parts(self, seconds: float):
		if not isinstance(seconds, float):
			raise TypeError(f"ERROR: seconds has to be float -> {seconds}")

		hours = int(seconds // 3600)
		rest = seconds % 3600
		
		minutes = int(rest // 60)
		rest = rest % 60

		seconds = int(rest)
		miliseconds = int((rest - seconds) * 100)

		return hours, minutes, seconds, miliseconds

		
	def draw(self, screen: pygame.Surface) -> None:
		if not isinstance(screen, pygame.Surface):
			raise TypeError(f"ERROR: variable screen has to be type pygame.Surface")

		if self.utc_start:
			time_on_timer = self.__str__()
			font = pygame.font.SysFont(None, 100)
			img = font.render(time_on_timer, True, black)
			screen.blit(img, (self.x, self.y))

		else:
			time_on_timer = "00:00:00.00"
			font = pygame.font.SysFont(None, 100)
			img = font.render(time_on_timer, True, black)
			screen.blit(img, (self.x, self.y))

	def __str__(self) -> str:
		if self.utc_start:
			current_time = self.current_timer_time()
			current_time = current_time.total_seconds()
			hours, minutes, seconds, miliseconds = self.get_time_parts(current_time)
			return f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}.{miliseconds:0>2}"
	
		return "Timer does not count time right now"




#-----------------------------------------------------------------------------------------------------------------

import unittest

class TestStringMethods(unittest.TestCase):
	def test_get_time_parts(self):
		timer = Timer(10, 10)
		hours, minutes, seconds, miliseconds = timer.get_time_parts(124589.58)
		self.assertEqual(hours, 34)
		self.assertEqual(minutes, 36)
		self.assertEqual(seconds, 29)
		self.assertEqual(miliseconds, 58)

	def test_current_timer_time(self):
		pass
	

	def test___str___timer_is_not_started(self):
		timer = Timer(10, 10)
		text = str(timer)

		self.assertEqual(text, "Timer does not count time right now")

	def test___str___timer_stopped(self):
		timer = Timer(10, 10)
		timer.utc_start = datetime.timedelta(seconds = 5.26)
		timer.final_time = datetime.timedelta(seconds = 7.98)
		text = str(timer)
		self.assertEqual(text, "00:00:02.72")

	def test___str___timer_running(self):
		pass
	   

if __name__ == '__main__':
	unittest.main()

		