import pygame
import RPi.GPIO as GPIO

from utils import create_particles, draw_mist
from fortune import tell_fortune, draw_card

# Setup for GPIO button
BUTTON_GPIO = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize pygame
pygame.init()
screen_width = 2160
screen_height = 3840
screen = pygame.display.set_mode((screen_width, screen_height))  # Portrait mode
running = True

# Load and scale background image
bg = pygame.image.load("background.jpeg")
bg = pygame.transform.scale(bg, (2160, 3840))

# Create a semi-transparent black surface
dark_overlay = pygame.Surface((screen_width, screen_height))
dark_overlay.set_alpha(100)  # 0 (fully transparent) to 255 (fully opaque)
dark_overlay.fill((0, 0, 0))  # Black

# Load and scale crystal ball image
crystal_ball = pygame.image.load("crystal_ball.png")
crystal_ball = pygame.transform.scale(crystal_ball, (1500, 1500))  # Adjust for portrait

# Center the crystal ball in portrait mode
crystal_x = (screen.get_width() - crystal_ball.get_width()) // 2
crystal_y = (screen.get_height() - crystal_ball.get_height()) // 2

# Load font and render text
pygame.font.init()
font = pygame.font.SysFont("papyrus", 256)  # Mystical font
small_font = pygame.font.SysFont("papyrus", 128)  # Smaller font for card meanings
title_text = font.render("Hello Stranger", True, (255, 215, 0))  # Gold text
subtitle_text_line_1 = font.render("Do you dare to", True, (255, 215, 0))
subtitle_text_line_2 = font.render("have your fortune told?", True, (255, 215, 0))

# Position the text for portrait mode
text_x = (screen.get_width() - title_text.get_width()) // 2
text_y = 100  # Higher in portrait mode
subtitle_text_line_1_x = (screen.get_width() - subtitle_text_line_1.get_width()) // 2
subtitle_text_line_2_x = (screen.get_width() - subtitle_text_line_2.get_width()) // 2
subtitle_text_y = screen.get_height() - 500  # Near the bottom

mist_particles = create_particles(crystal_ball, crystal_x, crystal_y)

# Game logic
fortune_start_time = None  # To track when the fortune screen is shown
fortune_duration = 30000  # 30 seconds in milliseconds
fortune_card_image = None  # To store the card image
fortune_card_title = None  # To store the card title
meaning_text = None  # To store the card meaning
fortune = None  # To store the fortune text

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background
    screen.blit(bg, (0, 0))
    screen.blit(dark_overlay, (0, 0))

    # Draw title text at the top
    screen.blit(title_text, (text_x, text_y))

    # Draw crystal ball in the center
    screen.blit(crystal_ball, (crystal_x, crystal_y))

    # Draw mist around the crystal ball
    draw_mist(mist_particles, screen, pygame)

    # Draw subtitle at the bottom
    screen.blit(subtitle_text_line_1, (subtitle_text_line_1_x, subtitle_text_y))
    screen.blit(subtitle_text_line_2, (subtitle_text_line_2_x, subtitle_text_y + 150))

    # Check if the button is pressed to show the fortune screen
    if GPIO.input(BUTTON_GPIO) == GPIO.LOW and fortune_start_time is None:
        print('button pressed')
        fortune_start_time = pygame.time.get_ticks()
        print('telling fortune')
        fortune_start_time = pygame.time.get_ticks()  # Record the time when the fortune screen starts
        # Generate a random card and store it for later use
        fortune_card_image, fortune_card_title, meaning_text, fortune = draw_card()

    # If the fortune screen is active, display it for 10 seconds
    if fortune_start_time is not None:
        # Show fortune screen with the saved card
        tell_fortune(fortune_card_image, fortune_card_title, meaning_text, fortune, screen, small_font, font, bg, dark_overlay)

        # Check if 10 seconds have passed
        current_time = pygame.time.get_ticks()
        if current_time - fortune_start_time > fortune_duration:
            print('done telling fortune and restarting')
            fortune_start_time = None  # Reset and go back to the main screen

    # Update the display
    pygame.display.flip()

GPIO.cleanup()
pygame.quit()