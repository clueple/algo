
#need the 2 libraries - pandas and numpy - to process market data and trade logic
import pandas as pd 
import numpy as np 

# Data location; can be stored locally or from web
# In complicated backtest model, this part is done in 'market_data' class
data_source = r'D:\Algo\short_example.xlsx'


# Extract data from data_source
# In this case
df = pd.read_excel(data_source,skiprows=9).loc[:, 'trade_day':'end_bal']

# Strategy is the logic to generate trade_signal
# Assume we've already processed the strategy and am ready to generate trade_signal
class strategy:
	def __init__(self,t_name):
		self.t_name = t_name
#number of lots to execute in a 'long'(buy) order
		self.long_pos = 1
#number of lots to execute in a 'short'(sell) order		
		self.short_pos = 1 
#the 'Open' price of stock/index; in this strategy, trade at 'Open' price when trade_signal appears
		self.open = df['Open']

# trade_signal == 1 indicates a long order whereas -1 indicates a short order
#trade_signal is determined based on strategy; for simplicity, only read from the excel file 'data_source' in this case
class trade_signal:
	def __init__(self):
		self.trade_signal = df['trade_signal']
		return self.trade_signal
	
# The portfolio class calculates the pnl (profit & loss) 
# and keeps track of the portfolio balance (asset position and cash balance)
# In complicated model, the portfolio class has more interaction with market_data and strategy class
# Test scripts below may or may not yield the expected result in the excel file 'short_example.xlsx'
class portfolio:
	def __init__(self):
		self.initial_cash = initial_cash
		self.index = df.index
		self.lot_size_long = lot_size_long
		self.lot_size_short = lot_size_short
		self.contract_size = contract_size

	def cash_delta_short(self):
#the positive cashflow when selling stock (trade_signal == -1); 	
		self.cash_delta_short = (-1)*trade_signal().trade_signal*strategy().open*self.lot_size_short*self.contract_size
		return self.cash_delta_short

	def cash_delta_long(self):
#the negative cashflow when buying stock (trade_signal == 1)		
		self.long = (-1)*trade_signal().trade_signal*strategy().open*self.lot_size_long*self.contract_size
		return self.long




'''test code to calculate the open_bal, end_bal, cash_delta, open_pos, pos_delta, and end_pos'''
	# def get_prev_end_bal(self,open_bal):
	
'''create an instance of portfolio'''
initial_cash = 10000
lot_size_short = 1
lot_size_long = 1
contract_size = 100

s = strategy('mav')
p = portfolio()

'''#display the result of code  '''

df['test_open_bal'] = 1
df['test_cash_delta'] = 1
df['test_end_bal'] = 1
df['test_open_pos'] = 1
df['test_pos_delta'] = 1
df['test_end_bal'] = 1

print(df)




