import curses
from helpers import print_center, get_middle
from snake import Snake
from random import randint

def set_up_board(screen):
    curses.noecho()
    screen.keypad(1)
    title(screen)

def title(screen):
    # Sets up the screen appearence
    set_screen_layout(screen)
    
    print_center(screen, "Spiral Snake - Move with arrow keys")
    print_center(screen, "By: SpiralWarrior", row_offset=1)
    print_center(screen, "[Press the Backspace key]", row_offset=5)
    
    curses.curs_set(0)  # Hides the cursor while waiting for prompt
    c = screen.getch()

    if c == curses.KEY_BACKSPACE:
        game_start(screen) 
    else:
        title(screen)

def game_start(screen):
    # Clears the screen
    set_screen_layout(screen)

    start_y, start_x = get_middle(screen) # Gets the middle of the screen for initiating the snake's head
    # The calculations of the starting position of the rest of the body is based on the snake's head
    _starting_head = [start_y, start_x]
    _starting_body = [[start_y+1, start_x], [start_y+2, start_x], [start_y+3, start_x]]
    _starting_tail = [start_y+4, start_x]

    snake = Snake(_starting_head, _starting_body, _starting_tail)
    game_loop(screen, snake)

def game_over(screen, snake):
    set_screen_layout(screen)
    snake.alive = False
    print_center(screen, "GAME OVER!")
    print_center(screen, "Your score: " + str(snake.score), row_offset=1)
    screen.nodelay(0)
    c = screen.getch()

def game_loop(screen, snake):
    screen.refresh()
    while (snake.alive):
        screen_update(screen, snake)

        if snake.head_pos == snake.apple_pos:
            increase_snake(screen, snake)
    
        screen.nodelay(1)

        screen.timeout(150)
        c = screen.getch()

        if c == curses.KEY_LEFT and snake.last_input != curses.KEY_RIGHT:
            move_snake(screen, curses.KEY_LEFT, snake)
        elif c == curses.KEY_UP and snake.last_input != curses.KEY_DOWN:
            move_snake(screen, curses.KEY_UP, snake)
        elif c == curses.KEY_DOWN and snake.last_input != curses.KEY_UP:
            move_snake(screen, curses.KEY_DOWN, snake)
        elif c == curses.KEY_RIGHT and snake.last_input != curses.KEY_LEFT:
            move_snake(screen, curses.KEY_RIGHT, snake)
        else:
            move_snake(screen, snake.last_input, snake)

def add_apple(screen, snake):
    num_col, num_rows = screen.getmaxyx()
    snake.apple_pos.clear()
    snake.apple_pos.append(randint(1, num_col-1))
    snake.apple_pos.append(randint(1, num_rows-1))

    screen.addch(snake.apple_pos[0], snake.apple_pos[1], "O")
    snake.apple_exists = True

def screen_update(screen, snake):
    set_screen_layout(screen)
    # HUD
    screen.addstr(0, 0, "Score: " + str(snake.score))
    y_middle, x_middle = get_middle(screen)
    screen.addstr(0, x_middle, "SPIRAL-SNAKE")

    # Apple 
    if not snake.apple_exists:
        add_apple(screen, snake)
    else:
        screen.addch(snake.apple_pos[0], snake.apple_pos[1], "O")

    # Snake
    screen.addch(snake.head_pos[0], snake.head_pos[1], snake.head)
    for position in snake.body_pos:
        screen.addch(position[0], position[1], snake.body)
    screen.addch(snake.tail_pos[0], snake.tail_pos[1], snake.tail)
    screen.refresh()

def move_snake(screen, input, snake):
    snake.tail_pos = list(snake.body_pos[-1]) # Gets the last element of the list

    i = (len(snake.body_pos)-(1))
    while i > 0:
        snake.body_pos[i] = list(snake.body_pos[i-1])
        i = i - 1
    
    snake.body_pos[0] = list(snake.head_pos)

    if input == curses.KEY_LEFT:
        snake.head_pos[1] -= 1
    elif input == curses.KEY_RIGHT:
        snake.head_pos[1] += 1
    elif input == curses.KEY_DOWN:
        snake.head_pos[0] += 1
    elif input == curses.KEY_UP:
        snake.head_pos[0] -= 1
    
    if snake.head_pos in snake.body_pos:
        game_over(screen, snake)
    
    y_max, x_max = screen.getmaxyx()

    x_game_over = [-1, x_max]
    y_game_over = [-1, y_max]

    if snake.head_pos[0] in y_game_over or snake.head_pos[1] in x_game_over:
        game_over(screen, snake)

    snake.last_input = input
    return 

def increase_snake(screen, snake):
    snake.body_pos.insert(0, list(snake.head_pos))
    snake.score += 1
    snake.apple_exists = False
    add_apple(screen, snake) 
    


def set_screen_layout(screen):
    screen.clear()
    screen.border(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    screen.bkgd(' ', curses.color_pair(1))


curses.wrapper(set_up_board)
