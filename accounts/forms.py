from django import forms
from .models import Account

class UploadCSVForm(forms.Form):
    file = forms.FileField()
    file_type = forms.ChoiceField(choices=[('csv', 'CSV'), ('tsv', 'TSV')], label='File Type')


class TransferForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.all(), label="From Account")
    to_account = forms.ModelChoiceField(queryset=Account.objects.all(), label="To Account")
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        from_account_id = kwargs.pop('from_account_id', None)
        super().__init__(*args, **kwargs)
        if from_account_id:
            self.fields['to_account'].queryset = Account.objects.exclude(id=from_account_id)
        else:
            self.fields['to_account'].queryset = Account.objects.all()
