from tkinter import *
from aux import *

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
        self.orders[1919] = {
            "id": 1919,
            "food": [("pizza", 1), ("hotdog", 2)],
            "name": "Charles",
            "phone": "1111111111",
            "stage": 2,
            "timer": 350
        }
        self.orders[2234] = {
            "id": 2234,
            "food": [("sandwich", 2), ("burger", 2)],
            "name": "Chucky",
            "phone": "1111111111",
            "stage": 3,
            "timer": 300
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
        self.info["timer"].set("ETA: " + secondsToTime(order["timer"]))

    def createInfoWidget(self):
        self.infoframe = Frame(self.main)
        self.infoframe.pack({"side": "top"})

        self.INFOLABEL = Label(self.infoframe, width=30, bd=1, relief="solid", text="Order Detail", justify=LEFT)
        self.INFOLABEL.pack({"side": "top"})

        self.ID = Label(self.infoframe, textvariable=self.info["id"], justify=LEFT)
        self.ID.pack({"side": "top"})
        self.CUSTOMER = Label(self.infoframe, textvariable=self.info["name"], justify=LEFT)
        self.CUSTOMER.pack({"side": "top"})
        self.PHONE = Label(self.infoframe, textvariable=self.info["phone"], justify=LEFT)
        self.PHONE.pack({"side": "top"})
        self.STAGE = Label(self.infoframe, textvariable=self.info["stage"], justify=LEFT)
        self.STAGE.pack({"side": "top"})
        self.TIMER = Label(self.infoframe, textvariable=self.info["timer"], justify=LEFT)
        self.TIMER.pack({"side": "top"})

    def createWidgets(self):
        self.main = Frame(self.root, bd=1, relief="solid")
        self.main.pack({"side": "top"})
        self.bottom = Frame(self.root)
        self.bottom.pack({"side": "top"})

        self.createListboxWidget()
        self.createInfoWidget()

        self.QUIT = Button(self.bottom)
        self.QUIT["text"] = "Quit"
        self.QUIT["command"] = self.root.quit
        self.QUIT.pack({"side": "top"})

    def __init__(self):
        self.root = Tk()

        self.orders = {}
        self.selectedOrder = None
        self.stages = ["idle", "prep", "cook", "assemble", "complete"]
        self.info = {"id": StringVar(), "name": StringVar(), "phone": StringVar(), "stage": StringVar(), "timer": StringVar()}

        self.populateOrders()
        self.createWidgets()
        self.decrementTimers()

        self.root.mainloop()


app = Application()
