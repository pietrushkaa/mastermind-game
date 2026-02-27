from kivy.config import Config

# Disabling fullscreen and setting fixed window sizes
Config.set("graphics", "fullscreen", "0")
Config.set("graphics", "width", "1200")
Config.set("graphics", "height", "1000")
Config.set("graphics", "resizable", "0")

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.graphics import Line
from sedzia import sprawdz
import random

# Global variables
spis_zasad = """
Game rules:
1. Below, enter the length of the code you want to guess and the number of colors.
2. You have 12 turns to guess the color code. Colors can repeat.
3. To enter the code, click a color, then click a slot in the row corresponding to the given turn.
4. After choosing all colors, click 'check'. If the code is incorrect,
the right side will show how many right colors are in the right place, and how many right colors are in the wrong place.
Good luck!
"""
tekst_legendy = """
Legend:
x | y
x - number of pegs of the right color and in the right place
y - number of pegs of the right color, but in the wrong place
"""
lista_kolorow = [
    "#00FFFF",
    "#0000FF",
    "#FF00FF",
    "#008000",
    "#FF0000",
    "#800080",
    "#FFFF00",
    "#008080",
    "#964b00",
    "#a7ff6a",
]  # list of colors available to use in the game in Hex code
liczba_kolorow = 0
dlugosc_sekwencji = 0
aktualny_kolor = None  # color recently chosen by the player during the game
zapytanie = []  # list encoding a single guess of the player
odpowiedz = []  # list encoding the hidden sequence
tura = 0  # current game turn, indexed from 0


class OknoGry(FloatLayout):
    def __init__(self, **kwargs):
        """
        Initializer of the class responsible for the main game window
        Creates surrender and check sequence buttons,
        labels, and the graphical layout based on FloatLayout
        """
        global tekst_legendy
        # calling the initializer of the parent class - FloatLayout
        super().__init__(**kwargs)
        Window.clearcolor = get_color_from_hex("#585858")
        self.spacing = 100

        # adding the surrender button
        self.poddaj_sie = Button(
            text="GIVE UP",
            font_size=18,
            size_hint=(0.12, 0.09),
            pos_hint={"top": 0.97, "x": 0.03},
            background_normal="",
            background_color=get_color_from_hex("#282828"),
            on_press=self.okienko_przegranej,
        )
        self.add_widget(self.poddaj_sie)

        # adding the check button
        self.sprawdz = Button(
            text="CHECK!",
            font_size=18,
            size_hint=(0.12, 0.09),
            pos_hint={"right": 0.97, "center_y": 0.5},
            background_normal="",
            background_color=get_color_from_hex("#282828"),
            on_press=self.sprawdzaj_zapytanie,
        )
        self.add_widget(self.sprawdz)

        # adding "Mastermind" label and legend
        self.mastermind_napis = Label(
            text="MASTERMIND",
            pos_hint={"center_x": 0.5, "top": 1},
            size_hint=(None, None),
            font_size=34,
        )
        self.add_widget(self.mastermind_napis)
        self.legenda = Label(
            text=tekst_legendy,
            pos_hint={"x": 0.84, "top": 0.91},
            size_hint=(None, None),
            text_size=(210, None),
            font_size=12,
            color=get_color_from_hex("#080303"),
            halign="right",
        )
        self.add_widget(self.legenda)

    def wybierz_kolor(self, instance):
        """
        Changes the global variable aktualny_kolor to the color of the just clicked color button
        and outlines the currently active color button, while removing the outline from the previous active one
        """
        global aktualny_kolor
        # removing the previous outline
        if aktualny_kolor != None:
            self.kolory.children[liczba_kolorow - aktualny_kolor].canvas.before.clear()
        # creating an outline on the current color button
        with instance.canvas.before:
            Line(
                rectangle=(instance.x, instance.y, instance.width, instance.height),
                width=3,
            )
        aktualny_kolor = liczba_kolorow - self.kolory.children.index(instance)

    def zmien_kolor(self, instance):
        """
        Changes the color of a given slot on the board to the current color
        and updates the global list zapytanie at the
        index of this slot to the current color
        """
        global aktualny_kolor, zapytanie
        if aktualny_kolor != None:
            instance.background_color = get_color_from_hex(
                lista_kolorow[aktualny_kolor - 1]
            )
            id_pola = self.plansza.children.index(instance)
            id_pola = dlugosc_sekwencji - id_pola % (dlugosc_sekwencji + 1)
            zapytanie[id_pola] = aktualny_kolor

    def wylacz_gre(self, instance=None):
        """Closes the entire application"""
        App.get_running_app().stop()

    def okienko_przegranej(self, instance=None):
        """
        Opens a popup window informing about the loss
        and revealing the hidden sequence
        """
        global odpowiedz, liczba_kolorow
        # creating a graphical representation of the hidden sequence
        odp_graficznie = GridLayout(
            cols=dlugosc_sekwencji,
            padding=30,
            spacing=5,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        for kolor in odpowiedz:
            odp_graficznie.add_widget(
                Button(
                    background_normal="",
                    background_color=get_color_from_hex(lista_kolorow[kolor - 1]),
                )
            )
        # creating the window's graphical layout
        layout_koniec = BoxLayout(orientation="vertical", spacing=50, padding=20)
        layout_koniec.add_widget(
            Label(text="Unfortunately, you lost! The correct sequence is:", font_size=17)
        )
        layout_koniec.add_widget(odp_graficznie)
        layout_koniec.add_widget(Button(text="Close game", on_press=self.wylacz_gre))
        przegrana = Popup(  # loss popup
            title="Game Over!",
            content=layout_koniec,
            size_hint=(None, None),
            size=(500, 300),
            auto_dismiss=False,
        )
        przegrana.open()

    def sprawdzaj_zapytanie(self, instance):
        """
        Checks the guess, displays a win or loss message
        Updates the tura variable and activates the next row on the board
        """
        global tura, zapytanie, odpowiedz, liczba_kolorow
        # case when the guess is not completely filled
        if not all(isinstance(x, int) for x in zapytanie):
            niepelne_zapytanie = Popup(
                title="Incomplete guess",
                content=Label(
                    text="To check the guess, fill in all empty slots first!",
                    font_size=17,
                ),
                size_hint=(None, None),
                size=(600, 200),
                auto_dismiss=True,
            )
            niepelne_zapytanie.open()
            return
        # checking the guess using the function from the sedzia.py module
        wlasciwe_miejsca, wlasciwe_kolory = sprawdz(
            liczba_kolorow, odpowiedz, zapytanie
        )
        # case of player's victory
        if wlasciwe_miejsca == len(odpowiedz):
            tekst_wygranej = (
                "Congratulations! You successfully guessed the sequence!\n"
                + "Sequence guessed in "
                + str(tura + 1)
                + " turns.\n"
                + "The game will close automatically."
            )
            wygrana = Popup(
                title="Victory!",
                content=Label(text=tekst_wygranej, font_size=17),
                size_hint=(None, None),
                size=(600, 200),
                auto_dismiss=False,
            )
            wygrana.open()
            Clock.schedule_once(self.wylacz_gre, 4)
            return
        # case of player's loss due to playing the last turn
        if tura == 11:
            self.okienko_przegranej()
            return
        # case when the guess was incorrect, but the game is not lost
        for i in range(
            1, dlugosc_sekwencji + 1
        ):  # disabling active buttons in the row of the previous turn
            self.plansza.children[(dlugosc_sekwencji + 1) * tura + i].disabled = True
        self.plansza.children[(dlugosc_sekwencji + 1) * tura].text = (
            str(wlasciwe_miejsca) + " | " + str(wlasciwe_kolory)
        )
        tura += 1
        for i in range(
            1, dlugosc_sekwencji + 1
        ):  # enabling active buttons in the row of the current turn
            self.plansza.children[(dlugosc_sekwencji + 1) * tura + i].disabled = False
        zapytanie = [None for i in range(dlugosc_sekwencji)]

    def stworz_kod(self):
        """
        Updates global variables:
        zapytanie - with a list of the sequence length filled with None
        odpowiedz - with a randomly chosen hidden sequence from available colors
        """
        global zapytanie, odpowiedz
        zapytanie = [None for i in range(dlugosc_sekwencji)]
        odpowiedz = random.choices(range(1, liczba_kolorow + 1), k=dlugosc_sekwencji)

    def dodaj_plansze(self):
        """
        Adds color and board buttons to the main game window
        """
        # adding the game board
        global tura, lista_kolorow
        self.plansza = GridLayout(
            cols=dlugosc_sekwencji + 1,
            padding=30,
            spacing=5,
            size_hint=(None, None),
            size=(700, 800),
            pos_hint={"center_x": 0.5, "center_y": 0.53},
        )
        for i in range(12):
            for j in range(dlugosc_sekwencji):
                pole = Button(
                    background_normal="",
                    background_color=get_color_from_hex("#282828"),
                    disabled=True if i != 11 else False,
                    on_press=self.zmien_kolor,
                )
                self.plansza.add_widget(pole)
            self.plansza.add_widget(
                Label(text="", font_size=23, halign="left", size_hint_x=None, width=80)
            )
        self.add_widget(self.plansza)

        # adding color buttons
        self.kolory = BoxLayout(
            orientation="horizontal",
            spacing=15,
            padding=10,
            size_hint=(1, 0.13),
            pos_hint={"y": 0},
        )
        for i in range(liczba_kolorow):
            przycisk = Button(
                background_normal="",
                background_color=get_color_from_hex(lista_kolorow[i]),
                on_press=self.wybierz_kolor,
            )
            self.kolory.add_widget(przycisk)
        self.add_widget(self.kolory)


class OknoStartowe(Popup):
    def __init__(self, okno_glowne, **kwargs):
        """
        Initializer of the class responsible for the start window of the game
        Creates labels: title and rules list, text fields for
        entering the number of colors and sequence length,
        start button, and the graphical layout based on BoxLayout
        """
        # calling the initializer of the parent class - Popup
        super().__init__(**kwargs)
        self.okno_glowne = okno_glowne
        layout_start = BoxLayout(orientation="vertical", spacing=30, padding=90)

        # adding the game title
        tytul = Label(
            text="Play Mastermind!", font_size=50, halign="center", bold=True
        )
        layout_start.add_widget(tytul)

        # adding the game rules list
        reguly = Label(
            text=spis_zasad,
            font_size=17,
            line_height=1.3,
            halign="center",
            text_size=(600, None),
            size_hint=(None, None),
            height=500,
            pos_hint={"center_x": 0.5, "top": 1},
        )
        layout_start.add_widget(reguly)

        # adding the field for entering the number of colors
        self.ile_kolorow = TextInput(
            size_hint=(0.1, None),
            height=30,
            pos_hint={"center_x": 0.5, "top": 1},
        )
        layout_start.add_widget(
            Label(text="Enter the number of colors (from 2 to 10):", font_size=17)
        )
        layout_start.add_widget(self.ile_kolorow)

        # adding the field for entering the sequence length
        self.jaka_dlugosc = TextInput(
            size_hint=(0.1, None),
            height=30,
            pos_hint={"center_x": 0.5, "top": 1},
        )
        layout_start.add_widget(
            Label(text="Enter the sequence length (from 1 to 10):", font_size=17)
        )
        layout_start.add_widget(self.jaka_dlugosc)

        # adding the start button
        przycisk_start = Button(
            text="START",
            font_size=17,
            size_hint=(None, None),
            size=(250, 50),
            pos_hint={"center_x": 0.5},
            on_press=self.przechwyc_tekst,
        )
        layout_start.add_widget(przycisk_start)

        self.title = "Start screen"
        self.content = layout_start
        self.auto_dismiss = False

    def przechwyc_tekst(self, instance):
        """
        Fills the global variables liczba_kolorow and dlugosc_sekwencji
        with the text entered in the text fields
        Creates the board and color buttons in the main window via appropriate functions from the OknoGry class
        and closes the start window
        If a field is empty or the data is not a number,
        it triggers an error popup
        """
        global liczba_kolorow, dlugosc_sekwencji
        k = self.ile_kolorow.text
        dl = self.jaka_dlugosc.text
        # creating the error popup
        blad = Popup(
            title="Error!",
            content=Label(
                text="Enter valid values, which are numbers from the given range!",
                font_size=17,
            ),
            size_hint=(None, None),
            size=(630, 250),
            auto_dismiss=True,
        )
        # attempting to create the board and color buttons,
        # in case of incorrect data, opening the error popup
        try:
            liczba_kolorow = int(k)
            dlugosc_sekwencji = int(dl)
            if 10 >= int(k) > 1 and 10 >= int(dl) > 0:
                self.okno_glowne.dodaj_plansze()
                self.okno_glowne.stworz_kod()
                self.dismiss()
            else:
                blad.open()
        except:
            blad.open()


class Gra(App):
    def build(self):
        """
        Creates and returns the graphical interface of the main game window
        Opens the start window right after opening the application
        """
        self.okno_glowne = OknoGry()
        self.okno_startowe = OknoStartowe(okno_glowne=self.okno_glowne)
        Clock.schedule_once(self.otworz_okno_startowe, 0.1)
        return self.okno_glowne

    def otworz_okno_startowe(self, instance):
        """Opens the start window of the game"""
        self.okno_startowe.open()


if __name__ == "__main__":
    Gra().run()