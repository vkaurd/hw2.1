import argparse

parser = argparse.ArgumentParser(description="Consensus and Profile")
parser.add_argument('-i', '--input', required=True, type=str)
parser.add_argument('output', type=str)
args = parser.parse_args()

dna_strings = []
current_dna = ""

with open(args.input, 'r') as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        # строка начинается с '>', это заголовок FASTA
        if line.startswith('>'):
            if current_dna != "":
                dna_strings.append(current_dna)
                current_dna = ""
        else:
            # Склеиваем ДНК
            current_dna = current_dna + line
            
    # последн ДНК из файла
    if current_dna != "":
        dna_strings.append(current_dna)

# длинa одной ДНК (первого элемента)
n = len(dna_strings[0])

# 2. Создаем 4 простых списка из нулей вместо структуры profile
count_A = [0] * n
count_C = [0] * n
count_G = [0] * n
count_T = [0] * n

# считаем буквы: бежим по каждой ДНК и индексу
for dna in dna_strings:
    for i in range(n):
        nucleotide = dna[i]
        # Проверяем букву и добавляем +1 в нужный список
        if nucleotide == 'A':
            count_A[i] = count_A[i] + 1
        elif nucleotide == 'C':
            count_C[i] = count_C[i] + 1
        elif nucleotide == 'G':
            count_G[i] = count_G[i] + 1
        elif nucleotide == 'T':
            count_T[i] = count_T[i] + 1

# 3. Составляем final строку
final_string = ""
for i in range(n):
    # Достаем значения для текущей позиции i из каждого списка
    a = count_A[i]
    c = count_C[i]
    g = count_G[i]
    t = count_T[i]
    
    # max число среди 4 букв
    max_count = max(a, c, g, t)
    
    # какая буква дала макс
    if max_count == a:
        final_string = final_string + "A"
    elif max_count == c:
        final_string = final_string + "C"
    elif max_count == g:
        final_string = final_string + "G"
    elif max_count == t:
        final_string = final_string + "T"

# 4. Записываем результаты в выходной файл
with open(args.output, 'w') as out_file:
    out_file.write(final_string + '\n')
    
    str_A = "A:"
    for number in count_A:
        str_A = str_A + " " + str(number)
    out_file.write(str_A + '\n')
    
    str_C = "C:"
    for number in count_C:
        str_C = str_C + " " + str(number)
    out_file.write(str_C + '\n')
    
    str_G = "G:"
    for number in count_G:
        str_G = str_G + " " + str(number)
    out_file.write(str_G + '\n')
    
    str_T = "T:"
    for number in count_T:
        str_T = str_T + " " + str(number)
    out_file.write(str_T + '\n')

print(f"Done! Saved to {args.output}")
