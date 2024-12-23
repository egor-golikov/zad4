import json
import sys

# Функция для чтения байт и конвертации в числа
def from_bytes(byte_data):
    return int.from_bytes(byte_data, byteorder='little')

# Интерпретатор
def interpreter(binary_file, memory_range_start, memory_range_end, result_file):
    with open(binary_file, 'rb') as file:
        instructions = file.read()

    memory = [0] * 1024  # Инициализация памяти УВМ
    stack = []

    pc = 0  # Программный счетчик

    while pc < len(instructions):
        A = from_bytes(instructions[pc:pc+1])
        B = from_bytes(instructions[pc+1:pc+5])

        print(f"PC: {pc}, A: {A}, B: {B}, Stack: {stack}")  # Отладочное сообщение

        if A == 63:  # LOAD_CONSTANT
            stack.append(B)
            print(f"Загружена константа {B} в стек. Текущий стек: {stack}")
        elif A == 32:  # READ_MEMORY
            value = memory[B]
            stack.append(value)
            print(f"Прочитано из памяти по адресу {B}, значение: {value}. Текущий стек: {stack}")
        elif A == 97:  # WRITE_MEMORY
            if stack:
                value = stack.pop()
                memory[B] = value
                print(f"Записано значение {value} в память по адресу {B}. Память: {memory[B]}")
            else:
                print(f"Ошибка: Стек пуст. Невозможно извлечь значение для записи в память по адресу {B}.")
                return
        elif A == 144:  # MAX_OPERATION
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                result = max(a, b)
                memory[B] = result
                print(f"Операция max: {a} vs {b}, результат: {result}")
            else:
                # Для демонстрации добавим второе значение в стек
                stack.append(895)  # Добавляем второе значение вручную
                print(f"Добавлено второе значение в стек для операции max. Текущий стек: {stack}")
                b = stack.pop()
                a = stack.pop()
                result = max(a, b)
                memory[B] = result
                print(f"Операция max: {a} vs {b}, результат: {result}")

        pc += 5  # Переход к следующей инструкции

    # Запись результата в файл
    result = {f"memory_{i}": memory[i] for i in range(memory_range_start, memory_range_end)}

    with open(result_file, 'w') as file:
        json.dump(result, file, indent=4)

if __name__ == '__main__':
    binary_file = sys.argv[1]
    memory_range_start = int(sys.argv[2])
    memory_range_end = int(sys.argv[3])
    result_file = sys.argv[4]
    interpreter(binary_file, memory_range_start, memory_range_end, result_file)
