# accounts/tests/test_models.py

from django.test import TestCase
from accounts.models import Account
from decimal import Decimal

class AccountModelTests(TestCase):

    def setUp(self):
        Account.objects.create(id='cc26b56c-36f6-41f1-b689-d1d5065b95af', name='Joy Dean', balance=Decimal('4497.22'))

    def test_account_creation(self):
        joy = Account.objects.get(id='cc26b56c-36f6-41f1-b689-d1d5065b95af')
        self.assertEqual(joy.name, 'Joy Dean')
        self.assertEqual(joy.balance, Decimal('4497.22'))

    def test_transfer_funds(self):
        account1 = Account.objects.create(id='ee06b224-2cf7-4313-97b2-4c5b76d1e88a', name='Account 1', balance=Decimal('5000'))
        account2 = Account.objects.create(id='dcf78c7e-97c1-4df6-abe3-88c41f935cc2', name='Account 2', balance=Decimal('3000'))

        amount = Decimal('1000')
        account1.balance -= amount
        account2.balance += amount

        account1.save()
        account2.save()

        self.assertEqual(account1.balance, Decimal('4000'))
        self.assertEqual(account2.balance, Decimal('4000'))
