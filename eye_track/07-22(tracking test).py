#!/usr/bin/python

# Programmed by hXR16F
# hXR16F.ar@gmail.com, https://github.com/hXR16F

import time
import pygame
from random import randint
import hangul_utils
import requests
import cv2

# 할 일
# Leaderboard 마무리
# -> 기록 제대로 표시 확인
# Calibration 화면 만들기

ko = {'Q':'ㅃ', 'W':'ㅉ', 'E':'ㄸ', 'R':'ㄲ', 'T':'ㅆ', 'Y':'ㅛ', 'U':'ㅕ', 'I':'ㅑ', 'O':'ㅒ', 'P':'ㅖ', 'A':'ㅁ', 'S':'ㄴ', 'D':'ㅇ', 'F':'ㄹ', 'G':'ㅎ', 'H':'ㅗ', 'J':'ㅓ', 'K':'ㅏ', 'L':'ㅣ', 'Z':'ㅋ', 'X':'ㅌ', 'C':'ㅊ', 'V':'ㅍ', 'B':'ㅠ', 'N':'ㅜ', 'M':'ㅡ',
'rt':'ㄳ', 'sw':'ㄵ', 'sg':'ㄶ', 'fr':'ㄺ', 'fa':'ㄻ', 'fq':'ㄼ', 'ft':'ㄽ', 'fx':'ㄾ', 'fv':'ㄿ', 'fg':'ㅀ', 'qt':'ㅄ', 'k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'nj':'ㅝ', 'np':'ㅞ', 'nl':'ㅟ', 'b':'ㅠ',  'm':'ㅡ', 'ml':'ㅢ', 'l':'ㅣ',
      'q':'ㅂ', 'w':'ㅈ', 'e':'ㄷ', 'r':'ㄱ', 't':'ㅅ', 'y':'ㅛ', 'u':'ㅕ', 'i':'ㅑ', 'o':'ㅐ', 'p':'ㅔ', 'a':'ㅁ', 'd':'ㅇ', 'f':'ㄹ', 'g':'ㅎ', 'h':'ㅗ', 'j':'ㅓ', 'k':'ㅏ', 'l':'ㅣ', 'z':'ㅋ', 'x':'ㅌ', 'c':'ㅊ', 'v':'ㅍ', 'b':'ㅠ', 'n':'ㅜ', 'm':'ㅡ', 's':'ㄴ', }
mo = {'k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'nj':'ㅝ', 'np':'ㅞ', 'nl':'ㅟ', 'b':'ㅠ',  'm':'ㅡ', 'ml':'ㅢ', 'l':'ㅣ',}


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
    time_add = (0.3 - score*0.5)
    if time_add <= 0:
        time_add = 0.05

    while True:
        screen.fill(bg_color)

        # Render the score in a large, gray font and display it at the center
        big_font = pygame.font.SysFont("malgungothic", 400)
        score_text = big_font.render(str(clicks), True, (60, 60, 60))
        score_rect = score_text.get_rect(center=(width / 2, height / 2))
        screen.blit(score_text, score_rect)

        for i in range(3):
            screen.blit(circle, circle_pos[i])
        '''
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click == True
            else:
                click == False
        '''

        touched = Circle_Check()
        if touched != -1:
            total_time += time_add  ##시간추가...! timeadd
            Circle_Appear(touched)  # Move the circle to a new position
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
        timer = Bigbigfont.render("time : {}".format(formatted_time), True, (200, 200, 200))

        screen.blit(timer, (width / 2 - timer.get_width() / 2, 30))

        # 시간바
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
        Title = Bigbigfont.render("EYE-AIM", True, (255,255,255))
        screen.blit(Title, (width/2-Title.get_width()/2, 40))
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
                button2_rect = start_text.get_rect()
                if button1_x <= mouse_x <= button1_x + Leaderboard_text.get_width() and button1_y<=mouse_y<=button1_y + Leaderboard_text.get_height():
                    Leaderboard()
                    break
                elif button2_x <= mouse_x <= button2_x + button2_rect[2] and button2_y<=mouse_y<=button2_y + button2_rect[3]:
                    return
        pygame.display.flip()



def Leaderboard():
    global Search_text
    global recorded
    global Input
    while True:
        Input = kofont.render("입력하기", True, (255, 255, 255))
        Search_text = font.render("검색하기", True, (255, 255, 255))
        reset_Leaderboard()
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if width/2-back_text.get_width()/2 <= mouse_x <= width/2+back_text.get_width()/2 and 900 <= mouse_y <= 900+back_text.get_height():
                    return
                if width/2-Input.get_width()/2 <= mouse_x <= width/2+Input.get_width()/2 and 600 <= mouse_y <= 600 + Input.get_height() and over == 0:
                    name = ''
                    previous = ''
                    while True:
                        Input = kofont.render(hangul_utils.join_jamos(jamos(name)), True, (255, 255, 255))
                        reset_Leaderboard()
                        out = 0
                        for ev2 in pygame.event.get():
                            if ev2.type == pygame.MOUSEBUTTONDOWN:
                                out = 1
                            elif ev2.type == pygame.KEYDOWN:
                                if ev2.key == pygame.K_RETURN:
                                    if recorded == 0:
                                        record[score].append(name)
                                        out = 1
                                        recorded = 1

                                        if score >= 0:
                                            if score < 20:
                                                coin = 50
                                            if score <= 20 < 30:
                                                coin = 75
                                            if score >= 30:
                                                coin = 100

                                            #requests.get(f"https://sada.ziho.kr/coin/add/{name.split('_')[0]}/{name.split('_')[1]}/100")
                                            if len(hangul_utils.join_jamos(jamos(name)).split('_')) == 2:
                                                requests.request('GET', f"https://sada.ziho.kr/coin/add/{hangul_utils.join_jamos(jamos(name)).split('_')[0]}/{hangul_utils.join_jamos(jamos(name)).split('_')[1]}/{coin}")


                                    break

                                elif ev2.key == pygame.K_BACKSPACE:
                                    if name != '':
                                        name = name[:-1]
                                        reset_Leaderboard()
                                else:

                                    if len(name) <= 13:

                                        if ev2.unicode in ko.keys():
                                            name += ko[ev2.unicode]
                                        else:
                                            name += ev2.unicode
                                        previous = ev2.unicode
                                    else:
                                        pygame.draw.rect(screen, bg_color, [width / 2 - Input.get_width() / 2, 500, Input.get_width(),Input.get_height()])
                                        Input = kofont.render("최대 글자수 : 13자", True, (255, 150, 150))
                                        screen.blit(Input, (width / 2 - Input.get_width() / 2, 600))
                                        pygame.display.flip()
                                        time.sleep(1)
                                        name = name[:13]
                                        Input = kofont.render(hangul_utils.join_jamos(jamos(name)), True, (255, 255, 255))
                                        reset_Leaderboard()
                                    break
                        name_text = kofont.render(hangul_utils.join_jamos(jamos(name)), True, (255, 255, 255))
                        screen.blit(name_text, (width/2-name_text.get_width()/2, 600))
                        pygame.display.flip()
                        if out == 1:
                            Input = kofont.render("입력하기", True, (255,255,255))
                            screen.blit(Input, (width/2-Input.get_width()/2, 600))
                            pygame.display.flip()
                            break
                if width / 2 - Search_text.get_width() / 2 <= mouse_x <= width / 2 + Search_text.get_width() / 2 and 700 <= mouse_y <= 700 + Search_text.get_height():
                    init = ''
                    while True:
                        Search_text = kofont.render(hangul_utils.join_jamos(jamos(init)), True, (255, 255, 255))
                        reset_Leaderboard()
                        out = 0
                        for ev2 in pygame.event.get():
                            if ev2.type == pygame.MOUSEBUTTONDOWN:
                                out = 1
                            elif ev2.type == pygame.KEYDOWN:
                                if ev2.key == pygame.K_RETURN:
                                    if sum(i.count(init) for i in record) != 0:
                                        show_ranking(init)
                                    else:
                                        pygame.draw.rect(screen, bg_color,
                                                         [width / 2 - Search_text.get_width() / 2, 700, Search_text.get_width(),
                                                          Search_text.get_height()])
                                        Search_text = kofont.render("등록되지 않은 사용자", True, (255, 150, 150))
                                        screen.blit(Search_text, (width / 2 - Search_text.get_width() / 2, 700))
                                        pygame.display.flip()
                                        time.sleep(1)
                                        Search_text = kofont.render("검색하기", True, (255, 255, 255))
                                        reset_Leaderboard()
                                    out = 1
                                    break

                                elif ev2.key == pygame.K_BACKSPACE:
                                    if init != '':
                                        init = init[:-1]
                                        reset_Leaderboard()
                                else:
                                    if len(init) <= 13:
                                        if ev2.unicode in ko.keys():
                                            init += ko[ev2.unicode]
                                        else:
                                            init += ev2.unicode
                                    else:
                                        pygame.draw.rect(screen, bg_color,
                                                         [width / 2 - Search_text.get_width() / 2, 700, Search_text.get_width(),
                                                          Search_text.get_height()])
                                        Search_text = kofont.render("최대 글자수 : 13자", True, (255, 150, 150))
                                        screen.blit(Search_text, (width / 2 - Search_text.get_width() / 2, 700))
                                        pygame.display.flip()
                                        time.sleep(1)
                                        init = init[:13]
                                        Search_text = kofont.render(hangul_utils.join_jamos(jamos(init)), True, (255, 255, 255))
                                        reset_Leaderboard()
                                    break
                        init_text = font.render(hangul_utils.join_jamos(jamos(init)), True, (255, 255, 255))
                        screen.blit(init_text, (width / 2 - init_text.get_width() / 2, 700))
                        pygame.display.flip()
                        if out == 1:
                            Search_text = kofont.render("검색하기", True, (255, 255, 255))
                            screen.blit(Search_text, (width / 2 - Search_text.get_width() / 2, 700))
                            pygame.display.flip()
                            break
        if over == 1:
            break


def reset_Leaderboard():
    ranking = ["1st: ", "2nd: ", "3rd: ", "4th: ", "5th: "]
    global Search_text
    global Input
    global Title
    global back_text

    screen.fill(bg_color)
    Bigfont = pygame.font.SysFont("malgungothic", 48)
    Title = Bigfont.render("순위", True, (255, 255, 255))
    back_text = font.render("뒤로", True, (255, 255, 255))
    score_text = font.render("점수 : " + str(score), True, (255, 255, 255))
    screen.blit(Title, (width / 2 - Title.get_width() / 2, 50))
    info_text = font.render("'인증번호_이름'을 입력해주세요. SADA Coin 시스템에 이용됩니다.", True, (255, 255, 255))
    cnt = 0
    for i in range(len(record)-1, -1, -1):
        if record[i] != []:
            for j in record[i]:
                cnt += 1
                if cnt > 5:
                    break
                screen.blit(kofont.render(ranking[cnt-1] + hangul_utils.join_jamos(jamos(j)) + f" : {i}", True, (255,255,255)),
                            (width/2-kofont.render(ranking[cnt-1] + hangul_utils.join_jamos(jamos(j)) + f" : {i}", True, (255,255,255)).get_width()/2, 110+50*(cnt-1)))

            if cnt > 5:
                break
    while cnt < 5:
        screen.blit(font.render(ranking[cnt] + "없음", True, (255, 255, 255)),
                    (width / 2 - font.render(ranking[cnt] + "없음", True, (255, 255, 255)).get_width() / 2,
                     110 + 50 * cnt))
        cnt += 1

    screen.blit(Input, (width / 2 - Input.get_width() / 2, 600))
    screen.blit(back_text, (width / 2 - back_text.get_width() / 2, 900))
    screen.blit(score_text, (40, 20))
    screen.blit(Search_text, (width / 2 - Search_text.get_width() / 2, 700))
    screen.blit(info_text, (width / 2 - info_text.get_width() / 2, 500))
    pygame.display.flip()


def show_ranking(name):
    global record
    back_text = font.render("뒤로", True, (255, 255, 255))
    Bigfont = pygame.font.SysFont("malgungothic", 48)
    screen.fill(bg_color)
    screen.blit(Bigfont.render(f"{hangul_utils.join_jamos(jamos(name))}의 점수", True, (255, 255, 255)), (width/2-Bigfont.render(f"{hangul_utils.join_jamos(name)}'s Score", True, (255, 255, 255)).get_width()/2, 40))
    screen.blit(back_text, (width / 2 - back_text.get_width() / 2, 900))
    cnt = sum(i.count(name) for i in record)
    pages = (cnt-1)//15+1
    column = 0
    gap = 200
    cnt = -1
    for i in range(len(record)-1, -1, -1):
        if name in record[i]:
            for j in record[i]:
                if j == name:
                    cnt += 1
                    if cnt % 15 == 0:
                        column += 1
                        cnt = 0
                    screen.blit(kofont.render(str(i), True, (255,255,255)), (width/2-font.render(str(i), True, (255, 255, 255)).get_width()/2+gap*(column-1)-(pages-1)*0.5*gap, 100+50*cnt))

    pygame.display.flip()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y = pygame.mouse.get_pos()
                if width / 2 - back_text.get_width() / 2 <= mouse_x <= width/2 + back_text.get_width()/2 and 900 <= mouse_y <= 900 + back_text.get_height():
                    return


def Calibration():
    pygame.mouse.set_visible(True)
    # COLOR_CHANGE = [(200,200,255), (150,150,255), (100,100,255)]

    pos = [[40, 40], [width / 2, 40], [width - 40, 40], [40, height / 2], [width / 2, height / 2],
           [width - 40, height / 2], [40, height - 40], [width / 2, height - 40], [width - 40, height - 40]]
    while True:
        for j in range(2):
            colors = [(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),
                      (255, 255, 255),
                      (255, 255, 255), (255, 255, 255), (255, 255, 255)]
            click_n = [0 for i in range(9)]
            screen.fill(bg_color)
            for i in range(len(pos)):
                pygame.draw.circle(screen, colors[i],pos[i], 15)
                pygame.display.flip()
                clicked = []
                b = 0

                while True:
                    screen.fill(bg_color)
                    pygame.draw.circle(screen, colors[i], pos[i], 15)
                    pygame.display.flip()
                    for ev in pygame.event.get():
                        if ev.type == pygame.MOUSEBUTTONDOWN:
                            mouse_x,mouse_y = pygame.mouse.get_pos()
                            if (mouse_x-pos[i][0])**2+(mouse_y-pos[i][1])**2 <= 225:
                                print(pos[i][0], pos[i][1])
                                #if click_n[i] < 1:
                                click_n[i] += 1
                                clicked = pos[i]
                                    #colors[i] = COLOR_CHANGE[click_n[i]]
                                #else:
                                b = 1
                    if b == 1:
                        break

            print(clicked if clicked != [] else '', end='')
        if sum(click_n) == 9:
            break



def Circle_Appear(i):
    circle_pos[i] = [randint(0, width - circle_size), randint(0, height - circle_size)]
    screen.blit(circle, circle_pos[i])


def Circle_Check():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for i in range(3):
        if (mouse_x - circle_pos[i][0]-60) ** 2 + (mouse_y - circle_pos[i][1]-60) ** 2 <= (circle_size/2 + 45) ** 2:
            return i
    return -1

def jamos(name):
    translated = ''
    final = ''
    mo_count = 0
    previous_cons = 0
    for i in range(len(name)):
        if name[i] in mo.values():
            if mo_count == 1:
                translated += intwine(name[i-1], name[i])
                mo_count = 0
            else:
                mo_count = 1
                if i != len(name)-1:
                    if previous_cons == 1 and name[i+1] not in mo.values():
                        translated += name[i]
        else:
            mo_count = 0
            translated += name[i]
            previous_cons = 1

    return translated

def intwine(char1, char2):
    if char1+char2 in char_dict.keys():
        return char_dict[char1+char2]
    else:
        return char1+char2


if __name__ == "__main__":

    fps = 100
    clock = pygame.time.Clock()
    size = width, height = 1920,1080
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    bg_color = 40, 40, 40

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    kofont = pygame.font.SysFont("malgungothic", 36)
    Bigbigfont = pygame.font.SysFont("malgungothic", 64)
    font = pygame.font.SysFont("malgungothic", 36) # https://fonts.google.com/specimen/Jura
    circle_click = pygame.mixer.Sound("assets/click.wav") # https://www.zapsplat.com/music/single-click-screen-press-on-smart-phone-1
    circle = pygame.image.load("assets/circle.png") # https://www.pngwing.com/en/free-png-zuamu
    circle_pos = [[], [], []]

    pygame.key.set_repeat(800, 100)
    pygame.display.set_caption("EyeAim")
    pygame.display.set_icon(circle)

    circle_size = 100
    circle = pygame.transform.scale(circle, (circle_size, circle_size))
    circle_rect = circle.get_rect()
    record = list([] for i in range(200))
    over = 0
    threshold = 10000
    char_dict = {"ㅗㅏ": "ㅘ", "ㅜㅣ": "ㅟ", "ㅗㅣ": "ㅚ", "ㅗㅐ": "ㅙ", "ㅜㅔ": "ㅞ", 'ㅡㅣ': 'ㅢ', 'ㅜㅓ': 'ㅝ'}

    while True:
        total_time = 5
        main()
        pygame.mouse.set_visible(True)
        show_finished_screen()
