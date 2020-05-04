# CSVファイルのカラムとmodelのフィールドの対応付け情報
COLUMNS_PROVINCE_STATE_04 = 'Province_State'
COLUMNS_COUNTRY_REGION_04 = 'Country_Region'
# COLUMNS_REPORT_DATE_04 = 'Last_Update'
COLUMNS_LATITUDE_04 = 'Lat'
COLUMNS_LONGITUDE_04 = 'Long_'
COLUMNS_TOTAL_CASES_04 = 'Confirmed'
COLUMNS_TOTAL_DEATHS_04 = 'Deaths'
COLUMNS_TOTAL_RECOVERED_04 = 'Recovered'
COLUMNS_ACTIVE_CASES_04 = 'Active'

READ_COLUMNS_04 = [COLUMNS_PROVINCE_STATE_04,
                   COLUMNS_COUNTRY_REGION_04,
                   COLUMNS_LATITUDE_04,
                   COLUMNS_LONGITUDE_04,
                   COLUMNS_TOTAL_CASES_04,
                   COLUMNS_TOTAL_DEATHS_04,
                   COLUMNS_TOTAL_RECOVERED_04,
                   COLUMNS_ACTIVE_CASES_04
                   ]

# CSVファイルのカラムとmodelのフィールドの対応付け情報
COLUMNS_PROVINCE_STATE_03 = 'Province/State'
COLUMNS_COUNTRY_REGION_03 = 'Country/Region'
COLUMNS_LATITUDE_03 = 'Latitude'
COLUMNS_LONGITUDE_03 = 'Longitude'
COLUMNS_TOTAL_CASES_03 = 'Confirmed'
COLUMNS_TOTAL_DEATHS_03 = 'Deaths'
COLUMNS_TOTAL_RECOVERED_03 = 'Recovered'

READ_COLUMNS_03 = [COLUMNS_PROVINCE_STATE_03,
                   COLUMNS_COUNTRY_REGION_03,
                   COLUMNS_LATITUDE_03,
                   COLUMNS_LONGITUDE_03,
                   COLUMNS_TOTAL_CASES_03,
                   COLUMNS_TOTAL_DEATHS_03,
                   COLUMNS_TOTAL_RECOVERED_03
                   ]

COLUMN_KEYS = [
    'province_state',
    'country_region',
    'latitude',
    'longitude',
    'confirmed',
    'deaths',
    'recovered',
    'active'
]

# チャートに表示する日付の書式
DATE_FORMAT_CHART = '%m/%d'
# レポートcsvファイルのファイル名の日付書式
DATE_FORMAT_REPORT_CSV = '%m-%d-%Y'

# レポートcsvの格納先パス
DIRECTORY_PATH_REPORT_CSV = 'static/csv/'
