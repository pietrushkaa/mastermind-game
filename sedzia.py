def sprawdz(
    k: int, sekwencja_ukryta: list[int], zapytanie: list[int]
) -> tuple[int, int]:
    """
    Function evaluating the correctness of a guess in the Mastermind game.
    The algorithm used in the function first counts the pegs of the right color 
    in the right place, and groups the remaining uncounted ones by color.
    Next, for each color, it compares the number of pegs of that color remaining 
    in the hidden sequence and in the guess, and adds the smaller of the two 
    to the number of pegs of the right color but in the wrong place.
    
    Accepts:
    k - number of colors
    sekwencja_ukryta - list encoding the hidden sequence
    zapytanie - list encoding a single guess
    Returns:
    tuple[wl_k_m, wl_k]
    wl_k_m - number of pegs of the right color and in the right place
    wl_k - number of pegs of the right color, but in the wrong place
    """
    # Detecting possible errors: checking if the data types are correct
    if (
        not isinstance(sekwencja_ukryta, list) 
        or not isinstance(zapytanie, list)
        or not isinstance(k, int)
    ):
        raise Exception("Data types are incorrect!")
    
    # Checking if the data in the lists are of type int and fall within the appropriate ranges
    if not all(isinstance(x, int) and k >= x > 0 for x in sekwencja_ukryta) or not all(
       isinstance(x, int) and k >= x > 0 for x in zapytanie):
        raise Exception("Data in the lists encoding the sequence or guess is incorrect!")
    
    # Checking if the sequence and guess lists are of equal length
    if len(sekwencja_ukryta) != len(zapytanie):
        raise Exception("The lists encoding the sequence and the guess are not of equal length!")

    ile_zostalo_zap = [0 for i in range(k)] 
    # ile_zostalo_zap[i] = how many pegs of color i are in the guess, remaining after discarding pegs of the right color and place
    ile_zostalo_sek = [0 for i in range(k)]  
    # ile_zostalo_sek[i] - how many pegs of color i are in the hidden sequence, remaining after discarding pegs of the right color and place

    # Counting pegs of the right color in the right place and populating ile_zap and ile_sek lists
    wl_k_m = 0
    for i in range(len(zapytanie)):
        if sekwencja_ukryta[i] == zapytanie[i]:
            wl_k_m += 1
        else:
            ile_zostalo_zap[sekwencja_ukryta[i] - 1] += 1 # 
            ile_zostalo_sek[zapytanie[i] - 1] += 1

    # Counting pegs of the right color but in the wrong place (according to the algorithm above)
    wl_k = 0
    for i in range(k):
        wl_k += min(ile_zostalo_sek[i], ile_zostalo_zap[i])
    return wl_k_m, wl_k
