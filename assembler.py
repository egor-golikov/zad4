import sys
import json

# Функция для конвертации значений в байты
def to_bytes(value, length):
    return value.to_bytes(length, byteorder='little')

# Загрузка константы
def load_constant(A, B):
    return to_bytes(A, 1) + to_bytes(B, 4)

# Чтение из памяти
def read_memory(A, B):
    return to_bytes(A, 1) + to_bytes(B, 4)

# Запись в память
def write_memory(A, B):
    return to_bytes(A, 1) + to_bytes(B, 4)

# Операция max
def max_operation(A, B):
    return to_bytes(A, 1) + to_bytes(B, 4)

# Ассемблер
def assembler(input_file, output_bin, log_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    binary_instructions = []
    log = []

    for line in lines:
        parts = line.split()
        cmd = parts[0]
        A = int(parts[1])
        B = int(parts[2])

        if cmd == 'LOAD_CONSTANT':
            instruction = load_constant(A, B)
        elif cmd == 'READ_MEMORY':
            instruction = read_memory(A, B)
        elif cmd == 'WRITE_MEMORY':
            instruction = write_memory(A, B)
        elif cmd == 'MAX':
            instruction = max_operation(A, B)
        else:
            raise ValueError(f"Unknown command: {cmd}")

        binary_instructions.append(instruction)
        log.append({'command': cmd, 'A': A, 'B': B})

    with open(output_bin, 'wb') as bin_file:
        bin_file.writelines(binary_instructions)

    with open(log_file, 'w') as log_json:
        json.dump(log, log_json, indent=4)

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_bin = sys.argv[2]
    log_file = sys.argv[3]
    assembler(input_file, output_bin, log_file)
