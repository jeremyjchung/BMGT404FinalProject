from tkinter import *
from tkinter import messagebox
from tkinter import font
from helper import *
from notifications import *
import pandas as pd

class Application(Frame):  
    def decrementTimers(self):
        for x in self.orders:
            order = self.orders[x]
            if order["timer"] > 0:
                order["timer"] -= 1

        selectedOrder = self.selectedOrder
        if selectedOrder != None:
            self.info["timer"].set("ETA: " + secondsToTime(selectedOrder["timer"]))

        self.root.after(1000, self.decrementTimers)

    def populateOrders(self):
        data = pd.read_csv("CarryOutOrders.csv", skiprows=[1])
        menu = ['Calzone','Salad','Tots','Stix','Wings','Dessert','Drink']
        for index,row in data.iterrows():
            order_id = int(str(id(row))[8:])
            numItems = 0
            food = []
            for item in menu:
                if isinstance(row[item], int):
                    numItems += row[item]
                    food.append((item, row[item]))
            self.orders[order_id] = {
                "id": order_id,
                "food": food,
                "name": row['Name'],
                "phone": row['Number'],
                "stage": 0,
                "timer": 350,
                "eta": 350
            }

        self.orders[1919] = {
            "id": 1919,
            "food": [("pizza", 1), ("hotdog", 2)],
            "name": "Charles",
            "phone": "111-111-1111",
            "stage": 0,
            "timer": 350,
            "eta": 350
        }

    def createListboxWidget(self):
        self.listboxframe = Frame(self.main)
        self.listboxframe.pack({"side": "left"})

        self.LISTBOXLABEL = Label(self.listboxframe, width=10, bd=1, relief="solid", justify=LEFT, text="Orders")
        self.LISTBOXLABEL.pack({"side": "top"})

        self.LISTBOX = Listbox(self.listboxframe, selectmode=SINGLE, width=10)
        self.LISTBOX.bind('<<ListboxSelect>>', self.onselect)
        self.LISTBOX.pack({"side": "top"})
        for i in self.orders:
            self.LISTBOX.insert(END, i)

    def onselect(self, e):
        w = e.widget
        i = int(w.curselection()[0])
        order = self.orders[w.get(i)]
        self.selectedOrder = order

        self.info["id"].set("ID: " + str(order["id"]))
        self.info["name"].set("Customer: " + order["name"])
        self.info["phone"].set("Phone: " + order["phone"])
        self.info["stage"].set("Stage: " + self.stages[order["stage"]])
        self.info["food"].set("Food: \n" + foodToStr(order["food"]))
        print(foodToStr(order["food"]))
        self.info["timer"].set("ETA: " + secondsToTime(order["timer"]))

        for i in range(0, order["stage"]):
            self.info["progress"][i].set(1)
        for i in range(order["stage"], len(self.stages)-1):
            self.info["progress"][i].set(0)

    def createInfoWidget(self):
        self.customFont = font.Font(family="Consolas", size=10)

        self.infoframe = Frame(self.main)
        self.infoframe.pack({"side": "left", "anchor": "n"})

        self.INFOLABEL = Label(self.infoframe, width=30, bd=1, relief="solid", text="Order Detail", justify=LEFT)
        self.INFOLABEL.pack({"side": "top"})

        self.ID = Label(self.infoframe, textvariable=self.info["id"])
        self.ID.pack({"side": "top", "anchor": "w"})
        self.CUSTOMER = Label(self.infoframe, textvariable=self.info["name"], justify=LEFT)
        self.CUSTOMER.pack({"side": "top", "anchor": "w"})
        self.PHONE = Label(self.infoframe, textvariable=self.info["phone"], justify=LEFT)
        self.PHONE.pack({"side": "top", "anchor": "w"})
        self.STAGE = Label(self.infoframe, textvariable=self.info["stage"], justify=LEFT)
        self.STAGE.pack({"side": "top", "anchor": "w"})
        self.FOOD = Label(self.infoframe, textvariable=self.info["food"], justify=LEFT, font=self.customFont)
        self.FOOD.pack({"side": "top", "anchor": "w"})
        self.TIMER = Label(self.infoframe, textvariable=self.info["timer"], justify=LEFT)
        self.TIMER.pack({"side": "top", "anchor": "w"})

    def createCheckboxWidget(self):
        self.checkboxframe = Frame(self.main)
        self.checkboxframe.pack({"side": "top", "anchor": "n"})

        self.CHECKBOXLABEL = Label(self.checkboxframe, width=30, bd=1, relief="solid", justify=LEFT, text="Order Progress")
        self.CHECKBOXLABEL.pack({"side": "top"})

        self.PREP = Checkbutton(self.checkboxframe, text="Prep", variable=self.info["progress"][0], command=self.checkboxListener)
        self.PREP.pack({"side": "top", "anchor": "w"})
        self.COOK = Checkbutton(self.checkboxframe, text="Cook", variable=self.info["progress"][1], command=self.checkboxListener)
        self.COOK.pack({"side": "top", "anchor": "w"})
        self.ASSEMBLE = Checkbutton(self.checkboxframe, text="Assemble", variable=self.info["progress"][2], command=self.checkboxListener)
        self.ASSEMBLE.pack({"side": "top", "anchor": "w"})

        self.buttonframe = Frame(self.main)
        self.buttonframe.pack({"side": "bottom", "anchor": "w"})

        self.TEXT = Button(self.buttonframe, text="Send Text", command=self.sendText)
        self.TEXT.pack({"side": "left", "anchor": "w"})

    def sendText(self):
        if self.selectedOrder == None:
            return

        p = "+1" + self.selectedOrder["phone"].replace("-", "")
        try:
            if self.selectedOrder["stage"] == 3:
                self.n.send_msg(p, "Your order is ready for pickup!")
            else:
                self.n.send_msg(p, "Your order is in the " + self.stages[self.selectedOrder["stage"]] + " phase. ETA " + secondsToTime(self.selectedOrder["timer"]))

            messagebox.showinfo("Success", "Text has been sent to " + self.selectedOrder["phone"])
        except:
            messagebox.showerror("Error", "Text failed to reach " + self.selectedOrder["phone"])

    def checkboxListener(self):
        if self.selectedOrder != None:
            self.selectedOrder["stage"] = 0
            for x in range(0, len(self.info["progress"])):
                if self.info["progress"][x].get() == 1:
                    self.selectedOrder["stage"] = x + 1

            for x in range(0, self.selectedOrder["stage"]):
                self.info["progress"][x].set(1)

            self.info["stage"].set("Stage: " + self.stages[self.selectedOrder["stage"]])
            # prep = 30%, cook = 60%, assemble = 10%
            if self.selectedOrder["stage"] == 0:
                self.selectedOrder["timer"] = self.selectedOrder["eta"]
            elif self.selectedOrder["stage"] == 1:
                self.selectedOrder["timer"] = int(0.7*self.selectedOrder["eta"])
            elif self.selectedOrder["stage"] == 2:
                self.selectedOrder["timer"] = int(0.1*self.selectedOrder["eta"])
            else:
                self.selectedOrder["timer"] = 0

    def createWidgets(self):
        self.main = Frame(self.root, bd=1, relief="solid")
        self.main.pack({"side": "top"})
        self.bottom = Frame(self.root)
        self.bottom.pack({"side": "top"})

        self.createListboxWidget()
        self.createInfoWidget()
        self.createCheckboxWidget()

        self.QUIT = Button(self.bottom)
        self.QUIT["text"] = "Quit"
        self.QUIT["command"] = self.root.quit
        self.QUIT.pack({"side": "top"})

    def __init__(self):
        self.root = Tk()
        self.root.title = "Order Magic"

        self.n = Notifications()
        self.orders = {}
        self.selectedOrder = None
        self.stages = ["prep", "cook", "assemble", "complete"]
        self.info = {"id": StringVar(), "name": StringVar(), "phone": StringVar(), "stage": StringVar(), "timer": StringVar(), "food": StringVar(), "progress": [IntVar(), IntVar(), IntVar()]}

        self.populateOrders()
        self.createWidgets()
        self.decrementTimers()

        self.root.mainloop()


app = Application()
