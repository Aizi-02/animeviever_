from clickhouse_driver import Client
import clickhouse_driver




client = Client(host='localhost',database = "animeviever")




print(client.execute('SHOW TABLES'))