l = [
    '003e7f49457f3e00',
    '0040447f7f404000',
    '00627351494f4600',
    '00226349497f3600',
    '00181814167f7f10',
    '00276745457d3900',
    '003e7f49497b3200',
    '000303797d070300',
    '00367f49497f3600',
    '00266f49497f3e00',
    '00020351590f0600',
]

for code in l:
    a = bytes.fromhex(code)
    b = ''.join(f'{i:08b}' for i in a)
    c = ['0'] * 64
    w = 8
    for pos in range(64):
        p = (pos//w)+(pos%w)*w
        c[p] = b[pos]

    e = list(reversed(list(''.join(c[i:i+w]) for i in range(0,len(c), 8))))
    # print('\n'.join(e))
    d = bytes([int(i, 2) for i in e])
    print(d.hex())
