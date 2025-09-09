import curses
import random
import time

# Directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100) # Refresh every 100 ms

    sh, sw = stdscr.getmaxyx()
    box = [[3,3], [sh-3, sw-3]]

    # Draw borders
    for y in range(box[0][0], box[1][0]):
        stdscr.addch(y, box[0][1], '|')
        stdscr.addch(y, box[1][1]-1, '|')
    for x in range(box[0][1], box[1][1]):
        stdscr.addch(box[0][0], x, '-')
        stdscr.addch(box[1][0]-1, x, '-')

    # Initial snake and food
    snake = [
        [sh//2, sw//2+1],
        [sh//2, sw//2],
        [sh//2, sw//2-1]
    ]
    direction = RIGHT

    food = [random.randint(box[0][0]+1, box[1][0]-2), random.randint(box[0][1]+1, box[1][1]-2)]
    stdscr.addch(food[0], food[1], '@')

    score = 0
    key = curses.KEY_RIGHT

    while True:
        next_key = stdscr.getch()
        if next_key != -1:
            key = next_key

        # Choose direction
        if key in [curses.KEY_UP, ord('w')] and direction != DOWN:
            direction = UP
        elif key in [curses.KEY_DOWN, ord('s')] and direction != UP:
            direction = DOWN
        elif key in [curses.KEY_LEFT, ord('a')] and direction != RIGHT:
            direction = LEFT
        elif key in [curses.KEY_RIGHT, ord('d')] and direction != LEFT:
            direction = RIGHT

        # Calculate next head
        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

        # Collision detection
        if (
            new_head[0] in [box[0][0], box[1][0]-1] or
            new_head[1] in [box[0][1], box[1][1]-1] or
            new_head in snake
        ):
            msg = f"Game Over! Score: {score}"
            stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg)
            stdscr.nodelay(0)
            stdscr.getch()
            break

        # Insert new head
        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = None
            while food is None:
                nf = [
                    random.randint(box[0][0]+1, box[1][0]-2),
                    random.randint(box[0][1]+1, box[1][1]-2)
                ]
                if nf not in snake:
                    food = nf
            stdscr.addch(food[0], food[1], '@')
        else:
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], ' ')

        stdscr.addch(new_head[0], new_head[1], '#')
        stdscr.addstr(box[0][0] - 2, box[0][1], f'Score: {score}')

if __name__ == "__main__":
    curses.wrapper(main)
