# в данном коде уже частично выполнено слияние с кодом вячеслава и максима
import pygame
import random
import sqlite3
import sys
import telebot
import pygame.locals

connect = sqlite3.connect('polzovateli.sqlite')
cursor = connect.cursor()
API_TOKEN = '6810674714:AAGKeBsa0NlUhx2jECLUhnGxHv4s_ZLZQm4'
bot = telebot.TeleBot(API_TOKEN)
API_TOKEN2 = '6855961014:AAGpEI1f1EveHzMvb49EJG70CEAutDnsGr0'
bot2 = telebot.TeleBot(API_TOKEN2)
login = ''

all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
balls2 = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Russkaya_ruletka:
    def __init__(self):
        pygame.init()
        self.BLACK = (0, 0, 0)
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.WHITE = (255, 255, 255)
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Русская Рулетка")
        self.gunshot_sound = pygame.mixer.Sound("rev.mp3")
        self.empty_sound = pygame.mixer.Sound("rev_1.mp3")
        self.font = pygame.font.Font(None, 36)
        self.current_level = None
        self.bullet_position = None
        self.background_image = pygame.image.load("kartinki/fon_russkaya_ruletka.jpg")
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.koeff = 0
        self.stavka = ''
        self.font = pygame.font.Font(None, 36)
        self.zamechanie = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect = (325, 100, 475, 40)
        self.input_stavka_x, self.input_stavka_y, self.input_stavka_width, self.input_stavka_height = \
            400, 550, 200, 30
        self.input_stavka_rect = pygame.Rect(
            self.input_stavka_x, self.input_stavka_y, self.input_stavka_width, self.input_stavka_height)
        self.stavka_flag = False
        self.play = False
        self.shots_count = 0
        self.bullets_list = []
        self.total = 0
        self.run_game()

    def power(self):
        if len(str(self.stavka)) != 0:
            if int(self.stavka) <= self.balance:
                self.stavka = int(self.stavka)
                cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                    self.balance - int(self.stavka)), (str(login))))
                connect.commit()
                cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                               (str(self.lose + int(self.stavka) * valuta_koef()), (str(login))))
                connect.commit()
                first = ['1', '2', '3', '4', '5', '6']
                bullets = random.sample(first, self.current_level)
                self.bullets_list = list(first)
                for bullet in bullets:
                    self.bullets_list[int(bullet) - 1] = ''
                text = ''
                for i in range(6):
                    if self.bullets_list[i] == '':
                        text += str(i + 1) + str(') ❌') + '.'
                    else:
                        text += str(i + 1) + str(') ✅') + '.'
                bot.send_message(5473624098, f'''======Russkaya ruletka======
                    {text.split('.')[0]}
                    {text.split('.')[1]}
                    {text.split('.')[2]}
                    {text.split('.')[3]}
                    {text.split('.')[4]}
                    {text.split('.')[5]}''')
                self.shots_count = 0
                self.total = 1
                self.koeff = 1 + self.current_level / (6 - self.current_level)
            else:
                self.font = pygame.font.Font(None, 25)
                self.zamechanie = self.font.render(f"У вас недостаточно средств!", True, (255, 0, 0))
                self.play = False
        else:
            self.font = pygame.font.Font(None, 25)
            self.zamechanie = self.font.render(f"Введите ставку!", True, (255, 0, 0))
            self.play = False

    def run_game(self):
        while True:
            global login
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            if self.play:
                if self.total == 0:
                    self.power()
                elif self.play:
                    self.screen.blit(self.background_image, (0, 0))
                    self.screen.blit(self.zamechanie, (325, 100, 475, 40))
                    f_shoot = pygame.font.Font(None, 30)
                    text_shoot = f_shoot.render('Выстрел', True, (255, 255, 255))
                    place_shoot = text_shoot.get_rect(center=(225, 525))
                    pygame.draw.rect(self.screen, (255, 255, 255), (100, 500, 250, 50), 2)
                    self.screen.blit(text_shoot, place_shoot)

                    f_take = pygame.font.Font(None, 30)
                    text_take = f_take.render('Забрать ставку', True, (255, 255, 255))
                    place_take = text_take.get_rect(center=(575, 525))
                    pygame.draw.rect(self.screen, (255, 255, 255), (450, 500, 250, 50), 2)
                    self.screen.blit(text_take, place_take)
                    self.balance = float(
                        str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?",
                                           (str(login),)).fetchall()[0][0]))
                    font = pygame.font.Font(None, 30)
                    text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
                    text_rect = (10, 10)
                    self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
                    self.screen.blit(text, text_rect)
                    font = pygame.font.Font(None, 30)
                    text = font.render(f"Возможный выигрыш: {round(self.stavka, 2)}", True, (255, 255, 255))
                    self.screen.blit(text, (10, 50, 780, 40))
                    font = pygame.font.Font(None, 25)
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     (self.button_x_menu, self.button_y_menu, self.button_width_menu,
                                      self.button_height_menu),
                                     3, border_radius=15)
                    text = font.render("Выйти в меню", True, (255, 255, 255))
                    text_rect = text.get_rect(
                        center=(self.button_x_menu + self.button_width_menu // 2,
                                self.button_y_menu + self.button_height_menu // 2))
                    self.screen.blit(text, text_rect)

                    pygame.display.flip()
            else:
                self.balance = float(
                    str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][
                            0]))
                self.screen.blit(self.background_image, (0, 0))
                self.zamechanie_rect = (10, 500, 780, 40)
                self.screen.blit(self.zamechanie, self.zamechanie_rect)

                self.font = pygame.font.Font(None, 30)
                text = self.font.render("Введите ставку:", True, (255, 255, 255))
                text_rect = (200, 550, 475, 40)
                self.screen.blit(text, text_rect)
                pygame.draw.rect(self.screen, (255, 255, 255), self.input_stavka_rect, 2)
                text_surface = self.font.render(str(self.stavka), True, (255, 255, 255))
                self.screen.blit(text_surface, (self.input_stavka_rect.x + 5, self.input_stavka_rect.y + 5))
                self.input_stavka_rect.w = max(200, text_surface.get_width() + 10)

                font = pygame.font.Font(None, 35)
                text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
                text_rect = (10, 10)
                self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
                self.screen.blit(text, text_rect)

                font = pygame.font.Font(None, 27)
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (self.button_x_menu, self.button_y_menu, self.button_width_menu,
                                  self.button_height_menu), 3, border_radius=15)

                text = font.render("Выйти в меню", True, (255, 255, 255))
                text_rect = text.get_rect(
                    center=(self.button_x_menu + self.button_width_menu // 2,
                            self.button_y_menu + self.button_height_menu // 2))
                self.screen.blit(text, text_rect)

                f1 = pygame.font.Font(None, 35)
                text1 = f1.render('ВЫБЕРИТЕ УРОВЕНЬ:', True, (255, 255, 255))
                place1 = text1.get_rect(center=(410, 50))
                self.screen.blit(text1, place1)

                f2 = pygame.font.Font(None, 39)
                text2 = f2.render('Уровень 1', True, (255, 255, 255))
                place_shoot = text2.get_rect(center=(225, 125))
                pygame.draw.rect(self.screen, (255, 255, 255), (125, 85, 180, 50), 2)
                self.screen.blit(text2, (150, 100))

                f3 = pygame.font.Font(None, 38)
                text3 = f3.render('Уровень 2', True, (255, 255, 255))
                place3 = text3.get_rect(center=(215, 190))
                pygame.draw.rect(self.screen, (255, 255, 255), (125, 165, 180, 50), 2)
                self.screen.blit(text3, place3)

                f4 = pygame.font.Font(None, 38)
                text4 = f4.render('Уровень 3', True, (255, 255, 255))
                place4 = text4.get_rect(center=(215, 270))
                pygame.draw.rect(self.screen, (255, 255, 255), (125, 245, 180, 50), 2)
                self.screen.blit(text4, place4)

                f5 = pygame.font.Font(None, 38)
                text5 = f5.render('Уровень 4', True, (255, 255, 255))
                place5 = text5.get_rect(center=(215, 350))
                pygame.draw.rect(self.screen, (255, 255, 255), (125, 325, 180, 50), 2)
                self.screen.blit(text5, place5)

                f5 = pygame.font.Font(None, 38)
                text5 = f5.render('Уровень 5', True, (255, 255, 255))
                place5 = text5.get_rect(center=(215, 430))
                pygame.draw.rect(self.screen, (255, 255, 255), (125, 405, 180, 50), 2)
                self.screen.blit(text5, place5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif self.play:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                                self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                            pygame.quit()
                            Menu()
                        if 100 <= mouse_x <= 350 and 500 <= mouse_y <= 550:
                            if self.bullets_list[self.shots_count] != '':
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Вам повезло!", True, (50, 255, 50))
                                self.zamechanie_rect = (325, 10, 475, 40)
                                self.stavka *= self.koeff
                                self.shots_count += 1
                                self.empty_sound.play()
                            else:
                                self.gunshot_sound.play()
                                self.play = False
                                self.zamechanie = self.font.render("Вам не повезло!", True, (255, 0,0))
                                self.stavka = ''
                            if self.shots_count >= 6 - self.current_level:
                                self.play = False
                                cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                                    self.balance + int(self.stavka)), (str(login))))
                                connect.commit()
                                cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                               (str(self.win + int(self.stavka) * valuta_koef()), (str(login))))
                                connect.commit()
                                self.stavka = ''
                                self.zamechanie = self.font.render(" ", True, (50, 255, 50))
                        elif 450 <= mouse_x <= 700 and 500 <= mouse_y <= 550:
                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                                self.balance + int(self.stavka)), (str(login))))
                            connect.commit()
                            cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                           (str(self.win + int(self.stavka) * valuta_koef()), (str(login))))
                            connect.commit()
                            cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                           (str(self.lose - int(self.stavka) * valuta_koef()), (str(
                                               login))))
                            connect.commit()
                            self.play = False
                            self.stavka = ''
                            self.zamechanie = self.font.render(" ", True, (50, 255, 50))
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if self.input_stavka_x <= mouse_x <= self.input_stavka_x + int(self.input_stavka_rect[2]) and\
                                self.input_stavka_y <= mouse_y <= self.input_stavka_y + int(self.input_stavka_rect[3]):
                            self.stavka_flag = True
                        elif self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                                self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                            pygame.quit()
                            Menu()
                        elif 125 < x < 305 and 85 < y < 135:
                            self.current_level = 1
                            self.total = 0
                            self.play = True
                            self.zamechanie = self.font.render(f" ", True, (255, 0, 0))

                        elif 125 < x < 305 and 165 < y < 215:
                            self.current_level = 2
                            self.total = 0
                            self.play = True
                            self.zamechanie = self.font.render(f" ", True, (255, 0, 0))

                        elif 125 < x < 305 and 245 < y < 295:
                            self.current_level = 3
                            self.total = 0
                            self.play = True
                            self.zamechanie = self.font.render(f" ", True, (255, 0, 0))

                        elif 125 < x < 305 and 325 < y < 375:
                            self.current_level = 4
                            self.total = 0
                            self.play = True
                            self.zamechanie = self.font.render(f" ", True, (255, 0, 0))

                        elif 125 < x < 305 and 405 < y < 455:
                            self.current_level = 5
                            self.total = 0
                            self.play = True
                            self.zamechanie = self.font.render(f" ", True, (255, 0, 0))

                    elif event.type == pygame.KEYDOWN:
                        if self.stavka_flag:
                            if event.key == pygame.K_BACKSPACE:
                                self.stavka = self.stavka[:-1]
                            else:
                                if str(event.unicode).isnumeric():
                                    if len(self.stavka) < 31:
                                        self.stavka += event.unicode
                                    else:
                                        self.font = pygame.font.Font(None, 25)
                                        self.zamechanie = self.font.render(
                                            "Вы достигли максимальной суммы ставки ставки!", True, (255, 0, 0))
                                else:
                                    self.font = pygame.font.Font(None, 25)
                                    self.zamechanie = self.font.render("Введите целое число!", True, (255, 0, 0))

            pygame.display.flip()


class Orel_Reshka:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.user_text = ''
        self.active = False
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 200, 530, 50, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.screen = pygame.display.set_mode((800, 600))
        self.background_image = pygame.image.load('kartinki/fon_monetka.jpg')
        self.screen.blit(self.background_image, (0, 0))
        pygame.display.set_caption("Монетка")
        self.font = pygame.font.Font(None, 36)
        self.orel_x, self.orel_y, self.orel_width, self.orel_height = 550, 550, 100, 30
        self.button_orel = pygame.Rect(self.orel_x, self.orel_y, self.orel_width, self.orel_height)
        pygame.draw.rect(self.screen, self.WHITE, self.button_orel, 2)
        self.text_orel = self.font.render("Орёл", True, self.WHITE)
        self.text_orel_pos = self.text_orel.get_rect(
            center=(self.orel_x + self.orel_width // 2, self.orel_y + self.orel_height // 2))
        self.reshka_x, self.reshka_y, self.reshka_width, self.reshka_height = 700, 550, 100, 30
        self.button_reshka = pygame.Rect(self.reshka_x, self.reshka_y, self.reshka_width, self.reshka_height)
        pygame.draw.rect(self.screen, self.WHITE, self.button_reshka, 2)
        self.text_reshka = self.font.render("Решка", True, self.WHITE)
        self.text_reshka_pos = self.text_reshka.get_rect(
            center=(self.reshka_x + self.reshka_width // 2, self.reshka_y + self.reshka_height // 2))
        self.itog = self.font.render("Выбирай!", True, (255, 255, 255))
        self.itog_rect = self.itog.get_rect(center=(400, 50))
        self.screen.blit(self.itog, self.itog_rect)
        self.user_choice = None
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def flip_coin(self):
        result = random.choice(['Орёл', 'Решка'])
        return result

    def paint(self):
        self.screen.blit(self.text_orel, self.text_orel_pos)
        self.screen.blit(self.text_reshka, self.text_reshka_pos)
        pygame.draw.rect(self.screen, self.WHITE, self.button_reshka, 2)
        pygame.draw.rect(self.screen, self.WHITE, self.button_orel, 2)
        self.screen.blit(self.itog, self.itog_rect)
        font = pygame.font.Font(None, 27)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu),
                         3, border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)
        self.font = pygame.font.Font(None, 30)
        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (20, 530)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, self.WHITE, self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.paint()
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.orel_x <= mouse_x <= self.orel_x + self.orel_width and \
                            self.orel_y <= mouse_y <= self.orel_y + self.orel_height:
                        if len(str(self.user_text)) == 0:
                            self.itog = self.font.render("Введите ставку!", True, (255, 0, 0))
                        else:
                            if int(self.user_text) <= self.balance:
                                self.font = pygame.font.Font(None, 30)
                                self.user_choice = 'Орёл'
                                cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                                    self.balance - int(self.user_text)), (str(login))))
                                connect.commit()
                                cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                               (str(self.lose + int(self.user_text) * valuta_koef()), (str(
                                                   login))))
                                connect.commit()
                                self.balance = float(
                                    str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?",
                                                       (str(login),)).fetchall()[0][0]))
                            else:
                                self.itog = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                    elif self.reshka_x <= mouse_x <= self.reshka_x + self.reshka_width and \
                            self.reshka_y <= mouse_y <= self.reshka_y + self.reshka_height:
                        if len(str(self.user_text)) == 0:
                            self.itog = self.font.render("Введите ставку!", True, (255, 0, 0))
                        else:
                            if int(self.user_text) <= self.balance:
                                self.font = pygame.font.Font(None, 30)
                                self.user_choice = 'Решка'
                                cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                                    self.balance - int(self.user_text)), (str(login))))
                                connect.commit()
                                cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                               (str(self.lose + int(self.user_text) * valuta_koef()), (str(
                                                   login))))
                                connect.commit()
                                self.balance = float(
                                    str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?",
                                                       (str(login),)).fetchall()[0][0]))
                            else:
                                self.itog = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                    elif self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    else:
                        self.user_choice = None

                    if self.user_choice is not None:
                        result = self.flip_coin()
                        if self.user_choice == result:
                            self.itog = self.font.render("Вы угадали!", True, (0, 100, 0))
                            self.itog_rect = self.itog.get_rect(center=(400, 10))
                            self.screen.blit(self.itog, self.itog_rect)
                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                                self.balance + int(self.user_text) * 1.9), (str(login))))
                            connect.commit()
                            cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                           (str(self.win + int(self.user_text) * 1.9 * valuta_koef()), (str(login))))
                            connect.commit()
                        else:
                            self.itog = self.font.render("Вы не угадали!", True, (255, 0, 0))
                            self.itog_rect = self.itog.get_rect(center=(400, 10))
                            self.screen.blit(self.itog, self.itog_rect)
                elif event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                self.user_text += event.unicode
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.itog = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
            pygame.display.flip()

class LOTEREYA:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("LOTEREYA")
        self.clock = pygame.time.Clock()
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.chislo = 0
        self.user_text, self.active, self.playing = '', False, False
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.btn_x, self.btn_y, self.btn_width, self.btn_height, self.btn_r = 700, 525, 100, 50, 50
        self.playing = False
        self.click = 0
        self.x, self.y, self.size = 75, 225, 150
        self.kart = ['🎲', '🏵', '🧊', '🍓', '🍒', '💰', '💎']
        self.kart_sl = {
            '🎲': 'lot_kubik.png',
            '🏵': 'lot_cvetochek.png',
            '🧊': 'lot_led.png',
            '🍓': 'lot_klubnika.png',
            '🍒': 'lot_vishnya.png',
            '💰': 'lot_money.png',
            '💎': 'lot_briliant.png',
        }
        self.x_kart = {
            '🎲': 0.05,
            '🏵': 0.1,
            '🧊': 0.25,
            '🍓': 0.4,
            '🍒': 0.65,
            '💰': 0.8,
            '💎': 1,
        }
        self.itog = ''
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 50)

        text = font.render("Лотерейный билет", True, (255, 255, 255))
        self.screen.blit(text, (250, 100))

        pygame.draw.rect(self.screen, (255, 255, 0), (50, 150, 550, 300))
        pygame.draw.rect(self.screen, (255, 0, 0), (600, 150, 150, 300))
        pygame.draw.circle(self.screen, (0, 0, 0), (750, 300), 50)

        if self.playing:
            self.screen.blit(pygame.image.load(f'kartinki/{self.kart_sl[self.itog[0]]}'), (self.x, self.y))
            self.screen.blit(pygame.image.load(f'kartinki/{self.kart_sl[self.itog[1]]}'), (self.x + 175, self.y))
            self.screen.blit(pygame.image.load(f'kartinki/{self.kart_sl[self.itog[2]]}'), (self.x + 350, self.y))
            if self.click != 0:
                self.click = 0
                winer = self.x_kart[self.itog[0]] * int(self.user_text) + self.x_kart[self.itog[1]] * int(
                    self.user_text) + self.x_kart[self.itog[2]] * int(self.user_text)
                cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                               (str(self.balance + int(winer)), (str(login))))
                connect.commit()
                cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                               (str(self.win + int(winer)), (str(login))))
                connect.commit()
                if winer - int(self.user_text) > 0:
                    self.zamechanie = self.font.render(f"Вы выиграли {winer - int(self.user_text)}", True, (0, 255, 0))
                else:
                    self.zamechanie = self.font.render(f"Вы проиграли {int(self.user_text) - winer}", True, (255, 0, 0))
            if self.chislo < 200:
                self.chislo += 1
            else:
                self.playing = False
        else:
            color = (128, 128, 128)
            pygame.draw.rect(self.screen, color, (self.x, self.y, self.size, self.size))
            pygame.draw.rect(self.screen, color, (self.x + 175, self.y, self.size, self.size))
            pygame.draw.rect(self.screen, color, (self.x + 350, self.y, self.size, self.size))
        self.screen.blit(pygame.image.load('kartinki/vortex_button.png'),
                         ((self.btn_x - self.btn_r * 150 / (self.btn_r * 2)),
                          self.btn_y - self.btn_r * 150 / (self.btn_r * 2)))
        pygame.draw.circle(self.screen, (255, 255, 255), (self.btn_x, self.btn_y), self.btn_r, 3)
        text = self.font.render("Стереть", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.btn_x, self.btn_y))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = self.font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def play(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.btn_x - self.btn_r <= mouse_x <= self.btn_x + self.btn_r and \
                            self.btn_y - self.btn_r <= mouse_y <= self.btn_y + self.btn_r:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if not self.playing:
                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                   (str(self.balance - int(self.user_text)),
                                                    (str(login))))
                                    connect.commit()
                                    cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                                   (str(self.lose + int(self.user_text)),
                                                    (str(login))))
                                    connect.commit()
                                    self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                                    self.playing = True
                                    self.chislo = 0
                                    self.click = 1
                                    self.itog = random.choice(self.kart) + random.choice(
                                        self.kart) + random.choice(self.kart)
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Игра уже запущена!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if not self.playing:
                        if self.active:
                            if event.key == pygame.K_BACKSPACE:
                                self.user_text = self.user_text[:-1]
                            else:
                                if str(event.unicode).isnumeric():
                                    if len(self.user_text) > 30:
                                        self.font = pygame.font.Font(None, 30)
                                        self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                           True, (255, 0, 0))
                                    else:
                                        self.user_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))

            pygame.display.flip()
            self.clock.tick(100)
