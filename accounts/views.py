import csv
import io
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Account
from .forms import UploadCSVForm, TransferForm

def import_accounts(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                csv_file = request.FILES['file']
                file_type = form.cleaned_data['file_type']
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)

                if file_type == 'csv':
                    delimiter = ','
                elif file_type == 'tsv':
                    delimiter = '\t'
                else:
                    messages.error(request, 'Unsupported file type.')
                    return render(request, 'accounts/import_accounts.html', {'form': form})

                next(io_string)  # Skip header
                for column in csv.reader(io_string, delimiter=delimiter, quotechar="|"):
                    try:
                        _, created = Account.objects.update_or_create(
                            id=column[0],
                            defaults={'name': column[1], 'balance': column[2]}
                        )
                    except Exception as e:
                        messages.error(request, f"Error processing row: {column}. Error: {e}")
                        continue

                messages.success(request, 'Accounts imported successfully.')
                return HttpResponseRedirect(reverse('accounts:list'))
            except Exception as e:
                messages.error(request, f"Error reading file: {e}")
    else:
        form = UploadCSVForm()

    return render(request, 'accounts/import_accounts.html', {'form': form})

def list_accounts(request):
    accounts = Account.objects.all()
    return render(request, 'accounts/list_accounts.html', {'accounts': accounts})

def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'accounts/account_detail.html', {'account': account})

def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']

            if from_account.balance < amount:
                messages.error(request, 'Insufficient funds in the source account.')
            else:
                from_account.balance -= amount
                to_account.balance += amount

                from_account.save()
                to_account.save()

                messages.success(request, 'Funds transferred successfully.')
                return HttpResponseRedirect(reverse('accounts:list'))
    else:
        form = TransferForm()
    return render(request, 'accounts/transfer_funds.html', {'form': form})
