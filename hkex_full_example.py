'''
Disclaimer:
All calculations done below are for practice purpose
All data and strategy deployed are not meant to be correct, complete, and 
adequate for real-time transaction.

No representation is being made that any account will or is likely to achieve profits or losses similar to those shown.
No opinions are given throughout the whole process.
Users are held responsible for their own judgment and use of the data, information, and any derived implication from this presentation.
'''

'''assumed stock data has been processed and saved to local device'''
import pandas as pd 
import numpy as np 

'''saved the HKEx (yahoo finance ticker == 0388.HK) at local machine, variable 'data_source'''
data_source = r'D:\Tut\hkex_20171024.xlsx'

'''assign table,'df', to read local data from 'data_source' '''
df = pd.read_excel(data_source)

'''create class,'Strategy', to store the tactic logic in; Strategy content is content-specific '''
class Strategy:
	def __init__(self):
		self.t_name = t_name
		self.long_win = long_win
		self.short_win = short_win
		self.calc_cond = df.index >= self.long_win
		self.trade_price = df['Open']
		self.close_price = df['Adj Close']

#calculate short-term (smav) and long-term (lmav) moving average
	def smav(self):
		self.smav = np.where(Strategy().calc_cond, Strategy().close_price.rolling(window = Strategy().short_win).mean(),0)
		return self.smav

	def lmav(self):
		self.lmav = np.where(Strategy().calc_cond, Strategy().close_price.rolling(window = Strategy().long_win).mean(),0)
		return self.lmav

#trend_day equals '1' when up_trend; equals '-1' when down_trend
#when short-term moving average goes above long-term moving average, a long(buy) signal appears
#when short-term moving average goes below long-term moving average, a sell(short) signal appears
	def trend_day(self):
		self.trend_day = np.where(Strategy().smav() > Strategy().lmav(),float(1),
			np.where(Strategy().smav() < Strategy().lmav() ,float(-1),0))
		return self.trend_day

#calculate the "previous trade day's trend" (prev_trend_day) to help generate trade_signal
	def prev_trend_day(self):
		self.prev_trend_day = np.where(Strategy().calc_cond, np.roll(Strategy().trend_day(),1),0)
		return self.prev_trend_day

# if the sum of "trend_day" and "prev_trend_day" is zero, generate the trade_signal that is equal to the current day's trade_signal
	def diff_trend_day(self):
		self.diff_trend_day = Strategy().trend_day() + Strategy().prev_trend_day()
		return self.diff_trend_day

'''create the Signal class to store the logic of trade_signal_generation '''
class Signal:
	def __init__(self):
		self.pattern = Strategy().trend_day() + Strategy().prev_trend_day()

# if the sum of "trend_day" and "prev_trend_day" is zero, generate the trade_signal that is equal to the current day's trade_signal
	def trade_signal(self):
		self.trade_signal = np.where(Strategy().diff_trend_day()==0, Strategy().trend_day(),0)
		return self.trade_signal

# once the trade_signal is generated, place the order event "the day after trade_signal"; since we don't add any cash and deposit restriction in this case, we simply call the trade_signal from previous day
	def order(self):
		self.order = np.where(Strategy().calc_cond, np.roll(Signal().trade_signal(),1),0)
		return self.order

''' create the Portfolio class to manage the stock/asset and cash position
	twist the tactic details such as number of lots(lot_size_long & lot_size_short) and shares per lots (contract_size)
	and start-up capital (initial_cash)
'''
class Portfolio:
	def __init__(self):
		self.lot_size_long = lot_size_long
		self.lot_size_short = lot_size_short
		self.contract_size = contract_size
		self.initial_cash = initial_cash
#calculate the projected amount to pay for long_order (long_amt); expects a negative result
		self.long_amt = (-1)*np.where(Signal().order() == 1, self.lot_size_long*self.contract_size*Strategy().trade_price,0)
#calculate the projected amount to receive for short_order (short_amt); expects a positive result		
		self.short_amt = (1)*np.where(Signal().order() == -1, self.lot_size_short*self.contract_size*Strategy().trade_price,0)

#the change in cash position equals to the amount paid for long_order and amount received from short_order
	def cash_delta(self):
		self.cash_delta = Portfolio().long_amt + Portfolio().short_amt
		return self.cash_delta

#the running total of the cash balance (end_bal) equals to the initial amount plus the accumulated change of cash_delta
	def end_bal(self):
		self.end_bal = Portfolio().initial_cash + Portfolio().cash_delta().cumsum()
		return self.end_bal

#the stock/asset ending position (end_pos) equals to the accumulated amount of effective trade_order up to the current day
	def end_pos(self):
		self.end_pos = Signal().order().cumsum()
		return self.end_pos

'''create an instance of strategy with global variables as follows'''
#tactic name is moving average crossover (mav)
t_name = 'mav'
#20-day is considered "long-term"; this is used in determining long-term moving average, and the day we start our strategy; number of days can be changed to test different scenarios
long_win = 20
#5-day is considered "short-term"; this is used in determining short-term moving average, and the day we start our strategy; number of days can be changed to test different scenarios
short_win = 5

# how many lots to be bought per long_order; this number can be changed to fit different scenarios
lot_size_long = 1
# how many lots to be sold per short_order; this number can be changed to fit different scenarios
lot_size_short = 1
# how many shares in 1 lot 
contract_size = 100
# start-up capital, $10,000, can be changed to fit different scenarios
initial_cash = 10000

#assign class object to different global variables
s = Strategy()
ts = Signal()
p = Portfolio()

''' print out the result for display purpose '''
#short-term moving average
df['smav'] = s.smav()
#long-term moving average
df['lmav'] = s.lmav()
#the day is 'up' or 'down'
df['trend_day'] = s.trend_day()
#the previous day is 'up' or 'down'
df['prev_trend_day'] = s.prev_trend_day()

df['trade_signal'] = ts.trade_signal()
#placed an order when previous day has trade_signal generated
df['order'] = ts.order()

#amount paid to buy assets/stocks 
df['long_amt'] = p.long_amt
#amount received to buy assets/stocks 
df['short_amt'] = p.short_amt

#change in cash position, positive figure indicates cash in-flow and vice versa
df['cash_delta'] = p.cash_delta()

#ending balance of cash 
df['end_bal'] = p.end_bal()
#ending position of stock/asset held; positive means long; negative means short
df['end_pos'] = p.end_pos()

#total value of portfolio equals "cash at hand" (end_bal) and the unrealized value 
# when unrealized value is positive (end_pos > 0); assume selling the long-posiiton stocks at current day's Open price (df['Open'])
# when unrealized value is negative (end_pos < 0); assume borrowing to pay off the liability (close the short position) at current day's Open price (df['Open'])
df['total_asset'] = df['end_bal'] + (df['end_pos']*df['Open']*contract_size)


# print the 31st row up to the 51st row for checking purpose
print(df.loc[30:50,:])
# print the last 21 days (from Oct 24, 2017, inclusive) for display purpose
print(df.tail(21))
#print the data type for each field (column)
print(df.dtypes)

'''using package matplotlib to print stock price graph (optional)'''
import matplotlib.pyplot as plt 

# assign a new table,'df1', where setting table column ['Date'] to be the new index of df1
df1 = df.set_index('Date')

# print the column ['total_asset'] of df1 
pnl_print = df1['total_asset'].plot()

plt.show(pnl_print)