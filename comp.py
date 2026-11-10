import argparse

parser = argparse.ArgumentParser(description="Connected Components using Component Labeling")
parser.add_argument('-i', '--input', required=True, type=str)
parser.add_argument('output', type=str)
args = parser.parse_args()

with open(args.input, 'r') as file:
    # Читаем первую строку и узнаем количество вершин v и ребер e
    first_line = file.readline().strip().split()
    v = int(first_line[0])
    e = int(first_line[1])

    # Создаем список меток компонентов, где изначально каждая вершина изолирована
    component_labels = []
    for i in range(v + 1):
        component_labels.append(i)

    # Читаем ребра из файла и объединяем связанные вершины в общие компоненты
    for line in file:
        line = line.strip()
        if not line:
            continue
        edge = line.split()
        u = int(edge[0])
        w = int(edge[1])
        
        label_u = component_labels[u]
        label_w = component_labels[w]
        
        # Если вершины принадлежат разным компонентам, объединяем их в один компонент
        if label_u != label_w:
            for k in range(1, v + 1):
                if component_labels[k] == label_w:
                    component_labels[k] = label_u

# 3. Переносим уникальные метки в множество, чтобы убрать дубликаты
unique_components = set()
for i in range(1, v + 1):
    unique_components.add(component_labels[i])

result = len(unique_components)

with open(args.output, 'w') as out_file:
    out_file.write(str(result) + '\n')

print(f"Done! Saved to {args.output}")
