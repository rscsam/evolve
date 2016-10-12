def mix_colors(a, b):
    arstr = a[1:3]
    agstr = a[3:5]
    abstr = a[5:7]
    brstr = b[1:3]
    bgstr = b[3:5]
    bbstr = b[5:7]
    ar = int('0x' + arstr, 16)
    ag = int('0x' + agstr, 16)
    ab = int('0x' + abstr, 16)
    br = int('0x' + brstr, 16)
    bg = int('0x' + bgstr, 16)
    bb = int('0x' + bbstr, 16)
    nr = int((ar + br) / 2)
    ng = int((ag + bg) / 2)
    nb = int((ab + bb) / 2)
    nrx = format(nr, '02x')
    ngx = format(ng, '02x')
    nbx = format(nb, '02x')
    return "#" + str(nrx) + str(ngx) + str(nbx)