import pygame
import numpy as np
import sys
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_SPACE, K_RIGHT, K_LEFT

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1600, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Solar System Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREY = (105, 105, 105)
RED = (255, 0, 0)

# Load planet images
planet_images = {
    "Sun": pygame.image.load("sun.jpg"),
    "Mercury": pygame.image.load("mercury.jpeg"),
    "Venus": pygame.image.load("venus.jpeg"),
    "Earth": pygame.image.load("earth.jpg"),
    "Mars": pygame.image.load("mars.jpeg"),
    "Jupiter": pygame.image.load("jupiter.jpeg"),
    "Saturn": pygame.image.load("saturn.jpeg"),
    "Uranus": pygame.image.load("uranus.jpeg"),
    "Neptune": pygame.image.load("neptune.jpeg"),
}

# Rocket image (larger size)
rocket_image_orig = pygame.image.load("ROCKET.jpg")
rocket_size = 50  # Adjusted size for rocket
rocket_image = pygame.transform.scale(rocket_image_orig, (rocket_size, rocket_size))
rocket_pos = [width // 2, height + rocket_size]  # Initial position of the rocket (middle of screen, below)
rocket_speed = 5
rocket_direction = np.array([0, -1])  # Initial direction vector (moving up)
rotate_rocket = False  # Flag to control rocket movement

# Planet data
planets = [
    {"name": "Sun", "radius": 50, "distance": 0, "speed": 0},
    {"name": "Mercury", "radius": 5, "distance": 80, "speed": 4.8},
    {"name": "Venus", "radius": 10, "distance": 120, "speed": 3.5},
    {"name": "Earth", "radius": 12, "distance": 160, "speed": 3.0},
    {"name": "Mars", "radius": 7, "distance": 200, "speed": 2.4},
    {"name": "Jupiter", "radius": 20, "distance": 240, "speed": 1.3},
    {"name": "Saturn", "radius": 17, "distance": 280, "speed": 1.0},
    {"name": "Uranus", "radius": 15, "distance": 320, "speed": 0.7},
    {"name": "Neptune", "radius": 15, "distance": 360, "speed": 0.6},
]

# Initial angles for the planets
angles = np.zeros(len(planets))

# Fonts
font = pygame.font.SysFont(None, 24)

# Toggle rotation flag
rotate_planets = True

def draw_planet(screen, image, x, y, radius):
    image = pygame.transform.scale(image, (2*radius, 2*radius))
    rect = image.get_rect(center=(int(x), int(y)))
    screen.blit(image, rect.topleft)

def draw_orbit(screen, x, y, radius):
    pygame.draw.circle(screen, DARK_GREY, (int(x), int(y)), radius, 1)

def draw_label(screen, text, x, y):
    label = font.render(text, True, WHITE)
    screen.blit(label, (x, y))

def draw_rocket(screen, x, y):
    screen.blit(rocket_image, (x, y))

def main():
    global rocket_pos, rocket_direction, rotate_rocket, rotate_planets

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if not rotate_rocket:
                        # Launch the rocket from Earth's position
                        earth_index = next((i for i, planet in enumerate(planets) if planet["name"] == "Earth"), None)
                        if earth_index is not None:
                            angle = angles[earth_index]
                            distance = planets[earth_index]["distance"]
                            x = width // 2 + distance * np.cos(angle)
                            y = height // 2 + distance * np.sin(angle)
                            rocket_pos = [x, y]
                            rotate_rocket = True
                    else:
                        rotate_rocket = not rotate_rocket  # Toggle rocket movement on space bar press

                # Adjust rocket movement based on arrow keys
                elif event.key == K_RIGHT:
                    rocket_direction = np.array([1, 0])  # Move right
                elif event.key == K_LEFT:
                    rocket_direction = np.array([-1, 0])  # Move left

            elif event.type == pygame.KEYUP:
                if event.key == K_RIGHT or event.key == K_LEFT:
                    rocket_direction = np.array([0, -1])  # Resume vertical movement

        screen.fill(BLACK)

        # Draw orbits
        for planet in planets:
            if planet["distance"] > 0:
                draw_orbit(screen, width // 2, height // 2, planet["distance"])

        # Draw planets and labels
        for i, planet in enumerate(planets):
            angle = angles[i]
            distance = planet["distance"]
            x = width // 2 + distance * np.cos(angle)
            y = height // 2 + distance * np.sin(angle)
            draw_planet(screen, planet_images[planet["name"]], x, y, planet["radius"])
            draw_label(screen, planet["name"], x + planet["radius"] + 5, y - planet["radius"])

            # Update the angle for the next frame if rotation is enabled
            if rotate_planets:
                angles[i] += planet["speed"] * 0.01

        # Update and draw rocket if launched and moving
        if rotate_rocket:
            rocket_pos[0] += rocket_speed * rocket_direction[0]
            rocket_pos[1] += rocket_speed * rocket_direction[1]
            if rocket_pos[0] > width + rocket_size // 2:
                rocket_pos[0] = -rocket_size // 2  # Wrap around when rocket goes off-screen
            elif rocket_pos[0] < -rocket_size // 2:
                rocket_pos[0] = width + rocket_size // 2
            if rocket_pos[1] < -rocket_size // 2:
                rocket_pos[1] = height + rocket_size // 2

        draw_rocket(screen, rocket_pos[0], rocket_pos[1])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
