from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE


# 国または地域
class Location(models.Model):
    class Meta:
        db_table = 'location'
        verbose_name = '国または地域'
        verbose_name_plural = 'Location'

    location_id = models.AutoField(primary_key=True)
    province_state = models.CharField('群/州', max_length=100, null=True)
    country_region_name = models.CharField('国または地域', max_length=100, null=False)

    def __str__(self):
        ret = self.country_region_name
        if self.province_state != self.country_region_name:
            ret = self.province_state + ': ' + ret
        else:
            ret = self.country_region_name
        return ret


# 統計
class Report(models.Model):
    class Meta:
        db_table = 'report'
        verbose_name = '世界コロナ統計'
        verbose_name_plural = 'World Coronavirus Report'

    report_id = models.AutoField(primary_key=True, editable=False)
    report_date = models.DateField('日付', null=False)
    location = models.ForeignKey(Location, on_delete=CASCADE, null=False)
    latitude = models.FloatField('緯度', validators=[MinValueValidator(0), MaxValueValidator(90)], null=True)
    longitude = models.FloatField('経度', validators=[MinValueValidator(0), MaxValueValidator(180)], null=True)
    total_cases = models.IntegerField('累計感染者数', validators=[MinValueValidator(0)], null=False, default=0)
    total_deaths = models.IntegerField('累計死亡者数', validators=[MinValueValidator(0)], null=False, default=0)
    total_recovered = models.IntegerField('累計完治者数', validators=[MinValueValidator(0)], null=False, default=0)
    active_cases = models.IntegerField('発症者数', validators=[MinValueValidator(0)], null=False, default=0)

    # str
    def __str__(self):
        return str(self.location)

    # modelを辞書形式に変換する関数
    def to_dict(self):
        return {
            'report_id': self.report_id,
            'report_date': self.report_date,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'total_cases': self.total_cases,
            'total_deaths': self.total_deaths,
            'total_recovered': self.total_recovered,
            'active_cases': self.active_cases,
        }


