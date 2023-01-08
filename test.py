def alala(x, **kwargs):
    if 'ololo' in kwargs:
        x += kwargs['ololo']
    return x


print(alala(1, ololo=2))
