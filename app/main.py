from analysis import get_spark_session
from analysis import query
import os
from itertools import islice
import matplotlib.pyplot as plt


def batched(iterable, n, *, strict=False): # From official itertools docs
    if n < 1:
        raise ValueError('n must be at least one')
    iterator = iter(iterable)
    batch = tuple(islice(iterator, n))
    while batch:
        if strict and len(batch) != n:
            raise ValueError('batched(): incomplete batch')
        yield batch
        batch = tuple(islice(iterator, n))


spark, df = get_spark_session()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

queries = [
        ('MPG vs cylinders',    lambda: query(df, ('mpg', '-'), ('cylinders', '-'))),
        ('MPG vs horsepower',   lambda: query(df, ('mpg', '-'), ('horsepower', '-'))),
        ('horsepower vs weight',lambda: query(df, ('horsepower', '-'), ('weight', '-'))),
        ('MPG vs weight',       lambda: query(df, ('mpg', '-'), ('weight', '-'))),
        ('MPG vs acceleration', lambda: query(df, ('mpg', '-'), ('acceleration', '-'))),
        ('displacement vs MPG', lambda: query(df, ('displacement', '-'), ('mpg', '-')))
]

def print_table(data, headers):
    MAX_ROWS = 20
    data = list(batched(data, MAX_ROWS))
    page = 0
    keep_going_local = True
    while keep_going_local:
        clear()
        print('\n')
        widths = [max(5, max(map(lambda x: len(str(x)), i)) + 2) for i in zip(*([headers] + list(data[page])))]
        page_data = [headers, ['-' * w for w in widths], *data[page]]
        for row in page_data:
            row_cells = []
            for cell, width in zip(row, widths):
                row_cells.append(str(cell) + ' ' * (width - len(str(cell))))
            print('|'.join(row_cells))
        print('\n\t<<', '(p)' if page > 0 else '(#)', '\t\t\t(q - quit)\t\t\t', '(n)' if page < len(data) - 1 else '(#)', '>>')
        print('\t\t', ' ' * 6, f'\t  ({page + 1}/{len(data) + 1})')
        choice = None
        while not(
            (choice == 'p' and page > 0)
            or 
            (choice == 'n' and page < len(data) - 1)
            or 
            choice == 'q'
        ):
            choice = input('>>> ').strip()
        if choice == 'p':
            page -= 1
        elif choice == 'n':
            page += 1
        else:
            keep_going_local = False

message = ''
keep_going = True
while keep_going:
    clear()
    if message:
        print('---', message, '---', '\n')
        message = ''
    print('Available queries:')
    for idx, q in enumerate(queries + [('Custom query', None)]):
        print(f'{idx}: {q[0]}')
    print('------------------------------')
    inp = input(' >>> ').strip()

    if inp in ('exit', 'q'):
        keep_going = False
        continue
    elif inp == 'help':
        print('Available commands:'
          '\thelp - (displays this command)'
          '\texit, q - quits the application'
          f'\tnumbers from 0 to {len(queries) - 1} - executes the selected query'
          f'\t{len(queries)} - allows the user to create a custom query'
        )
    elif inp.isnumeric():
        idx = int(inp)
        if idx < 0 or idx > len(queries):
            message = f'Invalid value: {idx}'
            continue
        elif idx == len(queries):
            clear()
            print('Create a custom query:')
            keep_going_local = True
            avail_cols = ["mpg","cylinders","displacement","horsepower","weight","acceleration"]
            chosen_cols = []
            while keep_going_local:
                choice = ''
                if len(avail_cols) > 0:
                    clear()
                    print('Current query: ')
                    for c, direction in chosen_cols:
                        print('- Column', c, 'ordering', 'ascending' if direction == '+' else 'descending')
                    print('-' * 30)
                    print('Available columns:')
                    print(*[f'{idx + 1}. {i}' for idx, i in enumerate(avail_cols)], sep='\n')
                    print('-' * 30)
                    choice = 'a' 
                    while (not choice.isnumeric() or 1 < int(choice) > len(avail_cols)) and (choice != '' or len(chosen_cols) == 0):
                        if len(chosen_cols) != 2:
                            question_txt = 'Select next column or press enter to evaulate query: '
                        else:
                            question_txt = 'Select next column or press enter to evaluate query or plot the results:' \
                                    '\n\tp - plot all data points' \
                                    '\n\tpl - plot all data points with labels' \
                                    '\n\tp [number] - plot top [number] data points' \
                                    '\n\tpl [number] - plot top [number] data points with labels' \
                                    '\n>>> '
                        choice = input(question_txt).strip()
                        if len(chosen_cols) == 2 and choice.startswith('p'):
                            if choice in ('p', 'pl'):
                                break 
                            if choice.split()[0] in ('p', 'pl'):
                                if choice.split()[1].isnumeric():
                                    break
                if choice != '':
                    if choice.startswith('p'):
                        keep_going_local = False
                        show_type = choice.split()[0]
                        limit = None if len(choice.split()) == 1 else int(choice.split()[1])
                        res = query(df, *chosen_cols)
                        rows = res.collect() 
                        if limit is not None:
                            rows = rows[:limit]
                        x = [i[chosen_cols[0][0]] for i in rows]
                        y = [i[chosen_cols[1][0]] for i in rows]
                        labels = None
                        if choice.startswith('pl'):
                            labels = [f"{r['name']}({r['origin']})" for r in rows]
                        clear() 
                        plt.scatter(x, y, marker='o', color='blue')
                        if labels is not None:
                            for xx, yy, l in zip(x, y, labels):
                                plt.text(xx, yy, l, fontsize=6)
                        plt.savefig('./fig.jpg')
                        plt.show()
                        input('Figure has been saved, press enter to continue...')
                        clear() 
                    else:
                        choice = int(choice) - 1
                        print(f'Evaluating column {avail_cols[choice]}. Choose ordering:\n1. Ascending\n2. Descending')
                        ordering_choice = 'a'
                        while ordering_choice not in '12':
                            ordering_choice = input('Ordering: ').strip()
                            chosen_cols.append((avail_cols[choice], '+' if ordering_choice == '1' else '-'))
                            avail_cols = [i for idx, i in enumerate(avail_cols) if idx != choice]
                        print('Chosen ordering', 'ascending' if ordering_choice == '1' else 'descending')
                else:
                    keep_going_local = False
                    res = query(df, *chosen_cols)
                    cols = res.columns
                    rows = res.collect()
                    print_table(rows, cols)

        else:
            res = queries[idx][1]()
            cols = res.columns
            rows = res.collect()
            rows = [[r[c] for c in cols] for r in rows]
            print_table(rows, cols)
            continue

spark.stop()
clear()
