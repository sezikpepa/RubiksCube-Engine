import pygame
import datetime
import pygame
from colors import white, red, yellow, orange, green, blue, grey, black, lime
from typing import Tuple

from rubiks_cube_structures import Rubiks_cube_net
from rubiks_cube_nets import empty_net, pll_corners_solved, solved_cube_net
from opposite_move import opposite_moves

class Parts_solved:
    def __init__(self, x: int, y: int):
        if not isinstance(x, int):
            raise TypeError(f"ERROR: variable x has to be int -> {x}")
        if not isinstance(y, int):
            raise TypeError(f"ERROR: variable y has to be int -> {y}")     
        if x < 0:
            raise ValueError(f"ERROR: variable x can not be negative -> {x}")
        if y < 0:
            raise ValueError(f"ERROR: variable y can not be negative -> {y}")

        self.x: int = x
        self.y: int = y

        self.cross: bool = None
        self.first_layer: bool = None
        self.first_two_layers: bool = None
        self.oll: bool = None
        self.pll: bool = None

        self.font = pygame.font.SysFont(None, 65)

    def reset(self) -> None:
        self.cross: bool = None
        self.first_layer: bool = None
        self.first_two_layers: bool = None
        self.oll: bool = None
        self.pll: bool = None

    def cross_solved(self, time) -> None:
        if not self.cross:
            self.cross = time

    def first_layer_solved(self, time) -> None:
        if not self.first_layer:
            self.first_layer = time

    def first_two_layers_solved(self, time) -> None:
        if not self.first_two_layers:
            self.first_two_layers = time

    def oll_solved(self, time) -> None:
        if not self.oll:
            self.oll = time

    def pll_solved(self, time) -> None:
        if not self.pll:
            self.pll = time

    def generate_time_text(self, type, text: str):
        if type:
            return self.font.render(f"{text}: {type}", True, black)
        return self.font.render(f"{text}:", True, black)

    def draw(self, screen) -> None:
        if not isinstance(screen, pygame.Surface):
            raise TypeError(f"ERROR: variable screen has to be pygame.Surface")

        img1 = self.generate_time_text(self.cross, "Cross")
        img2 = self.generate_time_text(self.cross, "First Layer")
        img3 = self.generate_time_text(self.cross, "Second layer")
        img4 = self.generate_time_text(self.cross, "OLL")
        img5 = self.generate_time_text(self.cross, "PLL")

        x = self.x
        y = self.y

        text_size = img1.get_size()      
        screen.blit(img1, (x, y))
        y += text_size[1]
       
        text_size = img2.get_size()      
        screen.blit(img2, (x, y))
        y += text_size[1]

        text_size = img3.get_size()      
        screen.blit(img3, (x, y))
        y += text_size[1]

        text_size = img4.get_size()      
        screen.blit(img4, (x, y))
        y += text_size[1]

        text_size = img5.get_size()      
        screen.blit(img5, (x, y))