import pygame
import time

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("EYE-AIM")

# Define colors
bg_color = (0, 0, 0)

# Set up fonts using SysFont
font_size = 30
big_font = pygame.font.SysFont('AppleGothic', 100)  # Use 'AppleGothic' for macOS
font = pygame.font.SysFont('AppleGothic', font_size)  # Smaller font size
kofont = pygame.font.SysFont('AppleGothic', 60)  # Korean font size

# Set up clock
fps = 60
clock = pygame.time.Clock()

# Load sound effects
circle_click = pygame.mixer.Sound('sound/circle_click.wav')

# Load circle images
circle = pygame.Surface((100, 100))
pygame.draw.circle(circle, (255, 0, 0), (50, 50), 50)
circle.set_colorkey((0, 0, 0))

circle_pos = [(100, 100), (width - 200, height - 200), (width / 2, height / 2)]

def main():
    global score
    global recorded
    global total_time
    recorded = 0

    clicks, misses = 0, 0
    finished = False

    text_first_click_info = font.render("원을 바라보면 시작", True, (255, 255, 255))
    calib_text = kofont.render("보정", True, (255, 255, 255))
    start = 0

    first_click = True
    Circle_Appear(0)
    Circle_Appear(1)
    Circle_Appear(2)
    start_ticks = pygame.time.get_ticks()

    score = 0
    time_add = (0.3 - score * 0.5)
    if time_add <= 0:
        time_add = 0.05

    while True:
        screen.fill(bg_color)

        # Render the score in a large, gray font and display it at the center
        score_text = big_font.render(str(clicks), True, (60, 60, 60))
        score_rect = score_text.get_rect(center=(width / 2, height / 2))
        screen.blit(score_text, score_rect)

        for i in range(3):
            screen.blit(circle, circle_pos[i])

        touched = Circle_Check()
        if touched != -1:
            total_time += time_add
            Circle_Appear(touched)
            touched = -1
            if first_click:
                first_click = False
                started = time.time_ns()
                start_ticks = pygame.time.get_ticks()
                start = 1
                pygame.draw.rect(screen, bg_color,
                                 (width / 6 - calib_text.get_width() / 2, 900, calib_text.get_height(),
                                  calib_text.get_height()))

            circle_click.stop()
            circle_click.play()
            clicks += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        if finished:
            score = clicks
            return

        if start == 1:
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        else:
            elapsed_time = total_time
        formatted_time = "{:.2f}".format(total_time - elapsed_time)
        timer = big_font.render("time : {}".format(formatted_time), True, (200, 200, 200))

        screen.blit(timer, (width / 2 - timer.get_width() / 2, 30))

        # Time bar
        if start == 1:
            time_fraction = max(0, total_time - elapsed_time) / total_time
            bar_length = int(time_fraction * (width - 50))
            bar_color = (255 * (1 - time_fraction), 255 * time_fraction, 200)
            pygame.draw.rect(screen, bar_color, (50, 1060, bar_length, 20))

        if int(total_time - elapsed_time) == 0 and start == 1:
            finished = True

        if first_click:
            screen.blit(text_first_click_info, (width / 2 - text_first_click_info.get_width() / 2, height / 1.6))
            screen.blit(calib_text, (width / 6 - calib_text.get_width() / 2, 900))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.circle(screen, (102, 102, 255), (mouse_x, mouse_y), 10)
        pygame.mouse.set_visible(False)
        clock.tick(fps)

        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if width / 6 - calib_text.get_width() / 2 <= mouse_x <= width / 6 + calib_text.get_width() / 2 and 900 <= mouse_y <= 900 + calib_text.get_height() and first_click:
                    Calibration()
        pygame.display.flip()

def show_finished_screen():
    Leaderboard()
    global recorded
    recorded = 0
    while True:
        screen.fill(bg_color)
        Title = big_font.render("EYE-AIM", True, (255, 255, 255))
        screen.blit(Title, (width / 2 - Title.get_width() / 2, 40))
        Leaderboard_text = kofont.render("순위", True, (255, 255, 255))
        start_text = font.render("다시 시작", True, (255, 255, 255))
        button1_x = (width * 3 / 2 / 2 - Leaderboard_text.get_width() / 2)
        button1_y = (height * 3 / 2 / 2 - Leaderboard_text.get_height() / 2)
        button2_x = (width / 2 - start_text.get_width() / 2)
        button2_y = (height / 2 - start_text.get_height() / 2)
        screen.blit(Leaderboard_text, (button1_x, button1_y))
        screen.blit(start_text, (button2_x, button2_y))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
            elif i.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button1_x <= mouse_x <= button1_x + Leaderboard_text.get_width() and button1_y <= mouse_y <= button1_y + Leaderboard_text.get_height():
                    Leaderboard()
                elif button2_x <= mouse_x <= button2_x + start_text.get_width() and button2_y <= mouse_y <= button2_y + start_text.get_height():
                    Leaderboard()
        pygame.display.update()
        clock.tick(fps)

def Leaderboard():
    global recorded
    while True:
        screen.fill(bg_color)
        Title = big_font.render("EYE-AIM", True, (255, 255, 255))
        screen.blit(Title, (width / 2 - Title.get_width() / 2, 40))
        Leaderboard_text = kofont.render("순위", True, (255, 255, 255))
        start_text = font.render("다시 시작", True, (255, 255, 255))
        button2_x = (width / 2 - start_text.get_width() / 2)
        button2_y = (height / 2 - start_text.get_height() / 2)

        screen.blit(Leaderboard_text, (width / 2 - Leaderboard_text.get_width() / 2, height / 2 - Leaderboard_text.get_height() / 2 - 100))
        screen.blit(start_text, (button2_x, button2_y))
        pygame.draw.rect(screen, (255, 255, 255), (100, 250, width - 200, height - 500), 3)
        y = 0

        with open('highscore.txt', 'r') as file:
            lines = file.readlines()

        for line in lines:
            highscore = line.strip()
            highscore_text = font.render(highscore, True, (255, 255, 255))
            screen.blit(highscore_text, (150, 250 + y))
            y += 30

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
            elif i.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button2_x <= mouse_x <= button2_x + start_text.get_width() and button2_y <= mouse_y <= button2_y + start_text.get_height():
                    main()
        pygame.display.update()
        clock.tick(fps)

def Calibration():
    global recorded
    global total_time
    global clicks
    global fps
    global calibration_time
    calibration_time = 5
    start_ticks = pygame.time.get_ticks()
    screen.fill(bg_color)
    calibration_text = font.render("Calibration", True, (255, 255, 255))
    screen.blit(calibration_text, (width / 2 - calibration_text.get_width() / 2, height / 2 - calibration_text.get_height() / 2))
    pygame.display.update()
    time.sleep(3)

    while True:
        screen.fill(bg_color)
        calibration_time = (pygame.time.get_ticks() - start_ticks) / 1000
        calibration_timer_text = font.render("{:.2f}".format(calibration_time), True, (255, 255, 255))
        screen.blit(calibration_timer_text, (width / 2 - calibration_timer_text.get_width() / 2, height / 2 - calibration_timer_text.get_height() / 2))

        for i in range(3):
            screen.blit(circle, circle_pos[i])

        pygame.draw.circle(screen, (102, 102, 255), (mouse_x, mouse_y), 10)
        pygame.mouse.set_visible(False)

        if calibration_time >= 5:
            calibration_time = round(calibration_time, 2)
            with open('highscore.txt', 'a') as file:
                file.write("[" + str(calibration_time) + "]\n")

            clicks = 0
            total_time = calibration_time
            main()

        pygame.display.update()
        clock.tick(fps)

# Run the main function
if __name__ == "__main__":
    main()
