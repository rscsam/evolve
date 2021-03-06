import random


def mix_colors(a, b):
    nrx = format(int((int('0x' + a[1:3], 16) + int('0x' + b[1:3], 16)) / 2), '02x')
    ngx = format(int((int('0x' + a[3:5], 16) + int('0x' + b[3:5], 16)) / 2), '02x')
    nbx = format(int((int('0x' + a[5:7], 16) + int('0x' + b[5:7], 16)) / 2), '02x')
    return "#" + str(nrx) + str(ngx) + str(nbx)


def mix_color_values(a, b):
    return "#" + str(format(int((a + b)/2), '02x'))


def mix_cv_for_value(a, b):
    result = 0
    result += ((((a << 26) >> 26) & 0x3F) + (((b << 26) >> 26) & 0x3F)) / 2
    result += ((((a << 20) >> 26) & 0x3F) - (((b << 20) >> 26) & 0x3F)) * 128
    result += ((((a << 14) >> 26) & 0x3F) - (((b << 14) >> 26) & 0x3F)) * 32768
    return result


def random_color():
    nrx = format(int(random.random()*256), '02x')
    ngx = format(int(random.random()*256), '02x')
    nbx = format(int(random.random()*256), '02x')
    return "#" + str(nrx) + str(ngx) + str(nbx)


def random_color_value():
    return random.random() * 16777216  # 2^24 or 256^3


def color_pack(c):
    return int(c[1:], 16)
