#PSEUDO CODE FOR THE TETRIS GAME
playfield = []
for i in range(9):
    row = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    playfield.append(row)


shape_L = [
    [0, 2, 0],
    [0, 2, 0],
    [0, 2, 2]
]
shape_L_bottoms = [[2, 1], [2, 2]]

spawn_y = 1
spawn_x = 4

anchor_y = 1
anchor_x = 4

its a loop bish lets say tick is like half a second
solid=false
if edge == 0 and solid==false, make sensor 5 wide and 4 tall
  have shape-L copy its 2s using +1 on x and +0 on y(i think) where sensors coord value of 0s may or may not turn into the shape-ls coord value of 2s  
  #this leave us with permanent empty left and right and bottom spaces whatever 3x3 shape you give, etc
  then the sensing blocks would be all left and right blocks, while refering to the shapeLbottoms +1 on y to be the active sensor and checker, etc...
  anchor coordinates will be dead center 2x,1y of sensor
elif edge != 0 and solid==false
  make sensor 4 wide and 4 tall
  if edge = 1
    have shape-L copy its 2s using +1 on x and +0 on y and the usual
    anchor coordinates would be  2x,1y
  else
    have shape-l copy its 2s using +0 on x and +0 also on y  
    anchor coordinates would be  1x,1y
  elif solid==true
    none

everytick(predeterminedtime), anchor_y -= 1 , every tick * 2
every left press, anchor_x -=1
every right press, anchor +=1
if anchor_x-1 == 1 edge = -1, ignore left press
if anchor_x+1 == 8 edge = 1, ignore right press
else edge = 0
#in such an "edgy" scenario im thinking of just turning the sensor to a 4x4 to fit, etc..
anyways if 2-6 ticks happen while the bottom sensor triggered without stopping, solid=true
if solid==false
  anyways everytick all the 2s vanish and replace by 0 while 1s stay... while sensor replace the proper position of two
  anyways sensor finally checks that if bottom sensors are 1 and it stops falling down for a couple of tick up until it considers as solidified, etc
  anyways left and right sensors check if x-1 and pressing left if the projection of the L-shape after the tick would have values that isnt 0 on the values that 2 would spawn on, etc(will start the check befor ethe tick even happens, so its future gaming lmao)
  same goes for x+1 and pressing right
    they get blocked or something, etc...
elif solid==true
   all 2 turns to 1 in the respective coordinates like from the reference anchor and boom boom boom
   check if occupied horizontal line of the L-shape when solidified all has 1 value, etc... then delete said horizontal list and then append a new list as the new 0 while the rest adjust, etc
   anchorx&y=spawnx&y
