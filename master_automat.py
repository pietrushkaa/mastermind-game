import itertools
import random
from sedzia import sprawdz

def funkcja_symulujaca ():
    """
    Funkcja automatycznej gry z algorytmem
    grającym samodzielnie w grę Mastermind.

    Algorytm polega na stworzeniu zbioru wszystkich
    możliwych ukrytych sekwencji (na początku będą tam
    wszystkie możliwe kombinacje o danej liczbie kolorów
    oraz długości sekwencji), a następnie usuwaniu z niego
    sekwencji, o których wiadomo, że nie mogą być prawidłową
    odpowiedzią w tej rundzie, aż do odgadnięcia kodu.
    Usuwanie nieprawidłowych sekwencji przebiega
    w następujący sposób:
    1. Wylosowanie ze zbioru obecnie możliwych sekwencji
    jednej i podanie jej jako zapytanie, wynik sprawdzania
    zapytania z sekwencją ukrytą jest zapisywany.
    2. Sprawdzenie wszystkich sekwencji ze zbioru i usunięcie
    tych, które użyte jako sekwencja ukryta dla aktualnego zapytania
    dają inny wynik, niż ten dla prawdziwej odpowiedzi
    zapisany powyżej.
    3. Powtarzanie kroków 1 i 2 aż do momentu wygranej.
    """
    spis_zasad = """
    Zasady:
    1. Wymyśl kod składający się z kolorów oznaczonych liczbami całkowitymi większymi od 0 i podaj go poniżej.
    2. Algorytm postara się jak najszybciej odgadnąć kod, wypisując każdą próbę odgadnięcia.
    """
    print(spis_zasad)

    # Wczytywanie z wejścia poprawnej liczby kolorów
    liczba_kolorow = input("Podaj liczbę kolorów: ")
    while not liczba_kolorow.isdigit() or int(liczba_kolorow) <= 0: # dopoki wprowadzona wartość jest nieprawidłowa, wypisuj komunikat o błędzie
        liczba_kolorow = input("Wartość nieprawidłowa! Wpisz poprawną liczbę kolorów: ")
    liczba_kolorow = int(liczba_kolorow)

    # Wczytywanie z wejścia poprawnej długości sekwencji ukrytej
    dlugosc_sekwencji = input("Podaj długość sekwencji ukrytej: ")
    while not dlugosc_sekwencji.isdigit() or int(dlugosc_sekwencji) <= 0:
        dlugosc_sekwencji = input("Wartość nieprawidłowa! Wpisz poprawną długość sekwencji ukrytej: ")
    dlugosc_sekwencji = int(dlugosc_sekwencji)

    # Wczytywanie z wejścia poprawnej sekwencji ukrytej
    sekwencja_ukryta = input("Podaj sekwencję ukrytą: ").split()
    while not all(x.isdigit() and liczba_kolorow>=int(x)>0 for x in sekwencja_ukryta) or len(sekwencja_ukryta) != dlugosc_sekwencji:
        sekwencja_ukryta = input("To nie jest poprawna sekwencja! Wpisz poprawną sekwencję ukrytą: ").split()
    sekwencja_ukryta = [int(x) for x in sekwencja_ukryta]

    # Tworzenie seta ze wszystkimi możliwymi kombinacjami sekwencji
    kombinacje = set(itertools.product(range(1,liczba_kolorow+1),repeat=dlugosc_sekwencji))

    print("Symulowana gra:")
    tura = 0
    wlasciwe_miejsce = 0
    wlasciwy_kolor = 0

    # Pętla symulująca grę, dopóki sekwencja nie zostanie odgadnięta
    while wlasciwe_miejsce != dlugosc_sekwencji:
        zapytanie = random.choice(list(kombinacje)) # wybieranie losowo następne zapytanie
        print("Zapytanie: ",end="")
        for x in zapytanie: print(x,end=" ")
        print('')
        wlasciwe_miejsce, wlasciwy_kolor = sprawdz(liczba_kolorow, sekwencja_ukryta, list(zapytanie)) # sprawdzanie zapytanie przy użyciu modułu 'sedzia'
        print("Trafione miejsce: ",wlasciwe_miejsce," trafiony kolor, niewłaściwe miejsce: ", wlasciwy_kolor)

        # Usuwanie z seta sekwencji, które są niemożliwe do osiągnięcia
        # Jest sens dalej rozpatrywać sekwencje, które dają ten sam wynik co sekwencja_ukryta w porównaniu z list(zapytanie) w funkcji 'sprawdz'
        # Gdy wyniki są różne, sekwencja jest usuwana
        kombinacje_lista = list(kombinacje)
        for mozliwa_odp in kombinacje_lista:
            wlasciwe_miejsce_t, wlasciwy_kolor_t = sprawdz(liczba_kolorow, list(mozliwa_odp), list(zapytanie))
            if wlasciwe_miejsce_t != wlasciwe_miejsce or wlasciwy_kolor_t != wlasciwy_kolor:
                kombinacje.remove(mozliwa_odp)
        tura += 1

    print("Koniec gry! Sekwencja odgadnięta w ",tura," ruchach.")

if __name__ == '__main__':
 funkcja_symulujaca()