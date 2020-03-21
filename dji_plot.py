import pandas as pd
import pandas_datareader.data as web
import datetime as dt 

'''get data from Yahoo Finance'''
stock = '^dji'
print_stock_name = stock.replace('^','').upper()
start = '1985-01-01'
end = dt.datetime.today()

#store fetched data in table 'df'
df = web.DataReader(stock, 'yahoo', start, end)

#drop the original df['Close'] column
df.drop(['Close'], axis=1, inplace=True)

#rename the original df['Adj Close'] column to df['Close']
df.rename(columns={'Adj Close':'Close'},inplace=True)

'''import the matplotlib module for graphing'''
from matplotlib import pyplot as plt 
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

'''testing plotting with Chinese'''
import matplotlib.font_manager as mfm

# font_path = r'c:\\Windows\fonts\kaiu.ttf'
font_path=r'c:\\WINDOWS\FONTS\DENG.TTF'
prop = mfm.FontProperties(fname=font_path)
# end

'''Filter Text'''
firstday_dataset = df.index[0]
filter_period_start = '2020-02-01'
filter_period_end = '2020-03-20'
filter_period = (df.index>=filter_period_start) & (df.index<=filter_period_end)
lastday_dataset = pd.to_datetime(df.index[-1]).strftime('%Y-%m-%d')


'''text being used in graph'''
curve1_label_text = f"收市價單日升跌%"
curve2_label_text = f"成交單日升跌%"
title_curve1 = f"{print_stock_name} - {curve1_label_text} - 期間: {filter_period_start} 至 {filter_period_end}"
title_curve2 = f"{print_stock_name} - {curve2_label_text} - 期間: {filter_period_start} 至 {filter_period_end}"


'''Create just a figure and only one subplot'''
plt.style.use('seaborn')
plt.figure()

'''data for graphing'''
x = df.index[filter_period]
#y1 data depicts the percentage change of df['Close'] column for filter period
y1 = (df['Close'].pct_change()*100)[filter_period]
#y2 data depicts the percentage change of df['Volume'] column for filter period
y2 = (df['Volume'].pct_change()*100)[filter_period]


'''Print out graph'''
plt.figure(1) #print everything in graph1

plt.subplot(211) #graph1 has 2 rows and subplot1 is in the 1st row
plt.xlabel(f"日期", color='r', FontProperties=prop)
plt.ylabel(f"{curve1_label_text}",rotation=0, ha='right', color='r',FontProperties=prop)
plt.title(f"{title_curve1}", FontProperties=prop)
plt.plot(x, y1,color='r') #plot data with x-axis using data 'x' , y1 for y-axis


plt.subplot(212) #graph1 has 2 rows and subplot2 is in the 2nd row
plt.xlabel(f"日期", color='b', FontProperties=prop)
plt.ylabel(f"{curve2_label_text}",rotation=0,ha='right',color='b',FontProperties=prop)
plt.title(f"{title_curve2}", FontProperties=prop)
plt.plot(x, y2,color='b') #plot data with x-axis using data 'x' , y2 for y-axis


plt.tight_layout()
plt.show()