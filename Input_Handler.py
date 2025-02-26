## 

def check_int_input(min=None,inclusive_min=True,max=None,inclusive_max=True):
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
            user_int=


