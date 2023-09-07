from django import forms
from django.utils import timezone

from .constants import YEARS


class CourtOrderForm(forms.Form):
    debtor_surname = forms.CharField(max_length=255, label="Фамилия заявителя")
    debtor_name = forms.CharField(max_length=255, label="Имя заявителя")
    debtor_lastname = forms.CharField(max_length=255,
                                      label="Отчество заявителя",
                                      required=False)
    court_number = forms.IntegerField(label="Номер судебного участка")
    court_city = forms.CharField(max_length=255, label="Город")
    debtor_adres = forms.CharField(widget=forms.TextInput,
                                   label="Адрес заявителя")
    court_order_date = forms.DateField(
        widget=forms.SelectDateWidget(years=YEARS),
        label="Дата вынесения судебного "
              "приказа",
        initial=timezone.now())
    court_order_number = forms.CharField(widget=forms.TextInput,
                                         label="Номер судебного приказа")
    claimer_name = forms.CharField(max_length=255,
                                   label="Наименование взыскателя")
    debt_size = forms.IntegerField(label="Размер долга по судебному приказу")
    court_order_date_receipt = forms.DateField(
        label="Дата получения судебного приказа",
        widget=forms.SelectDateWidget(years=YEARS),
        initial=timezone.now())
