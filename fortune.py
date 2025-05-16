import pygame
import random
import os
from utils import wrap_text
from cards import cards

card_images_folder = "card_images"

def draw_card():
    card = random.choice(cards)
    card_image_path = os.path.join(card_images_folder, card["image"])
    card_image = pygame.image.load(card_image_path)
    card_title = card["name"]
    meaning_text = card["meaning"]
    fortune = card["fortune"]
    card_image = pygame.transform.scale(card_image, (450, 450))  # Adjust for portrait
    return card_image, card_title, meaning_text, fortune

def tell_fortune(card_image, card_title, meaning_text, fortune, screen, small_font, font, bg, dark_overlay):
    screen.blit(bg, (0, 0))  # Draw the background
    screen.blit(dark_overlay, (0, 0))
    card_x = (screen.get_width() - card_image.get_width()) // 2
    card_y = (screen.get_height() - card_image.get_height()) // 2
    screen.blit(card_image, (card_x, card_y))
    
    # Center the card title horizontally
    card_title_text = font.render(card_title, True, (255, 215, 0))
    title_x = (screen.get_width() - card_title_text.get_width()) // 2
    title_y = card_y - card_title_text.get_height() - 100  # Adjust as needed
    screen.blit(card_title_text, (title_x, title_y))
    
    # Center the card meaning text horizontally
    wrapped_card_meaning = wrap_text(meaning_text, small_font, screen.get_width() - 20)
    meaning_y = card_y - card_title_text.get_height() - 50 # Adjust as needed
    for line in wrapped_card_meaning:
        meaning_text_line = small_font.render(line, True, (255, 215, 0))
        meaning_x = (screen.get_width() - meaning_text_line.get_width()) // 2
        meaning_y += small_font.get_height()
        screen.blit(meaning_text_line, (meaning_x, meaning_y))
    
    # Wrap the fortune text
    wrapped_fortune = wrap_text(fortune, small_font, screen.get_width() - 40)  # 40 is a padding from left and right
    fortune_y = meaning_y + card_image.get_height() + 50  # Adjust as needed

    for line in wrapped_fortune:
        fortune_text = small_font.render(line, True, (255, 215, 0))
        fortune_x = (screen.get_width() - fortune_text.get_width()) // 2
        fortune_y += small_font.get_height() # Adjust line spacing
        screen.blit(fortune_text, (fortune_x, fortune_y))