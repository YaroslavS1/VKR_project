# from datetime import timedelta, date
import datetime
from VKR_project.vkr_tests.tools import BaseTime

# def daterange(start_date, end_date):
#     for n in range(int((end_date - start_date).days)):
#         yield start_date + datetime.timedelta(n)
#
#
# start_date = datetime.date(2022, 4, 27)
# end_date = datetime.date(2022, 5, 1)
# for single_date in daterange(start_date, end_date):
#     print(single_date.strftime("%Y-%m-%d"))
#
# print(datetime.datetime.strptime('24.05.2010', "%d.%m.%Y").date())

# a = BaseTime('24.05.2010', '26.05.2010')
# print(a.start_date)
# print(a.end_date)
# for i in a.daterange:
#     print(i)
from VKR_project.vkr_tests.tools.ADV import AvgCampaign

a = AvgCampaign(
    name='Test campain',
    start_date='24.05.2010',
    end_date='26.05.2010',
    sum_cost=900
)
e = 0
for i in a.campaign:
    e = e + i.cost
    print(i)
print(e)
