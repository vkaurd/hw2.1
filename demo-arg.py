import argparse
from sequence_reader import FastaReader, FastqReader
from vcf_reader import VcfReader
from sam_reader import SamReader

parser = argparse.ArgumentParser(description="Анализ биоинформатических файлов (FASTA, FASTQ, SAM, VCF).")
parser.add_argument('-i', '--input', help="Путь к тестируемому файлу", required=True, type=str)
parser.add_argument('-f', '--format', help="Формат файла (fasta, fastq, sam, vcf)", required=True, type=str, choices=['fasta', 'fastq', 'sam', 'vcf'])

args = parser.parse_args()

# Забираем переданные значения в привычные переменные
filename = args.input
file_format = args.format

print("=" * 33)
print(f"Анализируем файл: {filename} (формат: {file_format})")
print("=" * 33)

'''
    Часть для vcf-файлов.
'''
if file_format == "vcf":
    r = VcfReader(filename)
    r._load_header()

    print("Мета-строки:")
    for m in r.get_meta_lines():
        print("  ", m)

    print("\nINFO ID:", " ".join(r.get_group_ids("INFO")))
    print("FORMAT ID:", " ".join(r.get_group_ids("FORMAT")))
    print("FILTER ID:", " ".join(r.get_group_ids("FILTER")))
    print("contig ID:", " ".join(r.get_group_ids("contig")))

    print("\nfileformat:", r.get_meta_value("fileformat"))
    print("source:", r.get_meta_value("source"))
    print("contig (простой ключ):", r.get_meta_value("contig"))

    print("\nКолонки:", " ".join(r.get_columns()))
    print("Кол-во вариантов:", r.count_variants())

    print("\nСтатистика по регионам (окно 100000):")
    stats = r.region_count_stats(bin_size=100000)
    print(stats)

    n = sum(1 for _ in r.get_region("1", 9000001, 9100000))
    print(f"\nВариантов в 1:9000001-9100000 = {n}")

'''
    Часть для sam-файлов.
'''
if file_format == "sam":
    r = SamReader(filename)
    r._load_header()

    print("Мета-строки:")
    for m in r.get_meta_lines():
        print(" ", m)

    print("\nPG ID:", " ".join(r.get_group_ids("PG")))
    print("RG ID:", " ".join(r.get_group_ids("RG")))
    print("SQ ID:", " ".join(r.get_group_ids("SQ")))

    print("\nКол-во выравниваний:", r.count_records())

    print("\nСтатистика по хромосомам:")
    stats = r.chromosome_stats()
    print(stats)

    print("\nВыравнивания в регионе chr1:100-500:")
    n = sum(1 for _ in r.get_region("chr1", 100, 500))
    print(f"Кол-во выравниваний в chr1:100-500 = {n}")

'''
    ЧАСТЬ ДЛЯ FASTA
'''
if file_format == "fasta":
    r = FastaReader(filename)
    
    count = r.get_sequences_count()
    print("Количество последовательностей в файле:")
    print(count)
    
    avg_len = r.get_average_length()
    print("Средняя длина последовательностей:")
    print(avg_len)

'''
    ЧАСТЬ ДЛЯ FASTQ
'''
if file_format == "fastq":
    r = FastqReader(filename)
    
    count = r.get_sequences_count()
    print("Количество последовательностей в файле:")
    print(count)
    
    avg_len = r.get_average_length()
    print("Средняя длина последовательностей:")
    print(avg_len)
    
    print("Строим и сохраняем график качества...")
    r.plot_quality()

#python3 demo-arg.py -i Human_DNA_fragment.fasta -f fasta
#python3 demo-arg.py -i 88_1_9001000-10001000_fullgenome.vcf -f vcf
#python3 demo-arg.py -i sample.sam -f sam
#python3 demo-arg.py -i 88_1_9001000-10001000_fullgenome.vcf -f vcf
