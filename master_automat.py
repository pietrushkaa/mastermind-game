import itertools
import random
from sedzia import sprawdz

def funkcja_symulujaca ():
    """
    Function for automatic gameplay with an algorithm
    playing the Mastermind game by itself.

    The algorithm works by creating a set of all
    possible hidden sequences (initially, it contains
    all possible combinations for a given number of colors
    and sequence length), and then removing from it
    sequences that are known to be impossible as the correct
    answer in the current round, until the code is guessed.
    The removal of incorrect sequences proceeds
    as follows:
    1. Drawing one sequence from the set of currently possible
    sequences and submitting it as a guess; the result of checking
    the guess against the hidden sequence is saved.
    2. Checking all sequences in the set and removing
    those which, when used as the hidden sequence for the current guess,
    yield a different result than the one for the true answer
    saved above.
    3. Repeating steps 1 and 2 until victory.
    """
    spis_zasad = """
    Rules:
    1. Come up with a code consisting of colors marked with integers greater than 0 and enter it below.
    2. The algorithm will try to guess the code as quickly as possible, printing out each guess attempt.
    """
    print(spis_zasad)

    # Reading a valid number of colors from input
    liczba_kolorow = input("Enter the number of colors:")
    while not liczba_kolorow.isdigit() or int(liczba_kolorow) <= 0: # as long as the entered value is invalid, print an error message
        liczba_kolorow = input("Invalid value! Please enter a valid number of colors:")
    liczba_kolorow = int(liczba_kolorow)

    # Reading a valid hidden sequence length from input
    dlugosc_sekwencji = input("Enter the length of the hidden sequence:")
    while not dlugosc_sekwencji.isdigit() or int(dlugosc_sekwencji) <= 0:
        dlugosc_sekwencji = input("Invalid value! Please enter a valid length of the hidden sequence:")
    dlugosc_sekwencji = int(dlugosc_sekwencji)

    # Reading a valid hidden sequence from input
    sekwencja_ukryta = input("Enter the hidden sequence:").split()
    while not all(x.isdigit() and liczba_kolorow>=int(x)>0 for x in sekwencja_ukryta) or len(sekwencja_ukryta) != dlugosc_sekwencji:
        sekwencja_ukryta = input("Invalid sequence! Please enter a valid hidden sequence (remember to represent colors by numbers from 1 to number of colors):").split()
    sekwencja_ukryta = [int(x) for x in sekwencja_ukryta]

    # Creating a set with all possible sequence combinations
    kombinacje = set(itertools.product(range(1,liczba_kolorow+1),repeat=dlugosc_sekwencji))

    print("Simulation of the game:")
    tura = 0
    wlasciwe_miejsce = 0
    wlasciwy_kolor = 0

    # Loop simulating the game until the sequence is guessed
   while wlasciwe_miejsce != dlugosc_sekwencji:
        zapytanie = random.choice(list(kombinacje)) # randomly selecting the next guess
        print("Guess: ",end="")
        for x in zapytanie: print(x,end=" ")
        print('')
        wlasciwe_miejsce, wlasciwy_kolor = sprawdz(liczba_kolorow, sekwencja_ukryta, list(zapytanie)) # checking the guess using the 'sedzia' module
        print("Right place: ",wlasciwe_miejsce," right color, wrong place: ", wlasciwy_kolor)

        # Removing from the set sequences that are impossible to achieve
        # It makes sense to only further consider sequences that yield the same result as sekwencja_ukryta when compared to list(zapytanie) in the 'sprawdz' function
        # If the results are different, the sequence is removed
        kombinacje_lista = list(kombinacje)
        for mozliwa_odp in kombinacje_lista:
            wlasciwe_miejsce_t, wlasciwy_kolor_t = sprawdz(liczba_kolorow, list(mozliwa_odp), list(zapytanie))
            if wlasciwe_miejsce_t != wlasciwe_miejsce or wlasciwy_kolor_t != wlasciwy_kolor:
                kombinacje.remove(mozliwa_odp)
        tura += 1

    print("Game over! Sequence guessed in ",tura," moves.")

if __name__ == '__main__':
    funkcja_symulujaca()
