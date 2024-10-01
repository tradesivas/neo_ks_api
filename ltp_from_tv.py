import tvDatafeed
from tvDatafeed import TvDatafeed,Interval
from datetime import date, time, datetime as dt
todays_date = date.today()
todays_date = date.today()
tdate = str(todays_date.year)+'-'+str(todays_date.month)+'-'+str(todays_date.day)
symbol = input("Enter Symbol: ")
data = TvDatafeed().get_hist(symbol=symbol,exchange='NSE',interval=Interval.in_daily,n_bars=1)
ltp= data.loc[tdate+' 09:15:00']['close']
print(ltp)