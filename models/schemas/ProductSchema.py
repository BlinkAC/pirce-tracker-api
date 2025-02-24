from datetime import datetime

from marshmallow import Schema, fields, post_dump


class PriceHistorySchema(Schema):
    date = fields.Str()
    price = fields.Float()


class ProductSchema(Schema):
    productId = fields.Str()
    productUrl = fields.Str()
    productStore = fields.Str(allow_none=True)
    additionDate = fields.Str(allow_none=True)
    lastUpdateDate = fields.Str(allow_none=True)
    isProductActive = fields.Int(allow_none=True)
    productImage = fields.Str(allow_none=True)
    highestPrice = fields.Float(allow_none=True)
    lowestPrice = fields.Float(allow_none=True)
    currentPrice = fields.Float(allow_none=True)
    priceHistory = fields.List(fields.Nested(PriceHistorySchema), allow_none=True)

    @post_dump
    def remove_none_fields(self, data, many, **kwargs):
        """Eliminar campos con valores None después de la serialización"""
        return {key: value for key, value in data.items() if value is not None}
