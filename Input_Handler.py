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
            elif inclusive_min:
                user_int = input(
                    f'Bitte geben Sie eine ganze Zahl eingeschlossen {min}'
                    + f' bis {max} ausgeschlossen ein: '
                    )
            elif inclusive_max:
                user_int = input(
                    f'Bitte geben Sie eine ganze Zahl ausgeschlossen {min}'
                    + f' bis {max} eingeschlossen an: '
                    )
            else:
                user_int = input(
                    f'Geben Sie ein Zahl von ausgeschlossen {min} bis'
                    + f' {max} ausgeschlossen an: '
                    ) 
        elif min != None:
            if inclusive_min:
                user_int = input('Bitte geben Sie eine ganze Zahl größer gleich {min} ein: ')
            else:
                user_int = input('Bitte geben Sie eine ganze Zahl echt größer {min} ein: ')
        elif max != None:
            if inclusive_max:
                user_int = input(f'Bitte geben Sie eine ganze Zahl kleiner oder gleich {max} ein: ')
            else:
                user_int = input(f'Bitte geben Sie eine ganze Zahl kleiner {max} ein: ')
        else:
            user_int = input(f'Bitte geben Sie eine beliebige ganze Zahl an: ')
            
        if user_int.isdecimal():
            return int(user_int)
        else:
            print("\n!Falsche Eingabe!\n")


