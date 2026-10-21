import math
exp= input('Введите выражение: ')
exp= exp.replace(' ', '')
if exp=='':
    print('Ошибка: выражение не введено')
    exit()
tokens = []
i = 0

while i < len(exp): # Повторяем действия пока не дойдём до конца строки
    char = exp[i]

    if char.isspace(): # Пропускаем пробелы
        i += 1

    # Проверяем начинается ли строка текста floor начиная с позиции i
    elif exp.startswith('floor', i): 
        tokens.append('floor')
        i += 5

    # Проверяем начинается ли выражение с меньшей или равно в текущей позиции
    elif exp.startswith('>=', i): 
        tokens.append('>=') # Побавляем оператор в список одним элементом
        i += 2 # Перемещаем счётчик на два символа вперёд

    # Проверяем, является ли текущий символ цифрой или точкой
    elif char.isdigit() or char == '.':
        num = ''

        while i < len(exp) and (
            exp[i].isdigit() or exp[i] == '.'
        ):
            num += exp[i]
            i += 1

        tokens.append(num)

    elif char in '+-*/()':
        tokens.append(char)
        i += 1

    else:
        raise ValueError(f'Неизвестный символ: {char}')

def calculate(tokens):
    # Обрабатываем унарный плюс и минус
    index = 0

    while index < len(tokens):
        if tokens[index] in ('+', '-'):
             # Определяем, является ли знак унарным
            if index == 0 or tokens[index - 1] in ('+', '-', '*', '/', '(', '>='):

                # Если знак минус, меняем знак следующего числа
                if tokens[index] == '-':
                    tokens[index + 1] = str(-float(tokens[index + 1]))
                del tokens[index] # Удаляем обработанный унарный знак из списка
            else:
                index += 1
        else:
            index += 1


    while '*' in tokens or '/' in tokens:
        for index, token in enumerate(tokens):
            if token=='*' or token=='/':
                left= float(tokens[index-1])
                right= float(tokens[index+1])

                if token=='*':
                    result= left*right
                elif token=='/':
                    result=left/right
    
                del tokens[index-1:index+2]
                tokens.insert(index-1, str(result))
                break   

    while '+' in tokens or '-' in tokens:
        for index, token in enumerate(tokens):
            if token=='+' or token=='-':
                left= float(tokens[index-1])
                right= float(tokens[index+1])

                if token=='+':
                    result= left + right
                elif token=='-':
                    result= left - right

                del tokens[index-1:index+2]
                tokens.insert(index-1, str(result))
                break

    if '>=' in tokens:
        index = tokens.index('>=')

        left = float(tokens[index - 1])
        right = float(tokens[index + 1])
        return left >= right

    return float(tokens[0])

def calculate_brackets(tokens):
    stack = []
    # Проверяем все токены на правильность скобок
    for token in tokens:
        if token == '(':
            stack.append(token)
        elif token == ')':
            # Если стек пуст, значит закрывающей скобке не соответствует открывающая
            if not stack:
                raise ValueError('Ошибка: лишняя закрывающая скобка')
            stack.pop()# Удаляем последнюю открывающую скобку из стека
    # Если в стеке остались скобки, значит не хватает закрывающей
    if stack:
        raise ValueError('Ошибка: отсутствует закрывающая скобка')
    if tokens.count('(') != tokens.count(')'):
        raise ValueError('Ошибка: скобки не согласованы')

    while '(' in tokens:
        open_index = None
        close_index = None
  
        for index, token in enumerate(tokens):
            if token == '(':
                open_index = index
            elif token == ')':
                close_index = index
                break

        inside = tokens[open_index + 1:close_index] # Выражение внутри скобок
        result = calculate(inside) # Результат вычисления внутри скобок
        # Проверяем стоит ли перед скобкой Floor
        if open_index>0 and tokens[open_index-1] == 'floor':
            result=math.floor(result)

            del tokens[open_index-1]

            open_index -=1
            close_index-=1
        # Удаляем всё от Floor (если он есть) или от открывающей скобки до закрывающей
        del tokens[open_index:close_index+1]
        # Вставляем результат на место удалённых элементов
        tokens.insert(open_index, str(result))
    
    return calculate(tokens)
    
try:
    answer=calculate_brackets(tokens)
    print(answer)
except ZeroDivisionError:
    print('Ошибка: на ноль делить нельзя!')
except ValueError as error:
    print(error)