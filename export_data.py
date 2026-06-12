from  main import Parser
import sqlite3
import pandas as pd

def to_sqlite(data,db_name='parsing_results'):
    connection = sqlite3.connect(f'outputs/{db_name}.db')
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Parse_results (
    Id INTEGER PRIMARY KEY,
    Organization TEXT NOT NULL,
    Address TEXT NOT NULL,
    Phone_number TEXT NOT NULL,
    URL_on_maps TEXT NOT NULL,
    URL_site TEXT NOT NULL,
    Keywords TEXT NOT NULL
    )
    """)

    query = 'INSERT OR REPLACE INTO Parse_results (Id, Organization, Address, Phone_number, URL_on_maps, URL_site, Keywords) VALUES (?, ?, ?, ?, ?, ?, ?)'

    cursor.executemany(query,data)

    connection.commit()
    connection.close()


def to_excel(data,path='outputs/parsing_results.xlsx'):
    df = pd.DataFrame(data)

    with pd.ExcelWriter(path, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

if __name__ == '__main__':
    parser = Parser(url='https://yandex.ru/maps', place='Ярославль', institution='Больницы')
    parser.parse()

    result = parser.get_result()
    to_excel(result)
    result = [x for x in zip( range(1, len(result['Название']) + 1), *result.values() )]
    to_sqlite(result)


