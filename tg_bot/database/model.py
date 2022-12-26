from tortoise import models, fields


class User(models.Model):
    id = fields.UUIDField(pk=True)
    tg_id = fields.IntField(min_value=1, null=False)
    language = fields.CharField(max_length=255, null=False, default="en")


class Photo(models.Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', null=False)
    photo = fields.BinaryField(null=False)


class Config(models.Model):
    key = fields.TextField(pk=True)
    value = fields.TextField(null=False)
