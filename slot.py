import pygame
import random

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer with default parameters
pygame.mixer.init()

# Screen dimensions
screen_width = 900
screen_height = 580

# Set up display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Slot Machine")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load images (replace with your own images)
symbols = [
    pygame.image.load('straw.jpg'),
    pygame.image.load('bell.jpg'),
    pygame.image.load('7.jpg')
]

# Load background image
background = pygame.image.load('machine.jpg')

# Load audio file (replace with your own audio file)
slot_sound = pygame.mixer.Sound('slot_sound.mp3')
jackpot = pygame.mixer.Sound('diffjack.mp3')
jackpot.set_volume(0.5)  # Set volume to 50%

# Slot machine properties
num_reels = 3
reel_width = 185
reel_height = 257
reel_positions = [131, 353, 577]
reel_y_offset = 230  # Moved up by 10 pixels

# Font for displaying messages
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Initialize money
player_money = 150  # Starting money
bet_amount = 10     # Amount bet per spin
win_amount = 50     # Amount won per win

# Time interval for updating reel images (in milliseconds)
reel_update_interval = 100

def draw_reels(reel_values):
    for i, value in enumerate(reel_values):
        reel_x = reel_positions[i]
        reel_y = 157
        # Draw white rectangle for the reel
        pygame.draw.rect(screen, WHITE, (reel_x, reel_y, reel_width, reel_height))
        # Draw the symbol inside the rectangle
        symbol = pygame.transform.scale(symbols[value], (reel_width, reel_height))
        screen.blit(symbol, (reel_x, reel_y))
        pygame.draw.rect(screen, GOLD, (reel_x, reel_y, reel_width, reel_height), 3)

def display_money(money):
    money_text = font.render(f"${money}", True, GREEN)
    screen.blit(money_text, (550, 445))

def main():
    global player_money
    running = True
    reel_values = [0, 1, 2]
    spinning = False
    spin_start_time = 0
    spin_duration = 2000  # milliseconds
    last_reel_update_time = 0

    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not spinning and player_money >= bet_amount:
                    spinning = True
                    spin_start_time = current_time
                    last_reel_update_time = current_time
                    player_money -= bet_amount  # Deduct bet amount
                    slot_sound.play()
                    print("Spinning started...")

        screen.fill(BLACK)
        screen.blit(background, (0, 0))  # Draw the background
        display_money(player_money)  # Display current money

        if spinning:
            if current_time - spin_start_time >= spin_duration:
                spinning = False
                slot_sound.stop()
                reel_values = [random.randint(0, len(symbols) - 1) for _ in range(num_reels)]
                print("Spinning stopped, final values:", reel_values)
                if reel_values[0] == reel_values[1] == reel_values[2]:
                    player_money += win_amount  # Add win amount
                    jackpot.play()  # Play jackpot sound only when winning
            elif current_time - last_reel_update_time >= reel_update_interval:
                last_reel_update_time = current_time
                reel_values = [random.randint(0, len(symbols) - 1) for _ in range(num_reels)]
                print("Spinning, current values:", reel_values)

        draw_reels(reel_values)

        if not spinning:
            if reel_values[0] == reel_values[1] == reel_values[2]:
                message = font.render("You Win!", True, RED)
            else:
                message = font.render("Try Again", True, RED)
            screen.blit(message, (155, 440))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

        # Check if player is out of money
        if player_money < bet_amount:
            game_over_text = font.render("Game Over", True, RED)
            screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
