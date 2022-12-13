from django.shortcuts import render
from django.views import generic
from .models import Sales
from .forms import SalesSearchForm
import pandas as pd
from .utils import get_customer_from_id,\
    get_salesman_from_id, get_chart


def home_view(request):
    form = SalesSearchForm(request.POST or None)
    sales_df = None
    position_df = None
    merged_df = None
    df = None
    chart = None
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        sale_qs = Sales.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if len(sale_qs):
            sales_df = pd.DataFrame(sale_qs.values())
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%d.%m.%Y'))
            sales_df['updated'] = sales_df['updated'].apply(lambda x: x.strftime('%d.%m.%Y'))
            sales_df.rename({
                'id': 'sales-id',
                'customer_id': 'customer',
                'salesman_id': 'salesman',
                'position_id': 'position',
                'total_price': 'total-price',

            }, axis=1, inplace=True)

            position_data = []
            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id()
                    }
                    position_data.append(obj)


            position_df = pd.DataFrame(position_data)
            position_df.rename({
                'position_id': 'position',
                'sales_id': 'sales-id',
            }, axis=1, inplace=True)

            merged_df = pd.merge(sales_df, position_df, on='sales-id')

            df = merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum')

            chart = get_chart(chart_type, df, labels=df['transaction_id'].values)
            sales_df = sales_df.to_html()
            position_df = position_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()



    context = {
        'form': form,
        'sales_df': sales_df,
        'position_df': position_df,
        'merged_df': merged_df,
        'df': df,
        'chart': chart,
    }
    return render(request, 'sales/home.html', context)

class SaleListView(generic.ListView):
    model = Sales
    template_name = 'sales/main.html'
    context_object_name = 'qs'
    #otherwise 'object_list'

# def sale_list_view(request):
#     qs = Sales.objects.all()
#     return render(request, 'sales/main.html', {'qs': qs})

class SaleDetailView(generic.DetailView):
    model = Sales
    template_name = 'sales/detail.html'

# def sale_detail_view(request, **kwargs):
#     pk = kwargs.get('pk')
#     obj = Sales.objects.get(pk=pk)
#     return render(request, 'sales/detail.html', {'object': obj})

