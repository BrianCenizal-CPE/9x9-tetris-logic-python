#Prototype for the 9x9 tetris game
import os
import time
import msvcrt

#WORLD SETUP (9X9)
playfield = []
for i in range(9):
    playfield.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

#SHAPE SETUP (3X3)
shape_L = [
    [0, 2, 0],
    [0, 2, 0],
    [0, 2, 2]
]
shape_L_bottoms = [[2, 1], [2, 2]]

#GAME STATE
anchor_y = 1
anchor_x = 4
solid = False
lock_ticks = 0
game_over = False

def draw():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("9x9 TETRIS - USE ARROW KEYS TO MOVE (Q TO QUIT)")
    print("---------------------------")
    for row in playfield:
        line = ""
        for cell in row:
            if cell == 1: line += "■ " 
            elif cell == 2: line += "▣ " 
            else: line += "□ "          
        print(line)
    print("---------------------------")

#REAL-TIME GAME LOOP
while not game_over:
    #VANISH THE 2s
    for r in range(9):
        for c in range(9):
            if playfield[r][c] == 2:
                playfield[r][c] = 0

    #INPUT HANDLING (the msvcrt logic)
    if msvcrt.kbhit(): #if a key is waiting in the buffer
        key = msvcrt.getch() #grab the key
        
        if key == b'\xe0' or key == b'\x00':
            key = msvcrt.getch() # Read the second part of the arrow key
            if key == b'K' and anchor_x > 1: # 'K' is Left Arrow
                anchor_x -= 1
            elif key == b'M' and anchor_x < 7: # 'M' is Right Arrow
                anchor_x += 1
        
        elif key == b'q' or key == b'Q': # Quit key
            break

    #FUTURE GAMING (Preemptive Collision Check)
    collision_detected = False
    for point in shape_L_bottoms:
        check_y = anchor_y + point[0] 
        check_x = (anchor_x - 1) + point[1]

        if check_y > 8: 
            collision_detected = True
            break
        elif playfield[check_y][check_x] == 1: 
            collision_detected = True
            break

    #MOVEMENT/SOLIDIFY LOGIC
    if collision_detected:
        lock_ticks += 1
        if lock_ticks >= 3: 
            solid = True
    else:
        anchor_y += 1 
        lock_ticks = 0

    #INHERITANCE
    if not solid:
        for r in range(3):
            for c in range(3):
                if shape_L[r][c] == 2:
                    py = (anchor_y - 1) + r
                    px = (anchor_x - 1) + c
                    playfield[py][px] = 2
    else:
        #BOOM BOOM BOOM (Solidify)
        for r in range(3):
            for c in range(3):
                if shape_L[r][c] == 2:
                    py = (anchor_y - 1) + r
                    px = (anchor_x - 1) + c
                    playfield[py][px] = 1
        
        #LINE CLEAR
        for r in range(9):
            if 0 not in playfield[r]:
                playfield.pop(r)
                playfield.insert(0, [0,0,0,0,0,0,0,0,0])

        #SHUT OFF CHECK (Future Gaming for Spawn)
        for r in range(3):
            for c in range(3):
                if shape_L[r][c] == 2:
                    target_y = (1 - 1) + r
                    target_x = (4 - 1) + c
                    if playfield[target_y][target_x] == 1:
                        game_over = True
        
        if game_over:
            draw()
            print("!!! SHUT OFF: SPAWN BLOCKED !!!")
            break

        #RESET AFTER SOLIDIFY
        anchor_y = 1
        anchor_x = 4
        solid = False
        lock_ticks = 0

    #RENDER
    draw()
    time.sleep(0.15)
