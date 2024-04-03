from tests.networkx_graph import generate_graph
import pygame
import sys
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.init()
font = pygame.font.Font(None, 36)

WHITE = (255, 255, 255)
BLUE = (148, 135, 199)
BLACK = (0, 0, 0)

class InputBox:
    def __init__(self, x, y, w, h, font, text='') -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = BLUE if self.active else BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, self.color)

    def update(self) -> None:
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen) -> None:
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def create_initial_window() -> dict[str, int]:
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    font = pygame.font.Font(None, 36)
    button_color = (148, 135, 199)
    button_position = (325, 350)
    button_size = (150, 60)
    button_text = 'Generate'
    text_surf = font.render(button_text, True, WHITE)
    text_rect = text_surf.get_rect()

    input_box = InputBox(300, 250, 140, 32, font)
    input_text = ''

    slider_width = 300
    slider_height = 200
    slider_x = (screen_width - slider_width) // 2
    slider = Slider(screen, slider_x, slider_height, slider_width, 10, min=1, max=20, step=2)
    output = TextBox(screen, 560, 195, 25, 25, fontSize=25)
    output.disable()

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check if mouse click is within the button area
                if button_position[0] <= mouse_pos[0] <= button_position[0] + button_size[0] and button_position[1] <= mouse_pos[1] <= button_position[1] + button_size[1]:
                    input_text = input_box.text  # Capture input text
                    running = False  # Exit loop to close the window
            input_box.handle_event(event)

        input_box.update()

        output = font.render(str(slider.getValue()), True, (10, 0, 0))

        screen.fill(WHITE)
        input_box.draw(screen)
        pygame.draw.rect(screen, button_color, (*button_position, *button_size))
        center_x = button_position[0] + (button_size[0] - text_rect.width) // 2
        center_y = button_position[1] + (button_size[1] - text_rect.height) // 2
        screen.blit(text_surf, (center_x, center_y))

        screen.blit(output, (slider_x + (slider_width // 2) - (output.get_width() // 2) + slider_width/2 + 25, slider_height - 7))
        pygame_widgets.update(events)
        pygame.display.flip()

    pygame.quit()
    slider_value = slider.getValue()
    return {"txt": input_text, "value": slider_value}


# init
dt = create_initial_window()    # dt is a dict
generate_graph(dt)
