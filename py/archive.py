import time, csv, pygame, tkinter
from csv import writer
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import ttk, messagebox
from textwrap import wrap

from PIL import ImageTk, Image
from params import params, texts, pathes, colors, errors


def window_home(self):
    self.destroy_object_on_screen()
    self.mainwindow.title(texts["window_name_home"])
    self.mainwindow.minsize(params["home_window_width"], params["home_window_height"])

    self.set_new_grid(3, 4, [3, 1, 1], [1, 1, 6, 1])

    button_rules = Button(text=texts["button_rules"],
                          pady=5, padx=5,
                          font=params["font_minor"],
                          command=self.window_rules,
                          relief=FLAT)
    # image_exit = ImageTk.PhotoImage(file="../png/png-exit.png")
    # button_exit = Button(image=image_exit, command=lambda: print("click"))
    button_exit = Button(text=texts["button_text"],
                         pady=5, padx=5,
                         font=params["font_minor"],
                         command=self.window_account,
                         relief=FLAT)
    text_choose_player = Label(text=texts["text_choose_player"], font=params["font_main"])
    text_description_home = Label(text=self.plus_red_line(texts["text_description_home"]), font=params["font_minor"],
                                  justify=LEFT)

    variable = StringVar(self.mainwindow)
    variable.set(texts["text_list_players_online"])

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox", fieldbackground="white", background="white")

    list_players_online = ttk.Combobox(self.mainwindow, textvariable=variable, state="readonly",
                                       font=params["font_large"], values=self.get_players_online())

    button_invite = Button(text=texts["button_invite"], font=params["font_minor"], height=1)

    button_rules.grid(column=2, row=0, columnspan=1, rowspan=1, sticky="E", pady=3)
    button_exit.grid(column=3, row=0, columnspan=1, rowspan=1, sticky="WE", pady=3)
    text_choose_player.grid(column=0, row=1, columnspan=4, rowspan=1, sticky="NWE", pady=10)

    text_description_home.grid(column=3, row=2, rowspan=1, sticky="SWE", pady=10)
    self.wrap_text(self.plus_red_line(texts["text_description_home"]), text_description_home, self.mainwindow)
    text_description_home.grid(column=0, row=2, columnspan=4, rowspan=1, sticky="SWE", pady=10)

    list_players_online.grid(column=0, row=3, columnspan=1, rowspan=1, sticky="NSWE", pady=30, padx=30)
    button_invite.grid(column=2, row=3, columnspan=2, rowspan=1, sticky="NSWE", pady=30, padx=5)

    self.objects_on_screen = [button_rules, button_exit, text_choose_player, list_players_online, button_invite,
                              text_description_home]