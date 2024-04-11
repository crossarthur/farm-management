from django.shortcuts import render, redirect
from .forms import *
from django.db.models import F, Sum, Avg, Count, ExpressionWrapper, IntegerField, DateTimeField, Min, Max
from .models import *
from django.contrib import messages
from django.db.models import F, Sum, Avg, Count, ExpressionWrapper, IntegerField, DateTimeField, Min, Max
from .models import *
from django.contrib import messages
from django.db.models.functions import TruncDate, Trunc, Floor, ExtractYear, ExtractMonth, ExtractDay, ExtractHour, \
    TruncHour, ExtractMinute, TruncMinute, Extract, TruncMonth, ExtractWeek
from datetime import timedelta, datetime
from django.utils import timezone

# Create your views here.


def batch(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    total_chicken_num = ChickenFigures_b.objects.values_list('total_chicken', flat=True).last()
    chickens_out = ChickenFigures_b.objects.values_list('chicken_out', flat=True).last()
    chicken_in_calculate1 = ChickenFigures_b.objects.aggregate(cal=Sum('chicken_mortality'))
    chicken_in_calculate = chicken_in_calculate1['cal']
    user = User.objects.all().count()
    most_frequent_user = CustomerRank_b.objects.values('customer_rk').annotate(
    user_count=Count('customer_rk')).order_by('-user_count').first()

    if most_frequent_user:
        user_value = most_frequent_user['customer_rk']
        user_count = most_frequent_user['user_count']

    context = {
        'imprest': imprest,
        'total_chicken_num': total_chicken_num,
        'chickens_out': chickens_out,
        'user_value': user_value,
        'user': user,
        'chicken_in_calculate': chicken_in_calculate,
    }
    return render(request, 'poultry_b/batch.html', context)


def add_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
     # Start App By adding birds
    imprest = Imprest_b.objects.values_list('imprest', flat=True).last()
    if request.method == 'POST':
        form = ChickenForm(request.POST)
        if form.is_valid():
            instance = form.save()

            messages.success(request, f'Total Number of Birds in Poultry is {instance.total_chicken}')
            return redirect('index_b')
    else:
        form = ChickenForm()
        return render(request, 'poultry_b/add_b.html', {'form': form, 'imprest': imprest})


def index_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    imprest1 = Imprest_b.objects.all()
    rating = CustomerRank_b.objects.all()
    # Last 7 days/ last 2 months
    now = timezone.now()
    result = Profit_b.objects.aggregate(
        total=models.Max('expenditure'),
        today=models.Max('expenditure', filter=models.Q(date=now.date())),
        yesterday=models.Max('expenditure', filter=models.Q(date__gte=(now - timedelta(minutes=2)).date())),
        last_7_day=models.Max('expenditure', filter=models.Q(date__gte=(now - timedelta(days=20)).date())),
    )

    # for chicken out in index
    overview = ChickenFigures_b.objects.all().order_by('-date')

    # Chicken in Graph every 2 hours
    # prnts = ChickenFigures_b.objects.annotate(hour=ExtractHour('date'), interval=F('hour') / 2 * 2).values(
        #'hour').annotate(sum=Sum('chicken_in')).values('hour', 'sum')
    prnts = ChickenFigures_b.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Sum('chicken_in'))

    prnts2 = ChickenFigures_b.objects.annotate(hour=ExtractHour('date'), interval=(F('hour') / 2) * 2).values('interval',
                                                                                                            'total_chicken').values_list(
        'interval', flat=True).distinct()

    # computation for total number of chickens, sum of feed, drugs necessities and production at intervals
    total_chicken_num = ChickenFigures_b.objects.values_list('total_chicken', flat=True).last()
    feed_total_cost = Feed_b.objects.aggregate(cal=Sum('feed_cost'))
    feed_total = feed_total_cost['cal']
    feed = Feed_b.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Sum('feed_cost')).values('week', 'sum')

    necs = Necessities_b.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Sum('necessities_cost')).values('week', 'sum')
    pros = Production_b.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Sum('production_cost')).values('week', 'sum')
    drugs_total_cost = Drugs_b.objects.aggregate(cal=Sum('drug_cost'))
    drugs_total = drugs_total_cost['cal']
    drugs = Drugs_b.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Sum('drug_cost')).values('week', 'sum')
    graph_income = ChickenFigures_b.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Sum('chicken_out_total_cost')).values('week', 'sum')
    print(f'expen {total_chicken_num}total_chicken_num')


    # total expenditure
    production1 = Production_b.objects.aggregate(cal=Sum('production_cost'))
    pro = production1['cal']
    feed1 = Feed_b.objects.aggregate(cal=Sum('feed_cost'))
    fee = feed1['cal']
    drug = Drugs_b.objects.aggregate(cal=Sum('drug_cost'))
    dru = drug['cal']
    necessities1 = Necessities_b.objects.aggregate(cal=Sum('necessities_cost'))
    nec = necessities1['cal']
    expenditure = 0
    if pro is not None and fee is not None and dru is not None and nec is not None:
        expenditure = (pro + fee + dru + nec)
    elif pro and fee and dru is not None:
        expenditure = fee + pro + dru
    elif pro and fee and nec is not None:
        expenditure = fee + pro + nec
    elif pro and dru and nec is not None:
        expenditure = pro + dru + nec
    elif fee and dru and nec is not None:
        expenditure = fee + dru + nec

    elif pro and fee is not None:
        expenditure = fee + pro
    elif pro and nec is not None:
        expenditure = pro + nec
    elif pro and dru is not None:
        expenditure = pro + dru
    elif fee and nec is not None:
        expenditure = fee + nec
    elif fee and dru is not None:
        expenditure = fee + dru
    elif dru and nec is not None:
        expenditure = dru + nec

    elif fee is not None:
        expenditure = fee
    elif dru is not None:
        expenditure = dru
    elif nec is not None:
        expenditure = nec
    elif pro is not None:
        expenditure = pro





    # total income
    chickens_out = ChickenFigures_b.objects.aggregate(cal=Sum('chicken_out_total_cost'))
    offals = Offals_b.objects.aggregate(cal=Sum('offals_cost'))
    graph_income = ChickenFigures_b.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Sum('chicken_out_total_cost')).values('week', 'sum')
    graph_income = Profit_b.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Max('income')).values('week', 'sum')

    income_chicken_out = chickens_out['cal']
    income_offals = offals['cal']
    profs = Profit_b.objects.values_list('income', flat=True).last()
    print(f'this is chi {income_offals}')

    cal = 0
    if income_chicken_out is not None:
        income = income_chicken_out
        print(f'tis is prof {profs}')

        if pro is not None and fee is not None and dru is not None and nec is not None:
            cal = income - expenditure
            print(f"this is my {cal}")
            graph_exp = Profit_b(expenditure=expenditure, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()
        elif fee is not None and pro is not None and dru:
            cal = income - expenditure
            graph_exp = Profit_b(expenditure=cal, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()

        elif pro and fee and nec is not None:
            cal = income - expenditure
            graph_exp = Profit_b(expenditure=cal, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()
        elif pro and dru and nec is not None:
            cal = income - expenditure
            graph_exp = Profit_b(expenditure=cal, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()
        elif fee and dru and nec is not None:
            cal = income - expenditure
            graph_exp = Profit_b(expenditure=cal, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()

        elif fee is not None and pro is not None:
            cal = income - expenditure
            graph_exp = Profit_b(expenditure=cal, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()
        elif pro and nec is not None:
            cal = income - expenditure
            graph_exp = Profit_b(expenditure=cal, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()
        elif pro and dru is not None:
            cal = income - expenditure
            graph_exp = Profit_b(expenditure=cal, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()
        elif fee and nec is not None:
            cal = income - expenditure
            graph_exp = Profit_b(expenditure=cal, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()
        elif fee and dru is not None:
            cal = income - expenditure
            graph_exp = Profit_b(expenditure=cal, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()
        elif dru and nec is not None:
            cal = income - expenditure
            graph_exp = Profit_b(expenditure=cal, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()


        elif pro is not None:
            cal = income - pro
            graph_exp = Profit_b(expenditure=cal, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()
        elif fee is not None:
            cal = income - expenditure
            graph_exp = Profit_b(expenditure=cal, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()
        elif dru is not None:
            cal = income - expenditure
            graph_exp = Profit_b(expenditure=cal, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()
        elif nec is not None:
            cal = income - expenditure
            graph_exp = Profit_b(expenditure=cal, income=income)
            Profit_b.objects.create(calculate=cal)
            graph_exp.save()


    else:
        income1 = 0
        income2 = 0
        income = 0


    print(graph_income)

    if cal < 0:
        print('loss')
    else:
        print('profit')

    # profit/loss arrow
    total_chicken_nu = ChickenFigures_b.objects.values_list('chicken_out_total_cost', flat=True).last()
    if income_offals is not None:
        income1 = income_offals + income
        print(f' this is the real {income_offals}')
        cal = income1 - expenditure
        graph_exp = Profit_b(expenditure=expenditure, income=income1)
        Profit_b.objects.create(calculate=cal)
        graph_exp.save()


    # prnts = Profit.objects.annotate(hour=ExtractHour('date'), interval=F('hour')% 2).values('hour').annotate(sum=Sum=(F('calculate')-expenditure)).values('hour', 'sum').distinct()
    # saving expenditure and income to database & saving calculate/profit to database

    # Data doesn't exist, create a new entry


    '''current_date = datetime.today()
    months_ago = 2
    six_month_previous_date = current_date - timedelta(days=(months_ago * 365 / 12))

    order = Profit.objects.filter(date__gte=six_month_previous_date, ).values(month=ExtractMonth('date')).annotate(
        count=F('calculate')).order_by('month')
    order = {r['month']: r['count'] for r in order}

    month = now().month
    result = [
        {'month': ((m % 12) + 1)//12, 'count': order.get((m % 12) + 1, 0)}
        for m in range(month - 1, month - 8, -1)
    ]
    print(result, month)'''

    # extracting maximum profit every at intervals to display as graph
    prof = Profit_b.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Max('calculate')).values('week', 'sum')

    profs = Profit_b.objects.values_list('calculate', flat=True).last()
    print(prof)

    feed1 = Feed_b.objects.annotate(hour=ExtractHour('date'), interval=F('hour') / 2 * 2).values('hour').annotate(
        sum=Sum('feed_cost')).values('hour', 'sum').distinct()
    necs1 = Necessities_b.objects.annotate(hour=ExtractHour('date'), interval=F('hour') / 2 * 2).values('hour').annotate(
        sum=Sum('necessities_cost')).values('hour', 'sum').distinct()
    pros1 = Production_b.objects.annotate(hour=ExtractHour('date'), interval=F('hour') / 2 * 2).values('hour').annotate(
        sum=Sum('production_cost')).values('hour', 'sum').distinct()
    drugs1 = Drugs_b.objects.annotate(hour=ExtractHour('date'), interval=F('hour') / 2 * 2).values('hour').annotate(
        sum=Sum('drug_cost')).values('hour', 'sum').distinct()
    print(feed1, necs1, pros1)


    nec_value = None
    feed_value = None
    feed_count = 0
    drug_value = None
    drug_count = 0
    user_value = None
    user_count = 0

    # most frequent customer
    most_frequent_user = CustomerRank_b.objects.values('customer_rk').annotate(
    user_count=Count('customer_rk')).order_by('-user_count').first()

    if most_frequent_user:
        user_value = most_frequent_user['customer_rk']
        user_count = most_frequent_user['user_count']






    # most frequent Drug Type
    most_frequent_drug = Drugs_b.objects.values('drug_description').annotate(
    drug_count=Count('drug_description')).order_by('-drug_count').first()

    if most_frequent_drug:
        drug_value = most_frequent_drug['drug_description']
        drug_count = most_frequent_drug['drug_count']


    # most frequent necessity

    most_frequent_nec = Necessities_b.objects.values('necessities_description').annotate(
    nec_count=Count('necessities_description')).order_by('-nec_count').first()

    if most_frequent_nec:
        nec_value = most_frequent_nec['necessities_description']
        nec_count = most_frequent_nec['nec_count']

     # most frequent feed_b

    most_frequent_feed = Feed_b.objects.values('feed_description').annotate(
    feed_count=Count('feed_description')).order_by('-feed_count').first()

    if most_frequent_feed:
        feed_value = most_frequent_feed['feed_description']
        feed_count = most_frequent_feed['feed_count']

    profs = Profit_b.objects.values_list('income', flat=True).last()

    print(expenditure)
    context = {
        "nec_value": nec_value,
        "feed_value": feed_value,
        "feed_count": feed_count,
        "drug_value": drug_value,
        "drug_count": drug_count,
        "user_value": user_value,
        "user_count": user_count,
        'prnts': prnts,
        'feed': feed,
        'drugs': drugs,
        'total_chicken_num': total_chicken_num,
        'feed_total': feed_total,
        'drugs_total': drugs_total,
        'expenditure': expenditure,
        'income': income,
        'cal': cal,

        'prof': prof,
        'profs': profs,
        'graph_income': graph_income,
        'necs': necs,
        'nec': nec,
        'pro': pro,
        'pros': pros,
        'fee': fee,
        'dru': dru,
        'result': result,
        'overview': overview,
        'rating': rating,
        'imprest': imprest,
        'imprest1': imprest1,

    }
    return render(request, 'poultry_b/index_b.html', context)


def chicken_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    # chickens_d = ChickenFigures.objects.get(chicken_details=request.user.id)
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    total_chicken_num = ChickenFigures_b.objects.values_list('total_chicken', flat=True).last()
    print(total_chicken_num)
    all_chicken_in = ChickenFigures_b.objects.all().order_by('-date')
    trun = ChickenFigures_b.objects.annotate(day=TruncDate('date')).values('day', ).annotate(c=Sum('chicken_in')).values(
        'day', )
    prnt = ChickenFigures_b.objects.filter(date=datetime(2023, 12, 23) - timedelta(days=1))
    prnts = ChickenFigures_b.objects.annotate(
        hour=ExtractHour('date'),
        days=F('hour') / 2 * 2
    ).values('hour', 'total_chicken')
    # prnts = ChickenFigures.objects.annotate(hour=TruncHour('date')).values('hour',).annotate(f=Sum('total_chicken')).values('hour', 'f')
    print(prnts)
    # total_chicken_num = total_chicken['sum']

    chicken_in_calculate = ChickenFigures_b.objects.aggregate(cal=Sum('chicken_in'))
    # chicken_in_calculate = ChickenFigures.objects.aggregate(Sum('name__chicken_in')).values()
    total_chicken_in = chicken_in_calculate['cal']

    date =  None
    queryset = None


    if request.method == 'GET':
        date = request.GET.get('date')
        print(date)
        # Filter data based on the selected date range
        if date:
            queryset = ChickenFigures_b.objects.filter(date__icontains=date)
            print(queryset)


        else:
            date = None
            queryset = ChickenFigures_b.objects.all()


    if request.method == 'POST':
        form = ChickenFigureForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            if instance.chicken_in is not None and total_chicken_num is not None:
                total_chicken_num += instance.chicken_in

                tot = ChickenFigures_b(total_chicken=total_chicken_num, chicken_in=instance.chicken_in)
                tot.save()

                if instance.chicken_in == 1:
                    messages.success(request, f'{instance.chicken_in} Chicken has been added.')
                    return redirect('.')
                elif instance.chicken_in >= 1:
                    messages.success(request, f'{instance.chicken_in} Chickens have been added.')
                    return redirect('.')

    else:
        form = ChickenFigureForm()
    context = {
        'form': form,
        'total_chicken_num': total_chicken_num,
        'all_chicken_in': all_chicken_in,
        'prnts': prnts,
        'queryset': queryset,
        'date': date,
        'imprest': imprest

    }

    return render(request, 'poultry_b/chicken_b.html', context)


def chickens_out_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    # chickens_d = ChickenFigures.objects.get(chicken_details=request.user.id)
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    overview = ChickenFigures_b.objects.all().order_by('-date')
    total_chicken_num = ChickenFigures_b.objects.values_list('total_chicken', flat=True).last()
    chicken_out_total_cost_num = ChickenFigures_b.objects.values_list('chicken_out_total_cost', flat=True).last()
    print(chicken_out_total_cost_num)
    # total_chicken_num = total_chicken['sum']

    chicken_in_calculate = ChickenFigures_b.objects.aggregate(cal=Sum('chicken_in'))
    # chicken_in_calculate = ChickenFigures.objects.aggregate(Sum('name__chicken_in')).values()
    # total_chicken_in = chicken_in_calculate['cal']
    #total2 = ColdRoomIn.objects.values_list('total_coldroom', flat=True).last()
    date = ''
    queryset = ''
    if request.method == 'GET':
        date = request.GET.get('date')
        print(date)
        # Filter data based on the selected date range
        if date:
            queryset = ChickenFigures_b.objects.filter(date__icontains=date)
            print(queryset)

        else:
            date = None
            queryset = ChickenFigures_b.objects.all()

    if request.method == 'POST':
        form = ChickenOutForm(request.POST)

        if form.is_valid():
            customer1 = form.cleaned_data['customer']
            instance = form.save(commit=False)

            if instance.chicken_out_kilogram > 0 and instance.chicken_out_unit_price > 0 and instance.chicken_out > 0 and instance.customer is not None and instance.total_chicken is not None:
                if instance.chicken_out < total_chicken_num:
                    total_chicken_num -= instance.chicken_out
                    chicken_out_total_cost_num = instance.chicken_out_kilogram * instance.chicken_out_unit_price
                    tot1 = ChickenFigures_b(total_chicken=total_chicken_num, chicken_out=instance.chicken_out,
                                      chicken_out_total_cost=chicken_out_total_cost_num,
                                      chicken_out_kilogram=instance.chicken_out_kilogram,
                                      chicken_out_unit_price=instance.chicken_out_unit_price, customer=instance.customer, customer_rank=customer1)
                    tot2 = CustomerRank_b(customer_rk=customer1)

                    tot2.save()
                    tot1.save()

                    messages.success(request, f'Total cost of chickens out is ₦{chicken_out_total_cost_num}')
                    return redirect('.')

                if instance.chicken_out == 1 and total_chicken_num >= instance.chicken_out:
                    messages.error(request, f'{instance.chicken_out} Chicken has been taken out.')
                    return redirect('.')

                elif 1 <= instance.chicken_out <= total_chicken_num:
                    messages.error(request, f'{instance.chicken_out} Chickens have been taken out.')
                    return redirect('.')

                else:
                    messages.error(request, 'Error in operation, please confirm number chickens in poultry')
                    return redirect('.')

                # elif total_chicken_num < instance.chicken_out:
                #     print('hello dear')

    else:
        form = ChickenOutForm()
    context = {
        'form': form,
        'total_chicken_num': total_chicken_num,
        'chicken_out_total_cost_num': chicken_out_total_cost_num,
        'overview': overview,
        'queryset': queryset,
        'date': date,
        'imprest': imprest
    }

    return render(request, 'poultry_b/chickens_out_b.html', context)


def chickens_slaughtered_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    overview = ChickenFigures_b.objects.all().order_by('-date')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    # chickens_d = ChickenFigures.objects.get(chicken_details=request.user.id)
    total_chicken_num = ChickenFigures_b.objects.values_list('total_chicken', flat=True).last()
    print(total_chicken_num)
    # total_chicken_num = total_chicken['sum']

    chicken = ChickenFigures_b.objects.aggregate(sum=Sum('chicken_slaughtered'))
    # chicken_in_calculate = ChickenFigures.objects.aggregate(Sum('name__chicken_in')).values()
    calculate = chicken['sum']
    print(calculate)

    if request.method == 'POST':
        form = ChickenSlaughteredForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            if instance.chicken_slaughtered is not None:
                total_chicken_num -= instance.chicken_slaughtered

                tot = ChickenFigures_b(total_chicken=total_chicken_num, chicken_slaughtered=instance.chicken_slaughtered)
                tot.save()
                if instance.chicken_slaughtered == 1:
                    messages.error(request, f'{instance.chicken_slaughtered} Chicken has been slaughtered.')
                    return redirect('.')
                elif instance.chicken_slaughtered >= 1:
                    messages.error(request, f'{instance.chicken_slaughtered} Chickens have been slaughtered.')
                    return redirect('.')
    else:
        form = ChickenSlaughteredForm()
    context = {
        'form': form,
        'overview': overview,
        'total_chicken_num': total_chicken_num,
        'imprest': imprest,
        'calculate': calculate
    }
    return render(request, 'poultry_b/chickens_slaughtered_b.html', context)


def delete_chickens_slaughtered_b(request, id):
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    delete = ChickenFigures_b.objects.get(pk=id)
    delete.delete()
    return redirect('chickens_slaughtered_b')


def chickens_mortality_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    overview = ChickenFigures_b.objects.all().order_by('-date')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    # chickens_d = ChickenFigures.objects.get(chicken_details=request.user.id)
    total_chicken_num = ChickenFigures_b.objects.values_list('total_chicken', flat=True).last()
    print(total_chicken_num)
    # total_chicken_num = total_chicken['sum']

    chicken_in_calculate = ChickenFigures_b.objects.aggregate(cal=Sum('chicken_mortality'))
    # chicken_in_calculate = ChickenFigures.objects.aggregate(Sum('name__chicken_in')).values()
    total_chicken_in = chicken_in_calculate['cal']

    if request.method == 'POST':
        form = ChickenMortalityForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            if instance.chicken_mortality is not None:
                total_chicken_num -= instance.chicken_mortality

                tot = ChickenFigures_b(total_chicken=total_chicken_num, chicken_mortality=instance.chicken_mortality)
                tot.save()
                if instance.chicken_mortality == 1:
                    messages.error(request, f'{instance.chicken_mortality} Chicken has died.')
                    return redirect('.')
                elif instance.chicken_mortality >= 1:
                    messages.error(request, f'{instance.chicken_mortality} Chickens have died.')
                    return redirect('.')

    else:
        form = ChickenMortalityForm()
    context = {
        'overview': overview,
        'form': form,
        'total_chicken_num': total_chicken_num,
        'imprest': imprest
    }
    return render(request, 'poultry_b/chickens_mortality_b.html', context)


def delete_chickens_mortality_b(request, id):
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    delete = ChickenFigures_b.objects.get(pk=id)
    delete.delete()
    return redirect('chickens_mortality_b')


def feed_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.feed_quantity is not None and instance.feed_cost is not None and instance.feed_description is not None:
                instance.save()
                form = FeedForm()
                messages.success(request, f'{instance.feed_quantity}KG of {instance.feed_description} has been submitted')
                return redirect('feed_overview_b')

            else:
                messages.error(request, 'error')
    else:
        form = FeedForm()
    context = {
        'form': form,
        'imprest': imprest,
    }
    return render(request, 'poultry_b/feed_b.html', context)


def feed_overview_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    chickens_feed = Feed_b.objects.all().order_by('-date')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'GET':
        date = request.GET.get('date')
        print(date)
        # Filter data based on the selected date range
        if date:
            queryset = Feed_b.objects.filter(date__icontains=date)
            print(queryset)

        else:
            date = None
            queryset = Feed_b.objects.all()

    context = {
        'chickens_feed': chickens_feed,
        "imprest": imprest,
        'date': date,
        'queryset': queryset
    }
    return render(request, 'poultry_b/feed_overview_b.html', context)


def drugs_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'POST':
        form = DrugForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.drug_cost is not None and imprest is not None and instance.drug_cost <= imprest:
                imprest -= instance.drug_cost
                tot = Imprest_b(total_imprest=imprest)
                tot2 = Drugs_b(drug_cost=instance.drug_cost,  drug_description=instance.drug_description)
                tot.save()
                tot2.save()
                messages.success(request, f'₦{instance.drug_cost} for {instance.drug_description} has been submitted')
                return redirect('drugs_overview_b')
            elif instance.drug_cost > imprest:
                messages.error(request, 'Insufficient funds in imprest')
                return redirect(".")
            else:
                messages.error(request, 'Error')
                return redirect('drugs_overview_b')

    else:
        form = DrugForm()
    context = {
        'form': form,
        'imprest': imprest
    }
    return render(request, 'poultry_b/drugs_b.html', context)


def drugs_overview_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    chickens_drug = Drugs_b.objects.all().order_by('-date')
    if request.method == 'GET':
        date = request.GET.get('date')
        print(date)
        # Filter data based on the selected date range
        if date:
            queryset = Drugs_b.objects.filter(date__icontains=date)
            print(queryset)

        else:
            date = None
            queryset = Drugs_b.objects.all()
        context = {
            'chickens_drug': chickens_drug,
            'queryset': queryset,
            'date': date,
            'imprest':imprest,
        }
        return render(request, 'poultry_b/drugs_overview_b.html', context)


def necessities_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'POST':
        form = NecessitiesForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request,
                             f'₦{instance.necessities_cost} for {instance.necessities_description} has been submitted')
            return redirect('necessities_overview_b')

    else:
        form = NecessitiesForm()
    context = {
        'form': form,
        'imprest': imprest,
    }
    return render(request, 'poultry_b/necessities_b.html', context)


def necessities_overview_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    necessities = Necessities_b.objects.all().order_by('-date')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'GET':
        date = request.GET.get('date')
        print(date)
        # Filter data based on the selected date range
        if date:
            queryset = Necessities_b.objects.filter(date__icontains=date)
            print(queryset)

        else:
            date = None
            queryset = Necessities_b.objects.all()
        context = {
            'necessities': necessities,
            'queryset': queryset,
            'date': date,
            'imprest': imprest,
        }
        return render(request, 'poultry_b/necessities_overview_b.html', context)


def delete_necessities_b(request, id):
    delete2 = Necessities_b.objects.get(pk=id)
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()

    delete2.delete()
    return redirect('necessities_overview_b')


def coldroom_in_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    global queryset, date
    t = ColdRoomIn_b.objects.filter(chickens_in_freezer=request.user.id)
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    out = ChickenFigures_b.objects.values_list('chicken_out', flat=True).last()
    total2 = ColdRoomIn_b.objects.values_list('total_coldroom', flat=True).last()
    total = ColdRoomIn_b.objects.all().order_by('-date')
    # total_coldroom_in = ColdRoomIn.objects.aggregate(cal=Sum('chickens_in_freezer'))
    # total_coldroom = total_coldroom_in['cal']

    if request.method == 'GET':
        date = request.GET.get('date')
        print(date)
        # Filter data based on the selected date range
        if date:
            queryset = ColdRoomIn_b.objects.filter(date__icontains=date)
            print(queryset)

        else:
            date = None
            queryset = ColdRoomIn_b.objects.all()

    if request.method == 'POST':
        form = ColdRoomInForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.chickens_in_freezer is not None and total2 is not None:
                total2 += instance.chickens_in_freezer
                sav = ColdRoomIn_b(total_coldroom=total2, chickens_in_freezer=instance.chickens_in_freezer)
                sav.save()
                messages.success(request, 'Chickens Add to Coldroom')
                return redirect(".")
            else:
                pass

    else:
        form = ColdRoomInForm()
    context = {
        'form': form,
        'total2': total2,
        'total': total,
        'queryset': queryset,
        'date': date,
        'imprest': imprest,

    }
    return render(request, 'poultry_b/coldroom_in_b.html', context)


def total_coldroom_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
     # Start App By adding birds
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    total2 = ColdRoomIn_b.objects.values_list('total_coldroom', flat=True).last()
    if request.method == 'POST':
        form = ColdRoomOutForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Chicken Added')
            return redirect('coldroom_in_b')
    else:
        form = ColdRoomOutForm()
    return render(request, 'poultry_b/total_coldroom_b.html', {'form': form, "imprest": imprest, 'total2': total2})


def production_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    total_production = Production_b.objects.aggregate(cal=Sum('production_cost'))
    total_production2 = total_production['cal']
    total = Production_b.objects.all().order_by('-date')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    production = Production_b.objects.values_list('production_cost', flat=True).last()

    '''imp = imprest - production
    tot = Imprest(imprest=imp)
    tot.save()
    print(imprest, production)'''

    date = ''
    queryset = ''
    if request.method == 'GET':
        date = request.GET.get('date')
        print(date)
        # Filter data based on the selected date range
        if date:
            queryset = Production_b.objects.filter(date__icontains=date)
            print(queryset)

        else:
            date = None
            queryset = Production_b.objects.all()

    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.production_cost is not None and imprest is not None:
                imprest -= instance.production_cost
                tot = Imprest_b(total_imprest=imprest)
                tot2 = Production_b(production_cost=instance.production_cost,  production_description=instance.production_description)
                tot.save()
                tot2.save()
                messages.success(request, f'{instance.production_description} has been submitted')
                return redirect(".")

            else:
                messages.error(request, 'Error')
                return redirect('production')

    else:

        form = ProductionForm()
        context = {
            'form': form,
            'total': total,
            'queryset': queryset,
            'date': date,
            'imprest': imprest,

            'total_production2': total_production2,
        }
        return render(request, 'poultry_b/production_b.html', context)

def delete_production_b(request, id):
    delete2 = Production_b.objects.get(pk=id)
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    if delete2 and delete2.production_cost is not None and imprest is not None and delete2.production_cost <= imprest:
                imprest += delete2.production_cost
                tot = Imprest_b(total_imprest=imprest)
                tot.save()

                delete2.delete()
                return redirect('production_b')


def delete_drugs_b(request, id):
    delete2 = Drugs_b.objects.get(pk=id)
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    if delete2 and delete2.drug_cost is not None and imprest is not None and delete2.drug_cost <= imprest:
                imprest += delete2.drug_cost
                tot = Imprest_b(total_imprest=imprest)
                tot.save()

                delete2.delete()
                return redirect('drugs_overview_b')


def total_imprest_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'POST':
        form = TotalImprestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Input for Imprest')
            return redirect('index_b')
    else:
        form = TotalImprestForm()
    return render(request, 'poultry_b/total_imprest_b.html', {'form': form, 'imprest': imprest})


def imprest_b(request):
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    drugs = Drugs_b.objects.values_list('drug_cost', flat=True).last()
    production = Production_b.objects.values_list('production_cost', flat=True).last()

    print(imprest)
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')

    if request.method == 'POST':

        form = ImprestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.imprest is not None and imprest is not None:
                w = instance.imprest + imprest
                tot = Imprest_b(imprest=instance.imprest, total_imprest=w)
                tot.save()
                messages.success(request, 'Imprest Added')
                return redirect('.')

    else:
        form = ImprestForm()
    context = {
        'form': form,
        'imprest': imprest,
        }
    return render(request, 'poultry_b/imprest_b.html', context)


def notepad_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'POST':
        form = NotePadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your note has been saved')
            return redirect('notepad_overview_b')
    else:
        form = NotePadForm()
    return render(request, 'poultry_b/notepad_b.html', {'form': form, 'imprest': imprest})


def notepad_overview_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    note = NotePad_b.objects.all().order_by('-date')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'GET':
        date = request.GET.get('date')

        # Filter data based on the selected date range
        if date:
            queryset = NotePad_b.objects.filter(date__icontains=date)
            print(queryset)

        else:
            date = None
            queryset = NotePad_b.objects.all()
        return render(request, 'poultry_b/notepad_overview_b.html', {'note': note, 'date': date, 'queryset': queryset, 'imprest': imprest})


def notepad_detail_b(request, id):
    upd = NotePad_b.objects.get(pk=id)
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    return render(request, 'poultry_b/notepad_detail_b.html', {'upd': upd, 'imprest': imprest})


def notepad_delete_b(request, id):
    delete2 = NotePad_b.objects.get(pk=id)
    messages.success(request, f'{delete2.title} has been deleted')
    delete2.delete()
    return redirect('notepad_overview_b')


def offals_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    income = Profit_b.objects.values_list('income', flat=True).last()
    print(income)
    if request.method == 'POST':
        form = OffalsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.offals_cost is not None and income is not None:
                income += instance.offals_cost
                print(f'this is {income}')
                tot = Profit_b(income=income)
                tot2 = Offals_b(offals_cost=instance.offals_cost, offals_description=instance.offals_description)
                tot.save()
                tot2.save()
                messages.success(request, 'offals have been submitted')
                return redirect('offals_overview_b')
    else:
        form = OffalsForm()

    context = {
        'form': form,
        'imprest': imprest,
    }
    return render(request, 'poultry_b/offals_b.html', context)


def offals_overview_b(request):
    off = Offals_b.objects.all().order_by('-date')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    context = {
        'off': off,
        'imprest': imprest,
    }
    return render(request, 'poultry_b/offals_overview_b.html', context)


def offals_overview_delete_b(request, id):

    delete2 = Offals_b.objects.get(pk=id)
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()

    delete2.delete()
    return redirect('offals_overview_b')


def delete_chicken_b(request, id):
    dele = ChickenFigures_b.objects.get(pk=id)
    dele.delete()
    return redirect('index_b')


def update_chicken_b(request, id):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    total_chicken_num = ChickenFigures_b.objects.values_list('total_chicken', flat=True).last()
    upd = ChickenFigures_b.objects.get(pk=id)
    form = ChickenFigureForm(request.POST or None, instance=upd)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.chicken_in is not None and total_chicken_num is not None:
            total_chicken_num += instance.chicken_in

            tot = ChickenFigures_b(total_chicken=total_chicken_num, chicken_in=instance.chicken_in)
            tot.save()

            if instance.chicken_in == 1:
                messages.success(request, f'{instance.chicken_in} Chicken has been added.')
                return redirect('chicken_b')
            elif instance.chicken_in >= 1:
                messages.success(request, f'{instance.chicken_in} Chickens have been added.')
                return redirect('chicken_b')

        elif request.method == 'POST':
            chicks = request.POST.get('chicks')
            edit = ChickenFigures_b.objects.get(pk=id)
            edit.chicken_out = chicks
            if edit.chicken_out is not None and instance.chicken_in is not None and total_chicken_num is not None:
                total_chicken_num -= edit.chicken_out
                tot = ChickenFigures_b(total_chicken=total_chicken_num, chicken_out=edit.chicken_out, chicken_in=instance.chicken_in)
                tot.save()

                if edit.chicken_out == 1:
                    messages.error(request, f'{instance.chicken_out} Chicken has been taken out.')
                    return redirect('chicken_b')
                elif edit.chicken_out >= 1:
                    messages.error(request, f'{instance.chicken_out} Chickens have been taken out.')
                    return redirect('chicken_b')

    return render(request, 'poultry_b/update_chicken_b.html', {'form': form, 'upd': upd, 'imprest': imprest})


def update_chicken_out_b(request, id):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    total_chicken_num = ChickenFigures_b.objects.values_list('total_chicken', flat=True).last()
    upd = ChickenFigures_b.objects.get(pk=id)
    form = ChickenOutForm(request.POST or None, instance=upd)
    if form.is_valid():
            customer1 = form.cleaned_data['customer']
            instance = form.save(commit=False)

            if instance.chicken_out_kilogram > 0 and instance.chicken_out_unit_price > 0 and instance.chicken_out > 0 and instance.customer is not None and instance.total_chicken is not None:
                total_chicken_num -= instance.chicken_out
                chicken_out_total_cost_num = instance.chicken_out_kilogram * instance.chicken_out_unit_price
                tot1 = ChickenFigures_b(total_chicken=total_chicken_num, chicken_out=instance.chicken_out,
                                      chicken_out_total_cost=chicken_out_total_cost_num,
                                      chicken_out_kilogram=instance.chicken_out_kilogram,
                                      chicken_out_unit_price=instance.chicken_out_unit_price, customer=instance.customer, customer_rank=customer1)
                tot2 = CustomerRank_b(customer_rk=customer1)
                tot2.save()
                tot1.save()

                messages.success(request, f'Total cost of chickens out is ₦{chicken_out_total_cost_num}')

                if instance.chicken_out == 1:
                    messages.error(request, f'{instance.chicken_out} Chicken has been taken out.')
                    return redirect('chickens_out_b')
                elif instance.chicken_out >= 1:

                    messages.error(request, f'{instance.chicken_out} Chickens have been taken out.')
                    return redirect('chickens_out_b')

            else:
                total_chicken_num -= instance.chicken_out
                tot1 = ChickenFigures_b(total_chicken=total_chicken_num, chicken_out=instance.chicken_out)
                tot1.save()
                return redirect('chickens_out_b')

    return render(request, 'poultry_b/update_chicken_out_b.html', {'form': form, 'upd': upd, 'imprest': imprest})


def update_drugs_b(request, id):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    upd = Drugs_b.objects.get(pk=id)
    form = DrugForm(request.POST or None, instance=upd)
    imprest1 = Imprest_b.objects.values_list('imprest', flat=True).last()
    if form.is_valid():
            instance = form.save(commit=False)
            if instance.drug_cost is not None and imprest is not None and instance.drug_cost <= imprest:
                imprest -= instance.drug_cost
                tot1 = Imprest_b(total_imprest=imprest)
                tot2 = Drugs_b(drug_cost=instance.drug_cost,  drug_description=instance.drug_description)
                tot1.save()
                tot2.save()
                messages.success(request, f'₦{instance.drug_cost} for {instance.drug_description} has been Updated')
                return redirect('drugs_overview_b')

            else:
                messages.error(request, 'Insufficient funds in impress')
                return redirect('drugs_overview_b')

    return render(request, 'poultry_b/update_drugs_b.html', {'form': form, 'upd': upd, 'imprest': imprest})


def update_feed_b(request, id):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    upd = Feed_b.objects.get(pk=id)
    form = FeedForm(request.POST or None, instance=upd)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.feed_quantity is not None and instance.feed_cost is not None and instance.feed_description is not None:
            instance.save()
            form = FeedForm()
            messages.success(request, f'{instance.feed_quantity}KG of {instance.feed_description} has been updated')
            return redirect('feed_overview_b')

        else:
            messages.error(request, 'error')

    return render(request, 'poultry_b/update_feed_b.html', {'form': form, 'upd': upd, 'imprest': imprest})


def update_production_b(request, id):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    upd = Production_b.objects.get(pk=id)
    form = ProductionForm(request.POST or None, instance=upd)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.production_cost is not None and imprest is not None and instance.production_cost <= imprest:
            imprest -= instance.production_cost
            tot = Imprest_b(total_imprest=imprest)
            tot2 = Production_b(production_cost=instance.production_cost, production_description=instance.production_description)
            tot.save()
            tot2.save()
            messages.success(request, 'Production have been updated')
            return redirect('production_b')

        else:
            messages.error(request, 'Insufficient funds in impress')
            return redirect('production_b')


    return render(request, 'poultry_b/update_production_b.html', {'form': form, 'upd': upd, 'imprest': imprest})


def update_necessities_b(request, id):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    upd = Production_b.objects.get(pk=id)
    form = ProductionForm(request.POST or None, instance=upd)
    if form.is_valid():
        form.save()
        messages.success(request,
                             'Necessities have been Updated')
        return redirect("production_b")

    return render(request, 'poultry_b/update_necessities_b.html', {'form': form, 'upd': upd, 'imprest': imprest})


def delete_models_b(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'POST':
        # Perform deletion of models here
        Feed_b.objects.all().delete()
        Drugs_b.objects.all().delete()
        Production_b.objects.all().delete()
        Necessities_b.objects.all().delete()
        Profit_b.objects.all().delete()
        ColdRoomIn_b.objects.all().delete()

        Offals_b.objects.all().delete()
        Imprest_b.objects.all().delete()
        ChickenFigures_b.objects.all().delete()


        '''customer_ids = ChickenFigures.objects.values('customer').distinct()

        # Extract the IDs as a list
        customer_ids_list = [customer['customer'] for customer in customer_ids]

        # Delete instances matching those 'customer' values
        ChickenFigures.objects.filter(customer=customer_ids_list).delete()'''

        objects_to_update = ChickenFigures_b.objects.all().exclude(customer_rank='customer_rank').delete()


        # Modify the fields you want to delete


        return redirect('index_b')

    return render(request, 'poultry_b/delete_models_b.html', {'imprest': imprest})

