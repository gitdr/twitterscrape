import datetime
import random
from calendar import monthrange


class DateGenerator:
  def generate_dates(self, start_date, end_date):
    num_days = (end_date - start_date).days
    return [start_date + datetime.timedelta(days=x) for x in range(0, num_days + 1)]
  
  def generate_dates_in_random_order(self, start_date, end_date):
    a = self.generate_dates(start_date, end_date)
    random.shuffle(a)
    return a
