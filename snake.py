import curses

class Snake:
    # body_pos is a list of lists, each element representing the position of a node of the snake's body
    def __init__(self, head_pos, body_pos, tail_pos):
        self.score = 0
        

        self.apple_exists = False
        self.apple_pos = list()

        self.head_pos = head_pos
        self.body_pos = body_pos
        self.tail_pos = tail_pos
        self.alive = True

        self.head = "@"
        self.body = "#"
        self.tail = "!"

        self.input_dict = {"left": curses.KEY_LEFT, "right": curses.KEY_RIGHT, "up": curses.KEY_UP, "down": curses.KEY_DOWN}

        self.last_input = self.input_dict["up"]