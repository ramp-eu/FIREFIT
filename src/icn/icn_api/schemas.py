from marshmallow import Schema, fields


class InspectionValueSchema(Schema):
    databaseType = fields.Str()
    databaseEndpoint = fields.Str()
    database = fields.Str()
    collection = fields.Str()
    imageFile = fields.Str()


class ImageSchema(Schema):
    type = fields.Str()
    value = fields.Nested(InspectionValueSchema)
    metadata = fields.Dict(required=False)


class ImageDataSchema(Schema):
    id = fields.Str()
    type = fields.Str()
    image = fields.Nested(ImageSchema)
    metadata = fields.Dict(required=False)


class ImageSubscriptionSchema(Schema):
    subscriptionId = fields.Str()
    data = fields.Nested(ImageDataSchema, many=True)






