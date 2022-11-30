from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models.functions import TruncMonth
from django.db.models import Value, CharField, Max
from shared.models.config import TeamZone


def build_stacked_bargraph(queryset, categories, months, category_name):
    # categories can be list of string or list of dict with 'name' key
    datasets = []
    category_names = [c['name'] if type(c) is dict else c for c in categories]
    raw_data = {c: {month.strftime("%Y-%m"): 0 for month in months}
                for c in category_names}
    for q in queryset:
        category = q.get(category_name)
        month = q.get('month').strftime("%Y-%m")
        raw_data[category][month] = raw_data[
            category].get(month, 0) + len(
            q.get("id_list_as_string", "").split(";"))
    for cat_name, count_per_month in raw_data.items():
        if len(count_per_month.values()):
            data = [{"x": month, "y": count}
                    for month, count in count_per_month.items()]
            category = categories[category_names.index(cat_name)]
            datasets.append({
                'data': data, 'category': cat_name,
                'color': category['color'] if type(category) is dict else None
            })
    return {'datasets': datasets}


def make_month_list(max_count, counter_model_list):
    try:
        MIN_COUNT = 6
        # oldest month in db
        max_date = max([counter_model.objects.aggregate(Max("date"))['date__max']
                        for counter_model in counter_model_list], default=datetime.today().date())
        # maximum 'max_count' months in list
        max_date = min((datetime.today().replace(
            day=1) + relativedelta(months=-max_count)).date(), max_date)
        # minimum "MIN_COUNT" months in list
        max_date = max(max_date, (datetime.today().replace(
            day=1) + relativedelta(months=-MIN_COUNT)).date())
        max_date = max_date.replace(day=1)
        result = []
        if max_date is not None:
            current = datetime.today().replace(day=1).date()
            while current > max_date:
                result.insert(0, current)
                current = current + relativedelta(months=-1)
        return result
    except Exception as e:
        print(e)
        return []


def get_counter_categories(counter_model_list, max_date, global_category):
    names = []
    for counter_model in counter_model_list:
        names += counter_model.objects.filter(
            date__gte=max_date).exclude(category=global_category).order_by().values_list('category', flat=True).distinct()
    categories = []
    for cat in sorted(set(names)):
        zone = TeamZone.objects.filter(short_name=cat).first()
        categories.append({'name': cat, 'color': zone.color if zone else None})
    return categories


def get_serialized_counters(counter_model_list):
    if not counter_model_list:
        return {}
    MAX_MONTH_COUNT = 24
    GLOBAL_CATEGORY = "Global"
    months = make_month_list(MAX_MONTH_COUNT, counter_model_list)
    max_date = datetime.today().replace(
        day=1) + relativedelta(months=-MAX_MONTH_COUNT)
    categories = get_counter_categories(
        counter_model_list, max_date, GLOBAL_CATEGORY)
    models = [counter_model.chart_name for counter_model in counter_model_list]
    totals = {'all': 0}
    model_month_counters = []
    category_month_counters = []
    for counter_model in counter_model_list:
        queryset = counter_model.objects.filter(date__gte=max_date)
        global_queryset = queryset.filter(category=GLOBAL_CATEGORY)
        total = sum(
            [counter.count for counter in global_queryset.all()])
        totals[counter_model.chart_name] = total
        totals['all'] += total
        model_month_counters += list(global_queryset.annotate(
            month=TruncMonth('date')).annotate(
            model_name=Value(counter_model.chart_name, output_field=CharField())).values('month', 'model_name', 'id_list_as_string').order_by('month').all())
        for cat in categories:
            totals[cat['name']] = totals.get(cat['name'], 0) + sum(
                [counter.count for counter in queryset.filter(category=cat['name']).all()])
        category_month_counters += list(queryset.exclude(category=GLOBAL_CATEGORY).annotate(month=TruncMonth('date')).values(
            'month', 'category', 'id_list_as_string').order_by('month').all())
    category_graph = build_stacked_bargraph(
        category_month_counters, categories, months, 'category')
    model_graph = build_stacked_bargraph(
        model_month_counters, models, months, 'model_name')
    return {
        'categories': categories,
        'forms': models,
        'totals': totals,
        'category_graph': category_graph,
        'form_graph': model_graph
    }
