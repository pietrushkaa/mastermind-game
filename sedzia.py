def sprawdz(
    k: int, sekwencja_ukryta: list[int], zapytanie: list[int]
) -> tuple[int, int]:
    """
    Funkcja oceniająca poprawność zapytania do gry Mastermind.
    Algorytm użyty w funkcji polega na zliczeniu w pierwszej 
    kolejności pionków o właściwym kolorze na właściwym miejscu 
    i posortowanie tych, które nie zostały zliczone względem koloru.
    Następnie dla każdego koloru należy porównać liczbę pionków 
    w tym kolorze pozostałych w sekwencji ukrytej oraz w zapytaniu 
    i dodać do liczby pionków o właściwym kolorze, ale na niewłaściwym
    miejscu mniejszą z nich.
    
    Przyjmuje:
    k - liczba kolorów
    sekwencja_ukryta - lista kodująca sekwencję ukrytą
    zapytanie - lista kodująca pojedyncze zapytanie
    Zwraca:
    krotka[wl_k_m, wl_k]
    wl_k_m - liczba pionków o właściwym kolorze i na właściwym miejscu
    wl_k - liczba pionków o właściwym kolorze, ale na niewłaściwym miejscu
    """
    # Wykrywanie możliwych błędów: sprawdzanie, czy dane są prawidłowych typów
    if (
        not isinstance(sekwencja_ukryta, list) 
        or not isinstance(zapytanie, list)
        or not isinstance(k, int)
    ):
        raise Exception("Dane są nieprawidłowych typów!")
    # Sprawdzanie, czy dane w listach są typu int i czy mieszczą się w odpowiednich przedziałach
    if not all(isinstance(x, int) and k >= x > 0 for x in sekwencja_ukryta) or not all(
       isinstance(x, int) and k >= x > 0 for x in zapytanie):
        raise Exception("Dane w listach kodujących sekwencję lub zapytanie są nieprawidłowe!")
    # Sprawdzanie, czy listy sekwencji i zapytania są tej samej długości
    if len(sekwencja_ukryta) != len(zapytanie):
        raise Exception("Listy kodujące sekwencję i zapytanie nie są równej długości!")

    ile_zostalo_zap = [0 for i in range(k)] 
    # ile__zostalo_zap[i] = ile jest w zapytaniu pionków koloru i, które pozostały po odrzuceniu pionków o właściwym kolorze i miejscu
    ile_zostalo_sek = [0 for i in range(k)]  
    # ile_zostalo_sek[i] - ile jest w sekwencji ukrytej pionków koloru i, które pozostały po odrzuceniu pionków o właściwym kolorze i miejscu

    # Zliczanie pionków o właściwym kolorze na właściwym miejscu oraz list ile_zap i ile_sek
    wl_k_m = 0
    for i in range(len(zapytanie)):
        if sekwencja_ukryta[i] == zapytanie[i]:
            wl_k_m += 1
        else:
            ile_zostalo_zap[sekwencja_ukryta[i] - 1] += 1 # 
            ile_zostalo_sek[zapytanie[i] - 1] += 1

    # Zliczanie pionków o właściwym kolorze, ale na niewłaściwym miejscu (według algorytmu j.w.)
    wl_k = 0
    for i in range(k):
        wl_k += min(ile_zostalo_sek[i], ile_zostalo_zap[i])
    return wl_k_m, wl_k
