import sys
import pygame
from jet import Jet
from settings import Settings
from ground import Ground
from enemy_tank import Enemy_Tank
from bomb import Bomb
from enemy_jet import Enemy_Jet
from enemy_missile import Enemy_Missile
from friendly_missile import Friendly_Missile
from button import PlayButton
from button import PauseButton
from button import PlayAgainButton
from game_stats import GameStats
from scoreboard import Scoreboard

class JetFighterGame:
    """Overall Class to manage game assests and behaviors"""
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()


        self.lives_left = self.settings.lives_left

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Jet Fighter Game")
        self.back_ground = pygame.image.load('images/blue_sky_background.bmp')
        self.back_ground = pygame.transform.scale(self.back_ground, (self.settings.screen_width, self.settings.screen_height))

        self.loop_speed = 80
        self.counter = 0

        # The following have to be initialized before running jet and enemy_jet in order for the game logic to work
        # Create instance of Gamestats and Scoreboard in order to use their functionality
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.score_multiplier = self.settings.score_multiplier

        self.jet = Jet(self)
        self.enemy_jet = Enemy_Jet(self)
        self.ground = Ground(self)



        self.bombs = pygame.sprite.Group()
        self.enemy_tanks = pygame.sprite.Group()
        self.enemy_missiles = pygame.sprite.Group()
        self.friendly_missiles = pygame.sprite.Group()

        self.game_active = False
        self.game_paused = False

        self.play_button = PlayButton(self, "Single Player")
        self.pause_button = PauseButton(self, "Pause")
        self.play_again_button = PlayAgainButton(self, "Play Again")
        self.trigger_decrease = 20
        self.make_new_tanks_trigger = 300
        self.shoot_enemy_missile_trigger = 175


    def run_game(self):
        """This is the main loop for the game"""
        # Need to make an instance of the first tank to run before the counter starts making new tanks
        first_tank = Enemy_Tank(self)
        self.enemy_tanks.add(first_tank)
        while not self.game_active:
            self._check_events()
            self._update_screen()

        while self.game_active:
                # Run the game while the game is not paused and the player still has lives
                if not self.game_paused:
                    # Always set this to the adjusted number in settings
                    self.lives_left = self.settings.lives_left
                    if self.lives_left <=0:
                        self._end_game()
                        break
                    self._check_events()

                    # This will move the tanks
                    # Pass in counter so tanks will speed themselves up over time
                    self.enemy_tanks.update(self.counter)

                    # This will update the bombs in our sprite group
                    self.bombs.update()
                    # Check Ground Collisions for bombs
                    self._check_ground_collision()

                    # Track Time using a counter
                    self.counter += 1

                    # After certain time make tanks
                    if (self.counter % self.make_new_tanks_trigger == 0):
                        self._make_new_tanks()

                    # After certain time make enemy jet shoot missiles
                    if (self.counter % self.shoot_enemy_missile_trigger == 0):
                        self._shoot_enemy_missile()

                    # After certain time decrement the time it will take to make new tanks and shoot enemy missiles
                    # Doing this to speed up the frequency at which these events happen, speeding up game play
                    # This will only decrement to a certain amount to maintain reasonable playability
                    if (self.counter % 500 == 0):
                        # make new tanks trigger can only reach this low
                        if self.make_new_tanks_trigger <= 150:
                            self.make_new_tanks_trigger = 150
                        else:
                            self.make_new_tanks_trigger -= self.trigger_decrease
                        # shoot enemy missile trigger can only reach this low
                        if self.shoot_enemy_missile_trigger <= 100:
                            self.shoot_enemy_missile_trigger = 100
                        else:
                            self.shoot_enemy_missile_trigger -= self.trigger_decrease

                    # Every 500 ms the tank movement speed, tank spawn speed, enemy jet movement speed, and enemy jet
                    # missile spawn frequency increases, so I will say that for every 10 times we speed up the game
                    # this will be a new level
                    # Set to 100 for testing
                    if (self.counter % 500*10) == 0:
                        self.scoreboard.prep_game_level()
                        self.settings.game_level += 1
                        print(f"self.settings: {self.settings.game_level}")
                        # With each level up a power up that grants and extra life will spawn and travel
                        # in at a cos curve shooting the power up grant you an additional life


                    # update the missiles so they travel across the screen.
                    self.enemy_missiles.update()
                    self.friendly_missiles.update()

                    # This will call the jet movement functions for each jet passing in the neccessary groups to
                    # detect for collisions between game elements (there is no particular reason most of this
                    # evaluation takes place in the jet move function)
                    # Also pass in counter so that the score multiplier is incremented based on game level and time
                    self.jet.move_jet(self.enemy_missiles, self.friendly_missiles, self.bombs, self.enemy_tanks, self.counter)
                    self.enemy_jet.flight(self.counter, self.friendly_missiles)

                    # Control FPS
                    self.clock.tick(self.loop_speed)

                    # Update Screen
                    self._update_screen()


                # If the game is paused just continue to draw everything at its last position
                # and continue to look for events in order to exit or unpause the game
                elif self.game_paused:
                    self._check_events()
                    self._update_screen()

    def _check_events(self):
        """This method responds to key events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check for mouse button down event and log the position of it
                #       so that we can check for the button being 'clicked' in our check play button function
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_pause_button(mouse_pos)
                self._check_play_again_button(mouse_pos)

    def _check_keydown_events(self, event):
        """This method responds to keypresses"""
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_UP:
            self.jet.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.jet.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._drop_bomb()
        elif event.key == pygame.K_RIGHT:
            self.jet.speeding_up = True
        elif event.key == pygame.K_LEFT:
            self._shoot_friendly_missile()

    def _check_play_button(self, mouse_pos):
        """ Start a new game when the player clicks Play"""
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # Only start the game if the game is not running and the button is clicked
        # These conditions mean that the game won't restart if the button area is accidentally clicked in game
        if play_button_clicked and not self.game_active:
            self.game_active = True
            self.first_start = False

    def _check_pause_button(self, mouse_pos):
        """ Pause the game if the game is not already paused"""
        pause_button_clicked = self.pause_button.rect.collidepoint(mouse_pos)
        if pause_button_clicked and not self.game_paused:
            self.game_active = True
            self.game_paused = True
        # If the pause button is clicked while the game is already paused then unpause the game
        elif pause_button_clicked and self.game_paused:
            self.game_paused = False

    def _check_play_again_button(self, mouse_pos):
        """Only respond to clicking the play again button if the game has stopped and there are no lives left"""
        play_again_button_clicked = self.play_again_button.rect.collidepoint(mouse_pos)
        # The play again button will reset the game and reset all game stats
        if self.lives_left <= 0 and play_again_button_clicked:
            # Empty Bomb, Missiles, and Tank List and Reset Jet positions
            # Reset the counter and all game stats:
            self.settings.lives_left = 1
            self.settings.game_level = 1
            self.jet._reset_jet()
            self.friendly_missiles.empty()
            self.enemy_missiles.empty()
            self.enemy_tanks.empty()
            self.bombs.empty()
            self.counter = 0
            self.enemy_jet.reset_jet()
            # Have to reset the points awarded for hitting tanks as this number otherwise increases relative to the
            # game level
            self.settings.tank_hit_points = 50
            # Before I set the current score back to zero I need to evaluate if this is a new highscore so I call
            # the following:
            self.scoreboard.check_high_score()
            # Once I've checked the score I reset the current stats to their respective starting value
            self.stats.reset_stats()
            # Call the prep score and prep high score functions so the score, high score, and level is displayed at the
            # start of the game
            self.scoreboard.prep_score()
            self.scoreboard.prep_high_score()
            self.scoreboard.prep_game_level()

            self.run_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_UP:
            self.jet.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.jet.moving_down = False
        elif event.key == pygame.K_RIGHT:
            self.jet.speeding_up = False

    def _make_new_tanks(self):
        """After counter hits target number/ after desired elapsed time, make a new tank"""
        new_enemy_tank = Enemy_Tank(self)
        self.enemy_tanks.add(new_enemy_tank)
    def _shoot_enemy_missile(self):
        """"After counter hits target number/ after desired elapsed time, make a new missile"""
        new_enemy_missile = Enemy_Missile(self)
        self.enemy_missiles.add(new_enemy_missile)
    def _shoot_friendly_missile(self):
        """On key event make a missile instance and add to group to be updated in game loop"""
        new_friendly_missile = Friendly_Missile(self)
        self.friendly_missiles.add(new_friendly_missile)

    def _drop_bomb(self):
        """Create a new bomb and add it to the Sprite group"""
        new_bomb = Bomb(self)
        self.bombs.add(new_bomb)

    def _check_ground_collision(self):
        """Check if the bomb's ground collision flag is true and delete bomb if it is"""
        for bomb in self.bombs.sprites():
            if bomb.ground_collision:
                bomb.kill()

    def _end_game(self):
        """Run until play again button is clicked or game is exited"""
        while True:
            self.screen.fill((255, 0, 0))
            self.font = pygame.font.SysFont(None, 72)
            self.img = self.font.render(f"GAME OVER", True, (230, 230, 230))
            self.img_rect = self.img.get_rect()
            self.img_rect.center = (self.screen.get_rect().width/2, self.screen.get_rect().height/2 - 90)
            self.screen.blit(self.img, self.img_rect)
            self.clock.tick(self.loop_speed)
            self.play_again_button.draw_button()
            self._check_events()
            pygame.display.flip()


    def _update_screen(self):
        """This method updates the screen"""
        self.screen.blit(self.back_ground, (0,0))
        self.ground.blitme()
        self.jet.blitme()
        self.enemy_jet.blitme()
        for enemy_missile in self.enemy_missiles.sprites():
            enemy_missile.draw_missile()

        for friendly_missile in self.friendly_missiles.sprites():
            friendly_missile.draw_missile()

        for enemey_tank in self.enemy_tanks.sprites():
            enemey_tank.draw_tank()

        for bomb in self.bombs.sprites():
            bomb.draw_bomb()

        # Draw a red backdrop if the game has not started yet
        if not self.game_active:
            self.screen.fill((0, 0, 0))

        # Draw the play button if the game is not active
        if not self.game_active:
            self.play_button.draw_button()

        # Draw the pause button
        self.pause_button.draw_button()

        # Draw the scoreboard to the screen
        self.scoreboard.show_score()

        # Makes the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run the game
    play_game = JetFighterGame()
    play_game.run_game()
