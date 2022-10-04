import pygame, sys, time

# Window properties' constant
WIDTH = 1200
HEIGHT = 800
FRAMERATE = 60
LANE_HEIGHT = 60
LANES_NUMBERS = 5
LANE_OUTLINE_OFFSET = 0.1
UPPER_OFFSET = (HEIGHT - LANE_HEIGHT * LANES_NUMBERS) / 2
LOWER_OFFSET = (HEIGHT + LANE_HEIGHT * LANES_NUMBERS) / 2

# Entity's property
ENTITY_WIDTH = 30

# Initializing window
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors' constant
WHITE = (255, 255, 255)
LIGHT_GRAY = (192, 192, 192)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
BLACK = (0, 0, 0)

# Fonts' constant
FONT_PATH = 'assets/font.otf'
FONT = pygame.font.Font(FONT_PATH, 24)
FONT_MEDIUM = pygame.font.Font(FONT_PATH, 18)
FONT_SMALL = pygame.font.Font(FONT_PATH, 12)


class Lane:
    
    lanes = []

    def __init__(self, lane):
        self.lane = lane
        Lane.lanes.append(self)

    def render_all():
        # Render the lanes
        for lane in Lane.lanes:
            lane.render()

        # Render the additional two lines to separate the visuals from the lanes
        y = UPPER_OFFSET - LANE_HEIGHT * LANE_OUTLINE_OFFSET
        pygame.draw.line(WINDOW, WHITE, (0, y), (WIDTH, y))
        y = LOWER_OFFSET + LANE_HEIGHT * LANE_OUTLINE_OFFSET
        pygame.draw.line(WINDOW, WHITE, (0, y), (WIDTH, y))

    def render(self):
        # Render the hovering effect if hovered
        if (pygame.mouse.get_pos()[1] - UPPER_OFFSET) // LANE_HEIGHT == self.lane:
            pygame.draw.rect(WINDOW, DARK_GRAY, pygame.Rect(0, UPPER_OFFSET + self.lane * LANE_HEIGHT, WIDTH, LANE_HEIGHT))
        
        # Render the upper offset
        y = UPPER_OFFSET + self.lane * LANE_HEIGHT
        pygame.draw.line(WINDOW, WHITE, (0, y), (WIDTH, y))
        pygame.draw.line(WINDOW, WHITE, (0, y + LANE_HEIGHT), (WIDTH, y + LANE_HEIGHT))


class Entity:

    entities = []

    def __init__(self, lane):
        self.health = 100
        self.max_health = 100
        self.lane = lane
        self.x = 0
        Entity.entities.append(self)

    def render_all():
        for entity in Entity.entities:
            entity.render()

    def tick_all(dt):
        for entity in Entity.entities:
            entity.tick(dt)
        
    def render(self):
        pygame.draw.rect(WINDOW, WHITE, pygame.Rect(self.x - ENTITY_WIDTH, UPPER_OFFSET + LANE_HEIGHT * self.lane + (LANE_HEIGHT - ENTITY_WIDTH) / 2, ENTITY_WIDTH, ENTITY_WIDTH))
        self.render_health_bar()

    def tick(self, dt):
        self.x += dt * 100
        self.health -= dt * 10 # purpose: test the render of the health bar

    def render_health_bar(self):
        y = UPPER_OFFSET + LANE_HEIGHT * self.lane + (LANE_HEIGHT - ENTITY_WIDTH) / 2
        y = (UPPER_OFFSET + LANE_HEIGHT * self.lane + y) / 2
        pygame.draw.line(WINDOW, WHITE, (self.x - ENTITY_WIDTH, y), (self.x - ENTITY_WIDTH + ENTITY_WIDTH * self.health / self.max_health, y))
        pass


def get_lane(y):
    return (y - UPPER_OFFSET) // LANE_HEIGHT


def main():
    # Setting window's properties
    pygame.display.set_caption('Blocky')
    pygame.display.set_icon(pygame.image.load('assets/icon.png'))

    # Variables for refreshing display
    clock = pygame.time.Clock()
    last_time = time.time()
    
    # Creating lanes
    for i in range(LANES_NUMBERS):
        Lane(i)

    # The game loop
    while True:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Entity(get_lane(event.pos[1]))

        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        
        # Background
        WINDOW.fill(BLACK)

        # Title
        text = FONT.render('Blocky', True, WHITE)
        WINDOW.blit(text, ((1200 - text.get_width()) / 2, 48))

        # Subtitle
        text = FONT_MEDIUM.render('An experimental game made by Dean', True, GRAY)
        WINDOW.blit(text, ((1200 - text.get_width()) / 2, 48 + 24 + 16))

        # Rendering lanes' line
        Lane.render_all()

        # Tick and render entities
        Entity.tick_all(dt)
        Entity.render_all()

        # Refresh display
        pygame.display.update()
        clock.tick(FRAMERATE)


main()
