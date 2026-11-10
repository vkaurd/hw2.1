import argparse

parser = argparse.ArgumentParser(description="Finding a Motif in DNA")
# Входной файл
parser.add_argument('-i', '--input', help="Путь к входному файлу с ДНК", required=True, type=str)
# Выходной файл
parser.add_argument('output', help="Путь к выходному файлу для результата", type=str)
args = parser.parse_args()

with open(args.input, 'r') as file:
    s = file.readline().strip()  # Основная строка ДНК 
    t = file.readline().strip()  # Мотив, который ищем 

positions = []
# Длина основной строки и мотивa
len_s = len(s)
len_t = len(t)

# Вычитаем len_t и прибавляем 1, чтобы не выходить за границы строки
for i in range(len_s - len_t + 1):
    # Вырезаем кусок строки s такой же длины, как мотив t
    window = s[i:i+len_t]
    
    # Если совпало с мотивом
    if window == t:
        # Добавляем индекс в список, прибавляя 1, нуммерация
        positions.append(str(i + 1))

# oбъединяем все позиции через пробел, просит Rosalind
result_string = " ".join(positions)

with open(args.output, 'w') as out_file:
    out_file.write(result_string + '\n')

print(f"Готово! Результаты поиска сохранены в: {args.output}")
