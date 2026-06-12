from  main import Parser
import sqlite3

connection = sqlite3.connect('outputs/parsing_results.db')
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

parser = Parser(url='https://yandex.ru/maps',place='Ярославль',institution='Больницы')
parser.parse()

result = parser.get_result()
result = [
    x for x in zip( range(1,len(result['Название'])+1) , *result.values() )
]

cursor.executemany(query,result)

connection.commit()
connection.close()

if __name__ == '__main__':
    pass