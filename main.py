from html import entities
import pygame, sys, os, time, random


# Pygame initializations
pygame.init()
pygame.font.init()

# Window initializations
WIDTH, HEIGHT = 1200, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# Lanes' constants
LANES_AMOUNT = 5
LANE_HEIGHT = 60

# Colors' constants
BLACK = (0, 0, 0)
DARK_GRAY = (64, 64, 64)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
WHITE = (255, 255, 255)

# Fonts
FONT = pygame.font.Font(os.path.join('assets', 'font.otf'), 24)
FONT_MEDIUM = pygame.font.Font(os.path.join('assets', 'font.otf'), 18)
FONT_SMALL = pygame.font.Font(os.path.join('assets', 'font.otf'), 12)

# Display initializations
CLOCK = pygame.time.Clock()
FRAMERATE = 60

# Entity constants
ENTITY_WIDTH = 30


def get_upper_offset(index=0) -> float:
    return (HEIGHT - LANE_HEIGHT * LANES_AMOUNT) / 2 + LANE_HEIGHT * index


def get_lower_offset() -> float:
    return (HEIGHT + LANE_HEIGHT * LANES_AMOUNT) / 2


def render_center(font: pygame.font.Font, str: str, color: tuple[int, int, int], x: float, y: float) -> None:
    texture = font.render(str, True, color)
    WINDOW.blit(texture, (x - texture.get_width() / 2, y))


class Lane:

    lanes = []

    def __init__(self, index) -> None:
        self.index = index
        self.entities = []
        Lane.lanes.append(self)

    def render(self, dt) -> None:
        # Render lanes
        if (pygame.mouse.get_pos()[1] - get_upper_offset(self.index)) // LANE_HEIGHT == 0:
            pygame.draw.rect(WINDOW, LIGHT_GRAY, pygame.Rect(0, get_upper_offset(self.index), WIDTH, LANE_HEIGHT)) # Hovering effect
        pygame.draw.rect(WINDOW, BLACK, pygame.Rect(0, get_upper_offset(self.index), WIDTH, LANE_HEIGHT + 1), 1)

        # Render entities
        for entity in self.entities:
            entity.render(dt)

        if random.random() < dt:
            self.entities.append(ExampleEntity(self, WIDTH))

    def handle_click(self, event: pygame.event.Event) -> bool:
        if (event.pos[1] - get_upper_offset(self.index)) // 64 == 0:
            self.entities.append(ExampleEntity(self, -ENTITY_WIDTH))
            return True
        return False

    
class Entity:

    def __init__(self, lane: Lane, x: int, movement_speed: int, health: int, attack: int) -> None:
        self.lane = lane
        self.x = x
        self.dx = 1 if x == -ENTITY_WIDTH else -1
        self.movement_speed = movement_speed
        self.health = health
        self.max_health = health
        self.attack = attack

    def render(self, dt) -> None:
        # Updates
        if self.health <= 0:
            self.lane.entities.remove(self)
            return
        b = True
        for otherEntity in self.lane.entities:
            if otherEntity is self or otherEntity.dx == self.dx:
                continue
            if pygame.Rect(self.x, get_upper_offset(self.lane.index) + (LANE_HEIGHT - ENTITY_WIDTH) / 2, ENTITY_WIDTH, ENTITY_WIDTH).colliderect(pygame.Rect(otherEntity.x, get_upper_offset(self.lane.index) + (LANE_HEIGHT - ENTITY_WIDTH) / 2, ENTITY_WIDTH, ENTITY_WIDTH)):
                b = False
                otherEntity.health -= self.attack * dt
                break
        if b:
            self.x += self.dx * self.movement_speed * dt
        if self.x < -ENTITY_WIDTH or self.x > WIDTH:
            self.lane.entities.remove(self)

        # Render
        pygame.draw.rect(WINDOW, DARK_GRAY, pygame.Rect(self.x, get_upper_offset(self.lane.index) + (LANE_HEIGHT - ENTITY_WIDTH) / 2, ENTITY_WIDTH, ENTITY_WIDTH))
        pygame.draw.rect(WINDOW, BLACK, pygame.Rect(self.x, get_upper_offset(self.lane.index) + (LANE_HEIGHT - ENTITY_WIDTH) / 2, ENTITY_WIDTH, ENTITY_WIDTH), 1)
        pygame.draw.rect(WINDOW, DARK_GRAY, pygame.Rect(self.x, get_upper_offset(self.lane.index) + (LANE_HEIGHT - ENTITY_WIDTH) / 2 / 3, ENTITY_WIDTH, (LANE_HEIGHT - ENTITY_WIDTH) / 2 / 3), 1)
        pygame.draw.rect(WINDOW, BLACK, pygame.Rect(self.x, get_upper_offset(self.lane.index) + (LANE_HEIGHT - ENTITY_WIDTH) / 2 / 3, ENTITY_WIDTH * self.health / self.max_health, (LANE_HEIGHT - ENTITY_WIDTH) / 2 / 3))


class ExampleEntity(Entity):

    def __init__(self, lane: Lane, x: int) -> None:
        super().__init__(lane, x, 200, 100, 50)


# Create lanes
for i in range(LANES_AMOUNT):
    Lane(i)

# Variables
last_time = time.time()

# Game loop
while True:
    for event in pygame.event.get():

        # Quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        # When mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            for lane in Lane.lanes:
                if lane.handle_click(event):
                    break
    
    # Render background
    WINDOW.fill(WHITE)

    # Render title and subtitles
    render_center(FONT, 'Blocky', BLACK, WIDTH / 2, 48)
    render_center(FONT_MEDIUM, 'A block game', DARK_GRAY, WIDTH / 2, 48 + 24 + 12)

    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    # Render lanes
    for lane in Lane.lanes:
        lane.render(dt)
    
    # Update display
    pygame.display.update()
    CLOCK.tick(FRAMERATE)
