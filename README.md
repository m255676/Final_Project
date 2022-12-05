# Final Project
 Jet Bomber Game

Objective:
- Hit as many tanks as you can
- Don't let the enemy shoot you down x
- Beat the high score

How to Play: 
1. Use Spacebar to drop bombs on Tanks
2. Use the left arrow key to shoot missiles
3. Use the right arrow key to speed up
4. Use the up arrow key to increase altitude
5. Use the down arrow key to decrease altitude

Game Play:
- You start out with three lives, shoot care packages 
that spawn at the start of every level in order to gain back lives
- Each pass you will only have 4 missiles and 4 bombs; they will reset when your jet 
returns the left side of the screen
- The game will speed up overtime: the tanks, tank spawn frequency, enemy jet, and enemy
missile spawn frequency all speed up
- As the game speeds up the point value
for hitting each tank will increase

Code Achievements Reference:

- Keyboard King: 
  - game.py line 200 
- Level Up: 
  - game.py line 134
  - game.py line 145
  - jet.py line 67
- Healthy Eater:
  - game.py line 137
  - power_up.py line 51
- Looking Weak:
  - jet.py line 40
- Points R Us:
  - jet.py line 73
  - scoreboard.py line 92
- Over Achiever:
  - scoreboard.py line 106
- Physical:
  - bomb.py line 67
- Tricky Trig:
  - enemy_jet.py line 43
  - power_up.py line 46
- Helping Hand:
  - Helped Paulina Finn
install keydown events so that her penguin moves up
while the spacebar is held down
- Shifting Screens:
  - game.py line 325
- Save Game:
  - game.py line 64, line 247
- Tick Tock:
  - game.py line 90

Additional Considerations for Grading:
- Conditional Explosion Images:
  - I feel this is worth 2 points.
  - The bomb explosion image changes depending on if the bomb has collided with
    the tank or with the ground. This is a feature that I feel adds to the game's aesthetic value.
    Also, because the ground is not a sprite object but a position on the screen, discerning between wether the bomb hit the
    tank or the ground first became a very ardious task and required a substantial amount of time before the flags and game logic
    accounted for this as I had to make considerations for each bomb's constant change in motion, the collision point at each tank, the collision height for which each bomb and the ground collide,
    and the changed image's new rect y pos.