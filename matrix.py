import math
from typing import List

def matrix_multiplication(a: list, b: list) -> List[List[list]]:
    try:
        columns_a = len(a[0])
        rows_a = len(a)
    except IndexError:
        raise IndexError(f"ERROR: invalid value in variable ’a’ - it have to be a two dimensional array")
    except TypeError:
        raise IndexError(f"ERROR: invalid value in variable ’a’ - it have to be a two dimensional array")

    try:
        columns_b = len(b[0])
        rows_b = len(b)
    except IndexError:
        raise IndexError(f"ERROR: invalid value in variable ’b’ - it have to be a two dimensional array")
    except TypeError:
        raise IndexError(f"ERROR: invalid value in variable ’b’ - it have to be a two dimensional array")

    try:
        result_matrix = [[j for j in range(columns_b)] for i in range(rows_a)]
        if columns_a == rows_b:
            for x in range(rows_a):
                for y in range(columns_b):
                    sum = 0
                    for k in range(columns_a):
                        sum += a[x][k] * b[k][y]
                    result_matrix[x][y] = sum
            return result_matrix

        else:
            raise ValueError("ERROR: columns of the first matrix must be equal to the rows of the second matrix")

    except (TypeError, ValueError):
        raise ValueError(f"ERROR: invalid value in matrixies, they have to be a two dimensional array with int or float in them")


#ROTATION MATRIXIES
angle = 0.01 * (157 / 60)
rotation_x = [[1, 0, 0],
              [0, math.cos(angle), -math.sin(angle)],
              [0, math.sin(angle), math.cos(angle)]]

rotation_y = [[math.cos(angle), 0, -math.sin(angle)],
              [0, 1, 0],
              [math.sin(angle), 0, math.cos(angle)]]

rotation_z = [[math.cos(angle), -math.sin(angle), 0],
              [math.sin(angle), math.cos(angle), 0],
              [0, 0 ,1]]

rotation_x_reverse = [[1, 0, 0],
                      [0, math.cos(angle), math.sin(angle)],
                      [0, -math.sin(angle), math.cos(angle)]]

rotation_y_reverse = [[math.cos(angle), 0, math.sin(angle)],
                      [0, 1, 0],
                      [-math.sin(angle), 0, math.cos(angle)]]

rotation_z_reverse = [[math.cos(angle), math.sin(angle), 0],
                      [-math.sin(angle), math.cos(angle), 0],
                      [0, 0 ,1]]

#SPEED ROTATION MATRIXIS
angle = 0.01 * (157 / 15)
rotation_x_speed = [[1, 0, 0],
              [0, math.cos(angle), -math.sin(angle)],
              [0, math.sin(angle), math.cos(angle)]]

rotation_y_speed = [[math.cos(angle), 0, -math.sin(angle)],
              [0, 1, 0],
              [math.sin(angle), 0, math.cos(angle)]]

rotation_z_speed = [[math.cos(angle), -math.sin(angle), 0],
              [math.sin(angle), math.cos(angle), 0],
              [0, 0 ,1]]

rotation_x_reverse_speed = [[1, 0, 0],
                      [0, math.cos(angle), math.sin(angle)],
                      [0, -math.sin(angle), math.cos(angle)]]

rotation_y_reverse_speed = [[math.cos(angle), 0, math.sin(angle)],
                      [0, 1, 0],
                      [-math.sin(angle), 0, math.cos(angle)]]

rotation_z_reverse_speed = [[math.cos(angle), math.sin(angle), 0],
                      [-math.sin(angle), math.cos(angle), 0],
                      [0, 0 ,1]]

#DRAW MATRIXIES
draw_matrix = [[1, 0, 0],
               [0, 1, 0]]

rotate_for_draw = rotation_y

for _ in range(15):
    rotate_for_draw = matrix_multiplication(rotate_for_draw, rotation_y_reverse)

for _ in range(5):
    rotate_for_draw = matrix_multiplication(rotate_for_draw, rotation_x)

for _ in range(2):
    rotate_for_draw = matrix_multiplication(rotate_for_draw, rotation_z)


#-----------------------------------------------------------------------------------------------------------------

import unittest

class TestStringMethods(unittest.TestCase):

    def test_matrix_multiplication(self):
        self.assertEqual(matrix_multiplication([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]])

        with self.assertRaises(ValueError):
           matrix_multiplication([[1, "x"], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]]
        with self.assertRaises(IndexError):
            matrix_multiplication([3], [[5, 6], [7, 8]]), [[19, 22], [43, 50]]
        with self.assertRaises(IndexError):
            matrix_multiplication(3, [[5, 6], [7, 8]]), [[19, 22], [43, 50]]
        with self.assertRaises(ValueError):
           matrix_multiplication([[1, "x"], [3, 4]], [[5, 6], [7, 8]]), [[19, 22, 33], [43, 50]]


if __name__ == '__main__':
    unittest.main()