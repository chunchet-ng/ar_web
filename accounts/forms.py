from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit, Reset
from .custom_layout_object import *
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm

class TransactionDetailsForm(forms.ModelForm):
    transactDet_desc = forms.CharField(
        widget=(forms.Textarea(attrs={'rows':'3', 'cols':'100'}))
    )
    class Meta:
        model = Transaction
        fields='__all__'

TransactionDetailsFormSet = inlineformset_factory(
    Transaction, TransactionDetails, form=TransactionDetailsForm,
    fields='__all__', can_delete=True, min_num=1, validate_min=True, extra=0
    )


class TransactionForm(forms.ModelForm):
    
    transact_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'value': datetime.now().strftime("%Y-%m-%d")})
    )

    class Meta:
        model = Transaction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = User.objects.select_related().filter(profile__role=1) | User.objects.select_related().filter(profile__role=2)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Div(
                Div(
                    Fieldset('Transaction details',
                        Field('transact_date'),
                        Field('owner'),
                        ), 
                        HTML("<br>"),
                        css_class='col-md-12',),
                Div(
                    Fieldset('Add Transactions',
                        Formset('transactions')),
                    css_class='m-3',),
                HTML("<br>"),
            css_class='row',),
            Div(ButtonHolder(Submit('submit', 'Save')), css_class="m-1"),
        )


class FilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Div(
                Div(
                    Fieldset('Transaction Details',
                        Field('transaction__transact_date'),
                        Field('transaction__owner'),
                        Field('transaction__creator'),
                        Field('transactDet_desc'),
                        ),
                        HTML("<br>"),
                        css_class='col-md-12',),
                Div(
                    ButtonHolder(
                        Submit('submit', 'Search'),
                    ),
                    css_class="col text-center"),
                css_class='row',
            )
        )

class MonthlyReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MonthlyReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Div(
                Div(
                    Fieldset('Transaction Details',
                        Field('transaction__transact_date'),
                        Field('transaction__owner'),
                        Field('date_range'),
                        ),
                        HTML("<br>"),
                        css_class='col-md-12',),
                Div(
                    ButtonHolder(
                        Submit('submit', 'Search'),
                    ),
                    css_class="col text-center"),
                css_class='row',
            )
        )

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, help_text='Required. Select user\'s role.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'role')