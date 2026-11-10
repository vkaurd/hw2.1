import click
from sequence_reader import FastaReader, FastqReader
from vcf_reader import VcfReader
from sam_reader import SamReader

# Общая опция для всех команд (как output_option в методичке)
input_option = click.option("-i", "--input", "filename", required=True, type=str, help="Путь к тестируемому файлу")


@click.group()
def main():
    """Анализ биоинформатических файлов (FASTA, FASTQ, SAM, VCF)."""
    pass


# ---------- КОМАНДА ДЛЯ VCF ----------
@main.command()
@input_option
def vcf(filename):
    """Анализ VCF файла."""
    print("=" * 33)
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


# ---------- КОМАНДА ДЛЯ SAM ----------
@main.command()
@input_option
def sam(filename):
    """Анализ SAM файла."""
    print("=" * 33)
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


# ---------- КОМАНДА ДЛЯ FASTA ----------
@main.command()
@input_option
def fasta(filename):
    """Анализ FASTA файла."""
    r = FastaReader(filename)

    count = r.get_sequences_count()
    print("Количество последовательностей в файле:")
    print(count)

    avg_len = r.get_average_length()
    print("Средняя длина последовательностей:")
    print(avg_len)


# ---------- КОМАНДА ДЛЯ FASTQ ----------
@main.command()
@input_option
def fastq(filename):
    """Анализ FASTQ файла."""
    r = FastqReader(filename)

    count = r.get_sequences_count()
    print("Количество последовательностей в файле:")
    print(count)

    avg_len = r.get_average_length()
    print("Средняя длина последовательностей:")
    print(avg_len)

    print("Строим и сохраняем график качества...")
    r.plot_quality()


if __name__ == "__main__":
    main()

#python3 demo-click.py --help
#python3 demo-click.py fasta -i Human_DNA_fragment.fasta
#python3 demo-click.py fastq -i "1_control_18S_2019_minq7 - Copy.fastq"
#python3 demo-click.py sam -i sample.sam
#python3 demo-click.py vcf -i 88_1_9001000-10001000_fullgenome.vcf
