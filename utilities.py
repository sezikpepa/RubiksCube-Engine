import pygame
import datetime
import pygame
from colors import white, red, yellow, orange, green, blue, grey, black, lime
from typing import Tuple

from rubiks_cube_structures import Rubiks_cube_net
from rubiks_cube_nets import empty_net, pll_corners_solved, solved_cube_net
from opposite_move import opposite_moves

import copy



class Button:
    def __init__(self, x: int, y: int, width: int, height: int, color, text: str, border_radius: int, border_color=black) -> None:
        if not isinstance(x, int):
            raise TypeError(f"ERROR: variable x has to be int -> {x}")
        if not isinstance(y, int):
            raise TypeError(f"ERROR: variable y has to be int -> {y}")
        if not isinstance(width, int):
            raise TypeError(f"ERROR: variable width has to be int -> {width}")
        if not isinstance(height, int):
            raise TypeError(f"ERROR: variable height has to be int -> {height}")
        if not isinstance(text, str):
            raise TypeError(f"ERROR: variable text has to be str -> {text}")
        if not isinstance(border_radius, int):
            raise TypeError(f"ERROR: variable border_radius has to be int -> {border_radius}")

        if x < 0:
            raise ValueError(f"ERROR: variable x can not be negative -> {x}")
        if y < 0:
            raise ValueError(f"ERROR: variable y can not be negative -> {y}")
        if width < 0:
            raise ValueError(f"ERROR: variable width can not be negative -> {width}")
        if height < 0:
            raise ValueError(f"ERROR: variable height can not be negative -> {height}")
        if border_radius < 0:
            raise ValueError(f"ERROR: variable border_radius can not be negative -> {border_radius}")

        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.color = color
        self.text: str = text
        self.keep_pressed: bool = False
        self.border_radius: int = border_radius
        self.border_color = border_color

    def draw(self, screen: pygame.Surface) -> None:
        if not isinstance(screen, pygame.Surface):
            raise TypeError(f"ERROR: variable screen has to be type pygame.Surface")

        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), border_radius = self.border_radius)
        pygame.draw.rect(screen, self.color, (self.x + 2, self.y + 2, self.width - 4, self.height - 4), border_radius = self.border_radius)

        font = pygame.font.SysFont(None, 35)
        img = font.render(self.text, True, black)
        text_size = img.get_size()
        x_for_print = self.x + ((self.width - text_size[0]) // 2)
        y_for_print = self.y + ((self.height - text_size[1]) // 2)
        screen.blit(img, (x_for_print, y_for_print))

    def clicked_check(self, mouse_position: Tuple[int]) -> bool:
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

        return self.x < mouse_position[0] < self.x + self.width and self.y < mouse_position[1] < self.y + self.height


class Net_inserter:
    def __init__(self, x: int, y: int, color_pickers_size: int, color_pickers_x: int, color_pickers_y: int, net_scale=50):
        if not isinstance(x, int):
            raise TypeError(f"ERROR: variable x has to be int -> {x}")
        if not isinstance(y, int):
            raise TypeError(f"ERROR: variable y has to be int -> {y}")
        if not isinstance(color_pickers_size, int):
            raise TypeError(f"ERROR: variable color_pickers_size has to be int -> {color_pickers_size}")
        if not isinstance(color_pickers_x, int):
            raise TypeError(f"ERROR: variable color_pickers_x has to be int -> {color_pickers_x}")
        if not isinstance(color_pickers_y, int):
            raise TypeError(f"ERROR: variable color_pickers_y has to be int -> {color_pickers_y}")
        if not isinstance(net_scale, int):
            raise TypeError(f"ERROR: variable net_scale has to be int -> {net_scale}")

        if x < 0:
            raise ValueError(f"ERROR: variable x cannot be negative -> {x}")
        if y < 0:
            raise ValueError(f"ERROR: variable y cannot be negative -> {y}")
        if color_pickers_size < 0:
            raise ValueError(f"ERROR: variable color_pickers_size cannot be negative -> {color_pickers_size}")
        if color_pickers_x < 0:
            raise ValueError(f"ERROR: variable color_pickers_x cannot be negative -> {color_pickers_x}")
        if color_pickers_y < 0:
            raise ValueError(f"ERROR: variable color_pickers_y cannot be negative -> {color_pickers_y}")
        if net_scale < 0:
            raise ValueError(f"ERROR: variable net_scale cannot be negative -> {net_scale}")


        self.color_pickers_size: int = color_pickers_size
        self.valid: bool = False

        self.x: int = x
        self.y: int = y

        self.net_scale: int = net_scale

        self.color_pickers_x: int = color_pickers_x
        self.color_pickers_y: int = color_pickers_y

        self.color_picked: str = None

        self.net: Rubiks_cube_net = Rubiks_cube_net(self.x, self.y, copy.deepcopy(empty_net), self.net_scale)

        self.choose_white_button = Button(self.color_pickers_x + self.color_pickers_size * 0, self.color_pickers_y, self.color_pickers_size, self.color_pickers_size, white, "", 5)
        self.choose_yellow_button = Button(self.color_pickers_x + self.color_pickers_size * 1, self.color_pickers_y, self.color_pickers_size, self.color_pickers_size, yellow, "", 5)
        self.choose_orange_button = Button(self.color_pickers_x + self.color_pickers_size * 2, self.color_pickers_y, self.color_pickers_size, self.color_pickers_size, orange, "", 5)
        self.choose_red_button = Button(self.color_pickers_x + self.color_pickers_size * 3, self.color_pickers_y, self.color_pickers_size, self.color_pickers_size, red, "", 5)
        self.choose_green_button = Button(self.color_pickers_x + self.color_pickers_size * 4, self.color_pickers_y, self.color_pickers_size, self.color_pickers_size, green, "", 5)
        self.choose_blue_button = Button(self.color_pickers_x + self.color_pickers_size * 5, self.color_pickers_y, self.color_pickers_size, self.color_pickers_size, blue, "", 5)
       
    def check_validity(self) -> bool:
        validity = self.net.check_validity()
        self.valid = validity

        return validity

    def draw(self, screen: pygame.Surface) -> None:
        if not isinstance(screen, pygame.Surface):
            raise TypeError(f"ERROR: variable screen has to be type pygame.Surface")

        self.net.draw(screen)

        self.choose_white_button.draw(screen)
        self.choose_yellow_button.draw(screen)
        self.choose_orange_button.draw(screen)
        self.choose_red_button.draw(screen)
        self.choose_blue_button.draw(screen)
        self.choose_green_button.draw(screen)

    def color_input(self, mouse_position: Tuple) -> None:
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

        if self.choose_white_button.clicked_check(mouse_position):
            self.color_picked = "white"
        elif self.choose_yellow_button.clicked_check(mouse_position):
            self.color_picked = "yellow"
        elif self.choose_orange_button.clicked_check(mouse_position):
            self.color_picked = "orange"
        elif self.choose_red_button.clicked_check(mouse_position):
            self.color_picked = "red"
        elif self.choose_green_button.clicked_check(mouse_position):
            self.color_picked = "green"
        elif self.choose_blue_button.clicked_check(mouse_position):
            self.color_picked = "blue"

    def box_clicked(self, mouse_position: Tuple) -> None:
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

        relative_x = (mouse_position[0] - self.x) // self.net_scale
        relative_y = (mouse_position[1] - self.y) // self.net_scale

        if 0 <= relative_x <= 8 and 0 <= relative_y <= 11:
            if self.net.faces[relative_y][relative_x] and self.color_picked:
                self.net.faces[relative_y][relative_x] = self.color_picked

    def reset(self) -> None:
        self.valid = False
        self.color_picked = None
        self.net = Rubiks_cube_net(self.x, self.y, copy.deepcopy(empty_net), self.net_scale)

    def show_invalid_state(self) -> None:
        self.net.border_color = red


class Info_window:
    def __init__(self, x: int, y: int, width: int, height: int, color, text: str, hide: bool):
        if not isinstance(x, int):
            raise TypeError(f"ERROR: variable x has to be int -> {x}")
        if not isinstance(y, int):
            raise TypeError(f"ERROR: variable y has to be int -> {y}")
        if not isinstance(width, int):
            raise TypeError(f"ERROR: variable width has to be int -> {width}")
        if not isinstance(height, int):
            raise TypeError(f"ERROR: variable height has to be int -> {height}")
        if not isinstance(text, str):
            raise TypeError(f"ERROR: variable text has to be str -> {text}")
        if not isinstance(hide, bool):
            raise TypeError(f"ERROR: variable hide has to be bool -> {hide}")

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
        self.text: str = text

        self.hide: bool = hide

    def reset(self) -> None:
        self.text = ""

    def draw(self, screen: pygame.Surface):
        if not isinstance(screen, pygame.Surface):
            raise TypeError(f"ERROR: variable screen has to be pygame.Surface")

        pygame.draw.rect(screen, "black", (self.x, self.y, self.width, self.height))

        if self.hide == False:
            pygame.draw.rect(screen, self.color, (self.x + 2, self.y + 2, self.width - 4, self.height - 4))
            font = pygame.font.SysFont(None, 35)
            img = font.render(self.text, True, black)
            text_size = img.get_size()
            x_for_print = self.x + ((self.width - text_size[0]) // 2)
            y_for_print = self.y + ((self.height - text_size[1]) // 2)
            screen.blit(img, (x_for_print, y_for_print))

        else:
            pygame.draw.rect(screen, "black", (self.x + 2, self.y + 2, self.width - 4, self.height - 4))

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


#-----------------------------------------------------------------------------------------------------------------

import unittest

class TestStringMethods(unittest.TestCase):
    #BUTTONS
    def test_button_clicked_check(self):
        button = Button(100, 200, 50, 100, blue, "TEST", 50)
        self.assertTrue(button.clicked_check((101, 201)))

        button = Button(100, 200, 50, 100, blue, "TEST", 50)
        self.assertFalse(button.clicked_check((99, 201)))

        with self.assertRaises(TypeError):
            button = Button(100, 200, 50, 100, blue, "TEST", 50)
            self.assertFalse(button.clicked_check((99, "x")))

        with self.assertRaises(TypeError):
            button = Button(100, 200, 50, 100, blue, "TEST", 50)
            self.assertFalse(button.clicked_check([99, 101]))
        

if __name__ == '__main__':
    unittest.main()
                   







