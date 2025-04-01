import random
import math

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        # Try adding the word to the current line
        test_line = current_line + ('' if current_line == "" else ' ') + word
        test_width = font.size(test_line)[0]
        # If the line is too wide, start a new line
        if test_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)  # Add the last line
    return lines

def create_particles(crystal_ball, crystal_x, crystal_y):
    mist_particles = []
    for _ in range(30):  # Create 30 mist particles
        mist_particles.append({
            "x": random.randint(crystal_x - 200, crystal_x + crystal_ball.get_width() + 400),
            "y": random.randint(crystal_y - 200, crystal_y + crystal_ball.get_height() + 400),
            "alpha": random.randint(50, 120),  # Optional: more ethereal
            "radius": random.randint(30, 120),  # Medium-large size
            "speed": random.uniform(0.5, 2.0),  # 💨 Faster mist
            "direction": random.uniform(0, 2 * math.pi)  # Drift direction
        })
    return mist_particles

def draw_mist(mist_particles, screen, pygame):
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