from azure.cosmos import CosmosDict
from data_access.CosmosDbConnector import CosmosDbConnector
from services.CosmosDbService import CosmosDbService
from datetime import datetime


class DataProcessorService:
    def __init__(self, cosmos_service: CosmosDbService):
        self.cosmos_service = cosmos_service

    def process_data(
        self,
        product: CosmosDict,
        actualPrice: float,
    ):  # cosmosInstance: CosmosDbService
        updatelist = []
        updateValuesList = []
        date = datetime.now().isoformat()
        testing = float(product["currentPrice"])
        if actualPrice != float(product["currentPrice"]):
            if actualPrice > float(product["currentPrice"]):

                updatelist.append("currentPrice")
                updateValuesList.append(actualPrice)

                updatelist.append("lastUpdateDate")
                updateValuesList.append(date)

                updatelist.append("priceHistory")
                updateValuesList.append({"price": actualPrice, "date": date})

                updatelist.append("productStore")
                updateValuesList.append("ML")

                if actualPrice > float(product["highestPrice"]):
                    updatelist.append("highestPrice")
                    updateValuesList.append(actualPrice)

                self.cosmos_service.update_product(
                    product, updatelist, updateValuesList
                )
            else:
                if actualPrice < float(product["lowestPrice"]):
                    updatelist.append("lowestPrice")
                    updateValuesList.append(actualPrice)

                updatelist.append("lastUpdateDate")
                updateValuesList.append(date)

                updatelist.append("currentPrice")
                updateValuesList.append(actualPrice)

                updatelist.append("priceHistory")
                updateValuesList.append(
                    {"price": actualPrice, "date": datetime.now().isoformat()}
                )
                updatelist.append("productStore")
                updateValuesList.append("ML")

                self.cosmos_service.update_product(
                    product, updatelist, updateValuesList
                )
        else:
            if float(product["currentPrice"]) == actualPrice:
                updatelist.append("lastUpdateDate")
                updateValuesList.append(date)
                updatelist.append("priceHistory")
                updateValuesList.append(date)
                updatelist.append("productStore")
                updateValuesList.append("ML")
                self.cosmos_service.update_product(
                    product, updatelist, updateValuesList
                )
