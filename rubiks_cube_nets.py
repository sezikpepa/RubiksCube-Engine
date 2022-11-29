
#NETS FOR RUBIKS CUBE - BASIC TEMPLATES-----------------------------------------------------------------------------------------

solved_cube_net = [[None, None, None, "blue", "blue", "blue", None, None, None],
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

solved_cube_net_white_up = [[None, None, None, "blue", "blue", "blue", None, None, None],
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

all_black_net =     [[None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    ["black", "black", "black", "black", "black", "black", "black", "black", "black"],
                    ["black", "black", "black", "black", "black", "black", "black", "black", "black"],
                    ["black", "black", "black", "black", "black", "black", "black", "black", "black",],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None]]


cross_on_yellow_net = [[None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "blue", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    ["black", "black", "black", "black", "white", "black", "black", "black", "black"],
                    ["black", "orange", "black", "white", "yellow", "white", "black", "red", "black"],
                    ["black", "black", "black", "black", "white", "black", "black", "black", "black",],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "green", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None]]


cross_on_white_net = [[None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "blue", "black", None, None, None],
                    [None, None, None, "black", "blue", "black", None, None, None],
                    ["black", "black", "black", "black", "white", "black", "black", "black", "black"],
                    ["black", "orange", "orange", "white", "white", "white", "red", "red", "black"],
                    ["black", "black", "black", "black", "white", "black", "black", "black", "black",],
                    [None, None, None, "black", "green", "black", None, None, None],
                    [None, None, None, "black", "green", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "yellow", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None]]


corners_solved_net = [[None, None, None, "blue", "blue", "blue", None, None, None],
                    [None, None, None, "black", "blue", "black", None, None, None],
                    [None, None, None, "black", "black", "black", None, None, None],
                    ["orange", "black", "black", "black", "black", "black", "black", "black", "red"],
                    ["orange", "orange", "black", "black", "black", "black", "black", "red", "red"],
                    ["orange", "black", "black", "black", "black", "black", "black", "black", "red",],
                    [None, None, None, "black", "black", "black", None, None, None],
                    [None, None, None, "black", "green", "black", None, None, None],
                    [None, None, None, "green", "green", "green", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None],
                    [None, None, None, "white", "white", "white", None, None, None]]

first_two_layers_solved_net = [[None, None, None, "black", "black", "black", None, None, None],
                        [None, None, None, "blue", "blue", "blue", None, None, None],
                        [None, None, None, "blue", "blue", "blue", None, None, None],
                        ["black", "orange", "orange", "white", "white", "white", "red", "red", "black"],
                        ["black", "orange", "orange", "white", "white", "white", "red", "red", "black"],
                        ["black", "orange", "orange", "white", "white", "white", "red", "red", "black",],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "black", "black", "black", None, None, None],
                        [None, None, None, "black", "black", "black", None, None, None],
                        [None, None, None, "black", "black", "black", None, None, None],
                        [None, None, None, "black", "black", "black", None, None, None]]


oll_dot_net = [[None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "black", "black", "black", None, None, None],
                        ["orange", "orange", "black", "black", "black", "black", "black", "red", "red"],
                        ["orange", "orange", "black", "black", "yellow", "black", "black", "red", "red"],
                        ["orange", "orange", "black", "black", "black", "black", "black", "red", "red",],
                        [None, None, None, "black", "black", "black", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None]]


oll_line_net = [[None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "black", "black", "black", None, None, None],
                        ["orange", "orange", "black", "black", "black", "black", "black", "red", "red"],
                        ["orange", "orange", "black", "yellow", "yellow", "yellow", "black", "red", "red"],
                        ["orange", "orange", "black", "black", "black", "black", "black", "red", "red",],
                        [None, None, None, "black", "black", "black", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None]]

oll_l_net = [[None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "black", "black", "black", None, None, None],
                        ["orange", "orange", "black", "black", "black", "black", "black", "red", "red"],
                        ["orange", "orange", "black", "black", "yellow", "yellow", "black", "red", "red"],
                        ["orange", "orange", "black", "black", "yellow", "black", "black", "red", "red",],
                        [None, None, None, "black", "black", "black", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None]]

oll_solved_net = [[None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "black", "black", "black", None, None, None],
                        ["orange", "orange", "black", "yellow", "yellow", "yellow", "black", "red", "red"],
                        ["orange", "orange", "black", "yellow", "yellow", "yellow", "black", "red", "red"],
                        ["orange", "orange", "black", "yellow", "yellow", "yellow", "black", "red", "red",],
                        [None, None, None, "black", "black", "black", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None]]

#TODO
pll_corners_solved = [[None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "green", "black", "green", None, None, None],
                        ["orange", "orange", "orange", "yellow", "yellow", "yellow", "red", "red", "red"],
                        ["orange", "orange", "black", "yellow", "yellow", "yellow", "black", "red", "red"],
                        ["orange", "orange", "orange", "yellow", "yellow", "yellow", "red", "red", "red",],
                        [None, None, None, "green", "black", "green", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "green", "green", "green", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None]]

pll_lights = [[]]

pll_diagonal = [[]]


empty_net = [[None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        ["white", "white", "white", "white", "white", "white", "white", "white", "white"],
                        ["white", "white", "white", "white", "white", "white", "white", "white", "white"],
                        ["white", "white", "white", "white", "white", "white", "white", "white", "white"],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None],
                        [None, None, None, "white", "white", "white", None, None, None]]