import pygame
import ctypes
import ctypes.wintypes
import sys
import random

pygame.init()
randint = random.randint

# --- Paramètres de base ---
button = {0, 1, 2, 3, 4}
WIDTH, HEIGHT = 100 * len(button) + 10, 100
FPS = 60
TRANSPARENCY = 255
plant = [[randint(0, 1) for _ in range(5)] for _ in range(5)]
lockwindow = True

# Get screen resolution
user32 = ctypes.windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)

# Crée une fenêtre sans bordure
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Fenêtre flottante")

# --- Récupère le handle Windows ---
hwnd = pygame.display.get_wm_info()["window"]

# Active le mode "fenêtre transparente et superposable"
ctypes.windll.user32.SetWindowLongW(hwnd, -20, 0x80000)
ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, TRANSPARENCY, 0x2)

# --- Rend la fenêtre toujours au premier plan ---
HWND_TOPMOST = -1
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_SHOWWINDOW = 0x0040
ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)

# --- Variables pour déplacement ---
running = True
dragging = False
offset_x = 0
offset_y = 0

clock = pygame.time.Clock()

# Fonction pour récupérer la position globale de la souris
def get_cursor_pos():
    pt = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def draw():
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, WIDTH, HEIGHT), border_radius=10)
    for i in button:
        pygame.draw.rect(
            screen,
            (100, 200, 100) if plant[i][0] else (200, 100, 100),
            (i * 80 + 20, HEIGHT // 2 - 40, 60, 60)
        )

# --- Boucle principale ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
            # position de la fenêtre actuelle
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            cursor_x, cursor_y = get_cursor_pos()
            offset_x = rect.left - cursor_x
            offset_y = rect.top - cursor_y

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False

    if dragging:
        cursor_x, cursor_y = get_cursor_pos()
        if lockwindow:
            new_left = cursor_x + offset_x
            new_top = cursor_y + offset_y
            # Empêcher la fenêtre de sortir de l'écran
            new_left = max(0, min(new_left, SCREEN_WIDTH - WIDTH))
            new_top = max(0, min(new_top, SCREEN_HEIGHT - HEIGHT - 40))
            ctypes.windll.user32.MoveWindow(hwnd, int(new_left), int(new_top), WIDTH, HEIGHT, True)
        else:
            ctypes.windll.user32.MoveWindow(hwnd, int(cursor_x + offset_x), int(cursor_y + offset_y), WIDTH, HEIGHT, True)

    # --- Rendu ---
    draw()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
