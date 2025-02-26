## 

def check_int_input(min=None,inclusive_min=True,max=None,inclusive_max=True):
    '''
    Funktion die user eingaben auf maximale und minimale integer Werte testet
    oder im default nur nach integer Werten sieht.
    param1: min type int
    param2: inclusive_min bool
    param3: max type int
    param4: inclusive_max bool
    return: user_int as int
    '''
    while True:
        if min != None and max != None:
            if inclusive_min and inclusive_max:
                user_int = input(f'Bitte geben Sie eine ganze Zahl von {min} bis {max} eingeschlossen ein: ')
                if user_int.isdecimal():
                    if max >= int(user_int) >= min:
                        return int(user_int)
                    else:
                        print("\n!Falsche Eingabe!\n")
            elif inclusive_min:
                user_int = input(
                    f'Bitte geben Sie eine ganze Zahl eingeschlossen {min}'
                    + f' bis {max} ausgeschlossen ein: '
                )
                if user_int.isdecimal():
                    if max > int(user_int) >= min:
                        return int(user_int)
                    else:
                        print("\n!Falsche Eingabe!\n")
            elif inclusive_max:
                user_int = input(
                    f'Bitte geben Sie eine ganze Zahl ausgeschlossen {min}'
                    + f' bis {max} eingeschlossen an: '
                    )
                if user_int.isdecimal():
                    if max >= int(user_int) > min:
                        return int(user_int)
                    else:
                        print("\n!Falsche Eingabe!\n")
            else:
                user_int = input(
                    f'Geben Sie ein Zahl von ausgeschlossen {min} bis'
                    + f' {max} ausgeschlossen an: '
                    )
                if user_int.isdecimal():
                    if max > int(user_int) > min:
                        return int(user_int)
                    else:
                        print("\n!Falsche Eingabe!\n")
        elif min != None:
            if inclusive_min:
                user_int = input('Bitte geben Sie eine ganze Zahl größer gleich {min} ein: ')
                if user_int.isdecimal():
                    if int(user_int) >= min:
                        return int(user_int)
                    else:
                        print("\n!Falsche Eingabe!\n")
            else:
                user_int = input('Bitte geben Sie eine ganze Zahl echt größer {min} ein: ')
                if user_int.isdecimal():
                    if int(user_int) > min:
                        return int(user_int)
                    else:
                        print("\n!Falsche Eingabe!\n")
        elif max != None:
            if inclusive_max:
                user_int = input(f'Bitte geben Sie eine ganze Zahl kleiner oder gleich {max} ein: ')
                if user_int.isdecimal():
                    if max >= int(user_int):
                        return int(user_int)
                    else:
                        print("\n!Falsche Eingabe!\n")
            else:
                user_int = input(f'Bitte geben Sie eine ganze Zahl echt kleiner {max} ein: ')
                if user_int.isdecimal():
                    if max > int(user_int):
                        return int(user_int)
                    else:
                        print("\n!Falsche Eingabe!\n")
        else:
            user_int = input(f'Bitte geben Sie eine beliebige ganze Zahl an: ')
            if user_int.isdecimal():
                return int(user_int)
            else:
                print("\n!Falsche Eingabe!\n")

        


