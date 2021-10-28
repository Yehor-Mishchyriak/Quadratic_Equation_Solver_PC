# imports
import tkinter as tk
from functools import reduce
from math import sqrt, gcd
import matplotlib
import matplotlib.pyplot as plt
import sympy as sp
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from numpy import linspace
from playsound import playsound
from sympy.printing.pretty.stringpict import stringPict

matplotlib.use('TkAgg')
playsound('press_button.mp3')
sp.init_printing()
x = sp.symbols('x')
d = sp.symbols('D')

# creation of the window
win = tk.Tk()
win.title('Quadratic equation solver')
win.geometry('575x650+640+150')
win.resizable(False, False)

# creation of frames
main_frame = tk.Frame(win, width=575, height=650)
graph_frame = tk.Frame(win, width=575, height=650, bg='#98ff98')

# importing PNGs
light_theme = tk.PhotoImage(file='Light_theme2.png')
dark_theme = tk.PhotoImage(file='Dark_theme3.png')
icon_pic = tk.PhotoImage(file='Quadratic equation solver.png')
win.iconphoto(True, icon_pic)
background_label_main = tk.Label(main_frame, image=light_theme)
background_label_main.place(x=0, y=0, relwidth=1, relheight=1)


# Custom matplotlib's toolbar
class NavigationToolbar(NavigationToolbar2Tk):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2Tk.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom')]


# creation of the functions
# This function changes theme of the program
def theme_changer():
    global theme_change_counter
    global language_change_counter
    theme_change_counter += 1
    if theme_change_counter % 2 == 0:
        background_label_main['image'] = dark_theme
        graph_button['bg'] = '#87CEFA'
        graph_button['activebackground'] = '#1E90FF'
        if language_change_counter % 2 == 0:
            theme_button['text'] = 'Светлая'
        else:
            theme_button['text'] = 'Light'
        for button in buttons:
            button['bg'] = '#2c4a52'
            button['activebackground'] = '#04202c'
        for label in labels:
            label['bg'] = '#bcbabe'
        for field in fields:
            field['bg'] = '#8e9b97'
            field['selectbackground'] = '#ffffff'
    else:
        background_label_main['image'] = light_theme
        graph_button['bg'] = '#FFA500'
        graph_button['activebackground'] = '#D2691E'
        for button in buttons:
            button['bg'] = '#1995ad'
            button['activebackground'] = '#217ca3'
        for label in labels:
            label['bg'] = '#4cb5f5'
        for field in fields:
            field['bg'] = '#f1f1f2'
            field['selectbackground'] = '#217ca3'
            if language_change_counter % 2 == 0:
                theme_button['text'] = 'Тёмная'
            else:
                theme_button['text'] = 'Dark'


# This function changes language of the program
def language_changer():
    global language_change_counter
    global click_counter
    language_change_counter += 1
    click_counter = 0
    if language_change_counter % 2 == 0:
        instruction_label['font'] = ('Arial Black', 13)
        instruction_label['text'] = 'Введите уравнение:'
        language_label['text'] = 'Язык: '
        theme_label['text'] = 'Тема: '
        creator_label['text'] = 'Создатель - Егор Мищиряк '
        text_label_if_x['text'] = 'Если x ='
        text_label_if_y['text'] = 'Если y ='
        language_button['text'] = 'English'
        solve_button['text'] = 'Решить'
        delete_button['text'] = 'УДАЛИТЬ'
        square_button['text'] = '2-ая степень'
        graph_button['text'] = 'Нарисуй график!'
        return_to_main['text'] = 'Главный экран'
        calculate_button['text'] = 'Высчитать'
        if theme_button['text'] == 'Dark':
            theme_button['text'] = 'Тёмная'
        else:
            theme_button['text'] = 'Светлая'
    else:
        instruction_label['font'] = ('Arial Black', 13)
        instruction_label['text'] = 'Enter an equation: '
        language_label['text'] = 'Language: '
        theme_label['text'] = 'Theme: '
        creator_label['text'] = 'Creator - Yehor Mishchyriak '
        language_button['text'] = 'Русский'
        solve_button['text'] = 'SOLVE'
        delete_button['text'] = 'DELETE'
        square_button['text'] = '2nd POWER'
        graph_button['text'] = 'Graph it!'
        return_to_main['text'] = 'Main screen'
        calculate_button['text'] = 'Calculate'
        text_label_if_x['text'] = 'If x ='
        text_label_if_y['text'] = 'If y ='
        if theme_button['text'] == 'Тёмная':
            theme_button['text'] = 'Dark'
        else:
            theme_button['text'] = 'Light'


# This function adds 'x' to the "ENTRY" widget
def put_x():
    users_input.insert(tk.END, 'x')


# This function adds symbol '²' to the "ENTRY" widget
def put_power():
    users_input.insert(tk.END, '²')


# This function clears the "ENTRY" widget
def delete():
    users_output['state'] = 'normal'
    x1_output['state'] = 'normal'
    x2_output['state'] = 'normal'
    y_output['state'] = 'normal'
    global click_counter
    users_input.delete(0, tk.END)
    users_output.delete(1.0, tk.END)
    click_counter = 0
    graph_button['state'] = 'disabled'
    users_output['state'] = 'disabled'
    x1_output.delete(0, tk.END)
    x2_output.delete(0, tk.END)
    y_output.delete(0, tk.END)
    x_input.delete(0, tk.END)
    y_input.delete(0, tk.END)
    x1_output['state'] = 'disabled'
    x2_output['state'] = 'disabled'
    y_output['state'] = 'disabled'


# This function distinguishes the type of an equation and derives coefficients from it
def coefficients_sort_of_equation(equation):
    a = []  # boxes
    b = []  # for coefficients

    # data input
    quadratic_equation = equation

    # data preparation
    quadratic_equation = quadratic_equation.lower()
    split_equation = list(quadratic_equation)
    while ' ' in split_equation:
        split_equation.remove(' ')
    # getting position of the second power in an equation
    try:
        if split_equation[-1] != '0':
            split_equation = 'ERROR'
        split_equation.remove('=')
        del split_equation[-1]
        # extracting coefficients
        # extracting 'a' coefficient:
        power2pos = split_equation.index('²')
        counter = power2pos
        for i in split_equation[power2pos::-1]:
            a.append(i)
            counter = counter - 1
            if i == '+' or i == '-':
                break
        del split_equation[counter + 1:power2pos + 1]
        a.remove('²')
        a.remove('x')

        if any(map(str.isdigit, a)):
            a.reverse()
            a_coeff = float(''.join(a))
        else:
            if '-' in a:
                a_coeff = -1.0
            else:
                a_coeff = 1.0
        # trying to identify the equation type:
        if not bool(split_equation):  # then it is type: "ax²=0"
            return 'ax²=0', a_coeff

        if 'x' not in split_equation:  # then it is type: "ax²+c=0"
            return 'ax²+c=0', a_coeff, float(''.join(split_equation))  # <=== 'c' coefficient

        # if 'x' in split_equation:     # then it is either type  "ax²+bx+c=0" or "ax²+bx=0"
        # extracting 'b' coefficient
        xpos = split_equation.index('x')
        counter2 = xpos
        for i in split_equation[xpos::-1]:
            b.append(i)
            counter2 = counter2 - 1
            if i == '+' or i == '-':
                break
        del split_equation[counter2 + 1:xpos + 1]
        b.remove('x')
        if any(map(str.isdigit, b)):
            b.reverse()
            b_coeff = float(''.join(b))
        else:
            if '-' in b:
                b_coeff = -1.0
            else:
                b_coeff = 1.0

        if not bool(split_equation):  # then it is type "ax²+bx=0"
            return 'ax²+bx=0', a_coeff, b_coeff
        # if neither from aforementioned conditions occurred then it is type "ax²+bx+c=0"
        return 'ax²+bx+c=0', a_coeff, b_coeff, float(''.join(split_equation))  # <=== 'c' coefficient

    except:
        return 'ERROR'


# This function turns coefficient whose type is float to str,
# BUT it is used to write coefficients in between other symbols.
# Moreover, instead of writing "...+1x" it'll write "...+x", thereby making it somewhat prettier.
# The idea is that it also adds "+" to the coeff, not "-", as "-" is automatically written in front of negative numbers.
def middle_mystr(coeff):
    if coeff == -1.0:
        return '-'
    elif coeff == 1.0:
        return '+'
    elif coeff > 0:
        return '+' + str(coeff)
    else:
        return str(coeff)


# This function turns coefficient whose type is float to str,
# BUT it is used to write coefficients at the beginning of an equation.
def beginning_mystr(coeff):
    if coeff == -1.0:
        return '-'
    elif coeff == 1.0:
        return ''
    else:
        return str(coeff)


# The same as "gcd", but works for 3 numbers
def nod(a, b, c=None):
    return ((a if b == 0 else nod(b, a % b)) if c is None
            else nod(nod(a, b), nod(a, c)))


# this two functions generate 'pretty' root output
def primfacs(n):
    i = 2
    primfac = []
    while i * i <= n:
        while n % i == 0:
            primfac.append(i)
            n = n / i
        i = i + 1
    if n > 1:
        primfac.append(n)
    return primfac


def nice_root(num):
    list_of_dividers = primfacs(num)
    outside_the_root = []
    for i in list_of_dividers:
        how_many_same_items = list_of_dividers.count(i)
        if how_many_same_items % 2 == 0:
            while i in list_of_dividers:
                outside_the_root.append(i)
                list_of_dividers.remove(i)
        else:
            while how_many_same_items != 1:
                outside_the_root.append(i)
                list_of_dividers.remove(i)
                how_many_same_items -= 1
    if bool(list_of_dividers):
        whole_part_inside_the_root = reduce(lambda x, y: x * y, list_of_dividers)
    else:
        whole_part_inside_the_root = 1
    if bool(outside_the_root):
        whole_part_outside_the_root = sqrt(reduce(lambda x, y: x * y, outside_the_root))
    else:
        whole_part_outside_the_root = 1
    return [whole_part_outside_the_root, whole_part_inside_the_root]


# This func generates nice fractions
def nice_dividing(number, divider):
    if str(number)[str(number).index('.') + 1] == '0':
        number = int(number)
    if str(divider)[str(divider).index('.') + 1] == '0':
        divider = int(divider)
    if isinstance(number, float) and isinstance(divider, float):
        symb_len_num = len(str(number)[str(number).index('.')::]) - 1
        symb_len_div = len(str(divider)[str(divider).index('.')::]) - 1
        if symb_len_num > symb_len_div:
            number = int(number * 10 ** symb_len_num)
            divider = int(divider * 10 ** symb_len_num)
        else:
            number = int(number * 10 ** symb_len_div)
            divider = int(divider * 10 ** symb_len_div)
    elif isinstance(number, float):
        symb_len_num = len(str(number)[str(number).index('.')::]) - 1
        number = int(number * 10 ** symb_len_num)
        divider = int(divider * 10 ** symb_len_num)
    elif isinstance(divider, float):
        symb_len_div = len(str(divider)[str(divider).index('.')::]) - 1
        number = int(number * 10 ** symb_len_div)
        divider = int(divider * 10 ** symb_len_div)
    if number < 0:
        number = ['-', abs(number)]
    else:
        number = ['', abs(number)]

    if divider < 0:
        divider = ['-', abs(divider)]
    else:
        divider = ['', abs(divider)]
    if number[1] < divider[1]:
        # 0 - whole-part; 1 - numerator; 2 - denominator
        if number[0] == '-' and divider[0] == '-':
            return ['', number[1] / gcd(number[1], divider[1]), divider[1] / gcd(number[1], divider[1])]
        elif all([number[0] == '-', divider[0] == '']) or all([number[0] == '', divider[0] == '-']):
            return ['-', number[1] / gcd(number[1], divider[1]), divider[1] / gcd(number[1], divider[1])]
        else:
            return ['', number[1] / gcd(number[1], divider[1]), divider[1] / gcd(number[1], divider[1])]
    else:
        fractional_part = number[1] - (divider[1] * (number[1] // divider[1]))
        # 0 - whole-part; 1 - numerator; 2 - denominator
        if number[0] == '-' and divider[0] == '-':
            return [number[1] // divider[1], fractional_part / gcd(fractional_part, divider[1]),
                    divider[1] / gcd(fractional_part, divider[1])]
        elif all([number[0] == '-', divider[0] == '']) or all([number[0] == '', divider[0] == '-']):
            return [-(number[1] // divider[1]), fractional_part / gcd(fractional_part, divider[1]),
                    divider[1] / gcd(fractional_part, divider[1])]
        else:
            return [number[1] // divider[1], fractional_part / gcd(fractional_part, divider[1]),
                    divider[1] / gcd(fractional_part, divider[1])]


# It helps write fractions
def fraction_writer(prior_thing, split_frac, prior_thing_position=1):
    internal_split_frac = list(map(str, split_frac[::]))  # the of split fraction is whole-part, numerator, denominator
    return stringPict(prior_thing + internal_split_frac[0]).right(' ', stringPict(
        stringPict(internal_split_frac[1]).below(stringPict.LINE, internal_split_frac[2])[0], prior_thing_position))[0]


def operations_with_fractions(fraction1, operator, fraction2):
    return stringPict(stringPict(' ' + operator, -1).right(fraction2)[0]).left(fraction1)[0]


# It helps extract a root from a fraction
def root_writer(split_root, prior_thing=''):
    internal_split_root = split_root[::]  # the of split root is outside-part, inside-part of the root
    if internal_split_root[0] == 1:
        internal_split_root[0] = ''
    return stringPict(prior_thing + str(internal_split_root[0])).right('', stringPict(
        str(sp.pretty(sp.sqrt((internal_split_root[1]), evaluate=False), use_unicode=False)), 1))[0]


def check_int(expression):
    if len(str(expression)[str(expression).index('.')::]) == 2 and str(expression)[
        str(expression).index('.') + 1] == '0':
        return True
    else:
        return False


def check_float(expression):
    if len(str(expression)[str(expression).index('.')::]) == 2 and str(expression)[
        str(expression).index('.') + 1] == '0':
        return False
    else:
        return True


def make_it_int(sequence):
    # sequence - [STRING, FLOAT, FLOAT, ..., FLOAT]
    list_of_powers = []
    for coeff in sequence[1::]:
        list_of_powers.append(len(str(coeff)[str(coeff).index('.')::]) - 1)
    list_to_return = list(map(lambda i: i * 10 ** max(list_of_powers), sequence[1::]))
    list_to_return.insert(0, sequence[0])
    return [list_to_return, str(10 ** max(list_of_powers))]


def plus_or_minus(number):
    if '-' in str(number):
        return ' - '
    else:
        return ' + '


# This function takes data derived by the function above, namely coefficients and equation type. Having this information
# the function can solve the equation
equation = ''


def solve():
    # users_output.insert(1.0, sp.pretty(sp.sqrt(1/x))) - Reminder
    users_output['state'] = 'normal'
    x1_output['state'] = 'normal'
    x2_output['state'] = 'normal'
    y_output['state'] = 'normal'
    global click_counter
    global equation
    click_counter = 0
    users_output.delete(1.0, tk.END)
    entered_equation = users_input.get()
    entered_equation = entered_equation.replace(' ', '')
    entered_equation = entered_equation.lower()
    gathered_data = coefficients_sort_of_equation(users_input.get())  # <=== tuple
    users_output.insert(1.0, '\n' * 100)
    # if entered data is incorrect:
    if gathered_data != 'ERROR':
        graph_button['state'] = 'normal'
        equation = entered_equation
    if gathered_data == 'ERROR':
        if language_change_counter % 2 == 0:  # - Russian
            users_output.insert(1.0, 'Упс... Я не знаю, как решить данную задачку')
        else:  # - English
            users_output.insert(1.0, 'Oops... I don\'t know how to solve this problem')
    # solution for "ax²=0": <<type-0, a-1>>
    elif gathered_data[0] == 'ax²=0':
        if gathered_data[1] == 0:
            users_output.insert(1.2, '1) ' + entered_equation)
            users_output.insert(3.2, '2) x = R')
        else:
            users_output.insert(1.2, '1) ' + entered_equation)
            users_output.insert(3.2, '2) x = 0')
    # solution for "ax²+c=0": <<type-0, a-1, c-2>>
    elif gathered_data[0] == 'ax²+c=0':
        if -gathered_data[2] / gathered_data[1] < 0:
            users_output.insert(1.2, '1) ' + entered_equation)
            users_output.insert(3.2, '2) ' + beginning_mystr(gathered_data[1]) + 'x² = ' + str(gathered_data[2] * -1))
            users_output.insert(5.2, '3) ' + 'x є ∅')
        else:
            users_output.insert(1.2, '1) ' + entered_equation)
            users_output.insert(3.2, '2) ' + beginning_mystr(gathered_data[1]) + 'x² = ' + str(-gathered_data[2]))
            users_output.insert(5.2, fraction_writer('3) x² = ', ['', -gathered_data[2], gathered_data[1]]))
            if check_int(gathered_data[2] / gathered_data[1]):
                users_output.insert(9.2, '4) x² = ' + str(-gathered_data[2] / gathered_data[1]))
                users_output.insert(11.2,
                                    root_writer([1, -gathered_data[2] / gathered_data[1]], prior_thing='5) x = ±'))
                if len(str(sqrt(-gathered_data[2] / gathered_data[1]))[
                       str(sqrt(-gathered_data[2] / gathered_data[1])).index('.')::]) > 3 and -gathered_data[2] / \
                        gathered_data[1] != nice_root(-gathered_data[2] / gathered_data[1])[1]:
                    users_output.insert(13.2, root_writer(nice_root(-gathered_data[2] / gathered_data[1]),
                                                          prior_thing='6) x = ±'))
                    if language_change_counter % 2 == 0:  # - Russian
                        users_output.insert(16.2, 'Альтернативный ответ: x = ±' + str(
                            sqrt(-gathered_data[2] / gathered_data[1])))
                    else:
                        users_output.insert(16.2, 'Alternative answer: x = ±' + str(
                            sqrt(-gathered_data[2] / gathered_data[1])))
                elif len(str(sqrt(-gathered_data[2] / gathered_data[1]))[
                         str(sqrt(-gathered_data[2] / gathered_data[1])).index('.')::]) < 3:
                    users_output.insert(15.2, '6) x = ±' + str(sqrt(-gathered_data[2] / gathered_data[1])))
                else:
                    if language_change_counter % 2 == 0:  # - Russian
                        users_output.insert(14.2, 'Альтернативный ответ: x = ±' + str(
                            sqrt(-gathered_data[2] / gathered_data[1])))
                    else:
                        users_output.insert(14.2, 'Alternative answer: x = ±' + str(
                            sqrt(-gathered_data[2] / gathered_data[1])))

            else:
                if gathered_data[1] < 0:
                    split_fraction = nice_dividing(gathered_data[2], -gathered_data[1])
                else:
                    split_fraction = nice_dividing(-gathered_data[2], gathered_data[1])
                users_output.insert(9.2, fraction_writer('4) x² = ', split_fraction))
                try:
                    numerator = split_fraction[0] * split_fraction[2] + split_fraction[1]
                except TypeError:
                    numerator = split_fraction[1]
                users_output.insert(12.2, fraction_writer('5) x = ±', ['', root_writer(nice_root(numerator)),
                                                                       root_writer(nice_root(split_fraction[2]))],
                                                          prior_thing_position=2))
                denominator = nice_root(split_fraction[2])
                numerator = nice_root(numerator)
                if denominator[0] == '':
                    denominator[0] = 1
                if numerator[0] == '':
                    numerator[0] = 1
                new_numerator = nice_root(numerator[1] * denominator[1])
                denominator = denominator[0] * denominator[1]
                numerator[0] = numerator[0] * new_numerator[0]
                numerator[1] = new_numerator[1]
                copy_of_the_numerator = numerator[::]
                users_output.insert(18.2, fraction_writer('6) x = ±', ['', root_writer(numerator), denominator],
                                                          prior_thing_position=2))
                nod_of_num_and_den = gcd(int(numerator[0]), int(denominator))
                numerator[0] = numerator[0] / nod_of_num_and_den
                denominator = denominator / nod_of_num_and_den
                if copy_of_the_numerator[0] != numerator[0] or copy_of_the_numerator[1] != numerator[1]:
                    if denominator == 1:
                        users_output.insert(18.2, root_writer(numerator, prior_thing='7) x = ±'))
                        if language_change_counter % 2 == 0:  # - Russian
                            users_output.insert(23.2, 'Альтернативный ответ: x = ±' + str(
                                sqrt(-gathered_data[2] / gathered_data[1])))
                        else:
                            users_output.insert(23.2, 'Alternative answer: x = ±' + str(
                                sqrt(-gathered_data[2] / gathered_data[1])))
                    else:
                        users_output.insert(18.2, fraction_writer('7) x = ±', ['', root_writer(numerator), denominator],
                                                                  prior_thing_position=2))
                        if language_change_counter % 2 == 0:  # - Russian
                            users_output.insert(23.2, 'Альтернативный ответ: x = ±' + str(
                                sqrt(-gathered_data[2] / gathered_data[1])))
                        else:
                            users_output.insert(23.2, 'Alternative answer: x = ±' + str(
                                sqrt(-gathered_data[2] / gathered_data[1])))
                else:
                    if language_change_counter % 2 == 0:  # - Russian
                        users_output.insert(23.2, 'Альтернативный ответ: x = ±' + str(
                            sqrt(-gathered_data[2] / gathered_data[1])))
                    else:
                        users_output.insert(23.2, 'Alternative answer: x = ±' + str(
                            sqrt(-gathered_data[2] / gathered_data[1])))

    # solution for "ax²+bx=0": <<type-0, a-1, b-2>>
    elif gathered_data[0] == 'ax²+bx=0':
        users_output.insert(1.2, '1) ' + entered_equation)
        users_output.insert(3.2, '2) x ⋅ (' + beginning_mystr(gathered_data[1]) + 'x' + middle_mystr(
            gathered_data[2]) + ') = 0')
        users_output.insert(5.2, '3) x₁ = 0; ' + beginning_mystr(gathered_data[1]) + 'x' + middle_mystr(
            gathered_data[2]) + ' = 0')
        users_output.insert(7.2, '4) ' + beginning_mystr(gathered_data[1]) + 'x = ' + str(-gathered_data[2]))
        users_output.insert(9.2, fraction_writer('5) x₂ = ', ['', -gathered_data[2], gathered_data[1]]))
        if check_int(gathered_data[2] / gathered_data[1]):
            users_output.insert(13.2, '6) x₂ = ' + str(-gathered_data[2] / gathered_data[1]))
        else:
            if abs(nice_dividing(-gathered_data[2], gathered_data[1])[1]) != abs(-gathered_data[2]):
                alt_ans_pos = 18.2
                users_output.insert(13.2,
                                    fraction_writer('6) x₂ = ', nice_dividing(-gathered_data[2], gathered_data[1])))
            else:
                alt_ans_pos = 14.2
            if language_change_counter % 2 == 0:  # - Russian
                users_output.insert(alt_ans_pos,
                                    'Альтернативный ответ: x₂ = ' + str(-gathered_data[2] / gathered_data[1]))
            else:
                users_output.insert(alt_ans_pos,
                                    'Alternative answer: x₂ = ' + str(-gathered_data[2] / gathered_data[1]))
    # solution for "ax²+bx+c=0": <<type-0, a-1, b-2, c-3>>
    elif gathered_data[0] == 'ax²+bx+c=0':
        discriminant = gathered_data[2] ** 2 - 4 * gathered_data[1] * gathered_data[3]
        if discriminant < 0:
            users_output.insert(1.2, '1) ' + entered_equation)
            users_output.insert(3.2, '2) D = b² - 4 ⋅ a ⋅ c')
            users_output.insert(5.2,
                                '3) D = ' + str(gathered_data[2]) + '² - 4 ⋅ ' + str(gathered_data[1]) + ' ⋅ ' + str(
                                    gathered_data[3]) + ' < 0; ==>')
            users_output.insert(7.2, '4) x є ∅')
        elif discriminant == 0:
            users_output.insert(1.2, '1) ' + entered_equation)
            users_output.insert(3.2, '2) D = b² - 4 ⋅ a ⋅ c')
            users_output.insert(5.2,
                                '3) D = ' + str(gathered_data[2]) + '² - 4 ⋅ ' + str(gathered_data[1]) + ' ⋅ ' + str(
                                    gathered_data[3]) + ' = 0; ==>')
            users_output.insert(7.2, fraction_writer('4) x = ', ['', '-b', '2 ⋅ a']))
            users_output.insert(11.2, fraction_writer('5) x = ', ['', -gathered_data[2], 2 * gathered_data[1]]))
            if check_int(-gathered_data[2] / 2 * gathered_data[1]):
                users_output.insert(15.2, '6) x = ' + str(-gathered_data[2] / (2 * gathered_data[1])))
            else:
                users_output.insert(15.2,
                                    fraction_writer('6) x = ', nice_dividing(-gathered_data[2], 2 * gathered_data[1])))
                if language_change_counter % 2 == 0:  # - Russian
                    users_output.insert(18.2,
                                        'Альтернативный ответ: x = ' + str(-gathered_data[2] / (2 * gathered_data[1])))
                else:
                    users_output.insert(18.2,
                                        'Alternative answer: x = ' + str(-gathered_data[2] / (2 * gathered_data[1])))

        else:
            if all([gathered_data[1] == 1.0, check_int(sqrt(discriminant))]):
                users_output.insert(1.2, '1) ' + entered_equation)
                users_output.insert(3.2, '2) x₁ + x₂ = -b; x₁ ⋅ x₂ = c. ==>')
                users_output.insert(5.2,
                                    '3) x₁ + x₂ =' + str(-gathered_data[2]) + '; x₁ ⋅ x₂ = ' + str(gathered_data[3]))
                users_output.insert(7.2, '4) x₁ = ' + str(
                    (-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1])) + '; x₂ = ' + str(
                    (-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1])))
            elif gathered_data[1] != 1.0 or all(
                    [gathered_data[1] == 1, len(str(sqrt(discriminant))[str(sqrt(discriminant)).index('.')::]) != 2]):
                gcd_of_3_nums = abs(nod(gathered_data[1], gathered_data[2], gathered_data[3]))
                if all([gathered_data[1] / gcd_of_3_nums == 1.0, check_int(sqrt(discriminant))]):
                    A, B, C = gathered_data[1] / gcd_of_3_nums, gathered_data[2] / gcd_of_3_nums, gathered_data[
                        3] / gcd_of_3_nums
                    users_output.insert(1.2, '1) ' + entered_equation)
                    users_output.insert(3.2, '2) x² ' + middle_mystr(B) + 'x ' + middle_mystr(C) + ' = 0')
                    users_output.insert(5.2, '3) x₁ + x₂ = -b; x₁ ⋅ x₂ = c. ==>')
                    users_output.insert(7.2, '4) x₁ + x₂ = ' + str(-B) + '; x₁ ⋅ x₂ = ' + str(C))
                    users_output.insert(9.2, '5) x₁ =' + str(
                        (-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1])) + '; x₂ = ' + str(
                        (-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1])))
                elif abs(gathered_data[2]) >= 8 and gathered_data[2] % 2 == 0:
                    if any(map(check_float, gathered_data[1::])):
                        multiplier = make_it_int(gathered_data)[1]
                        gathered_data = make_it_int(gathered_data)[0]
                        users_output.insert(1.2,
                                            '1) ' + entered_equation + ' | ⋅ ' + multiplier + ' ==> \n' + beginning_mystr(
                                                gathered_data[1]) + 'x²' + middle_mystr(
                                                gathered_data[2]) + 'x' + middle_mystr(gathered_data[3]) + '=0')
                    else:
                        users_output.insert(1.2, '1) ' + entered_equation)
                    discriminant_divide_4 = ((gathered_data[2] / 2) ** 2) - gathered_data[1] * gathered_data[3]
                    users_output.insert(3.2, stringPict(' - a ⋅ c', -1).left(stringPict(
                        operations_with_fractions(fraction_writer('2) ', ['', 'D', '4']), '=',
                                                  fraction_writer('', ['', 'b²', '4']))))[0])
                    users_output.insert(7.2,
                                        stringPict(str(-gathered_data[1]) + ' ⋅ ' + str(gathered_data[3]), -1).left(
                                            stringPict(
                                                operations_with_fractions(fraction_writer('3) ', ['', 'D', '4']), '=',
                                                                          fraction_writer('', ['', str(
                                                                              gathered_data[2]) + '²', '4']))))[0])
                    users_output.insert(11.2, stringPict(' = ' + str(discriminant_divide_4), -1).left(
                        fraction_writer('4) ', ['', 'D', '4']))[0])
                    x_through_d_formula = stringPict(
                        stringPict(' ±', -2).right(sp.pretty(sp.sqrt((d / 4), evaluate=False), use_unicode=False))[0],
                        1).left(fraction_writer('', ['', '-b', '2']))[0]
                    formula = fraction_writer('', ['', x_through_d_formula, 'a'])
                    users_output.insert(14.2, stringPict('5) x = ', -4).right(formula)[0])
                    x_through_d_formula = stringPict(
                        stringPict(' ±', -2).right(fraction_writer('', ['', sp.pretty(
                            sp.sqrt((discriminant_divide_4), evaluate=False), use_unicode=False), '1']))[0],
                        1).left(fraction_writer('', ['', str(-gathered_data[2]), '2']))[0]
                    formula = fraction_writer('', ['', x_through_d_formula, str(gathered_data[1])])
                    users_output.insert(20.2, stringPict('6) x = ', -4).right(formula)[0])
                    if check_int(sqrt(discriminant_divide_4)):
                        users_output.insert(27.2, fraction_writer('7) x₁ = ', ['',
                                                                               str(-gathered_data[2] / 2) + ' + ' + str(
                                                                                   sqrt(discriminant_divide_4)),
                                                                               str(gathered_data[1])]))
                        users_output.insert(31.2, fraction_writer(' x₂ = ', ['',
                                                                             str(-gathered_data[2] / 2) + ' - ' + str(
                                                                                 sqrt(discriminant_divide_4)),
                                                                             str(gathered_data[1])]))
                        # fix
                        if check_int((-gathered_data[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data[1]) and check_int((-gathered_data[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data[1]):
                            users_output.insert(35.2, '8) x₁ = ' + str(
                                (-gathered_data[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data[
                                    1]) + '; x₂ = ' + str(
                                (-gathered_data[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data[1]))
                        else:
                            users_output.insert(35.2, fraction_writer('8) x₁ = ', nice_dividing(
                                -gathered_data[2] / 2.0 + sqrt(discriminant_divide_4), gathered_data[1])))
                            users_output.insert(39.2, fraction_writer('   x₂ = ', nice_dividing(
                                -gathered_data[2] / 2.0 - sqrt(discriminant_divide_4), gathered_data[1])))
                            if language_change_counter % 2 == 0:  # - Russian
                                users_output.insert(43.2, 'Альтернативный ответ: x₁ = ' + str(
                                    (-gathered_data[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data[
                                        1]) + '; x₂ = ' + str(
                                    (-gathered_data[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data[1]))
                            else:
                                users_output.insert(43.2, 'Alternative answer: x₁ = ' + str(
                                    (-gathered_data[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data[
                                        1]) + '; x₂ = ' + str(
                                    (-gathered_data[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data[1]))
                    else:
                        if gathered_data[1] == 1.0:
                            users_output.insert(27.2, root_writer(nice_root(discriminant_divide_4),
                                                                  prior_thing='7) x = ' + str(
                                                                      -gathered_data[2] / 2) + ' ± '))
                            users_output.insert(30.2, root_writer(nice_root(discriminant_divide_4),
                                                                  prior_thing='8) x₁ = ' + str(
                                                                      -gathered_data[2] / 2) + ' + '))
                            users_output.insert(33.2, root_writer(nice_root(discriminant_divide_4),
                                                                  prior_thing='   x₂ = ' + str(
                                                                      -gathered_data[2] / 2) + ' - '))
                            alt_answ_pos1 = 37.2
                            alt_answ_pos2 = 38.2
                        else:
                            users_output.insert(27.2, fraction_writer('7) x = ', ['', stringPict(
                                str(-gathered_data[2] / 2) + ' ± ', -1).right(
                                root_writer(nice_root(discriminant_divide_4)))[0], str(gathered_data[1])]))
                            users_output.insert(31.2, fraction_writer('8) x₁ = ', ['', stringPict(
                                str(-gathered_data[2] / 2) + ' + ', -1).right(
                                root_writer(nice_root(discriminant_divide_4)))[0], str(gathered_data[1])]))
                            users_output.insert(35.2, fraction_writer('   x₂ = ', ['', stringPict(
                                str(-gathered_data[2] / 2) + ' - ', -1).right(
                                root_writer(nice_root(discriminant_divide_4)))[0], str(gathered_data[1])]))
                            alt_answ_pos1 = 41.2
                            alt_answ_pos2 = 42.2
                        if language_change_counter % 2 == 0:  # - Russian
                            users_output.insert(alt_answ_pos1, 'Альтернативный ответ: x₁ = ' + str(
                                (-gathered_data[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data[1]))
                            users_output.insert(alt_answ_pos2, '                      x₂ = ' + str(
                                (-gathered_data[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data[1]))
                        else:
                            users_output.insert(alt_answ_pos1, 'Alternative answer: x₁ = ' + str(
                                (-gathered_data[2] / 2 + sqrt(discriminant_divide_4)) / gathered_data[1]))
                            users_output.insert(alt_answ_pos2, '                    x₂ = ' + str(
                                (-gathered_data[2] / 2 - sqrt(discriminant_divide_4)) / gathered_data[1]))
                else:
                    if any(map(check_float, gathered_data[1::])):
                        multiplier = make_it_int(gathered_data)[1]
                        gathered_data = make_it_int(gathered_data)[0]
                        users_output.insert(1.2,
                                            '1) ' + entered_equation + ' | ⋅ ' + multiplier + ' ==> \n' + beginning_mystr(
                                                gathered_data[1]) + 'x²' + middle_mystr(
                                                gathered_data[2]) + 'x' + middle_mystr(gathered_data[3]) + '=0')
                    else:
                        users_output.insert(1.2, '1) ' + entered_equation)
                    discriminant = gathered_data[2] ** 2 - 4 * gathered_data[1] * gathered_data[3]
                    users_output.insert(3.2, '2) D = b² - 4 ⋅ a ⋅ c')
                    users_output.insert(5.2, '3) D = ' + str(gathered_data[2]) + '² - 4 ⋅ ' + str(
                        gathered_data[1]) + ' ⋅ ' + str(gathered_data[3]))
                    users_output.insert(7.2, '4) D = ' + str(discriminant))
                    users_output.insert(9.2, fraction_writer('5) x = ', ['', '-b ± √D', '2 ⋅ a']))
                    users_output.insert(12.2, fraction_writer('6) x = ', ['', stringPict(str(-gathered_data[2]) + ' ± ',
                                                                                         -1).right(
                        str(root_writer([1, discriminant])))[0], '2 ⋅ ' + str(gathered_data[1])]))
                    if check_int(sqrt(discriminant)):
                        users_output.insert(17.2, fraction_writer('7) x₁ = ', ['', str(-gathered_data[2]) + ' + ' + str(
                            sqrt(discriminant)), str(2.0 * gathered_data[1])]))
                        users_output.insert(21.2, fraction_writer('   x₂ = ', ['', str(-gathered_data[2]) + ' - ' + str(
                            sqrt(discriminant)), str(2.0 * gathered_data[1])]))
                        if check_int((-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1])) and check_int(
                                (-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1])):
                            users_output.insert(25.2, '8) x₁ = ' + str(
                                (-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1])))
                            users_output.insert(27.2, '   x₂ = ' + str(
                                (-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1])))
                        elif check_int((-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1])):
                            users_output.insert(25.2, '9) x₁ = ' + str(
                                (-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1])))
                            users_output.insert(27.2, fraction_writer('   x₂ = ', nice_dividing(
                                -gathered_data[2] + sqrt(discriminant), 2 * gathered_data[1])))
                            if language_change_counter % 2 == 0:  # - Russian
                                users_output.insert(31.2, 'Альтернативный ответ: x₂ = ' + str(
                                    (-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1])))
                            else:
                                users_output.insert(31.2, 'Alternative answer: x₂ = ' + str(
                                    (-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1])))
                        elif check_int((-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1])):
                            users_output.insert(25.2, '9) x₁ = ' + str(
                                (-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1])))
                            users_output.insert(27.2, fraction_writer('   x₂ = ', nice_dividing(
                                -gathered_data[2] - sqrt(discriminant), 2 * gathered_data[1])))
                            if language_change_counter % 2 == 0:  # - Russian
                                users_output.insert(31.2, 'Альтернативный ответ: x₂ = ' + str(
                                    (-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1])))
                            else:
                                users_output.insert(31.2, 'Alternative answer: x₂ = ' + str(
                                    (-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1])))
                        else:
                            users_output.insert(25.2, fraction_writer('9) x₁ = ', nice_dividing(
                                -gathered_data[2] - sqrt(discriminant), 2 * gathered_data[1])))
                            users_output.insert(29.2, fraction_writer('   x₂ = ', nice_dividing(
                                -gathered_data[2] + sqrt(discriminant), 2 * gathered_data[1])))
                            if language_change_counter % 2 == 0:  # - Russian
                                users_output.insert(33.2, 'Альтернативный ответ: x₁ = ' + str(
                                    (-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1])))
                                users_output.insert(34.2, '                      x₂ = ' + str(
                                    (-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1])))
                            else:
                                users_output.insert(33.2, 'Alternative answer: x₁ = ' + str(
                                    (-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1])))
                                users_output.insert(34.2, '                    x₂ = ' + str(
                                    (-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1])))
                    else:
                        split_root = nice_root(discriminant)
                        users_output.insert(16.2, fraction_writer('7) x₁ = ', ['', stringPict(
                            str(-gathered_data[2]) + ' + ', -1).right(root_writer(split_root))[0],
                                                                               str(2.0 * gathered_data[1])]))
                        users_output.insert(20.2, fraction_writer('   x₂ = ', ['', stringPict(
                            str(-gathered_data[2]) + ' - ', -1).right(root_writer(split_root))[0],
                                                                               str(2.0 * gathered_data[1])]))
                        nod_of_num_den = nod(gathered_data[2], split_root[0], 2.0 * gathered_data[1])
                        alt_answ_pos1 = 25.2
                        alt_answ_pos2 = 26.2
                        if nod_of_num_den != 1.0:
                            split_root[0] = split_root[0] / nod_of_num_den
                            alt_answ_pos1 = 33.2
                            alt_answ_pos2 = 34.2
                            if (2.0 * gathered_data[1]) / nod_of_num_den == 1.0:
                                users_output.insert(24.2, stringPict(
                                    '8) x₁ = ' + str(-gathered_data[2] / nod_of_num_den) + ' + ', -1).right(
                                    root_writer(split_root))[0])
                                users_output.insert(28.2, stringPict(
                                    '   x₂ = ' + str(-gathered_data[2] / nod_of_num_den) + ' - ', -1).right(
                                    root_writer(split_root))[0])
                            else:
                                if split_root[0] < 0:
                                    split_root[0] = abs(split_root[0])
                                    users_output.insert(24.2, fraction_writer('8) x₁ = ', ['', stringPict(
                                        str(-gathered_data[2] / nod_of_num_den) + ' - ', -1).right(
                                        root_writer(split_root))[
                                        0], str((2.0 * gathered_data[1]) / nod_of_num_den)]))
                                    users_output.insert(28.2, fraction_writer('   x₂ = ', ['', stringPict(
                                        str(-gathered_data[2] / nod_of_num_den) + ' + ', -1).right(
                                        root_writer(split_root))[
                                        0], str((2.0 * gathered_data[1]) / nod_of_num_den)]))

                                else:

                                    users_output.insert(24.2, fraction_writer('8) x₁ = ', ['', stringPict(
                                        str(-gathered_data[2] / nod_of_num_den) + ' + ', -1).right(root_writer(split_root))[
                                        0], str((2.0 * gathered_data[1]) / nod_of_num_den)]))
                                    users_output.insert(28.2, fraction_writer('   x₂ = ', ['', stringPict(
                                        str(-gathered_data[2] / nod_of_num_den) + ' - ', -1).right(root_writer(split_root))[
                                        0], str((2.0 * gathered_data[1]) / nod_of_num_den)]))

                        if language_change_counter % 2 == 0:  # - Russian
                            users_output.insert(alt_answ_pos1, 'Альтернативный ответ: x₁ = ' + str(
                                (-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1])))
                            users_output.insert(alt_answ_pos2, '                      x₂ = ' + str(
                                (-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1])))
                        else:
                            users_output.insert(alt_answ_pos1, 'Alternative answer: x₁ = ' + str(
                                (-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1])))
                            users_output.insert(alt_answ_pos2, '                    x₂ = ' + str(
                                (-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1])))
    x1_output.delete(0, tk.END)
    x2_output.delete(0, tk.END)
    y_output.delete(0, tk.END)
    x_input.delete(0, tk.END)
    y_input.delete(0, tk.END)
    users_output['state'] = 'disabled'
    x1_output['state'] = 'disabled'
    x2_output['state'] = 'disabled'
    y_output['state'] = 'disabled'


def annotate(text, coord):
    plt.annotate(text, xy=coord, xycoords='data',
                 xytext=[30, 30], fontsize=18, textcoords='offset points', arrowprops=dict(arrowstyle="-|>",
                                                                                           connectionstyle="arc3,rad=.2"))


def draw_the_graph():
    gathered_data = coefficients_sort_of_equation(users_input.get())  # <=== tuple
    entered_equation = equation
    entered_equation = list(entered_equation)
    del entered_equation[-1:-3:-1]
    entered_equation = ''.join(entered_equation)
    fig, ax = plt.subplots()
    ax.axis('equal')
    # make plot pretty
    ax.grid(which='major',
            color='k')
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    ax.xaxis.label.set_color('green')
    ax.yaxis.label.set_color('blue')
    ax.spines['bottom'].set_color('green')
    ax.spines['top'].set_color('green')
    ax.spines['left'].set_color('blue')
    ax.spines['right'].set_color('blue')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_linewidth(3)
    ax.spines['left'].set_linewidth(3)
    ax.minorticks_on()
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    fig.patch.set_facecolor('#98ff98')
    ax.xaxis.grid(True, which='minor')
    ax.yaxis.grid(True, which='minor')

    ax.set_title(entered_equation)
    # find 'x' on the graph
    if gathered_data[0] == 'ax²=0':
        annotate('x', [0, 0])
    elif gathered_data[0] == 'ax²+bx=0':
        annotate('x₁', [0, 0])
        annotate('x₂', [-gathered_data[2] / gathered_data[1], 0])
    elif gathered_data[0] == 'ax²+c=0':
        if -gathered_data[2] / gathered_data[1] < 0:
            pass
        else:
            annotate('x₁', [sqrt(-gathered_data[2] / gathered_data[1]), 0])
            annotate('x₂', [-sqrt(-gathered_data[2] / gathered_data[1]), 0])
    else:
        discriminant = gathered_data[2] ** 2 - 4 * gathered_data[1] * gathered_data[3]
        if discriminant < 0:
            pass
        elif discriminant == 0:
            annotate('x', [-gathered_data[2] / (2 * gathered_data[1]), 0])
        else:
            annotate('x₁', [(-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1]), 0])
            annotate('x₂', [(-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1]), 0])
    # put additional labels
    if language_change_counter % 2 == 0:
        ax.set_xlabel('Ось X', fontsize=16, fontweight='bold')
        ax.set_ylabel('Ось Y', fontsize=16, fontweight='bold')
    else:
        ax.set_xlabel('X-axis', fontsize=16, fontweight='bold')
        ax.set_ylabel('Y-axis', fontsize=16, fontweight='bold')
    plt.xlim(-2.5, 2.5)
    plt.ylim(-6.25, 6.25)
    x = linspace(-40, 40, 1600)
    ax.set_aspect(aspect='equal')
    if gathered_data[0] == 'ax²=0':
        y = gathered_data[1] * x ** 2
    elif gathered_data[0] == 'ax²+bx=0':
        y = (gathered_data[1] * (x ** 2)) + (gathered_data[2] * x)
    elif gathered_data[0] == 'ax²+c=0':
        y = (gathered_data[1] * (x ** 2)) + gathered_data[2]
    else:
        y = (gathered_data[1] * (x ** 2)) + (gathered_data[2] * x) + gathered_data[3]
    # draw the graph
    ax.plot(x, y, 'r-')
    # create widget for the graph
    canvas = FigureCanvasTkAgg(fig, graph_frame)

    # put the graph on the widget
    canvas.draw()
    # show widget for the graph
    toolbar = NavigationToolbar(canvas, graph_frame, pack_toolbar=False)
    toolbar.config(background='#98ff98')
    toolbar._message_label.destroy()
    toolbar.update()
    toolbar.place(x=43, y=420)
    canvas.get_tk_widget().place(x=-35, y=-10)


def graph_drawer():
    global click_counter
    main_frame.pack_forget()
    graph_frame.pack()
    if click_counter < 1:
        draw_the_graph()
    click_counter += 1
    plt.close('all')


def return_to_main():
    graph_frame.pack_forget()
    main_frame.pack()


def calculate():
    y_output['state'] = 'normal'
    x1_output['state'] = 'normal'
    x2_output['state'] = 'normal'
    x1_output.delete(0, tk.END)
    x2_output.delete(0, tk.END)
    y_output.delete(0, tk.END)
    gathered_data = coefficients_sort_of_equation(users_input.get())
    entered_X = x_input.get()
    entered_Y = y_input.get()
    try:
        if bool(entered_X):
            if gathered_data[0] == 'ax²=0':
                y_output.insert(0, gathered_data[1] * float(entered_X) ** 2)
            elif gathered_data[0] == 'ax²+bx=0':
                y_output.insert(0, (gathered_data[1] * (float(entered_X) ** 2)) + (gathered_data[2] * float(entered_X)))
            elif gathered_data[0] == 'ax²+c=0':
                y_output.insert(0, (gathered_data[1] * (float(entered_X) ** 2)) + gathered_data[2])
            else:
                y_output.insert(0, gathered_data[1] * float(entered_X) ** 2 + (gathered_data[2] * float(entered_X)) +
                                gathered_data[3])
        if bool(entered_Y):
            c_coeff = -float(entered_Y)
            if gathered_data[0] == 'ax²=0':
                if -c_coeff < 0:
                    x1_output.insert(0, '∅')
                    x2_output.insert(0, '∅')
                else:
                    x1_output.insert(0, -sqrt(-c_coeff / gathered_data[1]))
                    x2_output.insert(0, sqrt(-c_coeff / gathered_data[1]))
            elif gathered_data[0] == 'ax²+bx=0':
                discriminant = gathered_data[2] ** 2 - 4 * gathered_data[1] * c_coeff
                if discriminant < 0:
                    x1_output.insert(0, '∅')
                    x2_output.insert(0, '∅')
                elif discriminant == 0:
                    x1_output.insert(0, -gathered_data[2] / (gathered_data[1] * 2))
                    x2_output.insert(0, '---')
                else:
                    x1_output.insert(0, (-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1]))
                    x2_output.insert(0, (-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1]))
            elif gathered_data[0] == 'ax²+c=0':
                c_coeff = c_coeff + gathered_data[2]
                if -c_coeff < 0:
                    x1_output.insert(0, '∅')
                    x2_output.insert(0, '∅')
                elif c_coeff == 0:
                    x1_output.insert(0, 0)
                    x2_output.insert(0, '---')
                else:
                    x1_output.insert(0, -sqrt(-c_coeff / gathered_data[1]))
                    x2_output.insert(0, sqrt(-c_coeff / gathered_data[1]))
            else:
                c_coeff = c_coeff + gathered_data[3]
                discriminant = gathered_data[2] ** 2 - 4 * gathered_data[1] * c_coeff
                if discriminant < 0:
                    x1_output.insert(0, '∅')
                    x2_output.insert(0, '∅')
                elif discriminant == 0:
                    x1_output.insert(0, -gathered_data[2] / (gathered_data[1] * 2))
                    x2_output.insert(0, '---')
                else:
                    x1_output.insert(0, (-gathered_data[2] + sqrt(discriminant)) / (2 * gathered_data[1]))
                    x2_output.insert(0, (-gathered_data[2] - sqrt(discriminant)) / (2 * gathered_data[1]))
    except:
        pass
    y_output['state'] = 'disabled'
    x1_output['state'] = 'disabled'
    x2_output['state'] = 'disabled'


# creation of the widgets
# widgets for the main window
users_input = tk.Entry(main_frame, width=41, bg='#f1f1f2', bd=3, font=16, selectbackground='#217ca3',
                       selectforeground='#0f1b07')

users_output = tk.Text(main_frame, width=63, height=16, bg='#f1f1f2', bd=3, font=('Consolas', 16),
                       selectbackground='#217ca3',
                       selectforeground='#0f1b07', state='disabled', wrap='word')

instruction_label = tk.Label(main_frame, fg='#ffffff', font=('Arial Black', 13), text='Enter an equation: ',
                             bg='#4cb5f5')

language_label = tk.Label(main_frame, fg='#ffffff', font=('Arial Black', 16), text='Language: ', bg='#4cb5f5')

theme_label = tk.Label(main_frame, fg='#ffffff', font=('Arial Black', 16), text='Theme: ', bg='#4cb5f5')

creator_label = tk.Label(main_frame, fg='#ffffff', font=('Arial Black', 13), text='Creator - Yehor Mishchyriak ',
                         bg='#4cb5f5')

solve_button = tk.Button(main_frame, fg='#ffffff', bg='#1995ad',
                         activebackground='#217ca3', activeforeground='#ffffff', font=('Arial Black', 14),
                         cursor='hand2', text='SOLVE', bd=4, relief='ridge', height=2, width=10, command=solve)

delete_button = tk.Button(main_frame, fg='White', bg='#1995ad',
                          activebackground='#217ca3', activeforeground='#ffffff', font=('Arial Black', 14),
                          cursor='hand2', text='DELETE', bd=4, relief='ridge', height=2, width=10, command=delete)

square_button = tk.Button(main_frame, fg='#ffffff', bg='#1995ad',
                          activebackground='#217ca3', activeforeground='#ffffff', font=('Arial Black', 14),
                          cursor='hand2', text='2nd POWER', bd=4, relief='ridge', height=2, width=10, command=put_power)

x_button = tk.Button(main_frame, fg='#ffffff', bg='#1995ad',
                     activebackground='#217ca3', activeforeground='#ffffff', font=('Arial Black', 14),
                     cursor='hand2', text='X', bd=4, relief='ridge', height=2, width=10, command=put_x)

language_button = tk.Button(main_frame, fg='#ffffff', bg='#1995ad',
                            activebackground='#217ca3', activeforeground='#ffffff', font=('Arial Black', 13),
                            cursor='hand2', text='Русский', bd=4, relief='ridge', height=1, width=10,
                            command=language_changer)

theme_button = tk.Button(main_frame, fg='#ffffff', bg='#1995ad',
                         activebackground='#217ca3', activeforeground='#ffffff', font=('Arial Black', 13),
                         cursor='spraycan', text='Dark', bd=4, relief='ridge', height=1, width=10,
                         command=theme_changer)
# widgets for the graph window

graph_button = tk.Button(main_frame, fg='#ffffff', bg='#FFA500',
                         activebackground='#D2691E', activeforeground='#ffffff', font=('Arial Black', 13),
                         cursor='hand2', text='Graph it!', bd=4, relief='ridge', height=2, width=20,
                         command=graph_drawer, state='disabled')

return_to_main = tk.Button(graph_frame, fg='#ffffff', bg='green',
                           activebackground='#006400', activeforeground='#ffffff', font=('Arial Black', 14),
                           cursor='hand2', text='Main screen', bd=4, relief='ridge', height=2, width=15,
                           command=return_to_main)

x_input = tk.Entry(graph_frame, width=5, bg='#2E8B57', bd=3, font=16, selectbackground='#217ca3',
                   selectforeground='#0f1b07')
y_output = tk.Entry(graph_frame, width=20, bg='#90EE90', bd=3, font=16, selectbackground='#217ca3',
                    selectforeground='#0f1b07', state='disabled')
text_label_if_x = tk.Label(graph_frame, fg='black', font=('Arial', 14), text='If x =',
                           bg='#98ff98')
text_label_if_y = tk.Label(graph_frame, fg='black', font=('Arial', 14), text='If y =',
                           bg='#98ff98')
x1_output = tk.Entry(graph_frame, width=20, bg='#90EE90', bd=3, font=16, selectbackground='#217ca3',
                     selectforeground='#0f1b07', state='disabled')
x2_output = tk.Entry(graph_frame, width=20, bg='#90EE90', bd=3, font=16, selectbackground='#217ca3',
                     selectforeground='#0f1b07', state='disabled')

y_input = tk.Entry(graph_frame, width=5, bg='#2E8B57', bd=3, font=16, selectbackground='#217ca3',
                   selectforeground='#0f1b07')
comma1 = tk.Label(graph_frame, fg='black', font=('Arial', 16), text=',',
                  bg='#98ff98')
comma2 = tk.Label(graph_frame, fg='black', font=('Arial', 16), text=',',
                  bg='#98ff98')
yequals = tk.Label(graph_frame, fg='black', font=('Arial', 16), text='y =',
                   bg='#98ff98')
x1equals = tk.Label(graph_frame, fg='black', font=('Arial', 16), text='x₁ =',
                    bg='#98ff98')
x2equals = tk.Label(graph_frame, fg='black', font=('Arial', 16), text='x₂ =',
                    bg='#98ff98')
yequals2 = tk.Label(graph_frame, fg='black', font=('Arial', 16), text='y =',
                    bg='#98ff98')
xequals2 = tk.Label(graph_frame, fg='black', font=('Arial', 16), text='x =',
                    bg='#98ff98')
calculate_button = tk.Button(graph_frame, fg='#ffffff', bg='green',
                             activebackground='#006400', activeforeground='#ffffff', font=('Arial Black', 9),
                             cursor='hand2', text='Calculate', bd=4, relief='ridge', height=5, width=13,
                             command=calculate)

# auxiliary variables
theme_change_counter = 1
language_change_counter = 1
click_counter = 0

# lists of widgets
buttons = [solve_button, square_button, x_button, language_button, theme_button, delete_button]
labels = [instruction_label, language_label, theme_label, creator_label]
fields = [users_input, users_output]

# packing of widgets
# main frame
main_frame.pack()
language_label.place(x=1, y=0)
theme_label.place(x=320, y=0)
language_button.place(x=140, y=0)
theme_button.place(x=440, y=0)
instruction_label.place(x=1, y=50)
users_input.place(x=198, y=50)
solve_button.place(x=0, y=95)
delete_button.place(x=144, y=95)
square_button.place(x=288, y=95)
x_button.place(x=432, y=95)
users_output.place(x=0, y=180)
creator_label.place(x=0, y=575)
graph_button.place(x=300, y=576)
# graph frame

text_label_if_x.place(x=40, y=470)
x_input.place(x=125, y=470)
comma1.place(x=180, y=470)
yequals.place(x=190, y=470)
y_output.place(x=240, y=470)
text_label_if_y.place(x=40, y=500)
y_input.place(x=125, y=500)
comma2.place(x=180, y=500)
x1equals.place(x=190, y=500)
x2equals.place(x=190, y=530)
x1_output.place(x=240, y=500)
x2_output.place(x=240, y=530)
calculate_button.place(x=436, y=470)
return_to_main.place(x=190, y=564)

# starting program
win.mainloop()
