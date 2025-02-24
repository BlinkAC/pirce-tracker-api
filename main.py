from data_access.MySQLConnector import MySQLConnector
from data_access.CosmosDbConnector import CosmosDbConnector

# from services.DatabaseService import MySQLService
# from services.CosmosDbService import CosmosDbService
from services.CosmosDbService import CosmosDbService
from services.DataProcessorService import DataProcessorService

# from bs4 import BeautifulSoup
# import requests


from __init__ import create_app

# from services.DatabaseService import MySQLService

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

# mysql_connector = MySQLConnector(app["config"]["mysql"])

# # Crear instancia del servicio de productos
# mysql_service = MySQLService(mysql_connector)

# # Crear instancia del conector de la base de datos Cosmos DB
# db_connector = CosmosDbConnector(
#     app["config"]["cosmosDbClient"]["accountEndpoint"],
#     app["config"]["cosmosDbClient"]["primaryKey"],
#     app["config"]["cosmosDbClient"]["database_name"],
#     app["config"]["cosmosDbClient"]["container_name"],
# )

# #    Crear instancia del servicio de productos
# product_service = CosmosDbService(db_connector)

# data_processor_service = DataProcessorService(product_service)


# # TODO ESTO SERA LA CLOUD FUNCTION
# rows = mysql_service.get_rows(
#     "SELECT productId, productUrl FROM products WHERE isProductActive = 1"
# )
# print("Se obtuvieron {} productos".format(len(rows)))

# headers = requests.utils.default_headers()
# headers.update(
#     {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
#     }
# )

# for row in rows:
#     productDocument = product_service.get_product(row.productId)
#     for proxy in app["config"]["proxies"]:
#         proxies = {"http": proxy}
#         try:
#             print("Trying request {} with proxy {}".format(row.productId, proxy))
#             response = requests.get(
#                 row.productUrl,
#                 headers=headers,
#                 proxies=proxies,
#                 timeout=30,
#             )
#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.content, "html.parser")
#                 ml_price_container = soup.find(
#                     "div", class_="ui-pdp-price__second-line"
#                 )

#                 ml_image_container = soup.find("div", class_="ui-pdp-gallery__column")
#                 image_span = ml_image_container.find(
#                     "span", class_="ui-pdp-gallery__wrapper"
#                 )
#                 image_url = image_span.find("img")["src"]

#                 if ml_price_container:
#                     fraction_span = ml_price_container.find(
#                         "span", class_="andes-money-amount__fraction"
#                     )
#                     if fraction_span:
#                         current_price = float(fraction_span.text.replace(",", ""))
#                         if productDocument is not None:
#                             data_processor_service.process_data(
#                                 product=productDocument,
#                                 actualPrice=current_price,
#                             )
#                         else:
#                             print(
#                                 "No se encontró el producto en CosmosDB, agregando..."
#                             )
#                             product_service.add_product(
#                                 row.productId,
#                                 row.productStore,
#                                 current_price,
#                                 current_price,
#                                 current_price,
#                                 image_url,
#                             )
#                     else:
#                         print(
#                             "No se encontró el elemento <span> con la clase 'andes-money-amount__fraction'."
#                         )
#                 else:
#                     print(
#                         "No se encontró el contenedor con la clase 'ui-pdp-price__second-line'."
#                     )

#             break
#         except requests.exceptions.RequestException as e:
#             print(
#                 f"Request failed with proxy {proxy}: {str(e)} - Retrying with next proxy..."
#             )
#             continue
# TODO: para que sea funcional
# ver la forma de mejorar las condiciones
# ver la forma de implementar el uso de logs en vez de print
# ver la forma de implementar el uso de variables de entorno en vez de archivos de ['config']uracion

# evaluar si seguir con la implementacion de dependencias por el contructor o usar inyeccion de dependencias con libreria

# entender como funciona el codigo asincrono para verificar la forma en la que: se pueda hacer varias peticiones a la vez,
# actualizar los documentos y ejecutar las actualizaciones necesarias en cosmos

# ver donde o que parte exactamente ejecutara la se;al de la actualizacion de precios
# el seteo en azure de mysql, cosmos y de la azure funcion que alojara el codigo con un scheduler

# A futuro dependiendo se si lo sigo usando
# logica para diferentes tiendas -> se podria hacer una clase por tienda que herede de una clase padre y que busquen etiquetas en especifico por tienda
# comprar proxies privados para evitar el bloqueo de la ip
#
