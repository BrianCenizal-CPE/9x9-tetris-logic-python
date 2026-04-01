import os
import time
import msvcrt
import shapes

# WORLD SETUP (9x9)
playfield = []
for i in range(9):
    playfield.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

#GAME STATE
anchor_y = 1
anchor_x = 4
current_state = 0 # 0, 1, 2, or 3
solid = False
lock_ticks = 0
game_over = False

def can_it_fit(test_shape, test_y, test_x):
#Checks if a specific shape configuration would overlap any 1s or walls.

    for r in range(3):
        for c in range(3):
            if test_shape[r][c] == 2:
                #Calculate real playfield coordinates
                target_y = (test_y - 1) + r
                target_x = (test_x - 1) + c
                
                #Check if outside playfield (Walls/Floor)
                if target_y < 0 or target_y > 8 or target_x < 0 or target_x > 8:
                    return False
                
                #Check if overlapping a solid block (1)
                if playfield[target_y][target_x] == 1:
                    return False
    return True #It passes all tests!

def draw():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("9x9 TETRIS - ARROWS: MOVE | UP: ROTATE | Q: QUIT")
    print("---------------------------")
    for row in playfield:
        line = ""
        for cell in row:
            if cell == 1: line += "■ " 
            elif cell == 2: line += "▣ " 
            else: line += "□ "          
        print(line)
    print("---------------------------")
while not game_over:
    #VANISH THE 2s
    for r in range(9):
        for c in range(9):
            if playfield[r][c] == 2:
                playfield[r][c] = 0

    #INPUT HANDLING (Buffer Flush)
    key_pressed = None
    while msvcrt.kbhit():
        key = msvcrt.getch()
        if key == b'\xe0' or key == b'\x00':
            key_pressed = msvcrt.getch()
        else:
            key_pressed = key

    #Get the current shape state BEFORE handling input
    active_shape = shapes.L_STATES[current_state]

    if key_pressed:
        if key_pressed == b'K': # Left
            if can_it_fit(active_shape, anchor_y, anchor_x - 1):
                anchor_x -= 1
        elif key_pressed == b'M': # Right
            if can_it_fit(active_shape, anchor_y, anchor_x + 1):
                anchor_x += 1
        elif key_pressed == b'H': # Rotate (Up)
            next_s = (current_state + 1) % 4
            if can_it_fit(shapes.L_STATES[next_s], anchor_y, anchor_x):
                current_state = next_s
        elif key_pressed in [b'q', b'Q']:
            break

    #GRAVITY TICK (Checks Down)
    #update active_shape here again in case it just rotated
    active_shape = shapes.L_STATES[current_state]

    #Use can_it_fit to look one block down
    if can_it_fit(active_shape, anchor_y + 1, anchor_x):
        anchor_y += 1
        lock_ticks = 0 #its falling, so reset the timer
    else:
        #If it cant fit below, start solidifying
        lock_ticks += 1
        if lock_ticks >= 3: 
            solid = True

    #INHERITANCE/SOLIDIFY (Boom Boom Boom)
    if not solid:
        for r in range(3):
            for c in range(3):
                if active_shape[r][c] == 2:
                    py = (anchor_y - 1) + r
                    px = (anchor_x - 1) + c
                    playfield[py][px] = 2
    else:
        #Turn 2s to 1s
        for r in range(3):
            for c in range(3):
                if active_shape[r][c] == 2:
                    playfield[(anchor_y-1)+r][(anchor_x-1)+c] = 1
        
        #Line Clear
        for r in range(9):
            if 0 not in playfield[r]:
                playfield.pop(r)
                playfield.insert(0, [0,0,0,0,0,0,0,0,0])

        #SHUT OFF CHECK
        spawn_shape = shapes.L_STATES[0]
        for r in range(3):
            for c in range(3):
                if spawn_shape[r][c] == 2:
                    if playfield[(1-1)+r][(4-1)+c] == 1:
                        game_over = True
        
        if game_over:
            draw()
            print("!!! SHUT OFF: SPAWN BLOCKED !!!")
            break

        # RESET
        anchor_y = 1
        anchor_x = 4
        current_state = 0
        solid = False
        lock_ticks = 0

    #RENDER
    draw()
    time.sleep(0.30)
