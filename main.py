import csv, requests, json
from tkinter import *
from tkinter import ttk, messagebox
from textwrap import wrap

from PIL import ImageTk, Image
from params import params, texts, pathes, colors, errors
from game import main_game

class Main():

    def __init__(self, isresizable:bool=False):
        self.mainwindow = Tk()
        self.mainwindow.title(texts["window_name_account"])
        self.mainwindow.geometry("{}x{}".format(params["start_window_width"], params["start_window_height"]))
        self.mainwindow.minsize(params["start_window_width"], params["start_window_height"])
        self.mainwindow.iconbitmap(pathes["icon_main"])

        if not(isresizable): self.mainwindow.resizable(width=False, height=False)

        self.objects_on_screen = []
        self.login, self.password1, self.password2 = None, None, None

        self.window_account()
        self.mainwindow.mainloop()

    def plus_red_line(self, text:str):
        return texts["symbol_red_line"] + text

    def new_text_in_label(self, text:str, label:Label, window:Tk, mode:bool=True):
        window.update()
        if mode: label['text'] = text
        else: label['text'] += text
        window.update()

    def wrap_text(self, arr_text:str, label:Label, window):
        window.update()
        margin = params["rules_window_texts_margin"]*2
        arr_text = arr_text.split('\n')
        # new_arr = []
        new_arr = [""]*len(arr_text)

        # print("arr_text =", arr_text)

        for i,row in enumerate(arr_text):
            # print("{}) {}".format(i, row))
            self.new_text_in_label(row, label, window)

            average_char_width = label.winfo_width() / len(row)
            chars_per_line = int((window.winfo_width() - margin) / average_char_width)
            # print("{} / {} = {}".format(label.winfo_width(), len(row), average_char_width))
            # print("{} / {} = {}".format(window.winfo_width() - margin, average_char_width, chars_per_line))
            new_arr += ['\n'.join(wrap(row, chars_per_line)) + '\n' * 2]
            # while label.winfo_width() > window.winfo_width()-margin-extra_margin:
            #     new_arr[i] = '\n'.join(wrap(row, chars_per_line)) + '\n' * 2
            #     print(new_arr[i])
            #     self.new_text_in_label(new_arr[i], label, window)
            #     print("\t", chars_per_line, label.winfo_width(), window.winfo_width()-margin-extra_margin)
            #
            #     chars_per_line -= 1


        self.new_text_in_label("", label, window)
        for row in new_arr:
            self.new_text_in_label(row, label, window, False)

    def set_new_grid(self, columns:int=1, rows:int=1, columns_weights=[1], rows_weights=[1]):
        for i in range(11):
            self.mainwindow.columnconfigure(i, weight=(columns_weights[i] if i < columns else 0))
        for j in range(11):
            self.mainwindow.rowconfigure(j, weight=(rows_weights[j] if j < rows else 0))

    def set_player_status(self, status:bool=False):
        file_users = open(pathes["table_users"])
        reader = csv.DictReader(file_users)
        fieldnames = reader.fieldnames

        arr = [row for row in reader]
        file_users.close()

        file_users = open(pathes["table_users"], 'w')
        writer = csv.DictWriter(file_users, fieldnames=fieldnames)

        fieldnames_old = {}
        for elem in fieldnames: fieldnames_old[str(elem)] = str(elem)
        writer.writerow(fieldnames_old)

        for i, row in enumerate(arr):
            if row["nickname"] == self.login:
                arr[i]["status"] = str(status)
            writer.writerow(arr[i])

    def get_players_online(self):
        file_users = open(pathes["table_users"])
        reader = csv.DictReader(file_users)
        array = [row[params["name_column_nickname"]] for row in reader if row[params["name_column_status"]] == "True" and
                 row[params["name_column_nickname"]] != self.login]

        return array

    def window_login(self):
        global entry_nickname, entry_password

        self.destroy_object_on_screen()
        self.mainwindow.title(texts["window_name_login"])
        self.mainwindow.minsize(params["start_window_width"], params["start_window_height"])

        self.set_new_grid(1, 6, [1], [1]*6)

        text_nickname = Label(text=texts["text_nickname"],
                              font=params["font_tiny"])
        text_password = Label(text=texts["text_password"],
                              font=params["font_tiny"])

        entry_nickname = Entry(font=params["font_middle"],
                               width=params["entry_base_width"])
        entry_password = Entry(font=params["font_middle"],
                               width=params["entry_base_width"],
                               show=texts["symbol_password"])

        button_go_to_registration = Button(text=texts["button_go_to_registration"],
                              pady=5, padx=5,
                              font=params["font_minor"],
                              command=self.window_registration,
                              relief=FLAT)

        button_signin = Button(text=texts["button_signin"],
                               pady=5, padx=5,
                               font=params["font_main"],
                               command=self.check_signin,
                               background=colors["button_okay"],
                               activebackground=colors["button_okay_active"])

        text_nickname.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="S", pady=10)
        entry_nickname.grid(column=0, row=1, columnspan=2, rowspan=1, sticky="N", pady=10, ipady=5, ipadx=5)
        text_password.grid(column=0, row=2, columnspan=1, rowspan=1, sticky="S", pady=10)
        entry_password.grid(column=0, row=3, columnspan=2, rowspan=1, sticky="N", pady=10, ipady=5, ipadx=5)
        button_signin.grid(column=0, row=4, columnspan=1, rowspan=1, sticky="N", pady=10, padx=10)
        button_go_to_registration.grid(column=0, row=5, columnspan=1, rowspan=1, sticky="S", pady=10)

        self.objects_on_screen = [text_nickname, entry_password, text_password, entry_nickname, button_signin, button_go_to_registration]

    def window_registration(self):
        global entry_login, entry_first_password, entry_second_password
        self.destroy_object_on_screen()
        self.mainwindow.title(texts["window_name_registration"])
        self.mainwindow.minsize(params["start_window_width"], params["register_window_height"])

        self.set_new_grid(1, 8, [1], [1]*8)

        text_login = Label(text=texts["text_login"], font=params["font_tiny"])
        entry_login = Entry(font=params["font_middle"], width=params["entry_base_width"])

        text_first_password = Label(text=texts["text_first_password"], font=params["font_tiny"])
        entry_first_password = Entry(font=params["font_middle"], width=params["entry_base_width"], show=texts["symbol_password"])

        text_second_password = Label(text=texts["text_second_password"], font=params["font_tiny"])
        entry_second_password = Entry(font=params["font_middle"], width=params["entry_base_width"], show=texts["symbol_password"])

        button_register = Button(text=texts["button_register"],
                               pady=5, padx=5,
                               font=params["font_main"],
                               command=self.check_register,
                               background=colors["button_okay"],
                               activebackground=colors["button_okay_active"])
        button_go_to_login = Button(text=texts["button_go_to_login"],
                              pady=5, padx=5,
                              font=params["font_minor"],
                              command=self.window_login,
                              relief=FLAT)

        text_login.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="S", pady=10)
        entry_login.grid(column=0, row=1, columnspan=1, rowspan=1, sticky="N", pady=10, ipady=5, ipadx=5)
        text_first_password.grid(column=0, row=2, columnspan=1, rowspan=1, sticky="S", pady=10)
        entry_first_password.grid(column=0, row=3, columnspan=1, rowspan=1, sticky="N", pady=10, ipady=5, ipadx=5)
        text_second_password.grid(column=0, row=4, columnspan=1, rowspan=1, sticky="S", pady=10)
        entry_second_password.grid(column=0, row=5, columnspan=1, rowspan=1, sticky="N", pady=10, ipady=5, ipadx=5)

        button_register.grid(column=0, row=6, columnspan=1, rowspan=1, sticky="N", pady=10)
        button_go_to_login.grid(column=0, row=7, columnspan=1, rowspan=1, sticky="S", pady=10)

        self.objects_on_screen = [text_login, entry_login, text_first_password, entry_first_password, text_second_password,
                                  entry_second_password, button_register, button_go_to_login]

    def window_home(self):
        self.destroy_object_on_screen()
        self.mainwindow.title(texts["window_name_home"])
        self.mainwindow.minsize(params["home_window_width"], params["home_window_height"])

        self.set_new_grid(4, 5, [3,1,1,1], [1]*5)

        button_rules = Button(text=texts["button_rules"],
                                pady=5, padx=5,
                                font=params["font_minor"],
                                command=self.window_rules,
                                relief=FLAT)
        button_exit = Button(text=texts["button_exit"],
                             pady=5, padx=5,
                             font=params["font_minor"],
                             command=self.window_account,
                             relief=FLAT)

        text_choose_lobby = Label(text=self.plus_red_line(texts["text_choose_lobby"]), font=params["font_minor"],
                                      justify=LEFT)

        variable = StringVar(self.mainwindow)
        variable.set(texts["text_list_lobbies"])

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="white", background="white")

        self.list_lobbies = ttk.Combobox(self.mainwindow,
                                         textvariable=variable,
                                         state="readonly",
                                         font=params["font_large"],
                                         values=self.check_lobbies())

        button_join = Button(text=texts["button_join"], font=params["font_minor"], command=self.check_join_lobby)
        button_update = Button(text="Up", font=params["font_middle"], command=self.update_lobbies)

        text_create_lobby = Label(text=self.plus_red_line(texts["text_create_lobby"]), font=params["font_minor"],
                                      justify=LEFT)
        button_create_lobby = Button(text=texts["button_create_lobby"],
                                     pady=5, padx=5,
                                     font=params["font_minor"],
                                     command=self.check_create_lobby)

        button_rules.grid(column=2, row=0, columnspan=1, rowspan=1, sticky="E", pady=3)
        button_exit.grid(column=3, row=0, columnspan=1, rowspan=1, sticky="WE", pady=3)

        text_choose_lobby.grid(column=4, row=1, rowspan=1, sticky="NWE", pady=10)
        self.wrap_text(self.plus_red_line(texts["text_choose_lobby"]), text_choose_lobby, self.mainwindow)
        text_choose_lobby.grid(column=0, row=1, columnspan=4, rowspan=1, sticky="NWE", pady=10)

        self.list_lobbies.grid(column=0, row=2, columnspan=1, rowspan=1, sticky="NSWE", pady=10, padx=15)
        button_update.grid(column=1, row=2, columnspan=1, rowspan=1, sticky="NSWE", pady=10, padx=15)
        button_join.grid(column=2, row=2, columnspan=2, rowspan=1, sticky="NSWE", pady=10, padx=(20, 15))

        text_create_lobby.grid(column=4, row=3, rowspan=1, sticky="SWE", pady=10)
        self.wrap_text(self.plus_red_line(texts["text_create_lobby"]), text_create_lobby, self.mainwindow)
        text_create_lobby.grid(column=0, row=3, columnspan=4, rowspan=1, sticky="SWE", pady=10)

        button_create_lobby.grid(column=0, row=4, columnspan=4, rowspan=1, sticky="SWE", pady=10, padx=150)

        self.objects_on_screen = [button_rules, button_exit, text_choose_lobby, self.list_lobbies, text_create_lobby,
                                  button_create_lobby, button_join, button_update]

    def window_rules(self):
        rules = Rules()

    def window_lobby(self):
        self.destroy_object_on_screen()
        self.mainwindow.title(texts["window_name_lobby"].format(self.lobby))
        self.mainwindow.minsize(params["lobby_window_width"], params["lobby_window_height"])

        self.set_new_grid(4, 3, [1, 5, 1, 1], [1, 3, 1])

        button_rules = Button(text=texts["button_rules"],
                              pady=5, padx=5,
                              font=params["font_minor"],
                              command=self.window_rules,
                              relief=FLAT)
        button_exit = Button(text=texts["button_exit"],
                             pady=5, padx=5,
                             font=params["font_minor"],
                             command=self.check_leave_lobby,
                             relief=FLAT)

        players_frame = LabelFrame(self.mainwindow,
                                   text=texts["text_players_frame"],
                                   font=params["font_middle"])

        box_players = Listbox(players_frame,
                              selectmode=EXTENDED,
                              font=params['font_minor'])
        scroll_players = Scrollbar(players_frame,
                                   command=box_players.yview)
        box_players.config(yscrollcommand=scroll_players.set)

        self.insert_players(box_players)

        text_description_lobby = Label(
            text="\n".join(wrap(self.plus_red_line(texts["text_description_lobby"]).format(texts["button_start_game"]),40)),
            font=params["font_minor"], justify=LEFT)

        button_start_game = Button(text=texts["button_start_game"],
                             pady=5, padx=5,
                             font=params["font_minor"],
                             command=self.check_start_game)

        button_rules.grid(column=2, row=0, columnspan=1, rowspan=1, sticky="E", pady=3)
        button_exit.grid(column=3, row=0, columnspan=1, rowspan=1, sticky="WE", pady=3)
        players_frame.grid(column=0, row=1, columnspan=1, rowspan=2, sticky="NSWE", pady=20, padx=20)

        scroll_players.pack(side=RIGHT, padx=(0, 20))
        box_players.pack(side=RIGHT)

        text_description_lobby.grid(column=1, row=1, columnspan=3, rowspan=1, sticky="WE", pady=3)
        button_start_game.grid(column=1, row=2, columnspan=3, rowspan=1, sticky="WE", pady=3, padx=50)

        self.objects_on_screen = [button_rules, button_exit, players_frame, box_players, text_description_lobby,
                                  button_start_game]

    def create_error(self, message):
        messagebox.showerror("Ошибка", message)

    def check_signin(self):
        self.login = entry_nickname.get()
        self.password1 = entry_password.get()

        if self.login == "" or self.password1 == "":
            self.create_error(errors["empty_login_or_password"])
        else:
            text = "=== login_server "
            print(text + "="*(70-len(text)))
            accessToken = login_server(self.login, self.password1)
            print("answer:", accessToken)
            print("="*70)
            if accessToken.isdigit():
                text_errors = {"0": "non_exist_account", "1": "non_exist_password"}
                self.create_error(errors[text_errors[accessToken]])
            else:
                self.window_home()

    def check_register(self):
        global accessToken
        self.login = entry_login.get()
        self.password1 = entry_first_password.get()
        self.password2 = entry_second_password.get()
        flag = True
        if self.login == "" or self.password1 == "" or self.password2 == "":
            flag = False
            self.create_error(errors["empty_login_or_password"])


        if len(self.login) > params["const_max_length_login"]:
            flag = False
            self.create_error(errors["login_too_long"])

        elif self.password1 != self.password2:
            flag = False
            self.create_error(errors["not_equal_passwords"])

        if flag:
            text = "=== check_register "
            print(text + "=" * (70 - len(text)))
            accessToken = register_server(self.login, self.password1)
            print("answer:", accessToken)
            print("=" * 70)
            if accessToken.isdigit():
                texts_error = {"0": "login_does_exist"}
                self.create_error(errors[texts_error[accessToken]])
            else:
                self.window_home()

    def update_lobbies(self):
        arr = self.check_lobbies()
        self.list_lobbies.configure(values=arr)

    def check_lobbies(self):
        text = "=== check_lobbies "
        print(text + "=" * (70 - len(text)))
        answer = list_game_server(accessToken)
        print("answer:", answer)
        if str(answer).isdigit():
            texts_errors = {"0": "failed_get_lobbies", }
            self.create_error(errors[texts_errors[answer]])
            print("=" * 70)
            return []

        array = ["Лобби #"+str(elem['gameId']) for elem in answer]
        print("array:", array)
        print("=" * 70)
        return array

    def check_join_lobby(self):
        if self.list_lobbies.get() != "":
            text = "=== check_join_lobby "
            print(text + "=" * (70 - len(text)))
            self.lobby = int(self.list_lobbies.get()[self.list_lobbies.get().index("#") + 1:])
            answer = enter_game_server(accessToken, self.lobby)
            print("number lobby:", self.lobby)
            print("answer:", answer)
            print("="*70)
            if str(answer).isdigit():
                texts_errors = {"0": "failed_joining_lobby", "1": "player_in_game", "2": "game_finished"}
                self.create_error(errors[texts_errors[answer]].format(self.lobby))
            else:
                self.window_lobby()
        else:
            self.create_error(errors["no_name_lobby"])

    def check_create_lobby(self):
        text = "=== check_create_lobby "
        print(text + "=" * (70 - len(text)))
        answer = create_game_server(accessToken)
        print("answer:", answer)

        if str(answer)[0] == "e":
            print("=" * 70)
            texts_errors = {"e0": "failed_creating_lobby", "e1": "player_in_game",}
            self.create_error(errors[texts_errors[answer]])
        else:
            self.lobby = answer
            print("new lobby:", answer)
            print("=" * 70)
            self.window_lobby()

    def check_leave_lobby(self):
        text = "=== check_leave_lobby "
        print(text + "=" * (70 - len(text)))
        answer = leave_game_server(accessToken, self.lobby)
        print("answer:", answer)
        print("leave lobby:", self.lobby)
        print("=" * 70)
        if str(answer).isdigit() and str(answer) != '1':
            texts_errors = {"0": "failed_leaving_lobby", "1": "player_not_in_game"}
            self.create_error(errors[texts_errors[answer]])
        else:
            self.window_home()

    def insert_players(self, box:Listbox):
        text = "=== insert_players "
        print(text + "=" * (70 - len(text)))
        answer = get_score(accessToken)
        print("answer:", answer)
        print("leave lobby:", self.lobby)

        if str(answer).isdigit():
            print("=" * 70)
            texts_errors = {"0": "no_players_list",}
            self.create_error(errors[texts_errors[answer]])
        else:
            ids = [player['id'] for player in answer]
            for i,id in enumerate(ids):
                print("\t{}) id: {}".format(i,id))
                box.insert(END, "{}) {}".format(i+1, id))
                print("=" * 70)

    def check_start_game(self):
        main_game(accessToken, self.lobby)

    def window_account(self):
        global button_login, button_registration
        self.mainwindow.title(texts["window_name_account"])
        self.mainwindow.minsize(params["start_window_width"], params["start_window_height"])
        self.destroy_object_on_screen()

        self.set_new_grid(1, 2, [1], [1]*2)

        button_login = Button(text=texts["button_login"],
                              pady=5, padx=5,
                              font=params["font_main"],
                              command=self.window_login)
        button_registration = Button(text=texts["button_registration"],
                                     pady=5, padx=5,
                                     font=params["font_main"],
                                     command=self.window_registration)

        self.objects_on_screen = [button_login, button_registration]

        button_login.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="S", pady=10)
        button_registration.grid(column=0, row=1, columnspan=1, rowspan=1, sticky="N", pady=10)

        # mainwindow.update()
        # print(button_login.winfo_height())
        # print(mainwindow.winfo_height())

    def destroy_object_on_screen(self):
        # print(self.objects_on_screen)
        for i,elem in enumerate(self.objects_on_screen):
            elem.destroy()
        self.objects_on_screen = []

class Rules(Toplevel):
    def __init__(self, isresizable:bool=False):
        super().__init__()
        self.title(texts["window_name_rules"])
        self.geometry("{}x{}".format(params["rules_window_width"], params["rules_window_height"]))
        self.minsize(params["rules_window_width"], params["rules_window_height"])
        self.iconbitmap(pathes["icon_main"])

        if not(isresizable): self.resizable(width=False, height=False)

        self.tab_control()

        self.mainloop()

    def set_new_grid(self, columns:int=1, rows:int=1, columns_weights=[1], rows_weights=[1]):
        for i in range(11):
            self.columnconfigure(i, weight=(columns_weights[i] if i < columns else 0))
        for j in range(11):
            self.rowconfigure(j, weight=(rows_weights[j] if j < rows else 0))

    def new_text_in_label(self, text:str, label:Label, window:Tk, mode:bool=True):
        window.update()
        if mode: label['text'] = text
        else: label['text'] += text
        window.update()

    def wrap_text(self, arr_text:str, label:Label, window):
        window.update()
        arr_text = arr_text.split('\n')
        new_arr = []

        for i,row in enumerate(arr_text):
            new_arr += ['\n'.join(wrap(row, params["const_char_per_line"])) +
                        ('\n'*2 if row != arr_text[-1] else "")]

        self.new_text_in_label("", label, window)
        for row in new_arr:
            self.new_text_in_label(row, label, window, False)

    def tab_control(self):
        tabs = ttk.Notebook(self)
        tab1 = ttk.Frame(tabs)
        tab2 = ttk.Frame(tabs)
        tabs.add(tab1, text='Общие правила')
        tabs.add(tab2, text='Правила мультиплеера')

        self.tab1(tab1)
        self.tab2(tab2)

        tabs.pack(expand=1, fill="both")

    def tab1(self, tab:Frame):
        # self.set_new_grid(1, 6, [1], [1] * 6)

        label_p1 = Label(tab, text=texts["text_rules_p1"], font=params["font_minor"], justify=LEFT)

        self.img1 = ImageTk.PhotoImage(
            Image.open(pathes["example1"]).resize((params["const_width_example"], params["const_height_example"]),
                                                  Image.LANCZOS))
        self.example1 = Label(tab, image=self.img1)

        label_p2 = Label(tab, text=texts["text_rules_p2"], font=params["font_minor"], justify=LEFT)
        self.img2 = ImageTk.PhotoImage(
            Image.open(pathes["example2"]).resize((params["const_width_example"], params["const_height_example"]),
                                                  Image.LANCZOS))
        self.example2 = Label(tab, image=self.img2)
        label_p3 = Label(tab, text=texts["text_rules_p3"], font=params["font_minor"], justify=LEFT)
        self.img3 = ImageTk.PhotoImage(
            Image.open(pathes["example3"]).resize((params["const_width_example"], params["const_height_example"]),
                                                  Image.LANCZOS))
        self.example3 = Label(tab, image=self.img3)

        label_p1.grid(column=0, row=0, padx=params["rules_window_texts_margin"],
                      pady=params["rules_window_texts_margin"], sticky="W")
        self.wrap_text(texts["text_rules_p1"], label_p1, self)
        self.example1.grid(column=0, row=1, padx=params["rules_window_texts_margin"],
                           sticky="NW")
        label_p2.grid(column=0, row=2, padx=params["rules_window_texts_margin"],
                      pady=params["rules_window_texts_margin"], sticky="W")
        self.wrap_text(texts["text_rules_p2"], label_p2, self)
        self.example2.grid(column=0, row=3, padx=params["rules_window_texts_margin"],
                           sticky="NW")
        label_p3.grid(column=0, row=4, padx=params["rules_window_texts_margin"],
                      pady=params["rules_window_texts_margin"], sticky="W")
        self.wrap_text(texts["text_rules_p3"], label_p3, self)
        self.example3.grid(column=0, row=5, padx=params["rules_window_texts_margin"],
                           sticky="NW", pady=(0, params["rules_window_texts_margin"]))

    def tab2(self, tab:Frame):
        label_p4 = Label(tab, text=texts["text_rules_p4"], font=params["font_minor"], justify=LEFT)
        label_p4.grid(column=0, row=0, padx=params["rules_window_texts_margin"],
                           sticky="W", pady=params["rules_window_texts_margin"])
        self.wrap_text(texts["text_rules_p4"], label_p4, self)

def register_server(nickname, password):
    uri = "http://84.201.155.174/user/register"
    param = {"nickname": nickname, "password": password, }
    amount_requests = 0
    # errors_type = {"User already exist": "1", }
    error = "0"
    # 0 - дефолтная ошибка про User already exist
    while True:
        amount_requests += 1
        if amount_requests >= LIMIT_REQUESTS:
            return error
        try:
            response = requests.post(uri, json=param)
            if (response.status_code == 200):
                jsn = json.loads(response.text)
                print(jsn)
                if jsn['error']:
                    continue
                return jsn["accessToken"]
            else:
                print("Произошла ошибка :(")
        except Exception:
            continue

def login_server(nickname, password):
    uri = "http://84.201.155.174/user/login"
    param = {"nickname": nickname, "password": password, }
    amount_requests = 0

    errors_type = {"Wrong password": "1",}
    error = "0"
    # 0 - дефолтная ошибка про is not registered
    # 1 - Wrong password
    while True:
        amount_requests += 1
        if amount_requests >= LIMIT_REQUESTS:
            return error
        try:
            response = requests.post(uri, json=param)
            if (response.status_code == 200):
                jsn = json.loads(response.text)
                print(jsn)
                if jsn["error"]:
                    if "is not registered" not in jsn["error"]["message"]:
                        # error = errors_type[jsn["error"]["message"]]
                        return errors_type[jsn["error"]["message"]]

                    else: continue
                return jsn["accessToken"]
            else:
                print("Произошла ошибка :(")
        except Exception:
            continue

def create_game_server(token):
    uri = "http://84.201.155.174/set/room/create"
    param = {"accessToken": token, }
    amount_requests = 0
    errors_type = {"You are in a game already": "e1", }
    error = "e0"
    # e0 - дефолтная ошибка про Invalid token
    # e1 - You are in a game already
    while True:
        amount_requests += 1
        if amount_requests >= LIMIT_REQUESTS:
            return error
        try:
            response = requests.post(uri, json=param)
            if (response.status_code == 200):
                jsn = json.loads(response.text)
                print(jsn)
                if jsn['error']:
                    if "Invalid token" not in jsn['error']['message']:
                        # error = errors_type[jsn['error']['message']]
                        return errors_type[jsn['error']['message']]
                return jsn["gameId"]
            else:
                print("Произошла ошибка :(")
        except Exception:
            continue

def list_game_server(token):
    uri = "http://84.201.155.174/set/room/list"
    param = {"accessToken": token, }
    amount_requests = 0
    errors_type = {"You are in a game already": "1", }
    error = "0"
    # 0 - дефолтная ошибка про Invalid token
    # 1 - You are in a game already
    while True:
        amount_requests += 1
        if amount_requests >= LIMIT_REQUESTS:
            return error
        try:
            response = requests.post(uri, json=param)
            if (response.status_code == 200):
                jsn = json.loads(response.text)
                print(jsn)
                if jsn["error"]:
                    if 'Invalid token' not in jsn["error"]["message"]:
                        # error = errors_type[jsn["error"]["message"]]
                        return errors_type[jsn["error"]["message"]]
                    continue
                return jsn["games"]
            else:
                print("Произошла ошибка :(")
        except Exception:
            continue

def enter_game_server(token, gameId):
    uri = "http://84.201.155.174/set/room/enter"
    param = {"accessToken": token, "gameId": gameId, }
    amount_requests = 0
    errors_type = {"You are in a game already": "1", "Game finished": "2"}
    error = "0"
    # 0 - дефолтная ошибка про Invalid token
    # 1 - You are in a game already
    # 2 - Game finished
    while True:
        amount_requests += 1
        if amount_requests >= LIMIT_REQUESTS:
            return error
        try:
            response = requests.post(uri, json=param)
            if (response.status_code == 200):
                jsn = json.loads(response.text)
                print(jsn)
                if jsn["error"]:
                    if "Invalid token" not in jsn['error']['message']:
                        # error = errors_type[jsn['error']['message']]
                        return errors_type[jsn['error']['message']]
                    continue
                return jsn["success"]
            else:
                print("Произошла ошибка :(")
        except Exception:
            continue

def leave_game_server(token, gameId):
    uri = "http://84.201.155.174/set/room/leave"
    param = {"accessToken": token, "gameId": gameId, }
    amount_requests = 0
    errors_type = {"You are not in a game": "1", }
    error = "0"
    # 0 - дефолтная ошибка про Invalid token
    # 1 - You are not in a game
    while True:
        amount_requests += 1
        if amount_requests >= LIMIT_REQUESTS:
            return error
        try:
            response = requests.post(uri, json=param)
            if (response.status_code == 200):
                jsn = json.loads(response.text)
                print(jsn)
                if jsn['error']:
                    if "Invalid token" not in jsn['error']['message']:
                        # error = errors_type[jsn['error']['message']]
                        return errors_type[jsn['error']['message']]
                if jsn["success"]:
                    return True
            else:
                print("Произошла ошибка :(")
        except Exception:
            continue

def get_score(token):
    uri = "http://84.201.155.174/set/stats"
    param = {"accessToken": token, }
    amount_requests = 0
    errors_type = {"You are not in a game  ": "1", }
    error = "0"
    # 0 - дефолтная ошибка про Invalid token
    # 1 - You are not in a game
    while True:
        amount_requests += 1
        if amount_requests >= LIMIT_REQUESTS:
            return error
        try:
            response = requests.post(uri, json=param)
            if (response.status_code == 200):
                jsn = json.loads(response.text)
                print(jsn)
                if jsn['error']:
                    if 'Invalid token' not in jsn['error']['message']:
                        # error = errors_type[jsn['error']['message']]
                        return errors_type[jsn['error']['message']]
                else:
                    return jsn['stats']
            else:
                print("Произошла ошибка :(")
        except Exception:
            continue

LIMIT_REQUESTS = 20
accessToken = None

if __name__ == "__main__":
    main = Main(False)
    main.check_leave_lobby()