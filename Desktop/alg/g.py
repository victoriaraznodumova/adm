ECC_POS =([0,1,3,4,6,8,10,11,13,15], [0,2,3,5,6,9,10,12,13],
          [1,2,3,7,8,9,10,14,15], [4,5,6,7,8,9,10], [11,12,13,14,15]) #на каких позициях 1 в кодируемом сообщении
POSITION16_5 = (11,4,1,0,0)
ECC_POS21 = ([2,4,6,8,10,12,14,16,18,20], [2,5,6,9,10,13,14,17,18],
             [4,5,6,12,13,14,19,20], [8,9,10,11,12,13,14], [16,17,18,19,20])
POSITION21 = (0,1,3,7,15) #расположение контрольных битов

def is_bool(variable): #проверяет что вся строка в двоич сс
    new_bool = [x for x in variable if x in ["0","1"]]
    return len(variable) == len(new_bool)
    
def counter(position, variable): #возвращ кол-во контрольных битов
    list_bool = list(str(variable))    
    ecc_value = []

    for item_on_place in position:
        y = 0
        for x in item_on_place:
            if list_bool[x] == "1":
                y += 1
        if y % 2 == 0:
            ecc_value.append(0)
        else:
            ecc_value.append(1)
    return ecc_value
  
def to_hamming(value, position = POSITION16_5):
    bit16 = str(value)
    if len(bit16) != 16:
        raise ValueError("Error кооличество разрядов не равно 16")
    elif is_bool(bit16) != True:
        raise ValueError("Число не двоичное")

    ecc_date = counter(ECC_POS, bit16)
    print(ecc_date)
    bit16 = list(bit16)

    for x in position:
        bit16.insert(int(x), str(ecc_date.pop()))

    bit21 = ''.join(bit16)
    return(bit21)

def checker(variable, ecc21_date):
    list_21 = list(str(variable))
    ecc_old = []
    for x in POSITION21:
        a = list_21[x]
        ecc_old.append(int(a))
    error_list = []
    for i, x in enumerate(ecc_old):
        if ecc21_date[i] != x:
            error_list.append(i)
    return error_list

def to_16bit(variable):
    bit21ecc = str(variable)
    
    if len(bit21ecc) != 21:
        raise ValueError("Error число разрядов не 21")
    elif is_bool(bit21ecc) != True:
        raise ValueError("Число не двоичное")

    ecc21_date = counter(ECC_POS21, bit21ecc)
    err_list = checker(bit21ecc, ecc21_date)

    bit21ecc = list(bit21ecc)
    if err_list:
        err_pos = 0
        for x in err_list:
            err_pos += (POSITION21[x] + 1)
        err_pos -= 1    
        if bit21ecc[err_pos] == 0:
            del bit21ecc[err_pos]
            bit21ecc.insert(err_pos, '1')
        else:
            del bit21ecc[err_pos]
            bit21ecc.insert(err_pos, '0')
    
    #Преобразуем число, убирая контроль четности
    for x in [15, 7, 3, 1, 0]:
        del bit21ecc[x]
    bit16_len = ''.join(bit21ecc)    
    return bit16_len

print("///////////////")

word = "0100010000111101"
print("word: ", word)
word_21 = to_hamming(word)
print("coded 21-bit word: ", word_21)
word_16b = to_16bit(word_21)
print("decoded 16-bit word: ", word_16b)
print("check two words: ", word == word_16b )
