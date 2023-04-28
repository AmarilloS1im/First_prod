import re
def from_numeral_to_int(income_numeral_string):
    numerlas_to_int_dict = {
        'один': 1,
        'одна': 1,
        'две': 2,
        'два': 2,
        'три': 3,
        'четыре': 4,
        'пять': 5,
        'шесть': 6,
        'семь': 7,
        'восемь': 8,
        'девять': 9,
        'десять': 10,
        'одинадцать': 11,
        'двенадцать': 12,
        'тринадцать': 13,
        'четырнадцать': 14,
        'пятнадцать': 15,
        'шестнадцать': 16,
        'семнадцать': 17,
        'восемнадцать': 18,
        'девятнадцать': 19,
        'двадцать': 20,
        'тридцать': 30,
        'сорок': 40,
        'пятьдесят': 50,
        'шестьдесят': 60,
        'семьдесят': 70,
        'восемьдесят': 80,
        'девяносто': 90,
        'сто': 100,
        'двести': 200,
        'триста': 300,
        'четыреста': 400,
        'пятьсот': 500,
        'шестьсот': 600,
        'семьсот': 700,
        'восемьсот': 800,
        'девятьсот': 900

    }
    multipliers_dict = {
        'тысяча': 1000,
        'тысяч': 1000,
        'тысячи': 1000,
        'миллион': 1000,
        'миллионов': 1000,
        'миллиона': 1000,
        'миллиард': 1000,
        'миллиардов': 1000,
        'миллиарда': 1000,
        'триллион': 1000,
        'триллиона': 1000,
        'триллионов': 1000,
        'триллиард': 1000,
        'триллиарда': 1000,
        'триллиардов': 1000
    }
    income_numeral_string = income_numeral_string.lower().split(' ')
    integer_output = 0
    for x in income_numeral_string:
        if x in multipliers_dict.keys():
            integer_output *= multipliers_dict[x]
        else:
            integer_output += numerlas_to_int_dict[x]
    return integer_output


def from_int_to_numeral_en(income_number):
    def splited_num_by_digits(num):
        num = str(num)[::-1]
        return ' '.join(num[i:i + 3] for i in range(0, len(num), 3))[::-1]

    if len(splited_num_by_digits(income_number)) <= 3:
        income_number = [str(income_number)]
    else:
        income_number = splited_num_by_digits(income_number).split(' ')

    zero_to_ninety = {
        0: "",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "eleven",
        12: "twelve",
        13: "thirteen",
        14: "fourteen",
        15: "fifteen",
        16: "sixteen",
        17: "seventeen",
        18: "eighteen",
        19: "nineteen",
        20: "twenty",
        30: "thirty",
        40: "forty",
        50: "fifty",
        60: "sixty",
        70: "seventy",
        80: "eighty",
        90: "ninety",
        100: "one hundred",
        200: "two hundred",
        300: "three hundred",
        400: "four hundred",
        500: "five hundred",
        600: "six hundred",
        700: "seven hundred",
        800: "eight hundred",
        900: "nine hundred"
    }
    suffixes = {
        1: "",
        2: "thousand",
        3: "million",
        4: "billion",
        5: "trillion"}
    translated_nums = []
    inner_string = ''
    for x in range(0, len(income_number)):
        if int(income_number[x]) in zero_to_ninety.keys():
            translated_nums.append(zero_to_ninety[int(income_number[x])])
        elif len(income_number[x]) == 3 and int(income_number[x][0]) * 100 in zero_to_ninety.keys():
            inner_string = inner_string + zero_to_ninety[int(income_number[x][0]) * 100] + ' '
        elif len(income_number[x]) == 2 and int(income_number[x][0]) * 10 in zero_to_ninety.keys():
            inner_string = inner_string + zero_to_ninety[int(income_number[x][0]) * 10]
            if len(income_number[x]) == 2 and int(income_number[x][1]) != 0 and int(
                    income_number[x][1]) in zero_to_ninety.keys():
                inner_string = inner_string + '-' + zero_to_ninety[int(income_number[x][1])]
                translated_nums.append(inner_string)
        if len(income_number[x]) == 3 and int(income_number[x][1] + income_number[x][2]) in zero_to_ninety.keys():
            inner_string = inner_string + zero_to_ninety[int(income_number[x][1] + income_number[x][2])]
            translated_nums.append(inner_string)
        elif len(income_number[x]) == 3 and int(income_number[x][1]) * 10 in zero_to_ninety.keys():
            inner_string = inner_string + zero_to_ninety[int(income_number[x][1]) * 10]
            if len(income_number[x]) == 3 and int(income_number[x][2]) != 0 and int(
                    income_number[x][2]) in zero_to_ninety.keys():
                inner_string = inner_string + '-' + zero_to_ninety[int(income_number[x][2])]
                translated_nums.append(inner_string)
        inner_string = ''

    suffix_list = []
    while len(income_number) != 0:
        if len(income_number) in suffixes:
            suffix_list.append(suffixes[len(income_number)])
            income_number.pop(0)
        else:
            pass
    combo = list(zip(translated_nums, suffix_list))
    out_string = ''
    for digit, suffix in combo:
        out_string = out_string + digit + ' ' + suffix + ' '

    return out_string.strip()

def find_numerals(income_string):
    income_string = re.findall(r"[(].*\d+\s+копеек.{1}", income_string)
    if len(income_string) != 0:
        return income_string[0][1:-18]
    else:
        return False


def find_cents(income_string):
    income_string = re.findall(r"\d+\s+копеек", income_string)
    return income_string[0]


