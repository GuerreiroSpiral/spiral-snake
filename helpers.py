def print_center(screen, message, row_offset=0, col_offset=0):
    num_rows, num_col = screen.getmaxyx()
    middle_row = int((num_rows+row_offset+1)/2) 
    middle_column = int((num_col+col_offset+1)/2)

    x_pos = middle_column - (int(len(message)/2)) # Even with the middle column, we still need to consider the length of the message

    screen.addstr(middle_row, x_pos, message)
    screen.refresh()

def get_middle(screen):
    num_rows, num_col = screen.getmaxyx()
    return int(num_rows/2), int(num_col/2)