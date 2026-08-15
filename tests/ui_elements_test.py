import pygame
import pygame_gui

# Initialize Pygame
pygame.init()

# Set up the Pygame display
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Pygame GUI')

# Create a manager for UI elements
ui_manager = pygame_gui.UIManager(window_size)

# Function to handle events
def handle_events(event):
    if event.type == pygame.QUIT:
        return True
    if event.type == pygame.USEREVENT:
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            # Perform action when a button is pressed
            if event.ui_element == button:
                print("Button clicked!")
        elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            # Update parameter values when a slider is moved
            if event.ui_element == slider1:
                value = event.ui_element.get_current_value()
                print(f"Slider1 moved to {value}")

    # Let pygame_gui handle its own events
    ui_manager.process_events(event)
    return False

# Create UI elements
button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (100, 50)),
                                      text='Click Me!',
                                      manager=ui_manager)

slider1 = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((50, 150), (200, 20)),
                                                 start_value=50,
                                                 value_range=(0.0, 1.0),
                                                 manager=ui_manager)
slider2 = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((50, 200), (200, 20)),
                                                 start_value=50,
                                                 value_range=(0.0, 1.0),
                                                 manager=ui_manager)
slider2 = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((50, 250), (200, 20)),
                                                 start_value=50,
                                                 value_range=(0.0, 1.0),
                                                 manager=ui_manager)


import pygame
import pygame_gui

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Pygame GUI')

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))

    # Handle events
    for event in pygame.event.get():
        if handle_events(event):
            running = False

    # Update the UI
    ui_manager.update(1/60)
    ui_manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()

