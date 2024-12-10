import pygame
import sys
import math

# Configurações iniciais
WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 30, 30)
POINT_COLOR = (255, 0, 0)
LINE_COLOR = (200, 200, 200)
CURVE_COLOR = (0, 255, 0)
POINT_RADIUS = 6

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Editor de Curvas de Bézier")
clock = pygame.time.Clock()

# Lista de pontos de controle
control_points = []
dragging_point = None

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def de_casteljau(points, t):
    """Calcula um ponto na curva de Bézier usando o algoritmo de De Casteljau."""
    while len(points) > 1:
        points = [
            (
                (1 - t) * points[i][0] + t * points[i + 1][0],
                (1 - t) * points[i][1] + t * points[i + 1][1],
            )
            for i in range(len(points) - 1)
        ]
    return points[0]

def draw_curve(points):
    """Desenha a curva de Bézier usando o algoritmo de De Casteljau."""
    if len(points) < 2:
        return

    num_segments = 100
    curve_points = [de_casteljau(points, t / num_segments) for t in range(num_segments + 1)]

    for i in range(len(curve_points) - 1):
        pygame.draw.line(screen, CURVE_COLOR, curve_points[i], curve_points[i + 1], 2)

def draw():
    screen.fill(BG_COLOR)

    # Desenhar o polígono de controle
    if len(control_points) > 1:
        pygame.draw.lines(screen, LINE_COLOR, False, control_points, 1)

    # Desenhar pontos de controle
    for point in control_points:
        pygame.draw.circle(screen, POINT_COLOR, point, POINT_RADIUS)

    # Desenhar a curva
    draw_curve(control_points)

    pygame.display.flip()

def handle_events():
    global dragging_point

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo
                pos = event.pos

                # Verificar se um ponto de controle foi clicado
                for i, point in enumerate(control_points):
                    if distance(pos, point) <= POINT_RADIUS:
                        dragging_point = i
                        break
                else:
                    # Adicionar novo ponto de controle
                    control_points.append(pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Soltar clique esquerdo
                dragging_point = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Limpar todos os pontos
                control_points.clear()

    # Arrastar ponto de controle
    if dragging_point is not None:
        control_points[dragging_point] = pygame.mouse.get_pos()

# Loop principal
while True:
    handle_events()
    draw()
    clock.tick(60)
