# from data_access.MySQLConnector import MySQLConnector
from mysql.connector import Error
from models.product import Product


class MySQLService:
    add_product = (
        "INSERT INTO products "
        "(productId, productStore, additionDate, lastUpdateDate, isProductActive, productUrl) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )

    def __init__(self, mysql_connector):
        self.mysql_connector = mysql_connector

    def test_connection(self):
        try:
            connection = self.mysql_connector.get_connection()
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    def get_rows(self, query) -> list[Product]:
        connection = self.mysql_connector.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        products = []
        for row in rows:
            # Db is only retrieving id and url the rest is set at
            # this point
            product = Product(
                productId=row["productId"],
                productUrl=row["productUrl"],
                additionDate=None,
                isProductActive=None,
                lastUpdateDate=None,
                productStore=row.get("productStore", None),
                productImage=row.get("productImage", None),
                highestPrice=row.get("highestPrice", None),
                lowestPrice=None,
                currentPrice=None,
                priceHistory=None,
            )
            products.append(product)
        return products

    def update_row(self, query, params):
        connection = self.mysql_connector.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        cursor.close()

    def insert_row(self, params):
        connection = self.mysql_connector.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            self.add_product,
            (
                params["productId"],
                params["productStore"],
                params["additionDate"],
                params["lastUpdateDate"],
                params["isProductActive"],
                params["productUrl"],
            ),
        )
        connection.commit()
        cursor.close()


#         rows = mysql_service.get_rows("SELECT * FROM tu_tabla")
# print(rows)

# mysql_service.update_row("UPDATE products SET price = %s WHERE id = %s", (nuevo_precio, id))
