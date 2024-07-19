from django.test import TestCase
from .models import Account

class AccountModelTests(TestCase):

    def setUp(self):
        Account.objects.create(id='cc26b56c-36f6-41f1-b689-d1d5065b95af', name='Joy Dean', balance=4497.22)

    def test_account_creation(self):
        joy = Account.objects.get(id='cc26b56c-36f6-41f1-b689-d1d5065b95af')
        self.assertEqual(joy.name, 'Joy Dean')
        self.assertEqual(joy.balance, 4497.22)

    def test_transfer_funds(self):
        account1 = Account.objects.create(id='account1', name='Account 1', balance=5000)
        account2 = Account.objects.create(id='account2', name='Account 2', balance=3000)

        amount = 1000
        account1.balance -= amount
        account2.balance += amount

        account1.save()
        account2.save()

        self.assertEqual(account1.balance, 4000)
        self.assertEqual(account2.balance, 4000)
