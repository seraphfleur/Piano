import pygame


class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, is_int=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.click_area = pygame.Rect(x - 10, y - 15, width + 20, height + 30)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.is_int = is_int
        self.dragging = False
        self.handle_radius = 10
        self.update_handle_pos()

    def update_handle_pos(self):
        ratio = 0 if self.max_val == self.min_val else (self.val - self.min_val) / (self.max_val - self.min_val)
        self.handle_x = int(self.rect.x + ratio * self.rect.width)
        self.handle_y = self.rect.centery

    def handle_event(self, e):
        changed = False
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.click_area.collidepoint(e.pos):
                self.dragging = True
                changed = self._update_val_from_mouse(e.pos[0])
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            self.dragging = False
        elif e.type == pygame.MOUSEMOTION and self.dragging:
            changed = self._update_val_from_mouse(e.pos[0])

        return changed

    def _update_val_from_mouse(self, mouse_x):
        rel_x = max(self.rect.x, min(mouse_x, self.rect.right))
        ratio = (rel_x - self.rect.x) / self.rect.width
        raw_val = self.min_val + ratio * (self.max_val - self.min_val)

        old_val = self.val
        self.val = int(round(raw_val)) if self.is_int else round(raw_val, 2)
        self.update_handle_pos()
        return self.val != old_val

    def draw(self, screen):
        cy = self.rect.centery
        pygame.draw.line(screen, (200, 200, 205), (self.rect.x, cy), (self.rect.right, cy), 4)
        pygame.draw.line(screen, (70, 70, 75), (self.rect.x, cy), (self.handle_x, cy), 4)
        pygame.draw.circle(screen, (255, 255, 255), (self.handle_x, cy), self.handle_radius)
        pygame.draw.circle(screen, (80, 80, 85), (self.handle_x, cy), self.handle_radius, 2)
