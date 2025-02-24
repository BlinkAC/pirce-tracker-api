from azure.cosmos import exceptions, CosmosClient, PartitionKey


class CosmosDbConnector:
    def __init__(self, endpoint, key, database_name, container_name):
        self.client = CosmosClient(endpoint, key)
        self.database = self.client.create_database_if_not_exists(id=database_name)
        self.container = self.database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path="/id"),
            offer_throughput=400,
        )

    def upsert_item(self, item):
        try:
            self.container.upsert_item(item)
            print("Elemento insertado con éxito")
        except exceptions.CosmosResourceNotFoundError:
            print("Documento no encontrado")
        # except TypeError as e:
        #     print(f"Error de tipo: {e}")
        #     for key, value in item.items():
        #         if not isinstance(key, (str, int, float, bool, type(None))):
        #             print(f"Clave no válida: {key} ({type(key)})")
        #         if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
        #             print(f"Valor no válido para clave '{key}': {value} ({type(value)})")
        except Exception as e:
            print(f"Error al insertar el elemento: {e}")

    def read_item(self, item_id, partition_key):
        try:
            return self.container.read_item(item=item_id, partition_key=partition_key)
        except exceptions.CosmosResourceNotFoundError:
            return None

    def delete_item(self, item_id, partition_key1, partition_key2):
        self.container.delete_item(
            item=item_id, partition_key=(partition_key1, partition_key2)
        )

    def query_items(self, query):
        return list(
            self.container.query_items(query=query, enable_cross_partition_query=True)
        )
