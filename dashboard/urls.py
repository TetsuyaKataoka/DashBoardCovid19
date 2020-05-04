from django.urls import path
from dashboard import views

urlpatterns = [
    path('top/', views.top, name='top'),
    path('index/', views.index, name='index'),
    path('updateReport/', views.update_report, name='update_report'),
    path('updateReports/', views.update_reports, name='update_reports'),
    path('viewCountriesMax/', views.view_countries_max, name='view_countries_max'),
    path('viewReportDetail/', views.view_report_detail, name='view_report_detail'),
    path('viewReportDetailBySort/', views.view_report_detail_by_sort, name='view_report_detail_by_sort'),
    path('sample/', views.sample, name='sample'),

 ]