from tortoise import fields, models

class PriceRecord(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50)
    price = fields.DecimalField(max_digits=20, decimal_places=8)
    max_price = fields.DecimalField(max_digits=20, decimal_places=8)
    min_price = fields.DecimalField(max_digits=20, decimal_places=8)
    date = fields.DatetimeField(auto_now_add=True)
    difference = fields.DecimalField(max_digits=10, decimal_places=4)
    total_amount = fields.DecimalField(max_digits=20, decimal_places=8)
    coins = fields.JSONField()

    def __str__(self):
        return f"{self.title} - {self.price}"