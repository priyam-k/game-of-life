import pygame

pygame.init()
resx = 1350
width = 135  # 135
height = 70  # 70
scale = resx // width
resy = scale * height
border = 1
assert width <= resx
screen = pygame.display.set_mode((resx, resy))
pygame.display.set_caption("Conway's Game of Life")

grid = [[0 for x in range(width)] for y in range(height)]

grid[40][60] = 1
grid[41][60] = 1
grid[42][60] = 1
grid[42][61] = 1
grid[41][62] = 1


def neighbors(x, y):
    n = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            if grid[y + i][x + j] == 1:
                n += 1
    return n


def update():
    new_grid = [[0 for x in range(width)] for y in range(height)]
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            n = neighbors(x, y)
            if grid[y][x] == 1:
                if n < 2 or n > 3:  # n<2 n>3
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = 1
            elif grid[y][x] == 0:
                if n == 3:  # n=3
                    new_grid[y][x] = 1
                else:
                    new_grid[y][x] = 0
    return new_grid


def draw():
    for x in range(width):
        for y in range(height):
            if grid[y][x] == 1:
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (x * (scale + border), y * (scale + border), scale, scale),
                )
            elif grid[y][x] == 0:
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (x * (scale + border), y * (scale + border), scale, scale),
                )
            elif grid[y][x] == 2:
                pygame.draw.rect(
                    screen,
                    (0, 250, 0),
                    (x * (scale + border), y * (scale + border), scale, scale),
                )


def main():
    global grid
    clock = pygame.time.Clock()
    running = True
    paused = True
    fps = 10
    font = pygame.font.SysFont("Arial", 16)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                grid[y // (scale + border)][x // (scale + border)] = (
                    0 if pygame.key.get_pressed()[pygame.K_LALT] else 1
                )
            if pygame.mouse.get_pressed()[2]:
                x, y = pygame.mouse.get_pos()
                grid[y // (scale + border)][x // (scale + border)] = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
            if pygame.key.get_pressed()[pygame.K_PERIOD]:
                grid = update()
            if pygame.key.get_pressed()[pygame.K_EQUALS]:
                fps += 1
            if pygame.key.get_pressed()[pygame.K_MINUS]:
                fps = max(1, fps - 1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    grid = [[0 for x in range(width)] for y in range(height)]
                    paused = True
                if event.key in [
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                    pygame.K_4,
                    pygame.K_5,
                    pygame.K_6,
                    pygame.K_7,
                    pygame.K_8,
                    pygame.K_9,
                ]:
                    fps = (event.key - pygame.K_0) * 10
                if event.key == pygame.K_s:
                    with open("grid.txt", "w") as f:
                        for row in grid:
                            f.write(" ".join(map(str, row)) + "\n")
                if event.key == pygame.K_l:
                    with open("grid.txt", "r") as f:
                        grid = [[int(cell) for cell in line.split()] for line in f]

        if not paused:
            clock.tick(fps)
            grid = update()
        draw()
        # pygame.draw.rect(screen, (0, 0, 0), (0, 0, 100, 30), 10)
        screen.blit(font.render("FPS: " + str(fps), True, (255, 255, 255)), (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    main()
