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
from algs import pll_algs, sexy_move, oll_corners_algs, rotate_edges_alg, insert_edge_alg, swap_corners_alg
from itertools import permutations
from opposite_move import opposite_moves


class Square_on_cube:
    def __init__(self, p1: Tuple[float, float, float], p2: Tuple[float, float, float], p3: Tuple[float, float, float], p4: Tuple[float, float, float], color: pygame.Color) -> None:
        self.p1: Tuple[float, float, float] = p1
        self.p2: Tuple[float, float, float] = p2
        self.p3: Tuple[float, float, float] = p3
        self.p4: Tuple[float, float, float] = p4
   
        self.color: pygame.Color = color
        self.score: float = sum(p1[0] + p2[0] + p3[0] + p4[0]) + (sum(p1[1] + p2[1] + p3[1] + p4[1]) * 2) + (sum(p1[2] + p2[2] + p3[2] + p4[2]) * 10)

    def draw(self, screen: pygame.Surface, scale: float, cube_position: List[int]) -> None:
        if not isinstance(screen, pygame.Surface):
            raise TypeError(f"ERROR: variable screen has to be type pygame.Surface")
        if not isinstance(scale, (int, float)):
            raise TypeError(f"ERROR: variable scale has to be int or float -> {scale}")
        if not isinstance(cube_position, (list)):
            raise TypeError(f"ERROR: variable cubeposition has to be list -> {cube_position}")
        if len(cube_position) != 2:
            raise ValueError(f"ERROR: variable cubeposition can include only 2 elements -> {cube_position}")
        if not isinstance(cube_position[0], int):
            raise TypeError(f"ERROR: there can only be ints in variable cube_position -> {cube_position[0]}")
        if not isinstance(cube_position[1], int):
            raise TypeError(f"ERROR: there can only be ints in variable cube_position -> {cube_position[1]}")
        if cube_position[0] < 0:
            raise ValueError(f"ERROR: variable cube_position can include only positive numbers -> {cube_position[0]}")
        if cube_position[1] < 0:
            raise ValueError(f"ERROR: variable cube_position can include only positive numbers -> {cube_position[1]}")
        if scale <= 0:
            raise ValueError(f"ERROR: variable scale can include only positive numbers -> {scale}")

        point1 = [self.p1[0][0] * scale + cube_position[0], self.p1[1][0] * scale + cube_position[1]]
        point2 = [self.p2[0][0] * scale + cube_position[0], self.p2[1][0] * scale + cube_position[1]]
        point3 = [self.p3[0][0] * scale + cube_position[0], self.p3[1][0] * scale + cube_position[1]]
        point4 = [self.p4[0][0] * scale + cube_position[0], self.p4[1][0] * scale + cube_position[1]]
        pygame.draw.polygon(screen, self.color, (point1, point2, point3, point4))

    def __lt__(self, other: Square_on_cube) -> bool:
        if not isinstance(other, Square_on_cube):
            raise TypeError("ERROR: variable other for comparing can only be type Square_on_cube")

        return self.score < other.score

    def __str__(self) -> str:
        #print basic coordinates of points p1, p2, p3, p4 and color
        return f"{self.p1}:{self.p2}:{self.p3}:{self.p4}:{self.color}"

class Rubiks_cube_net:
    def __init__(self, position_x: int, position_y: int, net: list, net_scale: int, border_color="black"):
        if not isinstance(net, list):
            raise TypeError(f"ERROR: variable net has to be list -> {net}")
        if not isinstance(position_x, int):
            raise TypeError(f"ERROR: variable position_x has to be int -> {position_x}")
        if not isinstance(position_y, int):
            raise TypeError(f"ERROR: variable position_y has to be int -> {position_y}")
        if not isinstance(net_scale, int):
            raise TypeError(f"ERROR: variable net_scale has to be int -> {net_scale}")

        if position_x < 0:
            raise ValueError(f"ERROR: variable position_x can not be negative -> {position_x}")
        if position_y < 0:
            raise ValueError(f"ERROR: variable position_y can not be negative -> {position_y}")
        if net_scale < 0:
            raise ValueError(f"ERROR: variable net_scale can not be negative -> {net_scale}")
       
        self.faces: List[List[str]] = net
        self.x: int = position_x
        self.y: int = position_y
        self.net_scale: int = net_scale

        self.valid: bool = self.check_validity()

        self.border_color = border_color

    def mode_four_hinter_edges(self) -> list:
        wrongly_flipped_edges = []
        if self.faces[4][3] == "black":
            wrongly_flipped_edges.append("left")
        if self.faces[4][5] == "black":
            wrongly_flipped_edges.append("right")
        if self.faces[3][4] == "black":
            wrongly_flipped_edges.append("back")
        if self.faces[5][4] == "black":
            wrongly_flipped_edges.append("front")

        if len(wrongly_flipped_edges) == 4:
            return (4, wrongly_flipped_edges, None)

        elif len(wrongly_flipped_edges) == 0:
            return (0, None, None)

        elif len(wrongly_flipped_edges) == 2:
            if "front" in wrongly_flipped_edges and "back" in wrongly_flipped_edges:
                return (2, wrongly_flipped_edges, "line", "right")

            elif "left" in wrongly_flipped_edges and "right" in wrongly_flipped_edges:
                return (2, wrongly_flipped_edges, "line", "wrong")

            else:
                return (2, wrongly_flipped_edges, "l-shape")

    def mode_four_hinter_corners(self) -> list:
        corners = []
        if self.faces[3][3] != "yellow":
            corners.append("1")
        if self.faces[3][5] != "yellow":
            corners.append("2")
        if self.faces[5][5] != "yellow":
            corners.append("3")
        if self.faces[5][3] != "yellow":
            corners.append("4")


        return (len(corners), corners)

    def mode_five_hinter(self) -> list:     
        #CORNERS
        number_of_adjacent_corners = 0              
        for_return = []
        adjacent_corners_position = ""
        edges = []

        if self.faces[6][3] == self.faces[6][5]:
            number_of_adjacent_corners += 1
            adjacent_corners_position = "front"
            if self.faces[6][3] == self.faces[6][4]:
                edges.append("front")

        if self.faces[3][2] == self.faces[5][2]:
            number_of_adjacent_corners += 1
            adjacent_corners_position = "left"
            if self.faces[4][2] == self.faces[3][2]:
                edges.append("left")

        if self.faces[2][3] == self.faces[2][5]:
            number_of_adjacent_corners += 1
            adjacent_corners_position = "back"
            if self.faces[2][3] == self.faces[2][4]:
                edges.append("back")

        if self.faces[3][6] == self.faces[5][6]:
            number_of_adjacent_corners += 1
            adjacent_corners_position = "right"
            if self.faces[3][6] == self.faces[4][6]:
                edges.append("right")

        #EDGES


        if number_of_adjacent_corners == 1:
            return [1, adjacent_corners_position, edges]
        if number_of_adjacent_corners == 0:
            return [0, None, edges]
        if number_of_adjacent_corners == 4:
            return [4, None, edges]

    def extract_centres(self) -> list:
        centers = [[self.faces[1][4]], [self.faces[4][1]], [self.faces[4][4]], [self.faces[4][7]], [self.faces[7][4]], [self.faces[10][4]]]
        centers = [center[0] for center in centers]

        return centers

    def extract_edges(self) -> list:
        edges = []
        for y in range(0, 12, 3):
            edges.append([self.faces[y][4], self.faces[y - 1][4]])

        edges.append([self.faces[4][0], self.faces[10][3]])
        edges.append([self.faces[4][3], self.faces[4][2]])
        edges.append([self.faces[4][6], self.faces[4][5]])
        edges.append([self.faces[4][8], self.faces[10][5]])
        
        edges.append([self.faces[3][1], self.faces[1][3]])
        edges.append([self.faces[1][5], self.faces[3][7]])
        edges.append([self.faces[5][7], self.faces[7][5]])
        edges.append([self.faces[7][3], self.faces[5][1]])
        
        return edges

    def extract_corners(self) -> list:
        corners = []

        corners.append([self.faces[3][3], self.faces[3][2], self.faces[2][3]])
        corners.append([self.faces[3][5], self.faces[2][5], self.faces[3][6]])
        corners.append([self.faces[5][3], self.faces[5][2], self.faces[6][3]])
        corners.append([self.faces[5][5], self.faces[6][5], self.faces[5][6]])
        corners.append([self.faces[3][0], self.faces[0][3], self.faces[11][3]])
        corners.append([self.faces[5][0], self.faces[8][3], self.faces[9][3]])
        corners.append([self.faces[0][5], self.faces[3][8], self.faces[11][5]])
        corners.append([self.faces[5][8], self.faces[8][5], self.faces[9][5]])

        return corners            
     

    def check_validity(self) -> bool:
        #None in right places
        nones = set()
        for x in range(0, 3):
            for y in range(0, 3):
                nones.add(self.faces[y][x])
            for y in range(6, 12):
                nones.add(self.faces[y][x])

        for x in range(6, 9):
            for y in range(0, 3):
                nones.add(self.faces[y][x])
            for y in range(6, 12):
                nones.add(self.faces[y][x])

        nones = list(nones)
        if len(nones) != 1 or nones[0] is not None:
            self.valid = False
            return False
        
        
        centres = self.extract_centres()
        if not len(str(set(centres))) != 6:
            return False
        
        #there are unique edges
        edges = self.extract_edges()
        found_edges = []
        for edge in edges:
            if len(set(edge)) != 2:
                return False
            if edge in found_edges or edge[::-1] in found_edges:
                return False
            found_edges.append(edge)

       #there are unique corners
        corners = self.extract_corners()
        found_corners = []
        for corner in corners:
            corner = set(corner)
            if len(corner) != 3:
                return False
            permutations_ = permutations(corner, 3)
            for permutation in permutations_:
                if permutation in found_corners:
                    return False
            found_corners.append(corner)
        
        return True

        

    def y_axis_turn(self, x_start: int, x_end: int, direction: int) -> None:
        if not isinstance(x_start, (int)):
            raise TypeError(f"ERROR: variable x_start has to be int -> {x_start}")
        if not isinstance(x_end, (int)):
            raise TypeError(f"ERROR: variable x_end has to be int -> {x_end}")
        if not isinstance(direction, (int)):
            raise TypeError(f"ERROR: variable direction has to be int -> {direction}")

        if direction == 1:
            x = 1
        elif direction == -1:
            x = 3
        else:
            raise ValueError("Invalid value for direction - possible values are [1, -1]")

        if x_start not in (0, 1, 2):
            raise ValueError("Invalid value for x_start, possible values are [0, 1, 2]")
        if x_end not in (0, 1, 2):
            raise ValueError("Invalid value for x_end, possible values are [0, 1, 2]")
        if x_start > x_end:
            raise ValueError(f"Value of x_start have to be lower than x_end or same -> {x_start} > {x_end}")

        x_end += 1

        for _ in range(x):
            face1 = []
            for y in range(3, 6):
                row = []
                for x in range(3):
                    row.append(self.faces[y][x])
                face1.append(row)

            face2 = []
            for y in range(3):
                row = []
                for x in range(3, 6):
                    row.append(self.faces[y][x])
                face2.append(row)

            face3 = []
            for y in range(3, 6):
                row = []
                for x in range(6, 9):
                    row.append(self.faces[y][x])
                face3.append(row)

            face4 = []
            for y in range(6, 9):
                row = []
                for x in range(3, 6):
                    row.append(self.faces[y][x])
                face4.append(row)

            #face 1
            for y in range(3, 6):
                for x in range(x_start, x_end):
                    self.faces[y][x] = face2[x][-(y - 3 + 1)]
      
            #face2
            for y in range(x_start, x_end):
                for x in range(3, 6):
                    self.faces[y][x] = face3[x - 3][-(y + 1)]
           
            #face3
            for y in range(3, 6):
                for x in range(x_start + 1, x_end + 1):
                    self.faces[y][-x] = face4[-(x)][-(y - 3 + 1)]
            
            #face4
            for y in range(x_start + 6, x_end + 6):
                for x in range(3, 6):
                    self.faces[14 - y][x] = face1[x - 3][y - 6]



    def face_rotation(self, x_start: int, y_start: int, direction: int) -> None:
        if not isinstance(x_start, int):
            raise TypeError(f"ERROR: variable x_start has to be int -> {x_start}")
        if not isinstance(y_start, int):
            raise TypeError(f"ERROR: variable y_start has to be int -> {y_start}")
        if not isinstance(y_start, int):
            raise TypeError(f"ERROR: variable y_start has to be int -> {y_start}")

        if not (0 <= x_start <= 6):
            raise ValueError(f"ERROR: variable x_start has to be between 0 and 6 -> {x_start}")
        if not (0 <= y_start <= 9):
            raise ValueError(f"ERROR: variable x_start has to be between 0 and 9 -> {y_start}")

        if direction == -1:
            x = 3
        elif direction == 1:
            x = 1
        else:
            raise ValueError("Invalid value for direction - possible values are [1, -1]")

        for _ in range(x):
            backup = copy.deepcopy(self.faces)
            self.faces[y_start][x_start] = backup[y_start + 2][x_start]
            self.faces[y_start + 2][x_start] = backup[y_start + 2][x_start + 2]
            self.faces[y_start + 2][x_start + 2] = backup[y_start + 0][x_start + 2]
            self.faces[y_start + 0][x_start + 2] = backup[y_start + 0][x_start + 0]

            self.faces[y_start + 1][x_start + 0] = backup[y_start + 2][x_start + 1]
            self.faces[y_start + 2][x_start + 1] = backup[y_start + 1][x_start + 2]
            self.faces[y_start + 1][x_start + 2] = backup[y_start + 0][x_start + 1]
            self.faces[y_start + 0][x_start + 1] = backup[y_start + 1][x_start + 0]

    def draw(self, screen: pygame.Surface) -> None:
        if not isinstance(screen, pygame.Surface):
            raise TypeError(f"ERROR: variable screen has to be type pygame.Surface")

        for i in range(9):
            for j in range(12):
                coordinate_x = i * self.net_scale + self.x
                coordinate_y = j * self.net_scale + self.y
                if self.faces[j][i]:
                    pygame.draw.rect(screen, self.border_color, (coordinate_x, coordinate_y, self.net_scale, self.net_scale))
                    pygame.draw.rect(screen, self.faces[j][i], (coordinate_x + 1, coordinate_y + 1, self.net_scale - 2, self.net_scale - 2))


    def x_axis_turn(self, x_start: int, x_end: int, direction: int) -> None: 
        if not isinstance(x_start, int):
            raise TypeError(f"ERROR: variable x_start has to be int -> {x_start}")
        if not isinstance(x_end, int):
            raise TypeError(f"ERROR: variable x_end has to be int -> {x_end}")
        if not isinstance(direction, int):
            raise TypeError(f"ERROR: variable direction has to be int -> {direction}")

        if direction not in (1, -1):
            raise ValueError("Invalid value for direction, possible values are [1, -1]")
        if x_start not in (0, 1, 2):
            raise ValueError("Invalid value for x_start, possible values are [0, 1, 2]")
        if x_end not in (0, 1, 2):
            raise ValueError("Invalid value for x_end, possible values are [0, 1, 2]")
        if x_start > x_end:
            raise ValueError(f"Value of x_start have to be lower than x_end or same")

        backup = copy.deepcopy(self.faces)
        for x in range(x_start + 3, x_end + 4):
            for y in range(0, 12):
                self.faces[y][x] = backup[(y - (3 * direction) % 12)][x]

    def z_axis_turn(self, x_start: int, x_end: int, direction: int) -> None:
        if not isinstance(x_start, int):
            raise TypeError(f"ERROR: variable x_start has to be int -> {x_start}")
        if not isinstance(x_end, int):
            raise TypeError(f"ERROR: variable x_end has to be int -> {x_end}")
        if not isinstance(direction, int):
            raise TypeError(f"ERROR: variable direction has to be int -> {direction}")

        if x_start not in (0, 1, 2):
            raise ValueError(f"ERROR: Value of x_start have to be from (0, 1, 2) - x_start was {x_start}")
        if x_end not in (0, 1, 2):
            raise ValueError(f"ERROR: Value of x_end have to be from (1, 2, 3) - x_end was {x_end}")
        if x_start > x_end:
            raise ValueError(f"Value of x_start have to be lower than x_end or same")
        if direction not in (1, -1):
            raise ValueError(f"Invalid value for direction, possible values are [1, -1] -> {direction}")
        
        x_end += 1
        

        if direction == 1:
            x = 1
        elif direction == -1: 
            x = 3
        else:
            raise ValueError("Invalid value for direction, possible values are [1, -1]")

        for _ in range(x):
            backup = copy.deepcopy(self.faces)
            bottom_face = []
            for x in range(3, 6):
                line = []
                for y in range(9, 12):
                    line.append(backup[y][x])
                bottom_face.append(line)

            right_face = []
            for x in range(6, 9):
                line = []
                for y in range(3, 6):
                    line.append(backup[y][x])
                right_face.append(line)

            for y in range(x_start, x_end):
                for x in range(3, 9):
                    self.faces[y + 3][x] = backup[y + 3][x - 3]

                for x in range(0, 3):
                    self.faces[y + 3][x] = bottom_face[-(x + 1)][-(y + 1)]

                for x in range(3, 6):
                    self.faces[11 - y][x] = right_face[-(x - 3 + 1)][y]


    def change(self, move: str) -> None:
        if not isinstance(move, str):
            raise TypeError(f"ERROR: variable move has to be str -> {move}")

        if move == "x":
            self.x_axis_turn(0, 2, -1)
            self.face_rotation(6, 3, 1)
            self.face_rotation(0, 3, -1)

        elif move == "x’":
            self.x_axis_turn(0, 2, 1)
            self.face_rotation(6, 3, -1)
            self.face_rotation(0, 3, 1)

        elif move == "z":
            self.z_axis_turn(0, 2, 1)
            self.face_rotation(3, 6, 1)
            self.face_rotation(3, 0, -1)

        elif move == "z’":
            self.z_axis_turn(0, 2, -1)
            self.face_rotation(3, 6, -1)
            self.face_rotation(3, 0, 1)

        elif move == "y’":
            self.y_axis_turn(0, 2, 1) 
            self.face_rotation(3, 3, -1)
            self.face_rotation(3, 9, 1)

        elif move == "y":
            self.y_axis_turn(0, 2, -1) 
            self.face_rotation(3, 3, 1)
            self.face_rotation(3, 9, -1)

        elif move == "r":
            self.x_axis_turn(2, 2, -1)
            self.face_rotation(6, 3, 1)
            
        elif move == "r’":
            self.x_axis_turn(2, 2, 1)
            self.face_rotation(6, 3, -1)

        elif move == "f":
            self.z_axis_turn(2, 2, 1)
            self.face_rotation(3, 6, 1)

        elif move == "f’":
            self.z_axis_turn(2, 2, -1)
            self.face_rotation(3, 6, -1)

        elif move == "l":
            self.x_axis_turn(0, 0, 1)
            self.face_rotation(0, 3, 1)
            
        elif move == "l’":
            self.x_axis_turn(0, 0, -1)
            self.face_rotation(0, 3, -1)

        elif move == "b’":
            self.face_rotation(3, 0, -1)
            self.z_axis_turn(0, 0, 1)

        elif move == "b":
            self.face_rotation(3, 0, 1)
            self.z_axis_turn(0, 0, -1)

        elif move == "d":
            self.y_axis_turn(0, 0, 1) 
            self.face_rotation(3, 9, 1)

        elif move == "d’":
            self.y_axis_turn(0, 0, -1) 
            self.face_rotation(3, 9, -1)

        elif move == "u":
            self.y_axis_turn(2, 2, -1) 
            self.face_rotation(3, 3, 1)

        elif move == "u’":
            self.y_axis_turn(2, 2, 1) 
            self.face_rotation(3, 3, -1)

        else:
            raise ValueError(f"ERROR: Invalid value for move ’{move}’")


    def solved_check(self) -> bool:
        for y in range(4):
            for x in range(3):
                color_checker = self.faces[y * 3][x * 3]
                for i in range(0, 3):                   
                    for j in range(0, 3):
                        if self.faces[y * 3 + i][x * 3 + j] != color_checker:                       
                            return False
        return True

    def white_cross_check(self) -> bool:
        x = 4
        y = 10
        if self.faces[y][x] == "white":
            if self.faces[y - 3][x] == self.faces[y - 2][x] and self.faces[0][x] == self.faces[1][x] and self.faces[y][x - 2] == self.faces[y][x - 3] and self.faces[y][x + 2] == self.faces[y][x + 3]:
                if self.faces[y - 1][x] == "white" and self.faces[y + 1][x] == "white" and self.faces[y][x - 1] == "white" and self.faces[y][x + 1] == "white":
                    return True
        return False

    def first_layer_check(self) -> bool:
        for x in range(3, 6):
            for y in range(9, 12):
                if self.faces[y][3] != "white":
                    return False

        if not(self.faces[8][3] == self.faces[8][4] == self.faces[8][5] == self.faces[7][4]):
            return False
        if not(self.faces[3][0] == self.faces[4][0] == self.faces[5][0] == self.faces[4][1]):
            return False
        if not(self.faces[0][3] == self.faces[0][4] == self.faces[0][5] == self.faces[1][4]):
            return False
        if not(self.faces[3][8] == self.faces[4][8] == self.faces[5][8] == self.faces[4][7]):
            return False

        return True

    def second_layer_check(self) -> bool:
        if not self.first_layer_check():
            return False

        if not (self.faces[4][1] == self.faces[3][1] == self.faces[5][1]):
            return False
        if not (self.faces[4][7] == self.faces[3][7] == self.faces[5][7]):
            return False
        if not (self.faces[1][4] == self.faces[1][3] == self.faces[1][5]):
            return False

        if not (self.faces[7][4] == self.faces[7][3] == self.faces[7][5]):
            return False

        return True

    def oll_check(self) -> bool:
        if not self.second_layer_check():

            return False

        for x in range(3, 6):
            for y in range(3, 6):
                if self.faces[y][x] != "yellow":
                    return False

        return True

class Cube:
    def __init__(self, coeff_a: int, coeff_b: int, coeff_c: int, shift: float) -> None:
        if not isinstance(coeff_a, int):
            raise TypeError(f"ERROR: variable coeff_a has to be int -> {coeff_a}")
        if not isinstance(coeff_b, int):
            raise TypeError(f"ERROR: variable coeff_b has to be int -> {coeff_b}")
        if not isinstance(coeff_c, int):
            raise TypeError(f"ERROR: variable coeff_c has to be int -> {coeff_c}")
        if not isinstance(shift, (int, float)):
            raise TypeError(f"ERROR: variable shift can only be int or float -> {shift}")

        if coeff_a not in (-3, 0, 3):
            raise ValueError(f"ERROR: variable coeff_a can be -3, 0, 3 -> {coeff_a}")
        if coeff_b not in (-3, 0, 3):
            raise ValueError(f"ERROR: variable coeff_b can be -3, 0, 3 -> {coeff_b}")
        if coeff_c not in (-3, 0, 3):
            raise ValueError(f"ERROR: variable coeff_c can be -3, 0, 3 -> {coeff_c}")


        self.points: List[float] = [None, None, None, None, None, None, None, None]

        self.coeff_a: int = coeff_a
        self.coeff_b: int = coeff_b
        self.coeff_c: int = coeff_c

        self.render_decider: List[float] = []
        self.squares: List[Square_on_cube] = []

        self.score: float = None
        self.shift: float = shift
        
        self.points[0] = [[-shift + coeff_a], [-shift + coeff_b], [-shift + coeff_c]]
        self.points[1] = [[shift + coeff_a], [-shift + coeff_b], [-shift + coeff_c]]
        self.points[2] = [[shift + coeff_a], [-shift + coeff_b], [shift + coeff_c]]
        self.points[3] = [[-shift + coeff_a], [-shift + coeff_b], [shift + coeff_c]]
        self.points[4] = [[-shift + coeff_a], [shift + coeff_b], [-shift + coeff_c]]
        self.points[5] = [[shift + coeff_a], [shift + coeff_b], [-shift + coeff_c]]
        self.points[6] = [[shift + coeff_a], [shift + coeff_b], [shift + coeff_c]]
        self.points[7] = [[-shift + coeff_a], [shift + coeff_b], [shift + coeff_c]]

    def evaluate_score(self) -> None:
        self.score = self.squares[0].score

    def draw(self, screen: pygame.Surface, scale: float, cube_position: List[int]) -> None:
        if not isinstance(screen, pygame.Surface):
            raise TypeError(f"ERROR: variable screen has to be type pygame.Surface")
        if not isinstance(scale, (int, float)):
            raise TypeError(f"ERROR: variable scale has to be int or float -> {scale}")
        if not isinstance(cube_position, (list)):
            raise TypeError(f"ERROR: variable cubeposition has to be list -> {cube_position}")
        if len(cube_position) != 2:
            raise ValueError(f"ERROR: variable cubeposition can include only 2 elements -> {cube_position}")
        if not isinstance(cube_position[0], int):
            raise TypeError(f"ERROR: there can only be ints in variable cube_position -> {cube_position[0]}")
        if not isinstance(cube_position[1], int):
            raise TypeError(f"ERROR: there can only be ints in variable cube_position -> {cube_position[1]}")

        for square in self.squares:
            square.draw(screen, scale, cube_position)

    def create_copy(self) -> Cube:
        to_return = Cube(self.coeff_a, self.coeff_b, self.coeff_c, self.shift)

        for i in range(8):
            to_return.points[i] = self.points[i]

        return to_return

    def make_faces(self, net: Rubiks_cube_net) -> None:
        if not isinstance(net, Rubiks_cube_net):
            raise TypeError("ERROR: you have to enter only Rubiks_cube_net class as argument")
        else:
            #top
            if self.coeff_b == -3:
                color = net.faces[3 - (self.coeff_c // 3) + 1][(self.coeff_a // 3) + 1 + 3]
            else:
                color = black
            square = Square_on_cube(self.points[0], self.points[1], self.points[2], self.points[3], color)
            self.squares.append(square)

            #bottom
            if self.coeff_b == 3:
                color = net.faces[(self.coeff_c // 3) + 1 + 9][(self.coeff_a // 3) + 1 + 3]
            else:
                color = black
            square = Square_on_cube(self.points[4], self.points[5], self.points[6], self.points[7], color)
            self.squares.append(square)

            #front
            if self.coeff_c == -3:
                color = net.faces[self.coeff_b // 3 + 1 + 6][self.coeff_a // 3 + 1 + 3]
            else:
                color = black
            square = Square_on_cube(self.points[0], self.points[1], self.points[5], self.points[4], color)
            self.squares.append(square)

            #back 
            if self.coeff_c == 3:
                color = net.faces[0 - self.coeff_b // 3 + 1][self.coeff_a // 3 + 1 + 3]
            else:
                color = black
            square = Square_on_cube(self.points[2], self.points[3], self.points[7], self.points[6], color)
            self.squares.append(square)

            #left
            if self.coeff_a == -3:
                color = net.faces[3 - self.coeff_c // 3 + 1][0 - self.coeff_b // 3 + 1]
            else:
                color = black
            square = Square_on_cube(self.points[3], self.points[0], self.points[4], self.points[7], color)
            self.squares.append(square)
            
            #right
            if self.coeff_a == 3:
                color = net.faces[3 - self.coeff_c // 3 + 1][self.coeff_b // 3 + 1 + 6]
            else:
                color = black
            square = Square_on_cube(self.points[1], self.points[2], self.points[6], self.points[5], color)       
            self.squares.append(square)
          

        self.squares.sort(reverse=True)
        self.evaluate_score()

        
    def __lt__(self, other: Cube) -> bool:
        return self.score < other.score

    def __str__(self) -> str:
        #coeff_a, coeff_b, coeff_c, score       
        return f"{self.coeff_a}:{self.coeff_b}:{self.coeff_c}:{self.score}"

class Rubiks_cube: 

    def __init__(self, shift: float, net_scale: int, net_x: int, net_y: int, mode:int = 0, user_moves_blocked=True) -> None:
        if not isinstance(shift, (int, float)):
            raise TypeError(f"ERROR: variable shift can be int or float -> {shift}")
        if not isinstance(net_x, int):
            raise TypeError(f"ERROR: variable net_x has to be int -> {net_x}")
        if not isinstance(net_y, int):
            raise TypeError(f"ERROR: variable net_y has to be int -> {net_y}")
        if not isinstance(net_scale, int):
            raise TypeError(f"ERROR: variable net_scale has to be int -> {net_scale}")
        if not isinstance(mode, int) and mode is not None :
            raise TypeError(f"ERROR: variable mode has to be int -> {mode}")

        if shift < 0:
            raise ValueError(f"ERROR: variable shift has to be a positive number -> {shift}")
        if net_x < 0:
            raise ValueError(f"ERROR: variable net_x has to be a positive number -> {net_x}")
        if net_y < 0:
            raise ValueError(f"ERROR: variable net_y has to be a positive number -> {net_y}")
        if net_scale < 0:
            raise ValueError(f"ERROR: variable net_scale has to be a positive number -> {net_scale}")

        self.net_x: int = net_x
        self.net_y: int = net_y

        self.net_scale: int = net_scale

        self.solved: bool = False
        self.counter: int = 0
        self.moves_buffer: List[str] = []
        self.counter_max: int = 60
        self.net_scale: int = net_scale
        self.move_in_progress: bool = False
        self.reset_waiting: bool = False

        self.cubes: List[Cube] = []
        self.user_moves_blocked: bool = user_moves_blocked

        self.scrambling: bool = False

        self.mode: int = mode
        self.shuffled: bool = False

        if not mode:
            net = solved_cube_net
        elif mode == 1:
            net = cross_on_white_net
            self.new_scramble()
        elif mode == 2:
            net = corners_solved_net
            self.scramble_first_layer()

        elif mode == 3:
            net = first_two_layers_solved_net
            self.scramble_second_layer()
        
        elif mode == 4:
            net = oll_solved_net
            self.make_random_oll()

        elif mode == 5:
            net = solved_cube_net
            self.make_random_pll()
    

        self.net: Rubiks_cube_net = Rubiks_cube_net(self.net_x, self.net_y, copy.deepcopy(net), self.net_scale)  #WARNING: it does not work without copy
        self.net_setup: Rubiks_cube_net = copy.deepcopy(self.net)               #WARNING: it does not work without copy

        for i in range(-3, 6, 3):
            for j in range(-3, 6, 3):
                for k in range(-3, 6, 3):
                    self.cubes.append(Cube(i, j, k, shift))

    def scramble_second_layer(self) -> None:
        self.shuffled = True
        self.moves_buffer = ["x", "x"]

        for i in range(4):
            random_us = random.randint(0, 3)

            for element in insert_edge_alg:
                self.moves_buffer.append(element)

            if random_us == 1:
                self.moves_buffer.append("u")
            elif random_us == 2:
                self.moves_buffer.append("u2")
            elif random_us == 3:
                self.moves_buffer.append("u’")

            self.moves_buffer.append("y")

        self.scrambling = True


    def add_move(self, move) -> None:
        if not self.user_moves_blocked:
            if move[-1] == "2":
                self.moves_buffer.append(move[0])
                self.moves_buffer.append(move[0])
            else:
                self.moves_buffer.append(move)
 
    def make_random_oll(self) -> None:  #scramble top side
        self.shuffled = True
        alg = random.choice(copy.deepcopy(oll_corners_algs))

        repeating = random.randint(0, 2)
        if repeating >= 1:
            alg += rotate_edges_alg           
            if repeating >= 2:
                rotation = random.randint(0,3)
                if rotation == 1:
                    alg.append("y")
                elif rotation == 2:
                    alg.append("y2")
                elif rotation == 3:
                    alg.append("y’")
                
                alg += rotate_edges_alg

        self.moves_buffer = copy.deepcopy(alg)
        self.scrambling = True


    def scramble_first_layer(self) -> None:
        self.shuffled = True
        self.moves_buffer = ["x", "x"]

        random_y = random.randint(0, 3)
        if random_y == 1:
            self.moves_buffer.append("y")
        elif random_y == 2:
            self.moves_buffer.append("y2")
        elif random_y == 3:
            self.moves_buffer.append("y’")

        for move in swap_corners_alg:
            self.moves_buffer.append(move)

        self.moves_buffer.append("x2")


        for i in range(4):
            random_us = random.randint(0, 3)
            sexy_count = random.randint(0, 18)
            bigger = False
            while sexy_count >= 6:
                if not bigger:
                    bigger = True
                sexy_count -= 6

            if bigger and sexy_count % 2 == 0 and sexy_count > 0:
                sexy_count = sexy_count -1

            random_y = random.randint(0, 3)
            for i in range(sexy_count):
                self.moves_buffer += copy.deepcopy(sexy_move)

            if random_us == 1:
                self.moves_buffer.append("u")
            elif random_us == 2:
                self.moves_buffer.append("u2")
            elif random_us == 3:
                self.moves_buffer.append("u’")

            
            self.moves_buffer.append("y")


        self.scrambling = True
    

    def make_random_pll(self) -> None:  #scramble last layer for pll
        self.shuffled = True
        self.moves_buffer = copy.deepcopy(random.choice(pll_algs))
        self.scrambling = True


    def insert_own_net(self, net: Rubiks_cube_net) -> None:
        if not isinstance(net, Rubiks_cube_net):
            raise TypeError(f"ERROR: variable net has to be type Rubiks_cube_net")

        self.net.faces = copy.deepcopy(net.faces)
        self.net_setup.faces = copy.deepcopy(net.faces)
 
    def do_next_move(self) -> None:  #rubik's cube makes next turn in moves_buffer
        if self.moves_buffer:
            move = self.moves_buffer[0]
            if move[-1] == "2":
                self.moves_buffer = [move[0], move[0]] + self.moves_buffer[1:]
            if self.counter == self.counter_max * 2:
                self.move_in_progress = False
                self.counter = 0
                self.net.change(self.moves_buffer[0])
                self.moves_buffer = self.moves_buffer[1:]


            else:
                self.move_in_progress = True
                #WHOLE CUBE--------------------------------------------------------------
                if self.moves_buffer[0] == "x":
                    self.whole_cube_rotation(rotation_x_reverse)
                elif self.moves_buffer[0] == "x’":
                    self.whole_cube_rotation(rotation_x)

                elif self.moves_buffer[0] == "y":
                    self.whole_cube_rotation(rotation_y_reverse)
                elif self.moves_buffer[0] == "y’":
                    self.whole_cube_rotation(rotation_y)

                elif self.moves_buffer[0] == "z":
                    self.whole_cube_rotation(rotation_z)
                elif self.moves_buffer[0] == "z’":
                    self.whole_cube_rotation(rotation_z_reverse)
                #-----------------------------------------------------------------------------
                #SINGLE MOVES-----------------------------------------------------------------
                elif self.moves_buffer[0] == "f":
                    self.f_turn(rotation_z, [-2, -4])
                elif self.moves_buffer[0] == "f’":
                    self.f_turn(rotation_z_reverse, [-2, -4])

                elif self.moves_buffer[0] == "d":
                    self.d_turn(rotation_y, [2, 4])
                elif self.moves_buffer[0] == "d’":
                    self.d_turn(rotation_y_reverse, [2, 4])

                elif self.moves_buffer[0] == "r’":
                    self.r_turn(rotation_x, [2, 4])
                elif self.moves_buffer[0] == "r":
                    self.r_turn(rotation_x_reverse, [2, 4])

                elif self.moves_buffer[0] == "l":
                    self.r_turn(rotation_x, [-2, -4])
                elif self.moves_buffer[0] == "l’":
                    self.r_turn(rotation_x_reverse, [-2, -4])

                elif self.moves_buffer[0] == "u":
                    self.d_turn(rotation_y_reverse, [-2, -4])
                elif self.moves_buffer[0] == "u’":
                    self.d_turn(rotation_y, [-2, -4])

                elif self.moves_buffer[0] == "b":
                    self.f_turn(rotation_z_reverse, [2, 4])
                elif self.moves_buffer[0] == "b’":
                    self.f_turn(rotation_z, [2, 4])                

                else:
                    raise ValueError(f"ERROR: invalid value for move - value was {self.moves_buffer[0]}")

                #-------------------------------------------------------------------------------
                self.counter += 2

        else:
            self.user_moves_blocked = False
            

    def whole_cube_rotation(self, matrix: List[List[float]]) -> None:
        if not isinstance(matrix, list):
            raise TypeError(f"ERROR: variable matrix has to be a two_dimensional array -> {matrix}")
        for i in range(len(self.cubes)):
            for j in range(8):
                self.cubes[i].points[j] = matrix_multiplication(matrix, self.cubes[i].points[j])
           
    def draw(self, screen: pygame.Surface, scale: int, cube_position: List[int]) -> None:
        if not isinstance(screen, pygame.Surface):
            raise TypeError(f"ERROR: variable screen has to be type pygame.Surface")
        if not isinstance(scale, int):
            raise TypeError(f"ERROR: variable scale has to be int or float -> {scale}")
        if not isinstance(cube_position, (list)):
            raise TypeError(f"ERROR: variable cubeposition has to be list -> {cube_position}")
        if len(cube_position) != 2:
            raise ValueError(f"ERROR: variable cubeposition can include only 2 elements -> {cube_position}")
        if not isinstance(cube_position[0], int):
            raise TypeError(f"ERROR: there can only be ints in variable cube_position -> {cube_position[0]}")
        if not isinstance(cube_position[1], int):
            raise TypeError(f"ERROR: there can only be ints in variable cube_position -> {cube_position[1]}")


        rubiks_cube_for_draw: list = []
        for element in self.cubes:
            rubiks_cube_for_draw.append(element.create_copy())  #ONLY FOR DRAW PURPOSE - OTHERWISE IT WOULD ROTATE CUBE AROUND
        for i in range(len(rubiks_cube_for_draw)):
            for j in range(8):
                rubiks_cube_for_draw[i].points[j] = matrix_multiplication(rotate_for_draw, rubiks_cube_for_draw[i].points[j])

        for cube in rubiks_cube_for_draw:
            cube.make_faces(self.net_setup)

        rubiks_cube_for_draw.sort(reverse=True)

        for cube in rubiks_cube_for_draw:
            cube.draw(screen, scale, cube_position)

        self.net.draw(screen)

    def f_turn(self, matrix: List[list], checker: List[int]) -> None:   #z-axis turns
        if not isinstance(matrix, list):
            raise TypeError(f"ERROR: variable matrix has to be a two-dimensional array -> {matrix}")
        if not isinstance(checker, list):
            raise TypeError(f"ERROR: variable checker has to be a list -> {list}")

        for i in range(len(self.cubes)):
            for j in range(8):
                self.cubes[i].points[j][2][0] = round(self.cubes[i].points[j][2][0])
                if self.cubes[i].points[j][2][0] in checker:
                    self.cubes[i].points[j] = matrix_multiplication(matrix, self.cubes[i].points[j])

    def d_turn(self, matrix: List[list], checker: List[int]) -> None:  #y-axis turns
        if not isinstance(matrix, list):
            raise TypeError(f"ERROR: variable matrix has to be a two-dimensional array -> {matrix}")
        if not isinstance(checker, list):
            raise TypeError(f"ERROR: variable checker has to be a list -> {list}")

        for i in range(len(self.cubes)):
            for j in range(8):
                self.cubes[i].points[j][1][0] = round(self.cubes[i].points[j][1][0])
                if self.cubes[i].points[j][1][0] in checker:
                    self.cubes[i].points[j] = matrix_multiplication(matrix, self.cubes[i].points[j])

    def r_turn(self, matrix: List[list], checker: List[int]) -> None:  #x-axis turns
        if not isinstance(matrix, list):
            raise TypeError(f"ERROR: variable matrix has to be a two-dimensional array -> {matrix}")
        if not isinstance(checker, list):
            raise TypeError(f"ERROR: variable checker has to be a list -> {list}")

        for i in range(len(self.cubes)):
            for j in range(8):
                self.cubes[i].points[j][0][0] = round(self.cubes[i].points[j][0][0])
                if self.cubes[i].points[j][0][0] in checker:
                    self.cubes[i].points[j] = matrix_multiplication(matrix, self.cubes[i].points[j])

    def generate_random_move(self) -> None:
        if not self.moves_buffer:
            random_number = randint(0, 15)
            moves = ["x", "x’", "y", "y’", "z", "z’", "u", "u’", "d", "d’", "l", "l’", "r", "r’", "f", "f’", "b", "b’"]
            self.moves_buffer.append(moves[random_number])

    def new_scramble(self) -> None:
        self.shuffled = True
        self.reset_waiting = False
        self.user_moves_blocked = True
        moves = ["u", "u’", "d", "d’", "l", "l’", "r", "r’", "f", "f’", "b", "b"]

        previous_move = None
        while len(self.moves_buffer) < 20:
            generated_element = choice(moves)
            if opposite_moves[generated_element] != previous_move:            
                self.moves_buffer.append(generated_element)
                previous_move = generated_element

        self.scrambling = True

    def scramble(self) -> None: #rotating of rubik's cube by its moves_buffer but with higher speed
        if self.moves_buffer:
            self.user_moves_blocked = True 
            move = self.moves_buffer[0]
            if move[-1] == "2":
                self.moves_buffer = [move[0], move[0]] + self.moves_buffer[1:]
            if self.counter == self.counter_max * 2:
                self.move_in_progress = False
                self.counter = 0
                self.net.change(self.moves_buffer[0])
                self.moves_buffer = self.moves_buffer[1:]

            else:
                self.move_in_progress = True
                #WHOLE CUBE--------------------------------------------------------------
                if self.moves_buffer[0] == "x":
                    self.whole_cube_rotation(rotation_x_reverse_speed)
                elif self.moves_buffer[0] == "x’":
                    self.whole_cube_rotation(rotation_x_speed)

                elif self.moves_buffer[0] == "y":
                    self.whole_cube_rotation(rotation_y_reverse_speed)
                elif self.moves_buffer[0] == "y’":
                    self.whole_cube_rotation(rotation_y_speed)

                elif self.moves_buffer[0] == "z":
                    self.whole_cube_rotation(rotation_z_speed)
                elif self.moves_buffer[0] == "z’":
                    self.whole_cube_rotation(rotation_z_reverse_speed)
                #-----------------------------------------------------------------------------
                #SINGLE MOVES-----------------------------------------------------------------
                elif self.moves_buffer[0] == "f":
                    self.f_turn(rotation_z_speed, [-2, -4])
                elif self.moves_buffer[0] == "f’":
                    self.f_turn(rotation_z_reverse_speed, [-2, -4])

                elif self.moves_buffer[0] == "d":
                    self.d_turn(rotation_y_speed, [2, 4])
                elif self.moves_buffer[0] == "d’":
                    self.d_turn(rotation_y_reverse_speed, [2, 4])

                elif self.moves_buffer[0] == "r’":
                    self.r_turn(rotation_x_speed, [2, 4])
                elif self.moves_buffer[0] == "r":
                    self.r_turn(rotation_x_reverse_speed, [2, 4])

                elif self.moves_buffer[0] == "l":
                    self.r_turn(rotation_x_speed, [-2, -4])
                elif self.moves_buffer[0] == "l’":
                    self.r_turn(rotation_x_reverse_speed, [-2, -4])

                elif self.moves_buffer[0] == "u":
                    self.d_turn(rotation_y_reverse_speed, [-2, -4])
                elif self.moves_buffer[0] == "u’":
                    self.d_turn(rotation_y_speed, [-2, -4])

                elif self.moves_buffer[0] == "b":
                    self.f_turn(rotation_z_reverse_speed, [2, 4])
                elif self.moves_buffer[0] == "b’":
                    self.f_turn(rotation_z_speed, [2, 4])

                else:
                    raise ValueError(f"ERROR: invalid value for move - value was {self.moves_buffer[0]}")

                #-------------------------------------------------------------------------------
                self.counter += 8
        else:
            self.user_moves_blocked = False
            self.scrambling = False

    def white_cross_check(self) -> bool:
        return self.net.white_cross_check()


#-----------------------------------------------------------------------------------------------------------------

import unittest

class TestStringMethods(unittest.TestCase):
    def test_rubiks_cube_net_check_validity(self):
        net1 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        self.assertTrue(net1.check_validity())

        net2 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net2.faces = [[None, None, None, "red", "green", "green", None, None, None],
                    [None, None, None, "green", "blue", "white", None, None, None],
                    [None, None, None, "yellow", "green", "red", None, None, None],
                    ["white", "white", "blue", "red", "yellow", "white", "green", "blue", "white"],
                    ["red", "orange", "white", "red", "white", "orange", "white", "red", "orange"],
                    ["orange", "orange", "green", "red", "green", "green", "yellow", "blue", "yellow",],
                    [None, None, None, "yellow", "red", "orange", None, None, None],
                    [None, None, None, "blue", "green", "yellow", None, None, None],
                    [None, None, None, "blue", "red", "orange", None, None, None],
                    [None, None, None, "white", "yellow", "blue", None, None, None],
                    [None, None, None, "blue", "yellow", "yellow", None, None, None],
                    [None, None, None, "blue", "orange", "orange", None, None, None]]
        self.assertTrue(net2.check_validity())

        net3 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net3.faces = [[None, None, None, "red", "green", "green", None, None, None],
                    [None, None, None, "green", "blue", "white", None, None, None],
                    [None, None, None, "yellow", "red", "red", None, None, None],
                    ["white", "white", "blue", "red", "yellow", "white", "green", "blue", "white"],
                    ["red", "orange", "white", "red", "white", "orange", "white", "red", "orange"],
                    ["orange", "orange", "green", "red", "green", "green", "yellow", "blue", "yellow",],
                    [None, None, None, "yellow", "red", "orange", None, None, None],
                    [None, None, None, "blue", "green", "yellow", None, None, None],
                    [None, None, None, "blue", "red", "orange", None, None, None],
                    [None, None, None, "white", "yellow", "blue", None, None, None],
                    [None, None, None, "blue", "yellow", "yellow", None, None, None],
                    [None, None, None, "blue", "orange", "orange", None, None, None]]
        self.assertFalse(net3.check_validity())
        

    def test_rubiks_cube_net_extract_centers(self):
        net1 = Rubiks_cube_net(100, 200, all_black_net, 10)
        net1.faces = [[None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "blue", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    ["black", "black", "black", "black", "black", "black", "black", "black", "black"],
                    ["black", "orange", "black", "black", "yellow", "black", "black", "red", "black"],
                    ["black", "black", "black", "black", "black", "black", "black", "black", "black",],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "green", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "white", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None]]
        centers = net1.extract_centres()

        self.assertEqual(set(centers), set(["white", "yellow", "red", "orange", "blue", "green"]))

    def test_rubiks_cube_net_extract_edges(self):
        net1 = Rubiks_cube_net(100, 200, all_black_net, 10)
        net1.faces = [[None, None, None, "black", "1", "black", None, None, None],
                    [None, None, None, "21", "black", "22", None, None, None],
                    [None, None, None, "black", "2", "black", None, None, None],
                    ["black", "28", "black", "black", "3", "black", "black", "23", "black"],
                    ["11", "black", "12", "13", "black", "14", "15", "black", "16"],
                    ["black", "27", "black", "black", "4", "black", "black", "24", "black",],
                    [None, None, None, "black", "5", "black", None, None, None],
                    [None, None, None, "26", "black", "25", None, None, None],
                    [None, None, None, "black", "6", "black", None, None, None],
                    [None, None, None, "black", "7", "black", None, None, None],
                    [None, None, None, "18", "black", "17", None, None, None],
                    [None, None, None, "black", "8", "black", None, None, None]]

        edges = net1.extract_edges()
        control_edges = [["1", "8"], ["2", "3"], ["4", "5"], ["6", "7"], ["12", "13"], ["14", "15"], ["16", "17"], ["18", "11"], ["22", "23"], ["24", "25"], ["26", "27"], ["28", "21"]]

        for element in control_edges:
            if not (element in edges or element[::-1] in edges):
                self.assertTrue(False)
        self.assertTrue(True)

    def test_rubiks_cube_net_extract_corners(self):
        net1 = Rubiks_cube_net(100, 200, all_black_net, 10)
        net1.faces = [[None, None, None, "21", "blue", "24", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "1", "blue", "4", None, None, None],
                    ["20", "red", "2", "3", "yellow", "5", "6", "orange", "23"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    ["16", "red", "7", "8", "yellow", "11", "12", "orange", "13"],
                    [None, None, None, "9", "green", "10", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "17", "green", "14", None, None, None],
                    [None, None, None, "18", "white", "15", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "19", "white", "22", None, None, None]]

        corners = net1.extract_corners()
        control_corners = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["10", "11", "12"], ["13", "14", "15"], ["16", "17", "18"], ["19", "20", "21"], ["22", "23", "24"]]

        for i in range(len(control_corners)):
            found = False
            control_corner = control_corners[i]
            for j in range(len(corners)):
                corner = corners[j]
                if corner.sort() == corner.sort():
                    found = True
                    break

            if not found:
                self.assertTrue(False)
        self.assertTrue(True)


    def test_rubiks_cube_net_solved_check(self):
        net1 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net1.faces = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    ["orange", "orange", "orange", "white", "white", "white", "red", "red", "red"],
                    ["orange", "orange", "orange", "white", "white", "white", "red", "red", "red"],
                    ["orange", "orange", "orange", "white", "white", "white", "red", "red", "red"],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "yellow", "yellow", "yellow", None, None, None],
                    [None, None, None, "yellow", "yellow", "yellow", None, None, None],
                    [None, None, None, "yellow", "yellow", "yellow", None, None, None]]

        net2 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net2.faces = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    ["orange", "orange", "orange", "white", "white", "white", "red", "red", "red"],
                    ["orange", "orange", "orange", "white", "white", "white", "red", "red", "red"],
                    ["orange", "orange", "orange", "white", "white", "white", "red", "red", "red"],
                    [None, None, None, "green", "green", "white", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "yellow", "yellow", "yellow", None, None, None],
                    [None, None, None, "yellow", "yellow", "yellow", None, None, None],
                    [None, None, None, "yellow", "yellow", "yellow", None, None, None]]

        net3 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net3.faces = [[None, None, None, "orange", "orange", "orange", None, None, None],
                    [None, None, None, "orange", "orange", "orange", None, None, None],
                    [None, None, None, "orange", "orange", "orange", None, None, None],
                    ["green", "green", "green", "white", "white", "white", "blue", "blue", "blue"],
                    ["green", "green", "green", "white", "white", "white", "blue", "blue", "blue"],
                    ["green", "green", "green", "white", "white", "white", "blue", "blue", "blue"],
                    [None, None, None, "red", "red", "red", None, None, None],
                    [None, None, None, "red", "red", "red", None, None, None],
                    [None, None, None, "red", "red", "red", None, None, None],
                    [None, None, None, "yellow", "yellow", "yellow", None, None, None],
                    [None, None, None, "yellow", "yellow", "yellow", None, None, None],
                    [None, None, None, "yellow", "yellow", "yellow", None, None, None]]
        
        self.assertTrue(net1.solved_check())
        self.assertFalse(net2.solved_check())
        self.assertTrue(net3.solved_check())
    
    def test_rubiks_cube_net_moves_sequence_correct(self):
        net1 = Rubiks_cube_net(100, 200, solved_cube_net_white_up, 10)
        moves = ["r", "u", "l", "x", "b", "d", "f", "z", "u", "f’", "r’", "u", "y", "l’", "f", "f", "z", "l’", "b’", "f", "u"]

        for move in moves:
            net1.change(move)

        check_net = [[None, None, None, "white", "green", "white", None, None, None],
                    [None, None, None, "white", "blue", "white", None, None, None],
                    [None, None, None, "white", "blue", "orange", None, None, None],
                    ["red", "red", "red", "blue", "orange", "blue", "yellow", "blue", "blue"],
                    ["yellow", "red", "white", "orange", "yellow", "green", "white", "orange", "yellow"],
                    ["orange", "blue", "yellow", "green", "red", "yellow", "orange", "red", "red"],
                    [None, None, None, "red", "green", "green", None, None, None],
                    [None, None, None, "red", "green", "yellow", None, None, None],
                    [None, None, None, "white", "green", "yellow", None, None, None],
                    [None, None, None, "green", "yellow", "blue", None, None, None],
                    [None, None, None, "blue", "white", "orange", None, None, None],
                    [None, None, None, "green", "orange", "orange", None, None, None]]

        self.maxDiff = None
        self.assertListEqual(net1.faces, check_net)

    
    def test_white_cross_check(self):
        net = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net.faces = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None]]

        net2 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net2.faces = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    ["orange", "orange", "orange", "white", "white", "white", "red", "red", "red"],
                    ["orange", "orange", "orange", "white", "white", "white", "red", "red", "red"],
                    ["orange", "orange", "orange", "white", "white", "white", "red", "red", "red"],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "yellow", "yellow", "yellow", None, None, None],
                    [None, None, None, "yellow", "yellow", "yellow", None, None, None],
                    [None, None, None, "yellow", "yellow", "yellow", None, None, None]]

        net3 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net3.faces = [[None, None, None, "blue", "green", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "blue", "green", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None]]

        self.assertTrue(net.white_cross_check())
        self.assertFalse(net2.white_cross_check())
        self.assertFalse(net3.white_cross_check())

    def test_first_layer_check(self):
        net = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net.faces = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "blue", "green", "green", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None]]

        net2 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net2.faces = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "black", "blue", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    ["orange", "black", "black", "black", "black", "black", "black", "black", "red"],
                    ["orange", "orange", "black", "black", "black", "black", "black", "red", "red"],
                    ["orange", "black", "black", "black", "black", "black", "black", "black", "red"],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "green", "black", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None]]

        net3 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net3.faces = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "red", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None]]

        self.assertFalse(net.first_layer_check())
        self.assertTrue(net2.first_layer_check())
        self.assertFalse(net3.first_layer_check())

    def test_second_layer_check(self):
        net = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net.faces = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "red", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None]]

        net2 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net2.faces = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    ["orange", "orange", "black", "black", "black", "black", "black", "red", "red"],
                    ["orange", "orange", "black", "black", "black", "black", "black", "red", "red"],
                    ["orange", "orange", "black", "black", "black", "black", "black", "red", "red"],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None]]

        net3 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net3.faces = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "white", "blue", "blue", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    ["orange", "orange", "black", "black", "black", "black", "black", "red", "red"],
                    ["orange", "orange", "black", "black", "black", "black", "black", "red", "red"],
                    ["orange", "orange", "black", "black", "black", "black", "black", "red", "red"],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None]]

        net4 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net4.faces = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    ["orange", "orange", "black", "black", "black", "black", "black", "red", "red"],
                    ["orange", "orange", "black", "black", "black", "black", "black", "red", "red"],
                    ["orange", "white", "black", "black", "black", "black", "black", "red", "red"],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None]]
        
        self.assertFalse(net.second_layer_check())
        self.assertTrue(net2.second_layer_check())
        self.assertFalse(net3.second_layer_check())
        self.assertFalse(net4.second_layer_check())

    def test_oll_check(self) -> None:
        net1 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net1.faces = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    ["red", "red", "red", "yellow", "red", "yellow", "orange", "orange", "orange"],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None]]

        net2 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net2.faces = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    ["red", "red", "red", "red", "yellow", "yellow", "orange", "orange", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None]]

        net3 = Rubiks_cube_net(100, 200, solved_cube_net, 10)
        net3.faces = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "blue", "blue", "blue", None, None, None],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    ["red", "red", "red", "yellow", "yellow", "yellow", "orange", "orange", "orange"],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None]]

        self.assertFalse(net1.oll_check())
        self.assertFalse(net2.oll_check())
        self.assertTrue(net3.oll_check())

    def test_squares_str(self):
        square = Square_on_cube([[1], [-2], [2]], [[0], [-1], [1]], [[1], [-1], [2]], [[1], [-2], [2]], "white")
        self.assertEqual(str(square), "[[1], [-2], [2]]:[[0], [-1], [1]]:[[1], [-1], [2]]:[[1], [-2], [2]]:white")

    def test_cube_str(self):
        cube = Cube(-3, 0, 3, 1)
        self.assertEqual(str(cube), "-3:0:3:None")
        
    def test_squares_ordering(self):
        square1 = Square_on_cube(([6.4],[7.49],[5.14]),([6.11],[9.93],[5.07]),([3.21],[3.66],[4.97]),([5.62],[6.41],[7.95]), white)
        square2 = Square_on_cube(([5.31],[1.65],[5.22]),([4.05],[3.11],[5.97]),([5.6],[3.15],[2.02]),([9.62],[6.29],[9.53]), white)
        square3 = Square_on_cube(([2.34],[4.13],[6.22]),([7.74],[7.65],[2.05]),([1.05],[6.74],[7.36]),([6.73],[5.96],[3.26]), white)

        squares = [square1, square2, square3]
        squares.sort()
        self.assertTrue(squares[0].score <= squares[1].score <= squares[2].score)
     
       

if __name__ == '__main__':
    unittest.main()