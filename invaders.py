# Based on https://www.youtube.com/watch?v=Q-__8Xw9KTM&ab_channel=UnityCoin
import random
from classes.button import Button
from classes.player import Player
from classes.enemy import Enemy
from classes.explosion import Explosion
from classes.model import Model
from slimstampen.spacingmodel import Response
from utilities.constants import *
from utilities.main_functions import *
# import utility

# initialize font usage
pygame.font.init()
pygame.init()

# How big is our window going to be, dimensions depend on the screen preventing windows to be too big
infoObject = pygame.display.Info()

def main():
    # Dictates if while loop is going to run
    run = True
    # Amount of frames per second (checking if character is moving once every second)
    FPS = 60
    level = 0
    lives = 3
    main_font = pygame.font.SysFont("notosansmonocjkkr", 30)
    lost_font = pygame.font.SysFont("notosansmonocjkkr", 60)
    # If you want to know which fonts are available
    # print(src.font.get_fonts())

    enemies = []
    # Every level a new wave will be created of 5 enemies
    wave_length = 5
    enemy_velocity = 1

    # How fast the player can move every time you press the key a max of 5 pixels to move
    player_velocity = 5
    laser_velocity = 4

    # Define a player space ship at location
    player = Player(WIDTH / 2, HEIGHT)
    # Center the ship on screen
    player.x -= (player.get_width() / 2)
    player.y -= (player.get_height() + 50)

    clock = pygame.time.Clock()
    
    # Define reference to Model class
    model = Model()

    lost = False
    lost_count = 0

    def show_answer(is_correct, answer, x, y):

        if is_correct:
            text = "Correct!"
            box = CORRECT_BOX
            main_font_size = 30
            main_font = pygame.font.SysFont("notosansmonocjkkr", main_font_size)
            correct_label = main_font.render(text, 1, WHITE)
            y_label = y + box.get_height() / 2 - correct_label.get_height() / 2

        else:
            text = "Incorrect! Answer was: "
            box = INCORRECT_BOX
            main_font_size = 15
            main_font = pygame.font.SysFont("notosansmonocjkkr", main_font_size)
            correct_label = main_font.render(text, 1, WHITE)
            y_label = y + box.get_height() / 2 - 1.5 * correct_label.get_height()


        answer_font = pygame.font.SysFont("notosansmonocjkkr", 40)
        answer_label = answer_font.render(str(answer), 1, WHITE)
        WINDOW.blit(box, (
            x, y,
            box.get_width() + 50, box.get_height()))
        WINDOW.blit(correct_label, (
            x + 100, y_label))
        if not is_correct:
            WINDOW.blit(answer_label, (
                x + box.get_width() / 2 - answer_label.get_width() / 2, y_label + correct_label.get_height() / 2))
        pygame.display.update()
        # Show the correct answer for 2 seconds
        time.sleep(2)

    def kill_enemy(enemy):
        enemy_center_loc = (enemy.x + enemy.get_width() / 2, enemy.y + enemy.get_height() / 2)
        explosion = Explosion(enemy_center_loc, 'large')
        all_sprites.add(explosion)
        enemies.remove(enemy)

    def redraw_window():
        # Draw the background img at coordinate: 0,0 (which is the top left)
        WINDOW.blit(BACKGROUND, (0, 0))

        all_sprites.update()
        all_sprites.draw(WINDOW)

        # Draw text (f strings embed variables)
        lives_label = main_font.render(f"Lives: {lives}", 1, WHITE)
        level_label = main_font.render(f"Level: {level}", 1, WHITE)
        # Top left hand corner plus a little offset
        WINDOW.blit(lives_label, (10, 10))
        # Top light hand corner (width screen minus width of label minus 10 pixels offset
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        # Draw all enemies (before you initialize the player so the player goes over them)
        for enemy in enemies:
            enemy.draw(WINDOW)
        # Draw the player
        player.draw(WINDOW)

        if lost:
            lost_label = lost_font.render("You Lost!", 1, WHITE)
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))

        # refresh the display surface
        pygame.display.update()

    # TODO: When shooting an enemy tell the player the "explosion code" needs to be entered
    while run:
        clock.tick(FPS)

        redraw_window()
        # No more lives or health then you lost
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        if lost:
            # FPS * 3 = 3 sec
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        # If there are no more enemies on screen then
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                # TODO: when enemies overlap they need to be offset
                # TODO: probably -100 is too low
                # pick random positions way up the screen for enemies to spawn in to make it look like they come in at
                # different height and Random choice from color list
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # Check for all events (keypresses, mouseclick, etc.
        for event in pygame.event.get():
            # if the 'x' on the right top is pressed the game is quit
            if event.type == pygame.QUIT:
                # YOU COULD CHANGE THIS TO quit() to press 'x' and quit the program
                run = False
        # check and get all keyboard keys that are pressed
        keys = pygame.key.get_pressed()
        # Key to move and don't let the player move off screen
        if keys[pygame.K_LEFT] and player.x + player_velocity > 0:
            # Move to the left
            player.x -= player_velocity
        # Adding 50 for width of the player's spaceship
        if keys[pygame.K_RIGHT] and player.x + player_velocity + player.get_width() < WIDTH:
            # Move to the right
            player.x += player_velocity
        if keys[pygame.K_UP] and player.y + player_velocity > 0:
            # Move up
            player.y -= player_velocity
        if keys[pygame.K_DOWN] and player.y + player_velocity + player.get_height() < HEIGHT:
            # Move down
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Move the enemies downwards all the time, [:] means a copy of the list (just to be sure nothing bad happens)
        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            # Check if laser hit the player
            enemy.move_lasers(laser_velocity, player)
            # Roughly every 2 sec an enemy should shoot, randomly determined
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            # When the player collides with the enemy the enemy is removed and player's health reduces
            elif collide(enemy, player):
                player.health -= 10
                kill_enemy(enemy)

            # If the enemy moves off screen lose a life
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        # Laser velocity needs to be negative since the y value is lower upwards the screen, meaning laser will go up
        # TODO: Extra parameter SlimStampen question
        has_hit_enemy, enemy = player.move_lasers(-laser_velocity, enemies, WINDOW)
        if has_hit_enemy:

            kill_enemy(enemy)
            # Record question onset time
            question_onset_time = int(round(time.time() * 1000)) - START_TIME
            # Get a new question from the model
            new_fact = model.get_next_fact()
            answer = f"{new_fact[2]}"
            question = f"{new_fact[1]} = "
            # TODO: Add multiplication showing and check if answer is correct or wrong
            main_font = pygame.font.SysFont("notosansmonocjkkr", 30)
            answer_label = main_font.render(question, 1, (0, 0, 0))
            upper_label = main_font.render(f"Enter the kill code below", 1, (152, 76, 62))
            string = ""
            # src.draw.rect(WINDOW,(0,0,255),(WIDTH/2 - answer_label.get_width()/2, HEIGHT/2 - answer_label.get_height()/2,answer_label.get_width()+50,answer_label.get_height()))
            answer_box_x = WIDTH / 2 - ANSWER_BOX.get_width() / 2
            answer_box_y = HEIGHT / 2 - ANSWER_BOX.get_height() / 2
            WINDOW.blit(ANSWER_BOX, (
                answer_box_x, answer_box_y,
                ANSWER_BOX.get_width() + 50, ANSWER_BOX.get_height()))
            WINDOW.blit(answer_label, (
                answer_box_x + 30, HEIGHT / 2 + answer_label.get_height() / 4))
            WINDOW.blit(upper_label, (
                answer_box_x + 30, HEIGHT / 2 - 1.5 * answer_label.get_height()))
            pygame.display.update()

            while True:

                event = pygame.event.poll()
                keys = pygame.key.get_pressed()

                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)  # Returns string id of pressed key.

                    if len(key) == 1:  # This covers all letters and numbers not on numpad.
                        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                            # if  # Include any other shift characters here.
                            # else:
                            string += key.upper()
                        else:
                            string += key
                    # elif  # Include any other characters here.
                    elif key == "backspace":
                        # TODO: Make this work by erasing the current string
                        string = string[:-1]
                        WINDOW.blit(ANSWER_BOX, (
                            answer_box_x, answer_box_y,
                            ANSWER_BOX.get_width() + 50, ANSWER_BOX.get_height()))
                        WINDOW.blit(answer_label, (
                            answer_box_x + 30, HEIGHT / 2 + answer_label.get_height() / 4))
                        WINDOW.blit(upper_label, (
                            answer_box_x + 30, HEIGHT / 2 - 1.5 * answer_label.get_height()))
                        pygame.display.update()
                    elif event.key == pygame.K_RETURN:  # Finished typing.
                        # Record response time
                        response_time = int(round(time.time() * 1000)) - question_onset_time
                        # Log the response
                        # Stringify answer instead of typecasting string as int (since a string might not
                        # be castable)
                        if str(answer) == string:
                            print("Correct!")
                            resp = Response(new_fact, question_onset_time, response_time, True)
                            Model().m.register_response(resp)
                            show_answer(True, answer, answer_box_x, answer_box_y + ANSWER_BOX.get_height())
                        else:
                            print("Wrong! The correct answer was " + str(answer))
                            resp = Response(new_fact, question_onset_time, response_time, False)
                            Model().m.register_response(resp)
                            show_answer(False, answer, answer_box_x, answer_box_y + ANSWER_BOX.get_height())
                        break

                    text = main_font.render(string, 1, (108, 99, 255))
                    WINDOW.blit(text, (WIDTH / 2 - answer_label.get_width() / 2 + 40,
                                       HEIGHT / 2 + answer_label.get_height() / 4))
                    pygame.display.update()


def main_menu():
    title_font = pygame.font.SysFont("notosansmonocjkkr", 70)
    button_font = pygame.font.SysFont("notosansmonocjkkr", 30)
    startButton = Button(PURPLE, WIDTH/2, HEIGHT, 250, 80, button_font, "Start game!")
    # Move the startButton a bit upwards (by leaving a gap of its own height between the bottom and itself
    startButton.y -= startButton.height * 2
    # Center the startButton on screen
    startButton.x -= startButton.width / 2
    run = True
    while run:

        WINDOW.blit(BACKGROUND, (0, 0))
        startButton.draw(WINDOW)
        title_label = title_font.render("Multiplication Invaders", 1, WHITE)
        title_label_drop_shadow = title_font.render("Multiplication Invaders", 1, BLACK)
        offset = 3
        WINDOW.blit(title_label_drop_shadow, (WIDTH / 2 - title_label.get_width() / 2 + offset, HEIGHT / 2 - title_label.get_height() + offset))
        WINDOW.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, HEIGHT / 2 - title_label.get_height()))
        pygame.display.update()
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()

            # if pressing quit 'x' then stop
            if event.type == pygame.QUIT:
                run = False
            # if start button is pressed then start the game
            if event.type == pygame.MOUSEMOTION:
                if startButton.isHovered(position):
                    startButton.color = GREEN
                else:
                    startButton.color = PURPLE
            # if start button is pressed then start the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.isHovered(position):
                    #initi slipsta
                    main()
    pygame.quit()

main_menu()
