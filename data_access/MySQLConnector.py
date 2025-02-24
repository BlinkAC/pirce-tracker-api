import json
from mysql.connector import pooling

class MySQLConnector:
    def __init__(self, config):
        self.pool = pooling.MySQLConnectionPool(pool_name="mypool",
                                                pool_size=5,
                                                **config)

    def get_connection(self):
        return self.pool.get_connection()
