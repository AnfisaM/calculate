import math
exp= input('Введите выражение: ')
exp= exp.replace(' ', '')
if exp=='':
    print('Ошибка: выражение не введено')
    exit()
tokens = []
i = 0

while i < len(exp): #повторяем действия пока не дойдём до конца строки
    char = exp[i]

    if char.isspace(): #пропускаем пробелы
        i += 1

    elif exp.startswith('floor', i): #проверяем начинается ли строка текста floor начиная с позиции i
        tokens.append('floor')
        i += 5

    elif exp.startswith('>=', i):#проверяем начинается ли выражение с меньшей или равно в текущей позиции
        tokens.append('>=')#добавляем оператор в список одним элементом
        i += 2 #перемещаем счётчик на два символа вперёд

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
        raise ValueError(
            f'Неизвестный символ: {char}'
        )


def calculate(tokens):
        # Обрабатываем унарный плюс и минус
    index = 0

    while index < len(tokens):
        if tokens[index] in ('+', '-'):
            if index == 0 or tokens[index - 1] in (
                '+', '-', '*', '/', '(', '>='
            ):
                if tokens[index] == '-':
                    tokens[index + 1] = str(
                        -float(tokens[index + 1])
                    )

                del tokens[index]

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

    for token in tokens:
        if token == '(':
            stack.append(token)
        elif token == ')':
            if not stack:
                raise ValueError('Ошибка: лишняя закрывающая скобка')
            stack.pop()

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

        inside = tokens[open_index + 1:close_index]#выражение внутри скобок
        result = calculate(inside) #результат вычисления внутри скобок
        #проверяем стоит ли перед скобкой Floor
        if open_index>0 and tokens[open_index-1] == 'floor':
            result=math.floor(result)

            del tokens[open_index-1]

            open_index -=1
            close_index-=1
        #удаляем всё от Floor (если он есть) или от открывающийся скобки до закрывающей
        del tokens[open_index:close_index+1]
        #вставляем результат на место удалённых элементов
        tokens.insert(open_index, str(result))
    
    return calculate(tokens)
    
try:
    answer=calculate_brackets(tokens)
    print(answer)

except ZeroDivisionError:
    print('Ошибка: на ноль делить нельзя!')
except ValueError as error:
    print(error)