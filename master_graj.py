from kivy.config import Config

# Wyłączenie pełnego ekranu i ustawienie stałych rozmiarów okna
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

# Zmienne globalne
spis_zasad = """
Zasady gry:
1. Poniżej wpisz długość szyfru, jaki chcesz zgadywać i liczbę kolorów.
2. Masz 12 tur, żeby odgadnąć szyfr złożony z kolorów. Kolory mogą się powtarzać.
3. W celu wpisania szyfru, kliknij w kolor, a następnie w pole w rzędzie odpowiadającej danej turze.
4. Po wybraniu wszystkich kolorów kliknij 'sprawdź'. Jeśli szyfr nie jest poprawny,
po prawej pokaże się, ile jest właściwych kolorów na właściwym miejscu, a ile właściwych kolorów na niewłaściwym miejscu.
Powodzenia!
"""
tekst_legendy = """
Legenda:
x | y
x - liczba pionków o właściwym kolorze i na właściwym miejscu
y - liczba pionków o właściwym kolorze, ale na niewłaściwym miejscu
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
]  # lista możliwych do użycia w grze kolorów w kodzie Hex
liczba_kolorow = 0
dlugosc_sekwencji = 0
aktualny_kolor = None  # kolor wybrany ostatnio przez gracza podczas rozgrywki
zapytanie = []  # lista kodująca pojedyncze zapytanie gracza
odpowiedz = []  # lista kodująca sekwencję ukrytą
tura = 0  # aktualna tura gry, indeksowana od 0


class OknoGry(FloatLayout):
    def __init__(self, **kwargs):
        """
        Inicjalizator klasy odpowiadającej za główne okno gry
        Tworzy przyciski poddania i sprawdzania sekwencji,
        napisy i układ graficzny bazujący na FloatLayout
        """
        global tekst_legendy
        # wywołanie inicjalizatora klasy nadrzędnej - FloatLayout
        super().__init__(**kwargs)
        Window.clearcolor = get_color_from_hex("#585858")
        self.spacing = 100

        # dodanie przycisku poddania się
        self.poddaj_sie = Button(
            text="PODDAJ SIĘ",
            font_size=18,
            size_hint=(0.12, 0.09),
            pos_hint={"top": 0.97, "x": 0.03},
            background_normal="",
            background_color=get_color_from_hex("#282828"),
            on_press=self.okienko_przegranej,
        )
        self.add_widget(self.poddaj_sie)

        # dodanie przycisku sprawdzania
        self.sprawdz = Button(
            text="SPRAWDŹ!",
            font_size=18,
            size_hint=(0.12, 0.09),
            pos_hint={"right": 0.97, "center_y": 0.5},
            background_normal="",
            background_color=get_color_from_hex("#282828"),
            on_press=self.sprawdzaj_zapytanie,
        )
        self.add_widget(self.sprawdz)

        # dodanie napisów "Mastermind" i legendy
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
        Zmienio zmienną globalną aktualny_kolor na kolor właśnie klkniętego przycisku koloru
        i otacza ramką obecnie aktywny przycisk koloru, jednocześnie usuwając ramkę z poprzedniego aktywnego
        """
        global aktualny_kolor
        # usuwanie poprzedniej ramki
        if aktualny_kolor != None:
            self.kolory.children[liczba_kolorow - aktualny_kolor].canvas.before.clear()
        # tworzenie ramki na aktualnym przycisku koloru
        with instance.canvas.before:
            Line(
                rectangle=(instance.x, instance.y, instance.width, instance.height),
                width=3,
            )
        aktualny_kolor = liczba_kolorow - self.kolory.children.index(instance)

    def zmien_kolor(self, instance):
        """
        Zmienia kolor danego pola na planszy na aktualny kolor
        i aktualizuje listę globalną zapytanie pod
        numerem tego pola na aktualny kolor
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
        """Wyłącza całą aplikację"""
        App.get_running_app().stop()

    def okienko_przegranej(self, instance=None):
        """
        Otwiera okienko pop_up informujące o przegranej
        i ujawniające sekwencję ukrytą
        """
        global odpowiedz, liczba_kolorow
        # stworzenie graficznej reprezentacji sekwencji ukrytej
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
        # tworzenie układu graficznego okienka
        layout_koniec = BoxLayout(orientation="vertical", spacing=50, padding=20)
        layout_koniec.add_widget(
            Label(text="Niestety, przegrałeś! Prawidłowa sekwencja to:", font_size=17)
        )
        layout_koniec.add_widget(odp_graficznie)
        layout_koniec.add_widget(Button(text="Wyłącz grę", on_press=self.wylacz_gre))
        przegrana = Popup(  # okienko przegranej
            title="Przegrana!",
            content=layout_koniec,
            size_hint=(None, None),
            size=(500, 300),
            auto_dismiss=False,
        )
        przegrana.open()

    def sprawdzaj_zapytanie(self, instance):
        """
        Sprawdza zapytanie, wyświetla komunikat o wygranej lub przegranej
        Aktualizuje zmienną tura i aktywuje kolejny rząd na planszy
        """
        global tura, zapytanie, odpowiedz, liczba_kolorow
        # przypadek, gdy zapytanie nie jest całkowicie zapełnione
        if not all(isinstance(x, int) for x in zapytanie):
            niepelne_zapytanie = Popup(
                title="Niepełne zapytanie",
                content=Label(
                    text="Żeby sprawdzić zapytanie, wypełnij najpierw wszystkie puste pola!",
                    font_size=17,
                ),
                size_hint=(None, None),
                size=(600, 200),
                auto_dismiss=True,
            )
            niepelne_zapytanie.open()
            return
        # sprawdzanie zapytania przy użyciu funkcji z modułu sedzia.py
        wlasciwe_miejsca, wlasciwe_kolory = sprawdz(
            liczba_kolorow, odpowiedz, zapytanie
        )
        # przypadek wygranej gracza
        if wlasciwe_miejsca == len(odpowiedz):
            tekst_wygranej = (
                "Brawo! Udało ci się odgadnąć sekwencję!\n"
                + "Sekwencja odgadnięta w "
                + str(tura + 1)
                + " turach.\n"
                + "Gra zamknie się automatycznie."
            )
            wygrana = Popup(
                title="Wygrana!",
                content=Label(text=tekst_wygranej, font_size=17),
                size_hint=(None, None),
                size=(600, 200),
                auto_dismiss=False,
            )
            wygrana.open()
            Clock.schedule_once(self.wylacz_gre, 4)
            return
        # przypadek przegranej gracza z powodu rozegrania ostatniej tury
        if tura == 11:
            self.okienko_przegranej()
            return
        # przypadek, gdy zapytanie nie było prawidłowe, ale nie nastąpiła przegrana
        for i in range(
            1, dlugosc_sekwencji + 1
        ):  # wyłączenie przycisków aktywnych w rzędzie o numerze poprzedniej tury
            self.plansza.children[(dlugosc_sekwencji + 1) * tura + i].disabled = True
        self.plansza.children[(dlugosc_sekwencji + 1) * tura].text = (
            str(wlasciwe_miejsca) + " | " + str(wlasciwe_kolory)
        )
        tura += 1
        for i in range(
            1, dlugosc_sekwencji + 1
        ):  # włączenie przycisków aktywnych w rzędzie o numerze teraźniejsze tury
            self.plansza.children[(dlugosc_sekwencji + 1) * tura + i].disabled = False
        zapytanie = [None for i in range(dlugosc_sekwencji)]

    def stworz_kod(self):
        """
        Aktualizuje zmienne globalne:
        zapytanie - listą o długości sekwencji wypełnioną None
        odpowiedz - losowo wybraną spośród dostępnych kolorów sekwencją ukrytą
        """
        global zapytanie, odpowiedz
        zapytanie = [None for i in range(dlugosc_sekwencji)]
        odpowiedz = random.choices(range(1, liczba_kolorow + 1), k=dlugosc_sekwencji)

    def dodaj_plansze(self):
        """
        Dodaje przyciski kolorów i planszy do głównego okna gry
        """
        # dodanie planszy do gry
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

        # dodanie przycisków kolorów
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
        Inicjalizator klasy odpowiadającej za okno startowe gry
        Tworzy napisy: tytuł i spis zasad, pola tekstowe do
        wpisywania liczby kolorów i długości sekwencji
        przycisk startu i układ graficzny bazujący na BoxLayout
        """
        # wywołanie inicjalizatora klasy nadrzędnej - Popup
        super().__init__(**kwargs)
        self.okno_glowne = okno_glowne
        layout_start = BoxLayout(orientation="vertical", spacing=30, padding=90)

        # dodanie tytułu gry
        tytul = Label(
            text="Zagraj w Mastermind!", font_size=50, halign="center", bold=True
        )
        layout_start.add_widget(tytul)

        # dodanie spisu zasad gry
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

        # dodanie pola do wpisywania liczby kolorów
        self.ile_kolorow = TextInput(
            size_hint=(0.1, None),
            height=30,
            pos_hint={"center_x": 0.5, "top": 1},
        )
        layout_start.add_widget(
            Label(text="Wpisz liczbę kolorów (od 2 do 10):", font_size=17)
        )
        layout_start.add_widget(self.ile_kolorow)

        # dodanie pola do wpisywania długości sekwencji
        self.jaka_dlugosc = TextInput(
            size_hint=(0.1, None),
            height=30,
            pos_hint={"center_x": 0.5, "top": 1},
        )
        layout_start.add_widget(
            Label(text="Wpisz długość sekwencji (od 1 do 10):", font_size=17)
        )
        layout_start.add_widget(self.jaka_dlugosc)

        # dodanie przycisku startowego
        przycisk_start = Button(
            text="START",
            font_size=17,
            size_hint=(None, None),
            size=(250, 50),
            pos_hint={"center_x": 0.5},
            on_press=self.przechwyc_tekst,
        )
        layout_start.add_widget(przycisk_start)

        self.title = "Ekran startowy"
        self.content = layout_start
        self.auto_dismiss = False

    def przechwyc_tekst(self, instance):
        """
        Uzupełnia zmienne globalne liczba_kolorow i dlugosc_sekwencji
        tekstem wpisanym w polach tekstowych
        Tworzy w głównym oknie poprzez odpowiednie funkcje z klasy OknoGry
        planszę i przyciski kolorów oraz zamyka okno startowe
        W razie pustego pola lub gdy dane nie są liczbą
        aktywuje okienko z błędem
        """
        global liczba_kolorow, dlugosc_sekwencji
        k = self.ile_kolorow.text
        dl = self.jaka_dlugosc.text
        # tworzenie okienka z błędem
        blad = Popup(
            title="Błąd!",
            content=Label(
                text="Wpisz poprawne wartości, które są liczbami z podanego przedziału!",
                font_size=17,
            ),
            size_hint=(None, None),
            size=(630, 250),
            auto_dismiss=True,
        )
        # próba stworzenia planszy i przycisków kolorów,
        # w razie niepoprawnych danych otworzenie okienka z błędem
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
        Tworzy i zwraca interfejs graficzny okna głównego gry
        Otwiera okno startowe tuż po otwarciu aplikacji
        """
        self.okno_glowne = OknoGry()
        self.okno_startowe = OknoStartowe(okno_glowne=self.okno_glowne)
        Clock.schedule_once(self.otworz_okno_startowe, 0.1)
        return self.okno_glowne

    def otworz_okno_startowe(self, instance):
        """Otwiera okno startowe gry"""
        self.okno_startowe.open()


if __name__ == "__main__":
    Gra().run()
