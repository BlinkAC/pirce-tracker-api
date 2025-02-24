from datetime import datetime
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from data_access.CosmosDbConnector import CosmosDbConnector
from data_access.MySQLConnector import MySQLConnector
from models.schemas.ProductSchema import ProductSchema
from services.CosmosDbService import CosmosDbService
from services.DataProcessorService import DataProcessorService
from services.DatabaseService import MySQLService


def register_routes(app):
    # Crear instancia del conector de la base de datos Mysql
    mysql_connector = MySQLConnector(app.config["mysql"])

    # Crear instancia del servicio de productos
    mysql_service = MySQLService(mysql_connector)

    # Crear instancia del conector de la base de datos Cosmos DB
    db_connector = CosmosDbConnector(
        app.config["cosmosDbClient"]["accountEndpoint"],
        app.config["cosmosDbClient"]["primaryKey"],
        app.config["cosmosDbClient"]["database_name"],
        app.config["cosmosDbClient"]["container_name"],
    )

    #    Crear instancia del servicio de productos
    product_service = CosmosDbService(db_connector)

    data_processor_service = DataProcessorService(product_service)

    @app.route("/api/get-simple-data", methods=["GET"])
    def mysql_simple_data():
        data = mysql_service.get_rows(
            "SELECT productId, productUrl FROM products WHERE isProductActive = 1"
        )
        product_schema = ProductSchema(many=True)
        result = product_schema.dump(data)
        return jsonify(result)

    @app.route("/api/insert-product", methods=["POST"])
    def mysql_insert_product():
        date = datetime.now().isoformat()
        data = request.get_json()
        product_id = data.get("productId")

        product = mysql_service.insert_row(
            {
                "productId": product_id,
                "productStore": data.get("productStore"),
                "additionDate": date,
                "lastUpdateDate": date,
                "isProductActive": 1,
                "productUrl": data.get("productUrl"),
            }
        )
        return {"product inserted": f"{product_id}!"}, 200

    @app.route("/api/get-product-history", methods=["GET"])
    def cosmos_get_product():
        product_id = request.args.get("productId")
        product_store = request.args.get("productStore")
        product = product_service.get_product(product_id, product_store)
        product_schema = ProductSchema()
        result = product_schema.dump(product)
        return jsonify(result)

    # @app.route("/api/trigger-update", methods=["GET"])
    # def trigger_update():
    #     rows = mysql_service.get_rows(
    #         "SELECT productId, productUrl FROM products WHERE isProductActive = 1"
    #     )
    #     print("Se obtuvieron {} productos".format(len(rows)))

    #     headers = request.utils.default_headers()
    #     headers.update(
    #         {
    #             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    #         }
    #     )

    #     for row in rows:
    #         productDocument = product_service.get_product(row.productId,)
    #         for proxy in app.config["proxies"]:
    #             proxies = {"http": proxy}
    #             try:
    #                 print(
    #                     "Trying request {} with proxy {}".format(row.productId, proxy)
    #                 )
    #                 response = request.get(
    #                     row.productUrl,
    #                     headers=headers,
    #                     proxies=proxies,
    #                     timeout=30,
    #                 )
    #                 if response.status_code == 200:
    #                     soup = BeautifulSoup(response.content, "html.parser")
    #                     ml_price_container = soup.find(
    #                         "div", class_="ui-pdp-price__second-line"
    #                     )

    #                     ml_image_container = soup.find(
    #                         "div", class_="ui-pdp-gallery__column"
    #                     )
    #                     image_span = ml_image_container.find(
    #                         "span", class_="ui-pdp-gallery__wrapper"
    #                     )
    #                     image_url = image_span.find("img")["src"]

    #                     if ml_price_container:
    #                         fraction_span = ml_price_container.find(
    #                             "span", class_="andes-money-amount__fraction"
    #                         )
    #                         if fraction_span:
    #                             current_price = float(
    #                                 fraction_span.text.replace(",", "")
    #                             )
    #                             if productDocument is not None:
    #                                 data_processor_service.process_data(
    #                                     product=productDocument,
    #                                     actualPrice=current_price,
    #                                 )
    #                             else:
    #                                 print(
    #                                     "No se encontró el producto en CosmosDB, agregando..."
    #                                 )
    #                                 product_service.add_product(
    #                                     row.productId,
    #                                     row.productStore,
    #                                     current_price,
    #                                     current_price,
    #                                     current_price,
    #                                     image_url,
    #                                 )
    #                         else:
    #                             print(
    #                                 "No se encontró el elemento <span> con la clase 'andes-money-amount__fraction'."
    #                             )
    #                     else:
    #                         print(
    #                             "No se encontró el contenedor con la clase 'ui-pdp-price__second-line'."
    #                         )

    #                 break
    #             except request.exceptions.RequestException as e:
    #                 print(
    #                     f"Request failed with proxy {proxy}: {str(e)} - Retrying with next proxy..."
    #                 )
    #                 continue
    #     return {"product inserted"}, 200


# cnx = mysql.connector.connect(user="alexisChavarriaAdmin", password="{your_password}", host="products-cn.mysql.database.azure.com", port=3306, database="{your_database}", ssl_ca="{ca-cert filename}", ssl_disabled=False)
