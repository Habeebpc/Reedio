from django.db import models


class TransactionCategory(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(
        choices=(('income', 'Income'), ('expense', 'Expense')), max_length=16)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    created_by = models.ForeignKey('user_auth.User', on_delete=models.SET_NULL,
                                   null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    narration = models.TextField(null=True, blank=True)
    category = models.ForeignKey(TransactionCategory,
                                 on_delete=models.SET_NULL, null=True,
                                 blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                 blank=True)
    date = models.DateTimeField()
    transaction_type = models.CharField(
        choices=(('income', 'Income'), ('expense', 'Expense')), max_length=16)
    document = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
