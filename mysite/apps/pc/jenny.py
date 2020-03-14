from marshmallow import fields, Schema


class MoveSchema(Schema):
    move_type = fields.String()
    move_name = fields.String()


class MoveSetSchema(Schema):
    move_01 = fields.Nested(MoveSchema)
    move_02 = fields.Nested(MoveSchema)
    move_03 = fields.Nested(MoveSchema)
    move_04 = fields.Nested(MoveSchema)
    move_05 = fields.Nested(MoveSchema)
    move_06 = fields.Nested(MoveSchema)


class PcSchema(Schema):
    name = fields.String()
    gender = fields.String()
    specie_name = fields.String()
    specie_type = fields.String()
    ball_name = fields.String()
    item_name = fields.String()
    ability_name = fields.String()
    level = fields.Integer()
    bond = fields.Decimal()
    moves = fields.Nested(MoveSetSchema)
    description = fields.String()
