#!/usr/bin/env python3

import csv
import glob
import os
import datetime

search_dir = '/Users/WONDER/Desktop/Accounts/'

def remove_last_total(filename):
	lines = []
	with open(filename, newline='') as read_file:
		csv_reader = csv.reader(read_file, delimiter=',')
		for line in csv_reader:
			lines.append(line)
		if (len(lines)>2):
			lines = lines[:-1]

	with open(filename, 'w') as write_file:
		csv_writer = csv.writer(write_file)
		for line in lines:
			csv_writer.writerow(line)


def add_total(filename):
	totalDebit = 0
	totalCredit = 0

	with open(filename, newline='') as read_obj:
		reader = csv.DictReader(read_obj)
		for row in reader:
			try:
				totalDebit = totalDebit + float(row['Debit'])
			except:
				totalDebit = totalDebit
			try:
				totalCredit = totalCredit + float(row['Credit'])
			except:
				totalCredit = totalCredit 

	with open(filename, 'a+', newline='') as write_obj:
		csv_writer = csv.writer(write_obj)
		csv_writer.writerow(['','Grand Total','','','',totalDebit,totalCredit,str(totalCredit-totalDebit)])


def choose_customer():
	print('Choose the customer:')
	options = {}
	files = list(filter(os.path.isfile, glob.glob(search_dir + '*.csv')))
	files.sort(key=lambda x: os.path.getctime(x))
	for (key,value) in enumerate(files,start=100):
		options[str(key)] = value
		print(str(key) + ' - ' + value.replace('.csv','').replace(search_dir,''))
	rkey = input('Enter the customer number:')
	return options[rkey]


def debit_credit_entry():
	choice = input('credit/debit:')
	date = input('Enter Date of Transaction (DD-MM-YYYY):')
	customer = choose_customer()
	amount = input('Enter the Amount:')
	details = input('Enter the Details of Transaction:')

	if(choice == 'credit'):
		remove_last_total(customer)
		with open(customer, 'a+', newline='') as write_obj:
			csv_writer = csv.writer(write_obj)
			csv_writer.writerow([])
			csv_writer.writerow([date,details,'','',amount,'0',amount,''])
		add_total(customer)

	if(choice == 'debit'):
		remove_last_total(customer)
		with open(customer, 'a+', newline='') as write_obj:
			csv_writer = csv.writer(write_obj)
			csv_writer.writerow([date,details,'','',amount,amount,'0',''])
		add_total(customer)

	if(choice != 'credit' and choice != 'debit'):
		print('Invalid Input.')

	return choice


def sales_purchase_entry():
	choice = input('sale/purchase:')
	date = input('Enter Date of '+ choice + ' (DD-MM-YYYY):')
	customer = choose_customer()
	vehicle = input('Enter the vehicle number for the '+ choice + ':')
	nTypes = input('Number of types in the '+ choice + ':')
	materials = {}
	totalPrice = 0
	for i in range(1,int(nTypes)+1):
		tName = input('Name of Type-' + str(i) + ':')
		tQuantity = input('Quantity of Type-' + str(i) + ':')
		tRate = input('Rate of Type-' + str(i) + ':')
		tPrice = float(tRate) * float(tQuantity)
		materials[i] = (tName, tRate, tQuantity, round(tPrice,2))
		totalPrice = totalPrice + tPrice
	gst = input('Enter GST:')

	if(choice == 'sale'): 
		loading = input('Enter loading amount:')
		commission = input('Enter commission amount:')
		totalBill = totalPrice + float(gst) + float(loading) + float(commission)
		remove_last_total(customer)
		with open(customer, 'a+', newline='') as write_obj:
			csv_writer = csv.writer(write_obj)
			csv_writer.writerow([])
			csv_writer.writerow([date,vehicle,'','','','0',totalBill,''])
			for i in range(1,int(nTypes)+1):
				csv_writer.writerow(['',materials[i][0],materials[i][2],materials[i][1],materials[i][3],'','',''])
			csv_writer.writerow(['','GST','','',gst,'','',''])
			csv_writer.writerow(['','Loading','','',loading,'','',''])
			csv_writer.writerow(['','Commission','','',commission,'','',''])
			csv_writer.writerow([])

		add_total(customer)

	if(choice == 'purchase'):
		totalBill = totalPrice + float(gst)
		remove_last_total(customer)
		with open(customer, 'a+', newline='') as write_obj:
			csv_writer = csv.writer(write_obj)
			csv_writer.writerow([])
			csv_writer.writerow([date,vehicle,'','','',totalBill,'0',''])
			for i in range(1,int(nTypes)+1):
				csv_writer.writerow(['',materials[i][0],materials[i][2],materials[i][1],materials[i][3],'','',''])
			csv_writer.writerow(['','GST','','',gst,'','',''])

		add_total(customer)

	if(choice != 'sale' and choice != 'purchase'):
		print('Invalid Input.')

	return choice


def create_template():
	# name = input('Enter the Full Name:')
	print('Enter the Nick Name of the new customer')
	nick = input('[Try to avoid names with spaces and special characters]:')
	filename = nick + '.csv'
	if (os.path.isfile('./'+filename)):
		print('Customer already exists with this nick name.')
		decision = input('you want me to delete the previous record and create new one? (yes/no)')
		if (decision == 'yes'):
			with open(filename, 'w', newline='') as file:
				writer = csv.writer(file)
				writer.writerow(['Date', 'Particulars', 'Quantity', 'Rate', 'Amount', 'Debit', 'Credit', 'Balance'])
			return (nick, 'ok') 
		else:
			return (nick, 'nope')
	else:
		with open(filename, 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(['Date', 'Particulars', 'Quantity', 'Rate', 'Amount', 'Debit', 'Credit', 'Balance'])
	return (nick,'ok')


def get_balance(filename):
	with open(filename,'r') as F0:
		Reader = csv.reader(F0,delimiter=',')
		Rows = list(Reader)
		Tot_rows = len(Rows)
	counter = 0
	balance = 0.0
	with open(filename,'r') as F1:
		Read = csv.reader(F1,delimiter=',')
		for i in Read:
			if counter == Tot_rows-1:
				try:
					balance = float(i[6])-float(i[5])
				except ValueError:
					balance = 'NA'
			counter+=1
	return balance


def get_all_balances():
	files = list(filter(os.path.isfile, glob.glob(search_dir + '*.csv')))
	files.sort(key=lambda x: os.path.getctime(x))
	debit_balances = {}
	credit_balances = {}
	for customer in files:
		bal = get_balance(customer)
		if bal >= 0:
			credit_balances[customer] = bal
		else: 
			debit_balances[customer] = bal

	with open("DebitBalances.csv", 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(['Name', 'Balance'])
			for key,val in debit_balances.items():
				writer.writerow([key.replace('.csv','').replace(search_dir,''),val])

	with open("CreditBalances.csv", 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['Name', 'Balance'])
		for key,val in credit_balances.items():
			writer.writerow([key.replace('.csv','').replace(search_dir,''),val])
		

if __name__ == '__main__':

	# add users logic and log their access.

	print('\nWelcome to ledger bot (Beta)! :) \nI am qwerty, your virtual assistant, I help you keep track of your sales/purchase, debit/credit History. \n')

	currentTime = datetime.datetime.now()
	if currentTime.hour < 12:
		print('Good Morning!')
	elif 12 <= currentTime.hour < 16:
		print('Good Afternoon!')
	else:
		print('Good Evening!')

	print('what can help you with ?')
	print('1. Add a debit/credit transaction')
	print('2. Add a sale/purchase entry')
	print('3. Add a new customer')
	# print('4. Get all outstanding balances')

	choice = input('\nEnter Option number:')

	if(choice == '1'):
		mode = debit_credit_entry()
		if(mode == 'credit' or mode == 'debit'):
			get_all_balances()
			print(mode.upper() + ' Transaction added to corresponding customer.')

	if(choice == '2'):
		mode = sales_purchase_entry()
		if(mode == 'sale' or mode == 'purchase'):
			get_all_balances()
			print(mode.upper() + ' entry added to corresponding customer.')

	if(choice == '3'):
		(name,status) = create_template()
		if (status == 'ok'):
			print('Customer with nick name ' + name + ' added to your file repository.')
		else:
			print('Customer ' + name + ' not added.')

	# if(choice == '4'):
	# 	get_all_balances()

	if(choice > '3' or choice < '1'):
		print('Invalid Input.')

	print('\nHave a nice day!')
