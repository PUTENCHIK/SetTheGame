def main_game(mytoken, gameId):
    global mynick
    import pygame
    import random
    import json
    import requests
    from pygame.sprite import Sprite

    from pygame.locals import (
        K_ESCAPE,
        KEYDOWN,
        QUIT,
    )

    colors = {1: (0, 100, 58, 1), 2: (216, 100, 58, 1), 3: (96, 100, 58, 1)} # 1 - Красный 2 - Синий 3 - Зеленый
    shapes = {1: "Circle", 2: "Rhombus", 3: "Wave"}
    inside = {1: "Empty", 2: "Fill", 3: "Striped"}

    class Card(Sprite):
        def __init__(self, color, count, fill, ids, shape):
            self.id = ids
            self.is_clicked = False
            self.info = str(color) + str(shape) + str(fill) + str(count)
            self.attribute = {"color": color, "shape": shape, "inside": fill, "count": count}

        def spawn(self, multy_x, multy_y):
            self.figure_1 = pygame.image.load("../png/" + shapes[self.attribute["shape"]] + "-" + inside[self.attribute["inside"]] + ".png").convert_alpha()
            self.figure_1 = pygame.transform.scale(self.figure_1, (self.figure_1.get_rect().width / 2.5,
                                                                   self.figure_1.get_rect().height / 2.5))

            color = pygame.Color(0)
            color.hsla = colors[self.attribute["color"]]
            self.figure_1 = changColor(self.figure_1, color)

            self.frame = pygame.image.load("../png/" + "Frame.png").convert_alpha()
            self.frame = pygame.transform.scale(self.frame, (self.frame.get_rect().width * 0.8,
                                                                   self.frame.get_rect().height * 0.8))


            self.chosen_frame = pygame.image.load("../png/" + "Chosen-Frame.png").convert_alpha()
            self.chosen_frame = pygame.transform.scale(self.chosen_frame, (self.chosen_frame.get_rect().width * 0.8,
                                                             self.chosen_frame.get_rect().height * 0.8))


            self.figure_2 = self.figure_3 = self.figure_1
            if self.attribute["count"] == 1:
                self.rect_1 = self.figure_1.get_rect(
                    center=(350 + 170 * multy_x, 182 + 225 * multy_y)
                )
            elif self.attribute["count"] == 2:
                self.rect_1 = self.figure_1.get_rect(
                    center=(350 + 170 * multy_x, 155 + 225 * multy_y)
                )
                self.rect_3 = self.figure_2.get_rect(
                    center=(350 + 170 * multy_x, 217 + 225 * multy_y)
                )
            elif self.attribute["count"] == 3:
                self.rect_1 = self.figure_1.get_rect(
                    center=(350 + 170 * multy_x, 135 + 225 * multy_y)
                )
                self.rect_3 = self.figure_2.get_rect(
                    center=(350 + 170 * multy_x, 194 + 225 * multy_y)
                )
                self.rect_4 = self.figure_3.get_rect(
                    center=(350 + 170 * multy_x, 250 + 225 * multy_y)
                )

            self.point1 = (250 + 170 * multy_x, 60 + 225 * multy_y)
            self.point2 = (440 + 170 * multy_x, 315 + 225 * multy_y)

            self.rect_5 = self.chosen_frame.get_rect(
                center=(350 + 170 * multy_x, 190 + 225 * multy_y)
            )
            self.rect_2 = self.frame.get_rect(
                center=(350 + 170 * multy_x, 190 + 225 * multy_y)
            )


    def changColor(image, color):
        colouredImage = pygame.Surface(image.get_size())
        colouredImage.fill(color)
        finalImage = image.copy()
        finalImage.blit(colouredImage, (0, 0), special_flags=pygame.BLEND_MULT)
        return finalImage

    def draw_cards(cards):
        for multy_y in range(3):
            for multy_x in range(int(len(cards) / 3)):
                cards[multy_y * int(len(cards) / 3) + multy_x].spawn(multy_x, multy_y)


    def get_field(token):
        cards = []
        uri = "http://84.201.155.174/set/field"
        param = {"accessToken": token, }
        while True:
            try:
                response = requests.post(uri, json=param)
                if (response.status_code == 200):
                    jsn = json.loads(response.text)
                    for att in jsn["cards"]:
                        cards.append(Card(att["color"], att["count"], att["fill"], att["id"], att["shape"]))
                    return cards
                else:
                    print("Произошла ошибка! Начальные карты не получены :(")
            except Exception:
                continue

    def check_answer(token, answer):
        uri = "http://84.201.155.174/set/pick"
        param = {"accessToken": token, "cards": [answer[0].id, answer[1].id, answer[2].id] }
        while True:
            try:
                response = requests.post(uri, json=param)
                if (response.status_code == 200):
                    jsn = json.loads(response.text)["isSet"]
                    return jsn
                else:
                    print("Произошла ошибка :(")
            except Exception:
                continue

    def find_set(cards): # Поиск сетов
        counts_set = 0  # Счетчик сетов
        found_sets = []  # Айди карт для сета # -------------
        for i in range(len(cards)):
            card1 = cards[i]
            for j in range(i+1, len(cards)):
                card2 = cards[j]
                for l in range(j+1, len(cards)):
                    card3 = cards[l]
                    fit_attribute = 0 # Счетчик подходящих свойств
                    for g in range(4):
                        buffer = set([card1.info[g], card2.info[g], card3.info[g]])
                        if len(buffer) == 1 or len(buffer) == 3:
                            fit_attribute += 1
                        else:
                            break
                    if fit_attribute == 4:
                        found_sets.append([card1.id, card2.id, card3.id]) # -------------
                        counts_set += 1
        return [counts_set, found_sets] # -------------

    def lack_cards(token, cards):
        if find_set(cards)[0] == 0:
            uri = "http://84.201.155.174/set/add"
            param = {"accessToken": token, }
            while True:
                try:
                    response = requests.post(uri, json=param)
                    if (response.status_code == 200):
                        jsn = json.loads(response.text)
                        if jsn["error"]:
                            continue
                        return jsn["success"]
                    else:
                        print("Произошла ошибка :(")
                except Exception:
                    continue

    def get_score(token):
        global mynick
        uri = "http://84.201.155.174/set/stats"
        param = {"accessToken": token, }
        while True:
            try:
                response = requests.post(uri, json=param)
                if (response.status_code == 200):
                    jsn = json.loads(response.text)
                    online_player = []
                    maximum = 0
                    for i, player in enumerate(jsn["stats"]):
                        nick = prenick[int(str(player["id"])[2])] + nicks[player["id"] % len(nicks)]
                        if mynick == nick:
                            label_player = sign_player.render("(Это вы) " + mynick + ": " + str(player["score"]),
                                                              1, (random.randint(1, 150), random.randint(1, 150), random.randint(1, 150)))
                        else:
                            label_player = sign_player.render(nick + ": " + str(player["score"]),
                                                              1, (random.randint(1, 150), random.randint(1, 150), random.randint(1, 150)))
                        online_player.append(label_player)
                        if player["score"] > maximum:
                            maximum = player["score"]
                            index = i
                            win_nick = nick
                    if mynick == "":
                        mynick = prenick[int(str(player["id"])[2])] + nicks[player["id"] % len(nicks)]
                        label_player = sign_player.render("(Это вы) " + mynick + ": " + str(player["score"]), 1,
                                                          (random.randint(1, 150), random.randint(1, 150), random.randint(1, 150)))
                        online_player[i] = label_player
                    if jsn["status"] == "ended":
                        online_player[index] = sign_player.render("Win: " + win_nick + ": " + maximum,
                                                                  1, (random.randint(1, 150), random.randint(1, 150), random.randint(1, 150)))
                        return [online_player, False]
                    return [online_player, True]
                else:
                    print("Произошла ошибка :(")
            except Exception:
                continue

    def leave_game_server(token, gameId):
        uri = "http://84.201.155.174/set/room/leave"
        param = {"accessToken": token, "gameId": gameId, }
        while True:
            try:
                response = requests.post(uri, json=param)
                if (response.status_code == 200):
                    jsn = json.loads(response.text)
                    return jsn["success"]
                else:
                    print("Произошла ошибка :(")
            except Exception:
                continue

    def update():
        cards = get_field(mytoken)
        lack_cards(mytoken, cards)
        draw_cards(cards)
        online_player = get_score(mytoken)[0]
        return [cards, online_player]

    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 800

    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.mixer.music.load("../sounds/Main-theme.mp3")
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms = 0)
    pygame.mixer.music.set_volume(0.001)
    Take = pygame.mixer.Sound("../sounds/Take.wav")
    Take.set_volume(0.2)
    win = pygame.mixer.Sound("../sounds/Win.wav")
    win.set_volume(0.1)
    lose = pygame.mixer.Sound("../sounds/Lose.wav")


    nicks = ["Meepo", "Magnus", "Tomato", "Miracle", "Axe", "Veno", "Paradox", "Abaddon", "Chaos", "Knight",
             "Doom", "Breaker", "Dragon", "Spirit", "Elder", "Titan", "Legion", "Mars", "Night", "Omni", "Sven",
             "Tide", "Hunter", "Tiny", "Tusk", "Lord", "King", "Arc", "Clinkz", "Drow", "Ember", "Void", "Hood",
             "Wink", "Luna", "Medusa", "Morph", "Phantom", "Shadow", "Spectre", "Templar", "Ancient", "Crystal",
             "Lich", "Oracle", "Pugna", "Rubick", "Silencer", "Storm", "Tinker", "Zeus", "Bane", "Chen", "Dark",
             "Seer", "Willow", 'Dazzle', 'Enigma', 'Wisp', 'Marci', 'Mirana', 'Nyx', 'Phoenix', 'Snapfire', 'Venge',
             "Visage", 'Wind', 'Winter']

    prenick = ["M.", "D.", "T.", "L.", "X.", "N.", "B.", "K.", "F.", "P."]

    font_path = "../fonts/Montserrat-Regular.ttf"
    sign_score = pygame.font.Font(font_path, 36)
    label_score = sign_score.render("Scores: ", 1, (0, 0, 0))
    sign_mistake = pygame.font.Font(font_path, 36)
    label_mistake = sign_mistake.render("Incorrect set!", 1, (255, 255, 255))
    sign_player = pygame.font.Font(font_path, 24)
    sign_count = pygame.font.Font(font_path, 24)

    mynick = ""
    answer = []
    cards, online_player = update()

    endgame = True
    running = True
    total = 0

    while running:
        total += 1
        screen.fill((255, 255, 255))
        if total == 210:
            for c in answer:
                c.is_clicked = False
            answer = []
            cards, online_player = update()
            total = 0

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                for card in cards:
                    if card.point1[0] < x < card.point2[0] and card.point1[1] < y < card.point2[1]:
                        Take.play()
                        if card.is_clicked == True:
                            card.is_clicked = False
                            answer.remove(card)
                        else:
                            card.is_clicked = True
                            answer.append(card)
                        break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        if len(answer) == 3:
            if check_answer(mytoken, answer):
                win.play()
                cards, online_player = update()
                label_mistake = sign_mistake.render("Сorrect set!", 1, (157, 199, 93))
            else:
                lose.play()
                label_mistake = sign_mistake.render("Incorrect set!", 1, (255, 0, 0))
            for c in answer:
                c.is_clicked = False

            answer = []
            online_player, endgame = get_score(mytoken)


        for card in cards:
            if card.is_clicked == True:
                screen.blit(card.frame, card.rect_2)
                screen.blit(card.chosen_frame, card.rect_5)
            else:
                screen.blit(card.chosen_frame, card.rect_5)
                screen.blit(card.frame, card.rect_2)

            screen.blit(card.figure_1, card.rect_1)
            if card.attribute["count"] >= 2:
                screen.blit(card.figure_2, card.rect_3)
            if card.attribute["count"] == 3:
                screen.blit(card.figure_3, card.rect_4)
        label_count = sign_mistake.render("Time update: " + str(7 - total//30), 1, (0, 0, 0))
        screen.blit(label_count, (610, 10))
        screen.blit(label_score, (10, 10))
        screen.blit(label_mistake, (320, 10))
        for i, p in enumerate(online_player):
            screen.blit(p, (10, 60 + 30 * i))

        if endgame == False:
            label_end = sign_count.render("Игра окончена!", 1, (0, 0, 0))
            screen.blit(label_end, (1000, 10))
            running = False
        pygame.display.flip()
        clock.tick(30)

    leave_game_server(mytoken, gameId)
    if endgame == True:
        pygame.mixer.music.stop()
        pygame.quit()
    else:
        end = True
        while end:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    end = False
                elif event.type == QUIT:
                    end = False
        pygame.mixer.music.stop()
        pygame.quit()

