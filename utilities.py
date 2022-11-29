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
        self.time_since = None
        self.final_time = None

    def start(self) -> None:
        if not self.utc_start:
            self.utc_start = datetime.datetime.utcnow()

    def stop(self) -> None:
        if self.utc_start:
            self.final_time = self.utc_start - datetime.datetime.utcnow()

    def evaluate_time(self) -> None:
        now = datetime.datetime.utcnow()
        self.time_since = now - self.utc_start

        
    def draw(self, screen: pygame.Surface) -> None:
        if not isinstance(screen, pygame.Surface):
            raise TypeError(f"ERROR: variable screen has to be type pygame.Surface")

        if self.utc_start:
            if not self.final_time:
                self.evaluate_time()

            time_on_timer = self.time_since.total_seconds()

            rest = time_on_timer % 3600
            hours = int(time_on_timer // 3600)
            rest = time_on_timer % 60
            minutes = int(time_on_timer // 60)
        
            rest = str(rest).split(".")
            seconds = rest[0]
            miliseconds = str(rest[1])[:2]

            time_on_timer = f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}.{miliseconds:0>2}"
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
            if not self.final_time:
                self.evaluate_time()

            time_on_timer = self.time_since.total_seconds()

            rest = time_on_timer % 3600
            hours = int(time_on_timer // 3600)
            rest = time_on_timer % 60
            minutes = int(time_on_timer // 60)
        
            rest = str(rest).split(".")
            seconds = rest[0]
            miliseconds = str(rest[1])[:2]

        else:
            return f"00:00:00.00"

        return f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}.{miliseconds:0>2}"


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

    def draw(self, screen) -> None:
        if not isinstance(screen, pygame.Surface):
            raise TypeError(f"ERROR: variable screen has to be pygame.Surface")


        font = pygame.font.SysFont(None, 65)
        if self.cross:
            img1 = font.render(f"Cross: {self.cross}", True, black)
        else:
            img1 = font.render(f"Cross:", True, black)

        if self.first_layer:
            img2 = font.render(f"First Layer: {self.first_layer}", True, black)
        else:
            img2 = font.render(f"First Layer:", True, black)

        if self.first_two_layers:
            img3 = font.render(f"Second layer: {self.first_two_layers}", True, black)
        else:
            img3 = font.render(f"Second layer:", True, black)

        if self.oll:
            img4 = font.render(f"OLL: {self.oll}", True, black)
        else:
            img4 = font.render(f"OLL:", True, black)

        if self.pll:
            img5 = font.render(f"PLL: {self.pll}", True, black)
        else:
            img5 = font.render(f"PLL:", True, black)


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
            pass
        elif self.algorithm and not self.moves and (move == "u" or move == "u2" or move == "u’" or move == "y" or move == "y’"):
            self.reset()

        else:
            if self.moves:
                last_move = self.moves[-1]
                if opposite_moves[move] == last_move:
                    self.moves = self.moves[:-1]
                else:
                    self.moves.append(move)
            else:
                self.moves.append(move)

        self.check_for_shorter()

    def check_for_shorter(self) -> None:     #check if wrong moves can be shortened. For example U2 and U’ to U
        changed = True
        while changed:
            changed = False
            if len(self.moves) >= 2:
                if self.moves[-1] == self.moves[-2]:
                    if self.moves[-1][-1] != "2":
                        changed = True
                        complex_move = self.moves[-1]
                        self.moves = self.moves[:-2]
                        self.moves.append(f"{complex_move[0]}2")
                    elif self.moves[-1][-1] == "2":
                        changed = True
                        self.moves = self.moves[:-2]

                elif self.moves[-1][-1] == "2" and self.moves[-2][-1] != "2" and (self.moves[-1][0] == self.moves[-2][0]):
                    almost_last_move = self.moves[-2]
                    if almost_last_move[-1] == "’":
                        changed = True
                        self.moves = self.moves[:-2]
                        self.moves.append(almost_last_move[:-1])
                    else:
                        changed = True
                        self.moves = self.moves[:-2]
                        self.moves.append(f"{almost_last_move}’")

                elif self.moves[-1][-1] != "2" and self.moves[-2][-1] == "2" and (self.moves[-1][0] == self.moves[-2][0]):
                    last_move = self.moves[-1]
                    if last_move[-1] == "’":
                        changed = True
                        self.moves = self.moves[:-2]
                        self.moves.append(last_move[:-1])
                    else:
                        changed = True
                        self.moves = self.moves[:-2]
                        self.moves.append(f"{last_move}’")
       
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
    

    #ALGORITHM HELPER
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
                   







