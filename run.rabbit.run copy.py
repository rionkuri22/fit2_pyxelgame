import pyxel
import math  # used sqrt
import random  # used to change obstacle placement every time

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
PLAYER_SPEED = 1.2
ENEMY_SPEED = 0.9
TIMER = 30  # Game length is 30 seconds
BUTTON_SPEED = 0.5  # Speed of the button movement


class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH - 20  # Sets player's initial x-coordinate
        self.y = SCREEN_HEIGHT - 20  # Sets player's initial y-coordinate


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Button:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pressed = False # Initial state of the button (not pressed)
        self.direction = 1


class Obstacle:
    def __init__(self, x, y, design_x, design_y):
        self.x = x
        self.y = y
        self.design_x = design_x
        self.design_y = design_y


class Game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.load("IMAGES.pyxres")
        self.state = "start"  # Set initial game state to "start"
        self.level = 1  # Set initial game level to 1
        self.reset()
        pyxel.mouse(True)  # Enables mouse input
        pyxel.run(self.update, self.draw) # Start game loop

    def reset(self):
        self.player = Player() # Create player object
        self.enemies = [] # Empty list for enemies
        self.obstacles = []

        # Initialize the 4 buttons
        self.buttons = {
            "left": Button(0, SCREEN_HEIGHT // 2),
            "right": Button(SCREEN_WIDTH - 8, SCREEN_HEIGHT // 2),
            "top": Button(SCREEN_WIDTH // 2, 0),
            "bottom": Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 8)
        }

        self.timer = TIMER * 60  # Convert from seconds to frames (60 frames per second)
        self.collision_detected = False

        # Initialize enemies and obstacles based on level
        if self.level == 1:
            self.enemies = [Enemy(10, 10)]  # 1 enemy
            self.obstacles = self.generate_obstacles(7)  # 7 obstacles
        elif self.level == 2:
            self.enemies = [
                Enemy(10, 10),
                Enemy(SCREEN_WIDTH - 20, 10),
                Enemy(10, SCREEN_HEIGHT - 20)
            ]  # 3 enemies
            self.obstacles = self.generate_obstacles(7)  # 7 obstacles
        elif self.level == 3:
            self.enemies = [Enemy(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]  # 1 enemy
            self.obstacles = self.generate_obstacles(2)  # 2 obstacles

    def generate_obstacles(self, num_obstacles):
        obstacles = [] # Empty list for obstacles
        designs = [
            (0, 16),  # Obstacle design 1
            (16, 16),  # Obstacle design 2
            (32, 16),  # Obstacle design 3
            (48, 16)  # Obstacle design 4
        ]

        player_start_x = SCREEN_WIDTH - 20 # Player's starting x-coordinate
        player_start_y = SCREEN_HEIGHT - 20 # Player's starting y-coordinate
        min_distance = 20  # Minimum distance from player's start position

        for _ in range(num_obstacles):
            while True:
                obstacle_x = random.randint(20, SCREEN_WIDTH - 20)  # Randomly choose position
                obstacle_y = random.randint(20, SCREEN_HEIGHT - 20)
                design_index = random.randint(0, 3)  # Randomly choose design
                design_x, design_y = designs[design_index] # Get design coordinates

                # Check if the obstacle is not too close to the player's starting position
                if abs(obstacle_x - player_start_x) >= min_distance and abs(obstacle_y - player_start_y) >= min_distance:
                    obstacles.append(Obstacle(obstacle_x, obstacle_y, design_x, design_y)) # Add obstacle to list
                    break # Break loop when valid obstacle is placed

        return obstacles

    def check_collision_with_obstacles(self, x, y):
        for obstacle in self.obstacles:
            if abs(x - obstacle.x) < 15 and abs(y - obstacle.y) < 15: # Check if player is within 15 pixels of an obstacle
                return True
        return False

    def update(self):
        if self.state == "start":
            if pyxel.btnp(pyxel.KEY_1):
                self.level = 1
                self.state = "playing"
                self.reset()
            elif pyxel.btnp(pyxel.KEY_2):
                self.level = 2
                self.state = "playing"
                self.reset()
            elif pyxel.btnp(pyxel.KEY_3):
                self.level = 3
                self.state = "playing"
                self.reset()
        elif self.state == "playing":
            self.update_playing()
        elif self.state == "end":
            if pyxel.btnp(pyxel.KEY_0):
                if self.collision_detected:
                    self.state = "start"
                else:
                    self.level += 1
                    if self.level == 4:
                        self.state = "start"  # After completing Level 3, return to start
                    else:
                        self.state = "playing"
                    self.reset()

    def update_playing(self):
        # Player movement with key input
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            self.move_player(0, -PLAYER_SPEED)
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.move_player(0, PLAYER_SPEED)
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.move_player(-PLAYER_SPEED, 0)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.move_player(PLAYER_SPEED, 0)

        # Updates positions of enemies to move towards the player
        for i in range(len(self.enemies)):
            enemy = self.enemies[i]  # Current position of enemy
            dx = self.player.x - enemy.x  # Calculate distance between the enemy player and enemy
            dy = self.player.y - enemy.y
            dist = math.sqrt(dx * dx + dy * dy) # Calculate Euclidean distance between player and enemy using Pythagorean theorem
            if dist != 0:  # Checks if distance between player and enemy is not 0 to avoid errors from division by 0
                move_x = ENEMY_SPEED * (dx / dist) # Calculate enemy movement in x direction
                move_y = ENEMY_SPEED * (dy / dist)
                self.move_enemy(i, move_x, move_y)

        # Check collision with enemies
        for enemy in self.enemies:
            if self.check_collision(enemy.x, enemy.y):
                self.collision_detected = True
                self.state = "end"

        self.update_buttons()

        # Timer countdown
        self.timer -= 1
        if self.timer <= 0 and not self.collision_detected:
            self.state = "end"

    def move_player(self, dx, dy):
        new_x = self.player.x + dx # Calculate new x-coordinate for player
        new_y = self.player.y + dy

        # Check if "left" button is pressed to allow wrapping around
        if self.buttons["left"].pressed:
            if new_x < 0:
                self.player.x = SCREEN_WIDTH - 11  # Wraps player around to just before right edge of screen
                self.buttons[
                    "left"].pressed = False  # Prevents player from taking the same path out the left side and back out the right without clicking on the button again
            elif not self.check_collision_with_obstacles(new_x, self.player.y):
                self.player.x = new_x  # Disables player from wrapping and/or moving outside of the left side of screen without clicking button

        # Check if "right" button is pressed to allow wrapping around
        elif self.buttons["right"].pressed:
            if new_x >= SCREEN_WIDTH:
                self.player.x = 0
                self.buttons["right"].pressed = False
            elif not self.check_collision_with_obstacles(new_x, self.player.y):
                self.player.x = new_x

        # Check if "top" button is pressed to allow wrapping around
        elif self.buttons["top"].pressed:
            if new_y < 0:
                self.player.y = SCREEN_HEIGHT - 1
                self.buttons["top"].pressed = False
            elif not self.check_collision_with_obstacles(self.player.x, new_y):
                self.player.y = new_y

        # Check if "bottom" button is pressed to allow wrapping around
        elif self.buttons["bottom"].pressed:
            if new_y >= SCREEN_HEIGHT:
                self.player.y = 0
                self.buttons["bottom"].pressed = False
            elif not self.check_collision_with_obstacles(self.player.x, new_y):
                self.player.y = new_y

        # If no directional button is pressed, restrict movement within screen boundaries
        else:
            proposed_x = max(0, min(SCREEN_WIDTH - 15, new_x))
            proposed_y = max(0, min(SCREEN_HEIGHT - 15, new_y))

            # Check collision with obstacles before moving
            if not self.check_collision_with_obstacles(proposed_x, self.player.y):
                self.player.x = proposed_x
            if not self.check_collision_with_obstacles(self.player.x, proposed_y):
                self.player.y = proposed_y

    def move_enemy(self, index, dx, dy):
        enemy = self.enemies[index]
        new_x = enemy.x + dx
        new_y = enemy.y + dy
        # Allows enemy to also wrap around screen
        self.enemies[index].x = new_x % SCREEN_WIDTH
        self.enemies[index].y = new_y % SCREEN_HEIGHT

    def check_collision(self, enemy_x, enemy_y):
        # Collision when distance between player and enemy is less than 10 pixels in both x and y directions
        return abs(self.player.x - enemy_x) < 10 and abs(self.player.y - enemy_y) < 10

    def update_buttons(self):
        for side in self.buttons:
            button = self.buttons[side]
            if side in ["left", "right"]:
                # Move up or down based on direction
                button.y += BUTTON_SPEED * button.direction
                # Change direction if button reaches the edge of the screen
                if button.y <= 0 or button.y >= SCREEN_HEIGHT - 8:
                    button.direction *= -1
            elif side in ["top", "bottom"]:
                # Move left or right based on direction
                button.x += BUTTON_SPEED * button.direction
                # Change direction if button reaches the edge of the screen
                if button.x <= 0 or button.x >= SCREEN_WIDTH - 8:
                    button.direction *= -1

            # Check for mouse clicks
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if side == "left" and 0 <= pyxel.mouse_x < 8 and abs(pyxel.mouse_y - button.y) < 8:
                    button.pressed = True
                elif side == "right" and SCREEN_WIDTH - 8 <= pyxel.mouse_x < SCREEN_WIDTH and abs(
                        pyxel.mouse_y - button.y) < 8:
                    button.pressed = True
                elif side == "top" and 0 <= pyxel.mouse_y < 8 and abs(pyxel.mouse_x - button.x) < 8:
                    button.pressed = True
                elif side == "bottom" and SCREEN_HEIGHT - 8 <= pyxel.mouse_y < SCREEN_HEIGHT and abs(
                        pyxel.mouse_x - button.x) < 8:
                    button.pressed = True

    def draw(self):
        pyxel.cls(pyxel.COLOR_GREEN)  # Green background

        # Draw start screen
        if self.state == "start":
            pyxel.text(20, 20, "Run Rabbit Run", pyxel.COLOR_PINK)
            pyxel.text(25, 40, "Select Level", pyxel.COLOR_WHITE)
            pyxel.text(25, 50, "Press 1 to start from Level 1", pyxel.COLOR_WHITE)
            pyxel.text(25, 60, "Press 2 to start from Level 2", pyxel.COLOR_WHITE)
            pyxel.text(25, 70, "Press 3 to play Level 3", pyxel.COLOR_WHITE)
        elif self.state == "playing":
            if self.level == 3:
                self.draw_level_3()
            else:
                # Draw player
                pyxel.blt(self.player.x, self.player.y, 0, 16, 0, 15, 15, 2)  # Player starts at bottom right

                # Draw enemies (foxes)
                for enemy in self.enemies:
                    pyxel.blt(enemy.x, enemy.y, 0, 0, 0, 16, 16, 2)  # Player starts at top left

                # Draw obstacles
                for obstacle in self.obstacles:
                    pyxel.blt(obstacle.x, obstacle.y, 0, obstacle.design_x, obstacle.design_y, 15, 15, 2)

            # Draw buttons
            for side in self.buttons:
                button = self.buttons[side]
                color = pyxel.COLOR_RED if button.pressed else pyxel.COLOR_BLACK  # Button changes color when pressed
                if side in ["left", "right"]:
                    pyxel.rect(button.x, button.y, 8, 8, color)
                elif side in ["top", "bottom"]:
                    pyxel.rect(button.x, button.y, 8, 8, color)

            # Draw timer
            if self.timer <= 10 * 60:  # Change color to red when 10 seconds are left
                pyxel.text(5, 5, f"Time: {int(self.timer / 60)}", pyxel.COLOR_RED)
            else:
                pyxel.text(5, 5, f"Time: {int(self.timer / 60)}", pyxel.COLOR_WHITE)

        # Draw end screen
        elif self.state == "end":
            if self.collision_detected:
                pyxel.text(40, 50, "Game Over", pyxel.COLOR_PINK)
                pyxel.text(40, 60, "Press 0 to Restart", pyxel.COLOR_WHITE)
            else:
                pyxel.text(40, 50, f"Level {self.level} Complete!", 10)
                pyxel.text(40, 60, "Press 0 to Continue", pyxel.COLOR_WHITE)

    def draw_level_3(self):
        # Draw torchlight effect as a filled circle
        torchlight_radius = 40
        torchlight_center_x = self.player.x + 16 // 2  # Adjusts for center of player sprite
        torchlight_center_y = self.player.y + 15 // 2

        # Clear the screen with black color for the torchlight effect
        pyxel.cls(pyxel.COLOR_BLACK)

        # Draw filled circle for torchlight
        for r in range(torchlight_radius, 0, -1):
            pyxel.circ(torchlight_center_x, torchlight_center_y, r, pyxel.COLOR_YELLOW)

        for obstacle in self.obstacles:
            # Calculate distance from obstacle to player
            dx = obstacle.x - torchlight_center_x
            dy = obstacle.y - torchlight_center_y
            dist = math.sqrt(dx * dx + dy * dy)

            # Only draw obstacles within torchlight radius
            if dist <= torchlight_radius:
                pyxel.blt(obstacle.x, obstacle.y, 0, obstacle.design_x, obstacle.design_y, 15, 15, 2)

        for enemy in self.enemies:
            # Calculate distance from enemy to player
            dx = enemy.x - torchlight_center_x
            dy = enemy.y - torchlight_center_y
            dist = math.sqrt(dx * dx + dy * dy)

            # Only draw enemies within torchlight radius
            if dist <= torchlight_radius:
                pyxel.blt(enemy.x, enemy.y, 0, 0, 0, 16, 16, 2)

        # Draw player on top of enemies
        pyxel.blt(self.player.x, self.player.y, 0, 16, 0, 15, 15, 2)


# Start the game
Game()