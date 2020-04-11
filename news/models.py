from django.db import models


class Company(models.Model):
    ticker = models.CharField("Ticker", max_length=7, unique=True, db_index=True)
    name = models.CharField("Name", max_length=255, blank=True, null=True)
    industry = models.CharField("Industry", max_length=255, blank=True, null=True)
    enterprise_value = models.FloatField('EV ($M)', null=True)

    def __str__(self):
        return self.ticker + ' : ' + self.name

class Stock(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index=True)
    date = models.DateTimeField('Time registered')
    open_price = models.FloatField('Stock open price')
    close_price = models.FloatField('Stock close price')

    def __str__(self):
        return str(self.date) + ': ' + self.company.ticker + ' - ' + str(self.open_price) + ' - ' + str(self.close_price)

    @property
    def ticker(self):
        return self.company.ticker

