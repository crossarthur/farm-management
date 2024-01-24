from itertools import chain
from django.db.models.query_utils import DeferredAttribute
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.timezone import now

from .forms import *
from django.db.models import F, Sum, Avg, Count, ExpressionWrapper, IntegerField, DateTimeField, Min, Max
from .models import *
from django.contrib import messages
from django.db.models.functions import TruncDate, Trunc, Floor, ExtractYear, ExtractMonth, ExtractDay, ExtractHour, \
    TruncHour, ExtractMinute, TruncMinute, Extract, TruncMonth, ExtractWeek
from datetime import timedelta, datetime
from django.utils import timezone
from poultry_b.models import *


# Create your views here.


def batch(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    total_chicken_num = ChickenFigures.objects.values_list('total_chicken', flat=True).last()
    chickens_out = ChickenFigures.objects.values_list('chicken_out', flat=True).last()
    chicken_in_calculate1 = ChickenFigures.objects.aggregate(cal=Sum('chicken_mortality'))
    chicken_in_calculate = chicken_in_calculate1['cal']
    user = User.objects.all().count()
    most_frequent_user = CustomerRank.objects.values('customer_rk').annotate(
    user_count=Count('customer_rk')).order_by('-user_count').first()
    if most_frequent_user:
        user_value = most_frequent_user['customer_rk']
        user_count = most_frequent_user['user_count']


    imprest_b = Imprest_b.objects.values_list('total_imprest', flat=True).last()
    total_chicken_num_b = ChickenFigures_b.objects.values_list('total_chicken', flat=True).last()
    chickens_out_b = ChickenFigures_b.objects.values_list('chicken_out', flat=True).last()
    chicken_in_calculate1_b = ChickenFigures_b.objects.aggregate(cal=Sum('chicken_mortality'))
    chicken_in_calculate_b = chicken_in_calculate1_b['cal']
    user_b = User.objects.all().count()
    most_frequent_user_b = CustomerRank_b.objects.values('customer_rk').annotate(
    user_count=Count('customer_rk')).order_by('-user_count').first()

    if most_frequent_user_b:
        user_value_b = most_frequent_user['customer_rk']
        user_count = most_frequent_user['user_count']



    context = {
        'imprest': imprest,
        'total_chicken_num': total_chicken_num,
        'chickens_out': chickens_out,
        'user_value': user_value,
        'user': user,
        'chicken_in_calculate': chicken_in_calculate,

        'imprest_b': imprest_b,
        'total_chicken_num_b': total_chicken_num_b,
        'chickens_out_b': chickens_out_b,
        'user_value_b': user_value_b,
        'user_b': user,
        'chicken_in_calculate_b': chicken_in_calculate_b,
    }
    return render(request, 'poultry/batch.html', context)


def add(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
     # Start App By adding birds
    imprest = Imprest.objects.values_list('imprest', flat=True).last()
    if request.method == 'POST':
        form = ChickenForm(request.POST)
        if form.is_valid():
            instance = form.save()

            messages.success(request, f'Total Number of Birds in Poultry is {instance.total_chicken}')
            return redirect('index')
    else:
        form = ChickenForm()
        return render(request, 'poultry/add.html', {'form': form, 'imprest': imprest})


def register(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    # staff registration form
    if request.user.is_superuser:
        imprest = Imprest.objects.values_list('imprest', flat=True).last()
        if request.method == 'POST':
            form = SignupForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request, f'Welcome, Please Login')
                return redirect('.')

        else:
            form = SignupForm()

        return render(request, 'poultry/register.html', {'form': form, 'imprest': imprest})


def index(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    imprest1 = Imprest.objects.all()
    rating = CustomerRank.objects.all()
    # Last 7 days/ last 2 months
    now = timezone.now()
    result = Profit.objects.aggregate(
        total=models.Max('expenditure'),
        today=models.Max('expenditure', filter=models.Q(date=now.date())),
        yesterday=models.Max('expenditure', filter=models.Q(date__gte=(now - timedelta(minutes=2)).date())),
        last_7_day=models.Max('expenditure', filter=models.Q(date__gte=(now - timedelta(days=20)).date())),
    )

    # for chicken out in index
    overview = ChickenFigures.objects.all().order_by('-date')

    # Chicken in Graph every 2 hours
    # prnts = ChickenFigures_b.objects.annotate(hour=ExtractHour('date'), interval=F('hour') / 2 * 2).values(
        #'hour').annotate(sum=Sum('chicken_in')).values('hour', 'sum')
    prnts = ChickenFigures.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Sum('chicken_in'))

    prnts2 = ChickenFigures.objects.annotate(hour=ExtractHour('date'), interval=(F('hour') / 2) * 2).values('interval',
                                                                                                            'total_chicken').values_list(
        'interval', flat=True).distinct()

    # computation for total number of chickens, sum of feed, drugs necessities and production at intervals
    total_chicken_num = ChickenFigures.objects.values_list('total_chicken', flat=True).last()
    feed_total_cost = Feed.objects.aggregate(cal=Sum('feed_cost'))
    feed_total = feed_total_cost['cal']
    feed = Feed.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Sum('feed_cost')).values('week', 'sum')

    necs = Necessities.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Sum('necessities_cost')).values('week', 'sum')
    pros = Production.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Sum('production_cost')).values('week', 'sum')
    drugs_total_cost = Drugs.objects.aggregate(cal=Sum('drug_cost'))
    drugs_total = drugs_total_cost['cal']
    drugs = Drugs.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Sum('drug_cost')).values('week', 'sum')
    graph_income = ChickenFigures.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Sum('chicken_out_total_cost')).values('week', 'sum')
    print(f'expen {total_chicken_num}total_chicken_num')


    # total expenditure
    production1 = Production.objects.aggregate(cal=Sum('production_cost'))
    pro = production1['cal']
    feed1 = Feed.objects.aggregate(cal=Sum('feed_cost'))
    fee = feed1['cal']
    drug = Drugs.objects.aggregate(cal=Sum('drug_cost'))
    dru = drug['cal']
    necessities1 = Necessities.objects.aggregate(cal=Sum('necessities_cost'))
    nec = necessities1['cal']

    if pro is not None and fee is not None and dru is not None and nec is not None:
        expenditure = (pro + fee + dru + nec)
        print(f' ex {expenditure}')
    else:
        expenditure = 0


    # total income
    chickens_out = ChickenFigures.objects.aggregate(cal=Sum('chicken_out_total_cost'))
    offals = Offals.objects.aggregate(cal=Sum('offals_cost'))
    graph_income = ChickenFigures.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Sum('chicken_out_total_cost')).values('week', 'sum')
    graph_income = Profit.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Max('income')).values('week', 'sum')

    income_chicken_out = chickens_out['cal']
    income_offals = offals['cal']
    profs = Profit.objects.values_list('income', flat=True).last()
    print(f'this is chi {income_offals}')


    cal = 0
    if income_chicken_out is not None:
        income = income_chicken_out
        print(f'tis is prof {profs}')
        cal = income - expenditure
        graph_exp = Profit(expenditure=expenditure, income=income)
        Profit.objects.create(calculate=cal)
        graph_exp.save()

    else:
        income1 = 0
        income2 = 0
        income = 0

    print(f'exp{expenditure}')
    print(graph_income)

    if cal < 0:
        print('loss')
    else:
        print('profit')

    # profit/loss arrow
    total_chicken_nu = ChickenFigures.objects.values_list('chicken_out_total_cost', flat=True).last()
    if income_offals is not None:
        income1 = income_offals + income
        print(f' this is the real {income_offals}')
        cal = income1 - expenditure
        graph_exp = Profit(expenditure=expenditure, income=income1)
        Profit.objects.create(calculate=cal)
        graph_exp.save()
    fin = 0
    if cal != 0:
        fin = (total_chicken_nu / cal) * 100

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
    prof = Profit.objects.annotate(week=ExtractWeek('date')).values('week').annotate(sum=Max('calculate')).values('week', 'sum')

    profs = Profit.objects.values_list('calculate', flat=True).last()
    print(prof)

    feed1 = Feed.objects.annotate(hour=ExtractHour('date'), interval=F('hour') / 2 * 2).values('hour').annotate(
        sum=Sum('feed_cost')).values('hour', 'sum').distinct()
    necs1 = Necessities.objects.annotate(hour=ExtractHour('date'), interval=F('hour') / 2 * 2).values('hour').annotate(
        sum=Sum('necessities_cost')).values('hour', 'sum').distinct()
    pros1 = Production.objects.annotate(hour=ExtractHour('date'), interval=F('hour') / 2 * 2).values('hour').annotate(
        sum=Sum('production_cost')).values('hour', 'sum').distinct()
    drugs1 = Drugs.objects.annotate(hour=ExtractHour('date'), interval=F('hour') / 2 * 2).values('hour').annotate(
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
    most_frequent_user = CustomerRank.objects.values('customer_rk').annotate(
    user_count=Count('customer_rk')).order_by('-user_count').first()

    if most_frequent_user:
        user_value = most_frequent_user['customer_rk']
        user_count = most_frequent_user['user_count']






    # most frequent Drug Type
    most_frequent_drug = Drugs.objects.values('drug_description').annotate(
    drug_count=Count('drug_description')).order_by('-drug_count').first()

    if most_frequent_drug:
        drug_value = most_frequent_drug['drug_description']
        drug_count = most_frequent_drug['drug_count']


    # most frequent necessity

    most_frequent_nec = Necessities.objects.values('necessities_description').annotate(
    nec_count=Count('necessities_description')).order_by('-nec_count').first()

    if most_frequent_nec:
        nec_value = most_frequent_nec['necessities_description']
        nec_count = most_frequent_nec['nec_count']

     # most frequent feed_b

    most_frequent_feed = Feed.objects.values('feed_description').annotate(
    feed_count=Count('feed_description')).order_by('-feed_count').first()

    if most_frequent_feed:
        feed_value = most_frequent_feed['feed_description']
        feed_count = most_frequent_feed['feed_count']

    profs = Profit.objects.values_list('income', flat=True).last()


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
        'fin': fin,
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
    return render(request, 'poultry/index.html', context)


def delete_chicken(request, id):
    delete = ChickenFigures.objects.get(pk=id)
    delete.delete()
    return redirect('index')


def chicken(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')

    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    total_chicken_num = ChickenFigures.objects.values_list('total_chicken', flat=True).last()
    print(total_chicken_num)
    all_chicken_in = ChickenFigures.objects.all().order_by('-date')
    trun = ChickenFigures.objects.annotate(day=TruncDate('date')).values('day', ).annotate(c=Sum('chicken_in')).values(
        'day', )
    prnt = ChickenFigures.objects.filter(date=datetime(2023, 12, 23) - timedelta(days=1))
    prnts = ChickenFigures.objects.annotate(
        hour=ExtractHour('date'),
        days=F('hour') / 2 * 2
    ).values('hour', 'total_chicken')
    # prnts = ChickenFigures.objects.annotate(hour=TruncHour('date')).values('hour',).annotate(f=Sum('total_chicken')).values('hour', 'f')
    print(prnts)
    # total_chicken_num = total_chicken['sum']

    chicken_in_calculate = ChickenFigures.objects.aggregate(cal=Sum('chicken_in'))
    # chicken_in_calculate = ChickenFigures.objects.aggregate(Sum('name__chicken_in')).values()
    total_chicken_in = chicken_in_calculate['cal']

    date =  None
    queryset = None


    if request.method == 'GET':
        date = request.GET.get('date')
        print(date)
        # Filter data based on the selected date range
        if date:
            queryset = ChickenFigures.objects.filter(date__icontains=date)
            print(queryset)


        else:
            date = None
            queryset = ChickenFigures.objects.all()


    if request.method == 'POST':
        form = ChickenFigureForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            if instance.chicken_in is not None and total_chicken_num is not None:
                total_chicken_num += instance.chicken_in

                tot = ChickenFigures(total_chicken=total_chicken_num, chicken_in=instance.chicken_in)
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
        'imprest': imprest,


    }

    return render(request, 'poultry/chicken.html', context)


def chickens_out(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    # chickens_d = ChickenFigures.objects.get(chicken_details=request.user.id)
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    overview = ChickenFigures.objects.all().order_by('-date')
    total_chicken_num = ChickenFigures.objects.values_list('total_chicken', flat=True).last()
    chicken_out_total_cost_num = ChickenFigures.objects.values_list('chicken_out_total_cost', flat=True).last()
    print(chicken_out_total_cost_num)
    # total_chicken_num = total_chicken['sum']

    chicken_in_calculate = ChickenFigures.objects.aggregate(cal=Sum('chicken_in'))
    # chicken_in_calculate = ChickenFigures.objects.aggregate(Sum('name__chicken_in')).values()
    # total_chicken_in = chicken_in_calculate['cal']
    total2 = ColdRoomIn.objects.values_list('total_coldroom', flat=True).last()
    date = ''
    queryset = ''
    if request.method == 'GET':
        date = request.GET.get('date')
        print(date)
        # Filter data based on the selected date range
        if date:
            queryset = ChickenFigures.objects.filter(date__icontains=date)
            print(queryset)

        else:
            date = None
            queryset = ChickenFigures.objects.all()

    if request.method == 'POST':
        form = ChickenOutForm(request.POST)

        if form.is_valid():
            customer1 = form.cleaned_data['customer']
            instance = form.save(commit=False)

            if instance.chicken_out_kilogram > 0 and instance.chicken_out_unit_price > 0 and instance.chicken_out > 0 and instance.customer is not None and instance.total_chicken is not None:
                total_chicken_num -= instance.chicken_out
                chicken_out_total_cost_num = instance.chicken_out_kilogram * instance.chicken_out_unit_price
                tot1 = ChickenFigures(total_chicken=total_chicken_num, chicken_out=instance.chicken_out,
                                      chicken_out_total_cost=chicken_out_total_cost_num,
                                      chicken_out_kilogram=instance.chicken_out_kilogram,
                                      chicken_out_unit_price=instance.chicken_out_unit_price, customer=instance.customer, customer_rank=customer1)
                tot2 = CustomerRank(customer_rk=customer1)
                '''total3 = instance.chicken_out - total2
                tot3 = ColdRoomIn(total_coldroom=total3)
                tot3.save()'''
                tot2.save()
                tot1.save()

                messages.success(request, f'Total cost of chickens out is ₦{chicken_out_total_cost_num}')

                if instance.chicken_out == 1:
                    messages.error(request, f'{instance.chicken_out} Chicken has been taken out.')
                    return redirect('.')
                elif instance.chicken_out >= 1:

                    messages.error(request, f'{instance.chicken_out} Chickens have been taken out.')
                    return redirect('.')

            else:
                total_chicken_num -= instance.chicken_out
                tot1 = ChickenFigures(total_chicken=total_chicken_num, chicken_out=instance.chicken_out)
                tot1.save()
                return redirect('chickens_out')
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

    return render(request, 'poultry/chickens_out.html', context)


def chickens_slaughtered(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    overview = ChickenFigures.objects.all().order_by('-date')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    # chickens_d = ChickenFigures.objects.get(chicken_details=request.user.id)
    total_chicken_num = ChickenFigures.objects.values_list('total_chicken', flat=True).last()
    print(total_chicken_num)
    # total_chicken_num = total_chicken['sum']

    chicken_in_calculate1 = ChickenFigures.objects.aggregate(cal=Sum('chicken_slaughtered'))
    # chicken_in_calculate = ChickenFigures.objects.aggregate(Sum('name__chicken_in')).values()
    chicken_in_calculate = chicken_in_calculate1['cal']
    print(chicken_in_calculate)

    if request.method == 'POST':
        form = ChickenSlaughteredForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            if instance.chicken_slaughtered is not None:
                total_chicken_num -= instance.chicken_slaughtered

                tot = ChickenFigures(total_chicken=total_chicken_num, chicken_slaughtered=instance.chicken_slaughtered)
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
        'chicken_in_calculate': chicken_in_calculate
    }
    return render(request, 'poultry/chickens_slaughtered.html', context)


def chickens_mortality(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    overview = ChickenFigures.objects.all().order_by('-date')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    # chickens_d = ChickenFigures.objects.get(chicken_details=request.user.id)
    total_chicken_num = ChickenFigures.objects.values_list('total_chicken', flat=True).last()
    print(total_chicken_num)
    # total_chicken_num = total_chicken['sum']

    chicken_in_calculate = ChickenFigures.objects.aggregate(cal=Sum('chicken_mortality'))
    # chicken_in_calculate = ChickenFigures.objects.aggregate(Sum('name__chicken_in')).values()
    total_chicken_in = chicken_in_calculate['cal']

    if request.method == 'POST':
        form = ChickenMortalityForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            if instance.chicken_mortality is not None:
                total_chicken_num -= instance.chicken_mortality

                tot = ChickenFigures(total_chicken=total_chicken_num, chicken_mortality=instance.chicken_mortality)
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
    return render(request, 'poultry/chickens_mortality.html', context)



def feed(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.feed_quantity is not None and instance.feed_cost is not None and instance.feed_description is not None:
                instance.save()
                form = FeedForm()
                messages.success(request, f'{instance.feed_quantity}KG of {instance.feed_description} has been submitted')
                return redirect('feed_overview')

            else:
                messages.error(request, 'error')
    else:
        form = FeedForm()
    context = {
        'form': form,
        'imprest': imprest,
    }
    return render(request, 'poultry/feed.html', context)


def feed_overview(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    chickens_feed = Feed.objects.all().order_by('-date')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'GET':
        date = request.GET.get('date')
        print(date)
        # Filter data based on the selected date range
        if date:
            queryset = Feed.objects.filter(date__icontains=date)
            print(queryset)

        else:
            date = None
            queryset = Feed.objects.all()

    context = {
        'chickens_feed': chickens_feed,
        "imprest": imprest,
        'date': date,
        'queryset': queryset
    }
    return render(request, 'poultry/feed_overview.html', context)


def drugs(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'POST':
        form = DrugForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.drug_cost is not None and imprest is not None and instance.drug_cost <= imprest:
                imprest -= instance.drug_cost
                tot = Imprest(total_imprest=imprest)
                tot2 = Drugs(drug_cost=instance.drug_cost,  drug_description=instance.drug_description)
                tot.save()
                tot2.save()
                messages.success(request, f'₦{instance.drug_cost} for {instance.drug_description} has been submitted')
                return redirect('drugs_overview')
            elif instance.drug_cost > imprest:
                messages.error(request, 'Insufficient funds in imprest')
                return redirect(".")
            else:
                messages.error(request, 'Error')
                return redirect('drugs_overview')

    else:
        form = DrugForm()
    context = {
        'form': form,
        'imprest': imprest
    }
    return render(request, 'poultry/drugs.html', context)


def drugs_overview(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    chickens_drug = Drugs.objects.all().order_by('-date')
    if request.method == 'GET':
        date = request.GET.get('date')
        print(date)
        # Filter data based on the selected date range
        if date:
            queryset = Drugs.objects.filter(date__icontains=date)
            print(queryset)

        else:
            date = None
            queryset = Drugs.objects.all()
        context = {
            'chickens_drug': chickens_drug,
            'queryset': queryset,
            'date': date,
            'imprest':imprest,
        }
        return render(request, 'poultry/drugs_overview.html', context)


def delete_drugs(request, id):
    delete2 = Drugs.objects.get(pk=id)
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    if delete2 and delete2.drug_cost is not None and imprest is not None and delete2.drug_cost <= imprest:
                imprest += delete2.drug_cost
                tot = Imprest(total_imprest=imprest)
                tot.save()

                delete2.delete()
                return redirect('drugs_overview')


def necessities(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'POST':
        form = NecessitiesForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request,
                             f'₦{instance.necessities_cost} for {instance.necessities_description} has been submitted')
            return redirect('necessities_overview')

    else:
        form = NecessitiesForm()
    context = {
        'form': form,
        'imprest': imprest,
    }
    return render(request, 'poultry/necessities.html', context)


def necessities_overview(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    necessities = Necessities.objects.all().order_by('-date')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'GET':
        date = request.GET.get('date')
        print(date)
        # Filter data based on the selected date range
        if date:
            queryset = Necessities.objects.filter(date__icontains=date)
            print(queryset)

        else:
            date = None
            queryset = Necessities.objects.all()
        context = {
            'necessities': necessities,
            'queryset': queryset,
            'date': date,
            'imprest': imprest,
        }
        return render(request, 'poultry/necessities_overview.html', context)



def coldroom_in(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    global queryset, date
    t = ColdRoomIn.objects.filter(chickens_in_freezer=request.user.id)
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    out = ChickenFigures.objects.values_list('chicken_out', flat=True).last()
    total2 = ColdRoomIn.objects.values_list('total_coldroom', flat=True).last()
    total = ColdRoomIn.objects.all().order_by('-date')
    # total_coldroom_in = ColdRoomIn.objects.aggregate(cal=Sum('chickens_in_freezer'))
    # total_coldroom = total_coldroom_in['cal']

    if request.method == 'GET':
        date = request.GET.get('date')
        print(date)
        # Filter data based on the selected date range
        if date:
            queryset = ColdRoomIn.objects.filter(date__icontains=date)
            print(queryset)

        else:
            date = None
            queryset = ColdRoomIn.objects.all()

    if request.method == 'POST':
        form = ColdRoomInForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.chickens_in_freezer is not None and total2 is not None:
                total2 += instance.chickens_in_freezer
                sav = ColdRoomIn(total_coldroom=total2, chickens_in_freezer=instance.chickens_in_freezer)
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
    return render(request, 'poultry/coldroom_in.html', context)


def total_coldroom(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
     # Start App By adding birds
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    total2 = ColdRoomIn.objects.values_list('total_coldroom', flat=True).last()
    if request.method == 'POST':
        form = ColdRoomOutForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Chicken Added')
            return redirect('coldroom_in')
    else:
        form = ColdRoomOutForm()
    return render(request, 'poultry/total_coldroom.html', {'form': form, "imprest": imprest, 'total2': total2})


def production(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    total_production = Production.objects.aggregate(cal=Sum('production_cost'))
    total_production2 = total_production['cal']
    total = Production.objects.all().order_by('-date')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    production = Production.objects.values_list('production_cost', flat=True).last()

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
            queryset = Production.objects.filter(date__icontains=date)
            print(queryset)

        else:
            date = None
            queryset = Production.objects.all()

    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.production_cost is not None and imprest is not None and instance.production_cost <= imprest:
                imprest -= instance.production_cost
                tot = Imprest(total_imprest=imprest)
                tot2 = Production(production_cost=instance.production_cost,  production_description=instance.production_description)
                tot.save()
                tot2.save()
                messages.success(request, f'{instance.production_description} has been submitted')
                return redirect(".")
            elif instance.production_cost > imprest:
                messages.error(request, 'Insufficient funds in imprest')
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
        return render(request, 'poultry/production.html', context)


def delete_production(request, id):
    delete2 = Production.objects.get(pk=id)
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    if delete2 and delete2.production_cost is not None and imprest is not None and delete2.production_cost <= imprest:
                imprest += delete2.production_cost
                tot = Imprest(total_imprest=imprest)
                tot.save()

                delete2.delete()
                return redirect('production')


def delete_models(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'POST':
        # Perform deletion of models here
        Feed.objects.all().delete()
        Drugs.objects.all().delete()
        Production.objects.all().delete()
        Necessities.objects.all().delete()
        Profit.objects.all().delete()
        ColdRoomIn.objects.all().delete()

        Offals.objects.all().delete()
        Imprest.objects.all().delete()
        ChickenFigures.objects.all().delete()


        '''customer_ids = ChickenFigures.objects.values('customer').distinct()

        # Extract the IDs as a list
        customer_ids_list = [customer['customer'] for customer in customer_ids]

        # Delete instances matching those 'customer' values
        ChickenFigures.objects.filter(customer=customer_ids_list).delete()'''

        objects_to_update = ChickenFigures.objects.all().exclude(customer_rank='customer_rank').delete()


        # Modify the fields you want to delete


        return redirect('index')

    return render(request, 'poultry/delete_models.html', {'imprest': imprest})


def update_chicken(request, id):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    total_chicken_num = ChickenFigures.objects.values_list('total_chicken', flat=True).last()
    upd = ChickenFigures.objects.get(pk=id)
    form = ChickenFigureForm(request.POST or None, instance=upd)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.chicken_in is not None and total_chicken_num is not None:
            total_chicken_num += instance.chicken_in

            tot = ChickenFigures(total_chicken=total_chicken_num, chicken_in=instance.chicken_in)
            tot.save()

            if instance.chicken_in == 1:
                messages.success(request, f'{instance.chicken_in} Chicken has been added.')
                return redirect('chicken')
            elif instance.chicken_in >= 1:
                messages.success(request, f'{instance.chicken_in} Chickens have been added.')
                return redirect('chicken')

        elif request.method == 'POST':
            chicks = request.POST.get('chicks')
            edit = ChickenFigures.objects.get(pk=id)
            edit.chicken_out = chicks
            if edit.chicken_out is not None and instance.chicken_in is not None and total_chicken_num is not None:
                total_chicken_num -= edit.chicken_out
                tot = ChickenFigures(total_chicken=total_chicken_num, chicken_out=edit.chicken_out, chicken_in=instance.chicken_in)
                tot.save()

                if edit.chicken_out == 1:
                    messages.error(request, f'{instance.chicken_out} Chicken has been taken out.')
                    return redirect('chicken')
                elif edit.chicken_out >= 1:
                    messages.error(request, f'{instance.chicken_out} Chickens have been taken out.')
                    return redirect('chicken')

    return render(request, 'poultry/update_chicken.html', {'form': form, 'upd': upd, 'imprest': imprest})


def update_chicken_out(request, id):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    total_chicken_num = ChickenFigures.objects.values_list('total_chicken', flat=True).last()
    upd = ChickenFigures.objects.get(pk=id)
    form = ChickenOutForm(request.POST or None, instance=upd)
    if form.is_valid():
            customer1 = form.cleaned_data['customer']
            instance = form.save(commit=False)

            if instance.chicken_out_kilogram > 0 and instance.chicken_out_unit_price > 0 and instance.chicken_out > 0 and instance.customer is not None and instance.total_chicken is not None:
                total_chicken_num -= instance.chicken_out
                chicken_out_total_cost_num = instance.chicken_out_kilogram * instance.chicken_out_unit_price
                tot1 = ChickenFigures(total_chicken=total_chicken_num, chicken_out=instance.chicken_out,
                                      chicken_out_total_cost=chicken_out_total_cost_num,
                                      chicken_out_kilogram=instance.chicken_out_kilogram,
                                      chicken_out_unit_price=instance.chicken_out_unit_price, customer=instance.customer, customer_rank=customer1)
                tot2 = CustomerRank(customer_rk=customer1)
                tot2.save()
                tot1.save()

                messages.success(request, f'Total cost of chickens out is ₦{chicken_out_total_cost_num}')

                if instance.chicken_out == 1:
                    messages.error(request, f'{instance.chicken_out} Chicken has been taken out.')
                    return redirect('chickens_out')
                elif instance.chicken_out >= 1:

                    messages.error(request, f'{instance.chicken_out} Chickens have been taken out.')
                    return redirect('chickens_out')

            else:
                total_chicken_num -= instance.chicken_out
                tot1 = ChickenFigures(total_chicken=total_chicken_num, chicken_out=instance.chicken_out)
                tot1.save()
                return redirect('chickens_out')

    return render(request, 'poultry/update_chicken_out.html', {'form': form, 'upd': upd, 'imprest': imprest})


def update_drugs(request, id):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    upd = Drugs.objects.get(pk=id)
    print(upd.drug_cost + imprest)
    form = DrugForm(request.POST or None, instance=upd)
    imprest1 = Imprest.objects.values_list('imprest', flat=True).last()
    if form.is_valid():
            instance = form.save(commit=False)
            if instance.drug_cost is not None and imprest is not None and instance.drug_cost <= imprest:
                imprest -= instance.drug_cost
                tot = Imprest(total_imprest=imprest)
                tot2 = Drugs(drug_cost=instance.drug_cost,  drug_description=instance.drug_description)
                tot.save()
                tot2.save()
                messages.success(request, f'₦{instance.drug_cost} for {instance.drug_description} has been Updated')
                return redirect('drugs_overview')

            else:
                messages.error(request, 'Insufficient funds in impress')
                return redirect('drugs_overview')

    return render(request, 'poultry/update_drugs.html', {'form': form, 'upd': upd, 'imprest': imprest})


def update_feed(request, id):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    upd = Feed.objects.get(pk=id)
    form = FeedForm(request.POST or None, instance=upd)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.feed_quantity is not None and instance.feed_cost is not None and instance.feed_description is not None:
            instance.save()
            form = FeedForm()
            messages.success(request, f'{instance.feed_quantity}KG of {instance.feed_description} has been updated')
            return redirect('feed_overview')

        else:
            messages.error(request, 'error')

    return render(request, 'poultry/update_feed.html', {'form': form, 'upd': upd, 'imprest': imprest})


def update_production(request, id):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    upd = Production.objects.get(pk=id)
    form = ProductionForm(request.POST or None, instance=upd)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.production_cost is not None and imprest is not None and instance.production_cost <= imprest:
            imprest -= instance.production_cost
            tot = Imprest(total_imprest=imprest)
            tot2 = Production(production_cost=instance.production_cost, production_description=instance.production_description)
            tot.save()
            tot2.save()
            messages.success(request, 'Production have been updated')
            return redirect('production')

        else:
            messages.error(request, 'Insufficient funds in impress')
            return redirect('production')


    return render(request, 'poultry/update_production.html', {'form': form, 'upd': upd, 'imprest': imprest})


def update_necessities(request, id):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    upd = Production.objects.get(pk=id)
    form = ProductionForm(request.POST or None, instance=upd)
    if form.is_valid():
        form.save()
        messages.success(request,
                             'Necessities have been Updated')
        return redirect("production")

    return render(request, 'poultry/update_necessities.html', {'form': form, 'upd': upd, 'imprest': imprest})


def total_imprest(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'POST':
        form = TotalImprestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Input for Imprest')
            return redirect('index')
    else:
        form = TotalImprestForm()
    return render(request, 'poultry/total_imprest.html', {'form': form, 'imprest': imprest})


def imprest(request):
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    drugs = Drugs.objects.values_list('drug_cost', flat=True).last()
    production = Production.objects.values_list('production_cost', flat=True).last()

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
                tot = Imprest(imprest=instance.imprest, total_imprest=w)
                tot.save()
                messages.success(request, 'Imprest Added')
                return redirect('.')

    else:
        form = ImprestForm()
    context = {
        'form': form,
        'imprest': imprest,
        }
    return render(request, 'poultry/imprest.html', context)


def notepad(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'POST':
        form = NotePadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your note has been saved')
            return redirect('notepad_overview')
    else:
        form = NotePadForm()
    return render(request, 'poultry/notepad.html', {'form': form, 'imprest': imprest})


def notepad_overview(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    note = NotePad.objects.all().order_by('-date')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    if request.method == 'GET':
        date = request.GET.get('date')

        # Filter data based on the selected date range
        if date:
            queryset = NotePad.objects.filter(date__icontains=date)
            print(queryset)

        else:
            date = None
            queryset = NotePad.objects.all()
        return render(request, 'poultry/notepad_overview.html', {'note': note, 'date': date, 'queryset': queryset, 'imprest': imprest})


def notepad_detail(request, id):
    upd = NotePad.objects.get(pk=id)
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()

    return render(request, 'poultry/notepad_detail.html', {'upd': upd, 'imprest': imprest})


def notepad_delete(request, id):
    delete2 = NotePad.objects.get(pk=id)
    messages.success(request, f'{delete2.title} has been deleted')
    delete2.delete()
    return redirect('notepad_overview')


def offals(request):
    if not request.user.is_authenticated:
        messages.error(request, ' Please Login to Continue')
        return redirect('login')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    income = Profit.objects.values_list('income', flat=True).last()
    print(income)
    if request.method == 'POST':
        form = OffalsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.offals_cost is not None and income is not None:
                income += instance.offals_cost
                print(f'this is {income}')
                tot = Profit(income=income)
                tot2 = Offals(offals_cost=instance.offals_cost, offals_description=instance.offals_description)
                tot.save()
                tot2.save()
                messages.success(request, 'offals have been submitted')
                return redirect('offals_overview')
    else:
        form = OffalsForm()

    context = {
        'form': form,
        'imprest': imprest,
    }
    return render(request, 'poultry/offals.html', context)


def offals_overview(request):
    off = Offals.objects.all().order_by('-date')
    imprest = Imprest.objects.values_list('total_imprest', flat=True).last()
    context = {
        'off': off,
        'imprest': imprest,
    }
    return render(request, 'poultry/offals_overview.html', context)
