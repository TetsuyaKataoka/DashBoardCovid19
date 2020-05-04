import datetime
import glob
import os
from scipy import stats
import numpy as np
from dashboard.models import Location, Report
from dashboard.libraries import constants
import pandas as pd


# 日次実績レポートを更新する
def update_report(row_report_date: datetime.date):

    # カラム名を辞書形式で取得
    column_names = get_column_names(row_report_date)
    column_name_province_state = column_names[constants.COLUMN_KEYS[0]]
    column_name_country_region = column_names[constants.COLUMN_KEYS[1]]
    column_name_latitude = column_names[constants.COLUMN_KEYS[2]]
    column_name_longitude = column_names[constants.COLUMN_KEYS[3]]
    column_name_confirmed = column_names[constants.COLUMN_KEYS[4]]
    column_name_deaths = column_names[constants.COLUMN_KEYS[5]]
    column_name_recovered = column_names[constants.COLUMN_KEYS[6]]
    if constants.COLUMN_KEYS[7] in column_names.keys():
        column_name_active = column_names[constants.COLUMN_KEYS[7]]
    else:
        column_name_active = None

    # 文字列型の日付を取得
    str_report_date = row_report_date.strftime(constants.DATE_FORMAT_REPORT_CSV)

    # pandasで指定日付のcsvファイルを読み込み
    csv_file_name = constants.DIRECTORY_PATH_REPORT_CSV + str_report_date + '.csv'
    df_today_report = pd.read_csv(csv_file_name, usecols=column_names.values())

    # ------補完処理------

    # 緯度/経度が空白の行にそれぞれ0を代入
    # 読み込んだcsvファイルにactive caseを指す列がなかった場合補完
    if column_name_active is None:
        df_today_report[constants.COLUMNS_ACTIVE_CASES_04] = df_today_report[column_name_confirmed] - df_today_report[column_name_deaths] - df_today_report[column_name_recovered]
        column_name_active = constants.COLUMNS_ACTIVE_CASES_04

    df_today_report[column_name_latitude] = df_today_report[column_name_latitude].fillna(0)
    df_today_report[column_name_longitude] = df_today_report[column_name_longitude].fillna(0)
    # 州/都が空白の行は'Country_Region'を挿入
    df_today_report[column_name_province_state] = df_today_report[column_name_province_state].fillna(
        df_today_report[column_name_country_region])
    # ------補完処理完了------

    # ------データフレーム前処理------
    # 群/州、国名ごとに合計を算出するデータフレームを用意
    df_sum = df_today_report[[
        column_name_province_state,
        column_name_country_region,
        column_name_confirmed,
        column_name_deaths,
        column_name_recovered,
        column_name_active
    ]]
    # 群/州、国名ごとに合計を算出
    df_sum = df_sum.groupby([column_name_province_state, column_name_country_region]).sum()
    # 群/州、国名ごとに平均を算出するデータフレームを用意
    df_average = df_today_report[[
        column_name_province_state,
        column_name_country_region,
        column_name_latitude,
        column_name_longitude,
    ]]
    df_mean = df_average.groupby([column_name_province_state, column_name_country_region]).mean()

    # データフレームを結合
    df = pd.merge(df_sum, df_mean, on=[column_name_province_state, column_name_country_region], how='inner')

    # 不正値を削除
    df = df[df[column_name_active] >= 0]
    df[column_name_active] = df[column_name_confirmed] - df[column_name_deaths]- df[column_name_recovered]
    # Report_Dateを追加
    df['report_date'] = row_report_date

    for index, row_data in df.iterrows():

        row_province_state = index[0]
        row_country_region_name = index[1]
        row_report_date = row_report_date
        row_latitude = row_data[column_name_latitude]
        row_longitude = row_data[column_name_longitude]
        row_active_cases = row_data[column_name_active]
        row_total_deaths = row_data[column_name_deaths]
        row_total_recovered = row_data[column_name_recovered]
        row_total_cases = row_data[column_name_confirmed]

        # model Countryのレコードを取得。レコードが存在しなければINSERT
        Location.objects.get_or_create(
            province_state=row_province_state,
            country_region_name=row_country_region_name
        )

        # UPSERTするReportをモデルにセット
        upserted_report = Report(
            report_date=row_report_date,
            location=Location.objects.get(
                province_state=row_province_state,
                country_region_name=row_country_region_name
            ),
            latitude=row_latitude,
            longitude=row_longitude,
            total_cases=row_total_cases,
            total_deaths=row_total_deaths,
            total_recovered=row_total_recovered,
            active_cases=row_active_cases
        )

        # reportテーブルにデータが存在するか検証
        record_report = Report.objects.filter(
            report_date=upserted_report.report_date,
            location__province_state=upserted_report.location.province_state,
            location__country_region_name=upserted_report.location.country_region_name,
        )

        # upsert処理
        if len(record_report) == 0:
            upserted_report.save()
        else:
            record_report.update(
                report_date=upserted_report.report_date,
                location=upserted_report.location,
                latitude=upserted_report.latitude,
                longitude=upserted_report.longitude,
                total_cases=upserted_report.total_cases,
                total_deaths=upserted_report.total_deaths,
                total_recovered=upserted_report.total_recovered,
                active_cases=upserted_report.active_cases
            )
    return True


# レポート日付をもとにcsvファイルのカラム情報を辞書形式で取得する
def get_column_names(report_date: datetime.date):
    format_change_date = datetime.date(year=2020, month=3, day=22)
    if report_date.month == 2:
        csv_column_names = constants.READ_COLUMNS_04
    elif report_date < format_change_date:
        csv_column_names = constants.READ_COLUMNS_03
    else:
        csv_column_names = constants.READ_COLUMNS_04

    read_column_names = {}
    for i in np.arange(0, len(csv_column_names)):
        read_column_names[constants.COLUMN_KEYS[i]] = csv_column_names[i]

    return read_column_names

# 最新のレポートを,国別に感染者数の降順上位(max_countries)まで表示する
def view_latest_reports_by_country(max_countries):

    # 今日のレポートをfilterで取得する
    latest_reports = (Report.objects.filter(report_date__day=23)).order_by('total_cases').reverse()

    # クエリセットで取得したレポートをDataFrameにセット
    df_latest_reports = pd.DataFrame(list(latest_reports.values(
        'report_date',
        'location__province_state',
        'location__country_region_name',
        'latitude',
        'longitude',
        'total_cases',
        'total_deaths',
        'total_recovered',
        'active_cases',
    )))
    df_latest_reports = (df_latest_reports.groupby('location__country_region_name', as_index=False).sum()).sort_values('total_cases', ascending=False)

    # 表示件数の上限値対応
    if max_countries is not None:
        df_latest_reports = df_latest_reports[0:max_countries]

    dict_latest_reports = df_latest_reports.to_dict('record')
    return dict_latest_reports


# 世界全体の最新レポートを取得する
# 取得内容：世界全体の　total cases/active cases/total deaths/total recovered
def get_world_summary_report(report_date: datetime.date):
    # 最新日付のレポートを取得する
    yesterday = report_date + datetime.timedelta(days=-1)

    world_summary_reports = (Report.objects.filter(report_date=report_date)).order_by('total_cases')

    world_summary_reports_before_day = (Report.objects.filter(report_date=yesterday)).order_by('total_cases')

    # クエリセットで取得したレポートをDataFrameにセット
    df_world_summary_reports = pd.DataFrame(list(world_summary_reports.values(
        'total_cases',
        'total_deaths',
        'total_recovered',
        'active_cases',
    )))
    # 前日分
    df_world_summary_reports_before_day = pd.DataFrame(list(world_summary_reports_before_day.values(
        'total_cases',
        'total_deaths',
        'total_recovered',
        'active_cases',
    )))

    # データフレームの各行をsum(seriesができる)
    series_world_summary_reports = df_world_summary_reports.sum()
    series_world_summary_reports_before_day = df_world_summary_reports_before_day.sum()

    # 前日比集計
    series_world_summary_reports['diff_total_cases'] = series_world_summary_reports['total_cases'] - \
                                                       series_world_summary_reports_before_day['total_cases']
    series_world_summary_reports['diff_total_deaths'] = series_world_summary_reports['total_deaths'] - \
                                                       series_world_summary_reports_before_day['total_deaths']
    series_world_summary_reports['diff_total_recovered'] = series_world_summary_reports['total_recovered'] - \
                                                           series_world_summary_reports_before_day[
                                                               'total_recovered']
    series_world_summary_reports['diff_active_cases'] = series_world_summary_reports['active_cases'] - \
                                                        series_world_summary_reports_before_day['active_cases']

    series_world_summary_reports['report_date'] = report_date

    # seriesを辞書に変換してreturn
    return series_world_summary_reports.to_dict()


# 世界のレポートのチャートを取得する
def get_world_report_report(start_date: datetime.date, end_date: datetime.date, term):
    # 日付範囲で取得
    reports = Report.objects.filter(report_date__range=(start_date, end_date)).order_by('report_date')

    # 曜日でフィルタ
    reports = reports.filter(report_date__week_day=5)

    # データフレームに変換
    df = pd.DataFrame(list(reports.values(
        'location__country_region_name',
        'total_cases',
        'total_deaths',
        'total_recovered',
        'active_cases',
        'report_date',
    )))
    df = df.groupby(['report_date'], as_index=False).sum(axis=1)

    df.to_csv()


# レポートの詳細を取得する
def get_report_detail(start_date: datetime.date, end_date: datetime.date, term, countries):

    # 日付範囲で取得
    reports = Report.objects.filter(report_date__range=(start_date, end_date)).order_by('report_date')

    # 曜日でフィルタ
    # reports = reports.filter(report_date__week_day=5)

    # 国別に取得
    if countries is not None:
        reports = reports.filter(location__country_region_name__in=countries)

    # データフレームに変換
    df = pd.DataFrame(list(reports.values(
        'location__country_region_name',
        'total_cases',
        'total_deaths',
        'total_recovered',
        'active_cases',
        'report_date',
    )))

    # 検索条件がない場合は感染者数が上位5か国を抽出
    if countries is None:
        # 最新レポート日付の時点で累積感染者数上位5か国を抽出
        top_5_countries = df.loc[df['report_date'] == pd.to_datetime(end_date)].groupby(['location__country_region_name'], as_index=False).sum().sort_values('total_cases', ascending=False).head(5)['location__country_region_name'].values
        # 上位5カ国のみ分の行を抽出
        df = df[df['location__country_region_name'].isin(top_5_countries)]

    df_report_detail = pd.DataFrame()
    # 日別、国別にデータフレームを分割
    dfs = df.groupby(['location__country_region_name'])
    # 国別に集計
    for _country_region_name, _df in dfs:
        _df = _df.groupby(['report_date'], as_index=False).sum()
        _df['country_region_name'] = _country_region_name
        # 新規感染者数
        _df['new_cases'] = _df['total_cases'].diff()
        # 新規感染者数（移動平均）
        _df['new_cases_sma'] = _df['new_cases'].rolling(term).mean()
        # 新規死亡者数
        _df['new_deaths'] = _df['total_deaths'].diff()
        # 新規死亡者増加率
        _df['new_deaths_ratio'] = _df['total_deaths'].pct_change(1).replace([-np.inf, np.inf], np.NaN).fillna(0)
        # 新規死亡者数（移動平均）
        _df['new_deaths_sma'] = _df['new_deaths'].rolling(term).mean()
        # 新規回復者数
        _df['new_recovered'] = _df['total_recovered'].diff()
        # 新規回復者数（移動平均）
        _df['new_recovered_sma'] = _df['new_recovered'].rolling(term).mean()
        # データフレームを縦結合
        df_report_detail = pd.concat([df_report_detail, _df], axis=0)

    # 日付の書式を変換
    df_report_detail['report_date'] = df_report_detail['report_date'].dt.strftime(constants.DATE_FORMAT_CHART)

    df_report_detail.to_csv('detail.csv')
    # データフレームを辞書に変換してreturn
    dict_report_detail = df_report_detail.to_dict('record')
    return dict_report_detail


# 主成分分析を行う
def decompose_data_list(df: pd.DataFrame):
    pass


# 最新のレポートの日付を取得する
def get_latest_report_date():

    latest_report_date = datetime.date(2020, 1, 1)

    paths_report_file = glob.glob(constants.DIRECTORY_PATH_REPORT_CSV+'*.csv')
    for _path in paths_report_file:
        str_report_date = os.path.splitext(os.path.basename(_path))[0]
        report_date = datetime.datetime.strptime(str_report_date, constants.DATE_FORMAT_REPORT_CSV).date()
        # 日付同士の比較
        if report_date > latest_report_date:
            latest_report_date = report_date

    return latest_report_date


# 特定カラムの上位の国を取得する
def get_filter_countries(sort_type, report_date: datetime.date, number_of_countries):

    print(sort_type)

    # 並び替え対象のカラム名(デフォルトは感染者数)
    column_name = 'total_cases'
    if sort_type == 1:
        column_name = 'total_cases'
    elif sort_type == 2:
        column_name = 'total_deaths'
    elif sort_type == 3:
        column_name = 'active_cases'
    else:
        column_name = 'total_recovered'

    # 日付範囲で取得
    reports = Report.objects.filter(report_date=report_date)

    # データフレームに変換
    df = pd.DataFrame(list(reports.values(
        'location__country_region_name',
        column_name
    )))

    countries = df.groupby(['location__country_region_name']).sum().sort_values(column_name, ascending=False).head(number_of_countries).index.values
    return countries





