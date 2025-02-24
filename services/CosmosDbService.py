from data_access.CosmosDbConnector import CosmosDbConnector
from datetime import datetime
from models.product import Product
from azure.cosmos import CosmosDict
from typing import List, Any


class CosmosDbService:
    def __init__(self, db_connector: CosmosDbConnector):
        self.db_connector = db_connector

    def add_product(
        self,
        product_id,
        store,
        highest_price,
        lowest_price,
        current_price,
        productImage=None,
    ):
        item = {
            "id": product_id,
            "productStore": store,
            "additionDate": datetime.now().isoformat(),
            "lastUpdateDate": datetime.now().isoformat(),
            "highestPrice": highest_price,
            "lowestPrice": lowest_price,
            "currentPrice": current_price,
            "productImage": productImage,
            "priceHistory": [
                {"price": current_price, "date": datetime.now().isoformat()}
            ],
        }
        self.db_connector.upsert_item(item)

    def get_product(self, product_id, product_store) -> CosmosDict:
        document = self.db_connector.read_item(
            item_id=product_id, partition_key=(product_id, product_store)
        )

        return document
        # product = Product(
        #     productId=document["id"],
        #     lastUpdateDate=document["lastUpdateDate"],
        #     productImage=document["productImage"],
        #     highestPrice=document["highestPrice"],
        #     lowestPrice=document["lowestPrice"],
        #     currentPrice=document["currentPrice"],
        #     priceHistory=document["priceHistory"],
        #     productStore=document["productStore"],
        #     productUrl=None,
        #     additionDate=None,
        #     isProductActive=None,
        # )
        # return dict(product)

    def delete_product(self, product_id):
        self.db_connector.delete_item(item_id=product_id, partition_key=product_id)

    def query_products(self, query) -> list[Product]:
        rows = self.db_connector.query_items(query=query)
        products = []
        for row in rows:
            product = Product(
                productId=row["id"],
                lastUpdateDate=row["lastUpdateDate"],
                productImage=row["productImage"],
                highestPrice=row["highestPrice"],
                lowestPrice=row["lowestPrice"],
                currentPrice=row["currentPrice"],
                priceHistory=row["priceHistory"],
            )
            products.append(product)
        return products

    def update_product(self, product: CosmosDict, fields: List[str], values: list):
        for field in fields:
            if field == "priceHistory":
                # Get last historical price
                if (
                    product["priceHistory"][len(product["priceHistory"]) - 1]["price"]
                    == product["currentPrice"]
                ):
                    # Price is the same as last time then only update the date
                    product["priceHistory"][len(product["priceHistory"]) - 1][
                        "date"
                    ] = values[fields.index(field)]
                else:
                    # Product price has changed then create a new date-price entry
                    product[field].append(values[fields.index(field)])
            else:
                product[field] = values[fields.index(field)]
        self.db_connector.upsert_item(product)
