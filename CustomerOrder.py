# Carry Out Tracker Customer Side

# Takes customers order and adds it to a dictionary 

# The dictionary hold the user's name, telephone number, the items ordered, and the 
# the quantity of each item ordered

# From there the this dictionary entry is written to an excel file which is the database
# for all carry out orders that the restaurant still needs to complete

from tkinter import *
from PIL import Image, ImageTk
import csv
import os.path

root = Tk()

image = Image.open("OrderMagicLogo.png")
photo = ImageTk.PhotoImage(image)
logo = Label(image=photo)
logo.grid(row = 0, column = 0,columnspan=2, rowspan=2, sticky=W)

Label(root, text = "Customer Information",bg="red", font = "Helvetica 16 bold").grid(row = 2, column = 0, sticky = W)

Label(root, text="Name:", font = "Helvetica").grid(row=3,column = 0, sticky=W)
Label(root, text="Telephone Number:", font = "Helvetica").grid(row=4, column = 0, sticky=W)

name_entry = Entry(root)
phone_entry = Entry(root)
name_entry.grid(row=3, column=1, sticky=W)
phone_entry.grid(row=4, column=1, sticky=W)

Label(root, text = "Order Information",bg="red", font = "Helvetica 16 bold").grid(row = 6, column = 0, sticky = W)
Label(root, text="Calzone", font = "Helvetica").grid(row=8,column = 0, sticky=W)
Label(root, text="Salad", font = "Helvetica").grid(row=9, column = 0, sticky=W)
Label(root, text="Tater Tots", font = "Helvetica").grid(row=10,column = 0, sticky=W)
Label(root, text="Bread Stix", font = "Helvetica").grid(row=11, column = 0, sticky=W)
Label(root, text="Chicken Wings", font = "Helvetica").grid(row=12, column = 0, sticky=W)
Label(root, text="Dessert", font = "Helvetica").grid(row=13, column = 0, sticky=W)
Label(root, text="Fountain Drink", font = "Helvetica").grid(row=14, column = 0, sticky=W)

calzone_entry = Entry(root)
salad_entry = Entry(root)
tots_entry = Entry(root)
stix_entry = Entry(root)
wings_entry = Entry(root)
dessert_entry = Entry(root)
drink_entry = Entry(root)

calzone_entry.grid(row=8, column=1, sticky=W)
salad_entry.grid(row=9, column=1, sticky=W)
tots_entry.grid(row=10, column=1, sticky=W)
stix_entry.grid(row=11, column=1, sticky=W)
wings_entry.grid(row=12, column=1, sticky=W)
dessert_entry.grid(row=13, column=1, sticky=W)
drink_entry.grid(row=14, column=1, sticky=W)

def fetch():
	name = name_entry.get()
	number = phone_entry.get()
	calzone = calzone_entry.get()
	salad = salad_entry.get()
	tots = tots_entry.get()
	stix = stix_entry.get()
	wings = wings_entry.get()
	dessert = dessert_entry.get()
	drink = drink_entry.get()

	entries = [name, number, calzone, salad, tots, stix, wings, dessert, drink]
	print(entries)
	fields = ['Name','Number','Calzone','Salad','Tots','Stix','Wings','Dessert','Drink']
	order = {}
	
	cnt = 0
	for entry in entries:
		order[fields[cnt]] = entry
		cnt += 1
	csv_file = 'CarryOutOrders.csv'
	
	if os.path.exists(csv_file):
		with open(csv_file, 'r+') as csvfile:
			header = next(csv.reader(csvfile))
			writer = csv.DictWriter(csvfile, header, -999)
			writer.writerow(order)		
	else:
		try:
			with open(csv_file, 'w') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames=fields)
				writer.writeheader()
				writer.writerow(order)
		except IOError:
			print(IOError)    
                
	return order
	
def fetch_and_close():
	print(fetch())
	
	root.destroy()
	
	thanks = Tk()
	Label(thanks, text = "Thank you for placing your order with DP Dough! \n You will be receiving a text with the estimated wait time shortly!",bg="red", font = "Helvetica 16 bold").grid(row = 0, column = 0)
	thanks.mainloop()
	
	# Add intro text functionality
	
	
submit_button = Button(root, text='Place Order',command = fetch_and_close)
submit_button.grid(row=16, column = 1, sticky=W )

root.mainloop()