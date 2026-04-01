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
    #INPUT HANDLING (msvcrt with Future Gaming)
    if msvcrt.kbhit():
        key = msvcrt.getch()
        
        #arrow key detection
        if key == b'\xe0' or key == b'\x00':
            key = msvcrt.getch()
            
            #LEFT MOVE CHECK
            if key == b'K' and anchor_x > 1:
                can_move_left = True
                #Check every '2' in the shape against the playfield
                for r in range(3):
                    for c in range(3):
                        if active_shape[r][c] == 2:
                            # Calculate where this block WOULD be if we move left
                            target_y = (anchor_y - 1) + r
                            target_x = (anchor_x - 1) + c - 1
                            
                            if playfield[target_y][target_x] == 1:
                                can_move_left = False #Hit a solid!
                
                if can_move_left:
                    anchor_x -= 1

            #RIGHT MOVE CHECK
            elif key == b'M' and anchor_x < 7:
                can_move_right = True
                for r in range(3):
                    for c in range(3):
                        if active_shape[r][c] == 2:
                            # Calculate where this block WOULD be if we move right
                            target_y = (anchor_y - 1) + r
                            target_x = (anchor_x - 1) + c + 1
                            
                            if playfield[target_y][target_x] == 1:
                                can_move_right = False # Hit a solid!
                
                if can_move_right:
                    anchor_x += 1

            #UP ARROW (ROTATE)
            elif key == b'H': 
                # Same logic for rotation
                next_state = (current_state + 1) % 4
                next_shape = shapes.L_STATES[next_state]
                can_rotate = True
                
                for r in range(3):
                    for c in range(3):
                        if next_shape[r][c] == 2:
                            #Check if the rotated shape overlaps any 1s
                            target_y = (anchor_y - 1) + r
                            target_x = (anchor_x - 1) + c
                            
                            #boundary check for rotation (edge cases)
                            if target_x < 0 or target_x > 8 or target_y > 8:
                                can_rotate = False
                            elif playfield[target_y][target_x] == 1:
                                can_rotate = False
                
                if can_rotate:
                    current_state = next_state
        
        elif key == b'q' or key == b'Q':
            break

    #FUTURE GAMING (Preemptive Collision Check)

    #Get the shape and sensor datas from our library file
    active_shape = shapes.L_STATES[current_state]
    active_sensors = shapes.L_SENSORS[current_state]

    collision_detected = False
    for point in active_sensors:
        check_y = anchor_y + point[0] 
        check_x = (anchor_x - 1) + point[1]

        if check_y > 8: 
            collision_detected = True
            break
        elif playfield[check_y][check_x] == 1: 
            collision_detected = True
            break

    #MOVEMENT/SOLIDIFY
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
                if active_shape[r][c] == 2:
                    py = (anchor_y - 1) + r
                    px = (anchor_x - 1) + c
                    playfield[py][px] = 2
    else:
        #BOOM BOOM BOOM
        for r in range(3):
            for c in range(3):
                if active_shape[r][c] == 2:
                    py = (anchor_y - 1) + r
                    px = (anchor_x - 1) + c
                    playfield[py][px] = 1
        
        #LINE CLEAR
        for r in range(9):
            if 0 not in playfield[r]:
                playfield.pop(r)
                playfield.insert(0, [0,0,0,0,0,0,0,0,0])

        # SHUT OFF CHECK
        # Always check against State 0 (The spawn state)
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

    draw()
    time.sleep(0.30) #made it slower for testing
