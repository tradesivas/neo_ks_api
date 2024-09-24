import requests
import os
import datetime
from datetime import date
todays_date = date.today()
tdate = str(todays_date.day).zfill(2)+'_'+str(todays_date.month).zfill(2)+'_'+str(todays_date.year)
fno_url = 'https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_FNO_'+tdate+'.txt'    #change needed everyday
cash_url = 'https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_CASH_'+tdate+'.txt'
fno_file = 'ks_fno_scripmaster.txt'
cash_file = 'ks_cash_scripmaster.txt'
fno = requests.get(fno_url, allow_redirects=True)
open(fno_file, 'wb').write(fno.content)
cash = requests.get(cash_url, allow_redirects=True)
open(cash_file, 'wb').write(cash.content)