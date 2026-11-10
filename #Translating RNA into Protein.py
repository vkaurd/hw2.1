#Translating RNA into Protein
import argparse
rna_codon_table = {
    'UUU': 'F', 'CUU': 'L', 'AUU': 'I', 'GUU': 'V',
    'UUC': 'F', 'CUC': 'L', 'AUC': 'I', 'GUC': 'V',
    'UUA': 'L', 'CUA': 'L', 'AUA': 'I', 'GUA': 'V',
    'UUG': 'L', 'CUG': 'L', 'AUG': 'M', 'GUG': 'V',
    'UCU': 'S', 'CCU': 'P', 'ACU': 'T', 'GCU': 'A',
    'UCC': 'S', 'CCC': 'P', 'ACC': 'T', 'GCC': 'A',
    'UCA': 'S', 'CCA': 'P', 'ACA': 'T', 'GCA': 'A',
    'UCG': 'S', 'CCG': 'P', 'ACG': 'T', 'GCG': 'A',
    'UAU': 'Y', 'CAU': 'H', 'AAU': 'N', 'GAU': 'D',
    'UAC': 'Y', 'CAC': 'H', 'AAC': 'N', 'GAC': 'D',
    'UAA': 'Stop', 'CAA': 'Q', 'AAA': 'K', 'GAA': 'E',
    'UAG': 'Stop', 'CAG': 'Q', 'AAG': 'K', 'GAG': 'E',
    'UGU': 'C', 'CGU': 'R', 'AGU': 'S', 'GGU': 'G',
    'UGC': 'C', 'CGC': 'R', 'AGC': 'S', 'GGC': 'G',
    'UGA': 'Stop', 'CGA': 'R', 'AGA': 'R', 'GGA': 'G',
    'UGG': 'W', 'CGG': 'R', 'AGG': 'R', 'GGG': 'G'
}
parser = argparse.ArgumentParser(description='Translating RNA into Protein')
parser.add_argument('-i', '--input', help='Путь к входному файлу с РНК', required=True, type=str) #входной файл
parser.add_argument('output', help='Путь к выходному файлу с белком', type=str) #выходной файл
args = parser.parse_args()

with open(args.input, 'r') as file:
    rna_string = file.readline().strip()

protein_string = ""
for i in range(0, len(rna_string), 3): # идем по строке РНК с шагом 3
    codon = rna_string[i:i+3] # отрезаем 3 буквы
    amino_acid = rna_codon_table[codon] # переводим 3 букв по словарю
    if amino_acid == 'Stop':
        break
    protein_string = protein_string + amino_acid # добавляем букву аминокислоты к белку
    
with open(args.output, 'w') as out_file:
    out_file.write(protein_string + '\n')

print(f"Готово! Результат сохранен в файл: {args.output}")
