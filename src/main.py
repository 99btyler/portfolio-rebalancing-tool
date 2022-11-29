import sys


class Stock():

	def __init__(self):

		self.name = input("Stock name: ")

		self.amount = 0.0
		while True:
			try:
				self.amount = float(input("Stock amount: "))
				break
			except ValueError:
				continue # asks again

		self.desired_weight = 0.0
		while True:
			try:
				self.desired_weight = float(input("Stock desired_weight: "))
				break
			except ValueError:
				continue # asks again


if __name__ == "__main__":

	# Get number of stocks
	number_of_stocks = 0
	while True:
		try:
			number_of_stocks = int(input("number_of_stocks: "))
			break
		except ValueError:
			continue # asks again

	# Get data for each stock
	stocks = []
	for i in range(number_of_stocks):
		stocks.append(Stock())

	total_amount = 0.0
	total_desired_weight = 0.0
	for stock in stocks:
		total_amount += stock.amount
		total_desired_weight += stock.desired_weight

	if total_desired_weight != 100.0:
		print("ERROR: total_desired_weight doesn't add up to 100%")
		sys.exit(1)

	# Get amount to invest
	amount_to_invest = 0
	while True:
		try:
			amount_to_invest = float(input("amount_to_invest: "))
			break
		except ValueError:
			continue # asks again

	# Calculate
	new_total_amount = total_amount + amount_to_invest
	for stock in stocks:
		needed_value = (stock.desired_weight / 100.0) * new_total_amount
		difference = needed_value - stock.amount
		print(f"{stock.name}: {stock.amount}->{round(needed_value, 2)}({round(difference, 2)})")

