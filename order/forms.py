# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms

CURRENT_YEAR = datetime.now().year


class DailyReportDateRange(forms.Form):
    start_date = forms.DateField(
        label='Початкова дата',
        widget=forms.SelectDateWidget(
            attrs={'class': 'datepicker'},
            empty_label=("Рік", "Місяць", "День"),
            years=range(2025, CURRENT_YEAR+1),
        )
    )
    end_date = forms.DateField(
        label='Кінцева дата',
        widget=forms.SelectDateWidget(
            attrs={'class': 'datepicker'},
            empty_label=("Рік", "Місяць", "День"),
            years=range(2025, CURRENT_YEAR+1),
        )
    )
