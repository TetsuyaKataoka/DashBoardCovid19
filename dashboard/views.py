import datetime
import pprint
from django.http import JsonResponse
from django.shortcuts import render, redirect
from pandas._libs import json
from dashboard.libraries import logics


# top
def top(request):
    # 最新の集計日付を取得
    latest_report_date = logics.get_latest_report_date()

    # 累計感染者数、陽性患者数、死亡者数、回復者数を算出
    dict_world_summary_report = logics.get_world_summary_report(latest_report_date)

    p = {
        'dict_world_summary_report': dict_world_summary_report
    }
    return render(request, 'mainContent/top.html', p)

# index
def index(request):
    # dict_latest_reports = logics.view_latest_reports_by_country(None)
    # p = {
    #     'message': 'Top Page',
    #     'dict_latest_reports': dict_latest_reports,
    # }
    return render(request, 'dashboard.html')


# レポートの更新
def update_report(request):
    str_report_date = request.POST.get('report_date')

    logics.update_report(str_report_date)
    p = {
        'message': '更新'
    }
    return redirect('top')


# レポートの更新（ループ）
def update_reports(request):
    str_report_date = request.POST.get('report_date')
    update_date = datetime.datetime.strptime(str_report_date, '%Y/%m/%d').date()

    # 最新の集計日付を取得
    latest_report_date = logics.get_latest_report_date()

    while (update_date <= latest_report_date):
        logics.update_report(update_date)
        print(str(update_date) + '集計完了')
        update_date = update_date + datetime.timedelta(days=1)

    return redirect('top')


def view_countries_max(request):
    max_countries = int(request.GET.get('max_countries', None))
    if max_countries == -1:
        max_countries = None

    dict_latest_reports = logics.view_latest_reports_by_country(max_countries)

    p = {
        'dict_latest_reports': dict_latest_reports,
        'message': '読み込みました',
    }
    return render(request, 'canvasArea.html', p)


# sample
def sample(request):
    return render(request, 'mainContent/sampleContent.html')


# 感染者数の詳細を表示する画面のViewメソッド
def view_report_detail(request):
    str_start_date = '2020/03/10'
    start_date = datetime.datetime.strptime(str_start_date, '%Y/%m/%d').date()

    str_end_date = '2020/05/01'
    end_date = datetime.datetime.strptime(str_end_date, '%Y/%m/%d').date()

    dict_report_detail = logics.get_report_detail(start_date, end_date, 7, None)

    p = {
        'dict_report_detail': dict_report_detail
    }
    # pprint.pprint(dict_report_detail, indent=4, width=4)
    return render(request, 'mainContent/report_detail.html', p)


# 感染者数の詳細を表示する画面のViewメソッド(並び替え時)
def view_report_detail_by_sort(request):

    str_start_date = '2020/03/10'
    start_date = datetime.datetime.strptime(str_start_date, '%Y/%m/%d').date()
    str_end_date = '2020/05/01'
    end_date = datetime.datetime.strptime(str_end_date, '%Y/%m/%d').date()

    # ソートの種類をフォームから取得
    sort_type = int(request.GET.get('name_sort_type', None))

    # 上位の国を取得する
    filter_countries = logics.get_filter_countries(sort_type=sort_type, report_date=end_date, number_of_countries=5)

    # レポートの詳細を取得
    dict_report_detail = logics.get_report_detail(start_date, end_date, 7, filter_countries)

    return JsonResponse(json.dumps(dict_report_detail), safe=False)

def main(request):
    return render(request, 'sample.html')