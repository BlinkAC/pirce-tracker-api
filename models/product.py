# src/models/mysql_row.py
from datetime import datetime
from azure.cosmos import CosmosDict


class Product:
    def __init__(
        self,
        productId: str,
        productUrl: str,
        productStore,
        additionDate,
        lastUpdateDate,
        isProductActive,
        productImage,
        highestPrice,
        lowestPrice,
        currentPrice,
        priceHistory,
    ):
        self.productId = productId
        self.productStore = productStore
        self.additionDate = additionDate
        self.lastUpdateDate = lastUpdateDate
        self.isProductActive = isProductActive if isProductActive is not None else 1
        self.productUrl = productUrl
        self.productImage = productImage
        self.highestPrice = highestPrice if highestPrice is not None else 0.0
        self.lowestPrice = lowestPrice if lowestPrice is not None else 0.0
        self.currentPrice = currentPrice if currentPrice is not None else 0.0
        self.priceHistory = priceHistory

    # Con el método __repr__, al imprimir una instancia de MySQLRow, se obtiene una representación clara del objeto:
    # con:
    # sin:  <__main__.MySQLRow object at 0x7f8c7d2b4e50>
    def __repr__(self):
        return f"MySQLRow(id={self.productId}, url='{self.productUrl}', other_field='{self.additionDate}')"
