import django_tables2 as tables
from .models import *
from django_tables2.utils import A
from django.utils.html import format_html

class TransactionDetailSearchTable(tables.Table):
    action = tables.LinkColumn('accounts:transaction_detail', text='View', kwargs={'pk': A('transaction__transact_id')}, \
                         orderable=False, empty_values=(), attrs={"a": {"class": "btn btn-outline-info"}})

    transaction__transact_date = tables.DateColumn(format ='d/m/Y')

    class Meta:
        # model = Product
        # template_name = 'django_tables2/bootstrap4.html'
        # empty_text = 'No record found'
        # fields = ['invoice__invoice_reference', 'invoice__invoice_date', 'invoice__customer_name' 
        # ,'invoice__customer_phone','invoice__customer_email','invoice__customer_address','product_desc']

        model = TransactionDetails
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'No record found'
        fields = ['transaction__transact_date', 'transactDet_desc', 'transaction__owner', 'transaction__creator']

class TransactionDetailTable(tables.Table):
    
    # https://stackoverflow.com/questions/49854515/using-django-tables-2-how-do-you-cut-off-a-long-text-field-with-an-ellipsis
    transactDet_desc = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.transactDet_desc}}">{{record.transactDet_desc|truncatechars:10}}', footer="Total", attrs={"tf": {"class": "bold_large"}})

    rm = tables.Column(
        footer=lambda table: round(sum(x.rm for x in table.data if x.rm), 2),
        empty_values=["0.00"],
        attrs={"tf": {"class": "bold_large"}}
    )

    def render_rm(self, record):
        if record.rm:
            return '{:0.2f}'.format(record.rm)
        else:
            return "0.00"
    
    usd = tables.Column(
        footer=lambda table: round(sum(x.usd for x in table.data if x.usd), 2),
        empty_values=["0.00"],
        attrs={"tf": {"class": "bold_large"}}
    )

    def render_usd(self, record):
        if record.usd:
            return '{:0.2f}'.format(record.usd)
        else:
            return "0.00"
    
    rmb = tables.Column(
        footer=lambda table: round(sum(x.rmb for x in table.data if x.rmb), 2),
        empty_values=["0.00"],
        attrs={"tf": {"class": "bold_large"}}
    )

    def render_rmb(self, record):
        if record.rmb:
            return '{:0.2f}'.format(record.rmb)
        else:
            return "0.00"

    # def render_discounted(self, record):
    #     if (record.product_unit_price and record.product_quantity):
    #         if record.product_unit_disc != None:
    #             value = record.product_unit_price * record.product_quantity * (1 - record.product_unit_disc/100)
    #             return '{:0.2f}'.format(value)
    #         else:
    #             value = record.product_unit_price * record.product_quantity
    #             return '{:0.2f}'.format(value)
    #     else:
    #         return 0

    class Meta:
        model = TransactionDetails
        template_name = 'django_tables2/bootstrap4.html'
        exclude = ['transactDet_id', 'transaction']
        orderable=False

class MonthlyReportTable(tables.Table):
    
    transaction__transact_date = tables.DateColumn(format ='d/m/Y', footer="Total", attrs={"tf": {"class": "bold_large"}})

    # https://stackoverflow.com/questions/49854515/using-django-tables-2-how-do-you-cut-off-a-long-text-field-with-an-ellipsis
    transactDet_desc = tables.TemplateColumn('<data-toggle="tooltip" title="{{record.transactDet_desc}}">{{record.transactDet_desc|truncatechars:10}}', attrs={"tf": {"class": "bold_large"}})

    rm = tables.Column(
        footer=lambda table: round(sum(x.rm for x in table.data if x.rm), 2),
        empty_values=["0.00"],
        attrs={"tf": {"class": "bold_large"}}
    )

    def render_rm(self, record):
        if record.rm:
            return '{:0.2f}'.format(record.rm)
        else:
            return "0.00"
    
    usd = tables.Column(
        footer=lambda table: round(sum(x.usd for x in table.data if x.usd), 2),
        empty_values=["0.00"],
        attrs={"tf": {"class": "bold_large"}}
    )

    def render_usd(self, record):
        if record.usd:
            return '{:0.2f}'.format(record.usd)
        else:
            return "0.00"
    
    rmb = tables.Column(
        footer=lambda table: round(sum(x.rmb for x in table.data if x.rmb), 2),
        empty_values=["0.00"],
        attrs={"tf": {"class": "bold_large"}}
    )

    def render_rmb(self, record):
        if record.rmb:
            return '{:0.2f}'.format(record.rmb)
        else:
            return "0.00"

    class Meta:
        model = TransactionDetails
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['transaction__transact_date', 'transactDet_desc', 'rm', 'usd',  'rmb']
        orderable=False
        empty_text = 'No record found'
        attrs = {"style": "margin-bottom:5rem"}