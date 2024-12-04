import math
from random import randint
from dataclasses import dataclass
import matplotlib.pyplot as plt

# Visuals initialization
# ----

import pygame
pygame.font.init()

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Three Body Problem")

# ----

N_BODIES = 3
ERROR_MARGIN = 1e-8
RADIUS = 25
G = 6.6743 * 10 ** -11

X = []
Y = []


def get_random_color() -> tuple[int, int, int]:
    return tuple([randint(0, 255) for _ in range(3)])


@dataclass
class Pair:
    x: float
    y: float

    def mag(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def tuple(self) -> tuple:
        return (self.x, self.y)

    def normalize(self) -> "Pair":
        div = self.mag()
        return Pair(self.x / max(div, ERROR_MARGIN), self.y / max(div, ERROR_MARGIN))

    def __iadd__(self, other: "Pair") -> "Pair":
        self.x += other.x
        self.y += other.y
        return self


class Body:
    bodies = 0

    def __init__(self, position: Pair, mass: int = 10 ** 11):
        self.body_num = Body.bodies
        self.position = position
        self.velocity = Pair(0, 0)
        self.mass = mass
        self.color = get_random_color()
        Body.bodies += 1

    def render(self):
        pygame.draw.circle(WINDOW, self.color,
                           (self.position.x, self.position.y), RADIUS)

    @staticmethod
    def mass(bodies: list["Body"]) -> int:
        return sum(body.mass for body in bodies)

    @staticmethod
    def com(bodies: list["Body"]) -> Pair:
        co = Pair(0, 0)
        for body in bodies:
            co.x += body.mass * body.position.x
            co.y += body.mass * body.position.y
        mass = Body.mass(bodies)
        co.x /= mass
        co.y /= mass
        return co


def update(bodies: list[Body]):
    dv = []

    for i, curr in enumerate(bodies):
        total_force_x = 0
        total_force_y = 0

        for body in bodies:
            if body != curr:
                dx = body.position.x - curr.position.x
                dy = body.position.y - curr.position.y

                distance_squared = dx**2 + dy**2
                distance_squared = max(RADIUS * RADIUS, distance_squared)
                distance = math.sqrt(distance_squared)

                force_magnitude = G * curr.mass * body.mass / distance_squared

                force_x = force_magnitude * (dx / distance)
                force_y = force_magnitude * (dy / distance)

                total_force_x += force_x
                total_force_y += force_y

        dv.append(Pair(
            total_force_x / curr.mass,
            total_force_y / curr.mass
        ))

    for i, body in enumerate(bodies):
        body.velocity += dv[i]
        body.position.x += body.velocity.x 
        body.position.y += body.velocity.y 


def render(bodies: list[Body]):
    WINDOW.fill((0, 0, 0))
    for body in bodies:
        body.render()
    pygame.draw.circle(WINDOW, (255, 255, 255),
                       Body.com(bodies).tuple(), RADIUS / 2)
    pygame.display.update()


def equilateral_triangle_centered(cx, cy, side_length=100):
    height = side_length * math.sqrt(3) / 2
    x0 = cx - side_length / 2
    y0 = cy + height / 3
    x1 = cx + side_length / 2
    y1 = cy + height / 3
    x2 = cx
    y2 = cy - 2 * height / 3
    return [(x0, y0), (x1, y1), (x2, y2)]


def main():
    x_pos = [randint(1, 6) * 100 for _ in range(N_BODIES)]
    y_pos = [randint(1, 6) * 100 for _ in range(N_BODIES)]

    positions = list(zip(x_pos, y_pos))

    # positions = equilateral_triangle_centered(
    #     WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 200)

    bodies = [Body(Pair(*positions[i])) for i in range(N_BODIES)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update(bodies)
        render(bodies)


if __name__ == "__main__":
    main()
