# Projekt Mastermind - implementacja gry i algorytmu symulującego grę
## Opis projektu
Projekt składa się z 3 modułów:
1. Tryb gry interaktywnej - pozwala na zagranie w grę Mastermind w wersji rozszerzonej, 
   czyli z możliwością wybrania liczby kolorów i pól, posiada interfejs graficzny.
   Dokładne zasady gry są wypisywane podczas uruchamiania aplikacji oraz są ogólnodostępne
   w internecie.
2. Tryb automatyczny - algorytm symulujący grę w wersji rozszerzonej, nie posiada 
   interfejsu graficznego - dane są wpisywane bezpośrednio do konsoli.
3. Moduł oceniający - zawiera funkcję weryfikującą zapytanie z sekwencją ukrytą, jest 
   używany w pozostałych 2 modułach i nie jest interaktywny.
## Użyte technologie
Projekt został utworzony przy pomocy:
- Python 3.12.3
- Kivy 2.2.1
## Sposób użycia
1. Żeby uruchomić tryb gry interaktywnej należy wpisać w konsolę polecenie: python3 master_graj.py
   Uwaga! Do tworzenia graficznego interfejsu została użyta biblioteka Kivy, która jest potrzebna,
   żeby aplikacja zadziałała prawidłowo. Instrukcje pobrania Kivy można znaleźć na stronie:
   https://kivy.org/doc/stable/gettingstarted/installation.html
2. Żeby uruchomić tryb automatyczny należy wpisać w konsolę polecenie: python3 master_automat.py
## Źródła
Przy tworzeniu tego projektu korzystałam ze stron:
https://www.w3schools.com/python/
https://kivy.org/doc/stable/
oraz z kursu Kivy https://www.youtube.com/watch?v=l8Imtec4ReQ