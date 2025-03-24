import pygame
import math
import random

from cards import draw_card  # Assuming cards module is correctly set up

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((720, 900))  # Portrait mode
running = True

# Load and scale background image
bg = pygame.image.load("background.jpeg")
bg = pygame.transform.scale(bg, (720, 900))

# Load and scale crystal ball image
crystal_ball = pygame.image.load("crystal_ball.png")
crystal_ball = pygame.transform.scale(crystal_ball, (450, 450))  # Adjust for portrait

# Center the crystal ball in portrait mode
crystal_x = (screen.get_width() - crystal_ball.get_width()) // 2
crystal_y = (screen.get_height() - crystal_ball.get_height()) // 2

# Load font and render text
pygame.font.init()
font = pygame.font.SysFont("papyrus", 64)  # Mystical font
small_font = pygame.font.SysFont("papyrus", 32)  # Smaller font for card meanings
title_text = font.render("Hello Stranger", True, (255, 215, 0))  # Gold text
subtitle_text = font.render("Dare to have your fortune told?", True, (255, 215, 0))

# Position the text for portrait mode
text_x = (screen.get_width() - title_text.get_width()) // 2
text_y = 100  # Higher in portrait mode
subtitle_text_x = (screen.get_width() - subtitle_text.get_width()) // 2
subtitle_text_y = screen.get_height() - 150  # Near the bottom

# Mist settings
mist_particles = []
for _ in range(30):  # Create 30 mist particles
    mist_particles.append({
        "x": random.randint(crystal_x, crystal_x + crystal_ball.get_width()),
        "y": random.randint(crystal_y, crystal_y + crystal_ball.get_height()),
        "alpha": random.randint(50, 150),  # Random opacity
        "radius": random.randint(5, 40),  # Random size for the mist particles
        "speed": random.uniform(0.01, 0.1),  # Speed at which it moves
        "direction": random.uniform(0, 2 * math.pi)  # Random direction (angle in radians)
    })

def draw_mist():
    # Animate mist particles
    for mist in mist_particles:
        # Update direction slowly to create smooth drifting motion
        mist["direction"] += random.uniform(-0.01, 0.01)  # Small random change to direction

        # Calculate new position based on direction and speed
        mist["x"] += mist["speed"] * math.cos(mist["direction"])
        mist["y"] += mist["speed"] * math.sin(mist["direction"])

        # Create a semi-transparent mist (circle)
        mist_surface = pygame.Surface((mist["radius"] * 2, mist["radius"] * 2), pygame.SRCALPHA)
        pygame.draw.circle(mist_surface, (255, 255, 255, mist["alpha"]), (mist["radius"], mist["radius"]), mist["radius"])

        # Blit the mist surface onto the screen at the calculated position
        screen.blit(mist_surface, (mist["x"] - mist["radius"], mist["y"] - mist["radius"]))

        # Make sure mist stays within the bounds of the screen
        if mist["x"] < 0 or mist["x"] > screen.get_width():
            mist["direction"] = math.pi - mist["direction"]  # Bounce off the left/right edges
        if mist["y"] < 0 or mist["y"] > screen.get_height():
            mist["direction"] = -mist["direction"]  # Bounce off the top/bottom edges

def tell_fortune(card_image, card_title, meaning_text):
    screen.blit(bg, (0, 0))  # Draw the background
    card_x = (screen.get_width() - card_image.get_width()) // 2
    card_y = (screen.get_height() - card_image.get_height()) // 2
    screen.blit(card_image, (card_x, card_y))
    card_title_text = font.render(card_title, True, (255, 215, 0))
    card_meaning_text = small_font.render(meaning_text, True, (255, 215, 0))
    screen.blit(card_title_text, (text_x, text_y))
    screen.blit(card_meaning_text, (100, 700))

# Game logic
fortune_start_time = None  # To track when the fortune screen is shown
fortune_duration = 5000  # 5 seconds in milliseconds
fortune_card_image = None  # To store the card image
fortune_card_title = None  # To store the card title
meaning_text = None  # To store the card meaning

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background
    screen.blit(bg, (0, 0))

    # Draw title text at the top
    screen.blit(title_text, (text_x, text_y))

    # Draw crystal ball in the center
    screen.blit(crystal_ball, (crystal_x, crystal_y))

    # Draw mist around the crystal ball
    draw_mist()

    # Draw subtitle at the bottom
    screen.blit(subtitle_text, (subtitle_text_x, subtitle_text_y))

    # Check if the spacebar is pressed to show the fortune screen
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and fortune_start_time is None:
        fortune_start_time = pygame.time.get_ticks()  # Record the time when the fortune screen starts
        # Generate a random card and store it for later use
        fortune_card_image, fortune_card_title, meaning_text = draw_card()

    # If the fortune screen is active, display it for 10 seconds
    if fortune_start_time is not None:
        # Show fortune screen with the saved card
        tell_fortune(fortune_card_image, fortune_card_title, meaning_text)

        # Check if 10 seconds have passed
        current_time = pygame.time.get_ticks()
        if current_time - fortune_start_time > fortune_duration:
            fortune_start_time = None  # Reset and go back to the main screen

    # Update the display
    pygame.display.flip()

pygame.quit()