import math
bit = 0b0110001
#get num
pin = 0
value = False

y = round(math.pow(2, pin))
rs = (bit&y)>>pin




if value:
    if not rs:
        print(bin(bit|round(math.pow(2, pin))))
else:
    if rs:
        print(bin(bit&round(math.pow(2, pin))^bit))