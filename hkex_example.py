'''need the following libraries to get data from yahoo finance'''

import pandas_datareader as pdr 

#need numpy to do calculation
import numpy as np 

#get HKEx, ticker == '0388.HK' from yahoo finance; save the data in dataframe 'df'
# df = pdr.get_data_yahoo('0388.HK')

#let's screen out those trade_days with volume equals zero (we only want valid trade_days)
# df = df[df['Volume']>0]

#for reliability, save the 'df' to excel 
#let's specify the file location in local machine; name the file 'hkex.xlsx'
data_source = r'D:\AlgoTrade\hkex.xlsx'
# df.to_excel(data_source)



#let's point to the "data_source" for our market data 
#before that, we need Python package, Pandas, to read data from Excel
import pandas as pd 

#read data from Excel file 'data_source'; assign the name 'df' to the data 
df = pd.read_excel(data_source)

# remember to comment out the code when we grab HKEx data from yahoo finance

# Let's move on
# Our backtest model is divided into 4 sections:
# market_data, which is the one we just did;
# strategy, which we'll be doing 
# signal, which is the result of strategy
# portfolio, which keep tracks of the investment cash and stock position 

# Once we get the long or short signal, we're going to buy or sell 
# at the DAY FOLLOWING THE SIGNAL DAY, at the OPEN price



#create strategy class to capture our moving average tactic
# define the basic strategy info 
#(t_name: tactic_name, long_win: long-term definition, short_win: short-term definition)
# also we need the df['Open'] column to calculate trade_amount
# df['Adj Close'] to calculate short and long-term moving average
class strategy:
	def __init__(self):
		self.t_name = t_name
		self.long_win = long_win
		self.short_win = short_win
		self.open = df['Open']
		self.close = df['Adj Close']

# calculate the short-term moving average of day close ('Adj Close')
	def smav(self):
		self.smav = np.where(df.index>= self.long_win, self.close.rolling(window=self.short_win).mean(),0)
		return self.smav

# calculate the long-term moving average of day close ('Adj Close')
	def lmav(self):
		self.lmav = np.where(df.index>= self.long_win, self.close.rolling(window=self.long_win).mean(),0)
		return self.lmav

# define the up_trend_day
	def up_trend_day(self):
		self.up_trend_day = np.where(self.smav > self.lmav,1,0)
		return self.up_trend_day

# define the down_trend_day
	def down_trend_day(self):
		self.down_trend_day = np.where(self.smav < self.lmav,-1,0)
		return self.down_trend_day

# count the trade_day when it's in up_trend
# detail explanation is in url: https://www.youtube.com/watch?v=x7HjlxrCStI 
	def up_trend_count(self):
		self.count_value_up_trend = 1
		self.reset_value_up_trend = 0

		self.no_reset_up_trend = (self.up_trend_day == self.count_value_up_trend).cumsum()
		self.reset_up_trend = (self.up_trend_day == self.reset_value_up_trend)

		self.excess_up_trend = np.maximum.accumulate(self.no_reset_up_trend*self.reset_up_trend)
		self.up_trend_count = self.no_reset_up_trend - self.excess_up_trend
		return self.up_trend_count

# count the trade_day when it's in down_trend
# detail explanation is in url: https://www.youtube.com/watch?v=x7HjlxrCStI 
	def down_trend_count(self):
		self.count_value_down_trend = (-1)
		self.reset_value_down_trend = 0

		self.no_reset_down_trend = (self.down_trend_day == self.count_value_down_trend).cumsum()
		self.reset_down_trend = (self.down_trend_day == self.reset_value_down_trend)

		self.excess_down_trend = np.maximum.accumulate(self.no_reset_down_trend*self.reset_down_trend)
		self.down_trend_count = self.no_reset_down_trend - self.excess_down_trend
		return self.down_trend_count


# class Signal:
# 	def __init__(self):
# 		pass

# 	def trade_signal(self):
# 		self.trade_signal = np.where(np.roll(strategy().up_trend_count(),1)==1, 1,
# 			np.where(np.roll(strategy().down_trend_count(),1)==1, -1,0))
# 		return self.trade_signal



#create global variables so that we can change for each instance
t_name = 'mav' #stands for moving average
long_win = 20 # long-term means 20 days; can be varied depending on users
short_win = 5 # short-term means 5 days; can be varied depending on users

#create a strategy class instance; this can add flexibility to tactics e.g. 2 moving mav tactic with diff names
s = strategy()

# ts = Signal()

#add the smav and lmav column to df to check whether our calculation is correct
df['smav'] = s.smav()
df['lmav'] = s.lmav()

df['up_trend_day'] = s.up_trend_day()
df['down_trend_day'] = s.down_trend_day()

df['up_trend_count'] = s.up_trend_count() #check rows 223 to 230 for up_trend_count 1 to 8
df['down_trend_count'] = s.down_trend_count() # check rows 211 to 222 for down_trend_count 1 to 12

# df['trade_signal'] = ts.trade_signal()


print(df[200:250])
print(df.dtypes)