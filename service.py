from tkinter import *

class Application(Frame):

    def populateOrders(self):
        self.orders[1919] = {
            "id": 1919,
            "food": [("pizza", 1), ("hotdog", 2)],
            "name": "Charles",
            "phone": "1111111111",
            "stage": 2
        }
        self.orders[2234] = {
            "id": 2234,
            "food": [("sandwich", 2), ("burger", 2)],
            "name": "Chucky",
            "phone": "1111111111",
            "stage": 3
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

    def orderToString(self, order):
        lst = []
        lst.append(("ID: " + str(order["id"])))
        lst.append(("Customer: " + order["name"]))
        lst.append(("Phone: " + order["phone"]))
        lst.append(("Stage: " + self.stages[order["stage"]]))

        return "\n".join(lst)

    def onselect(self, e):
        w = e.widget
        i = int(w.curselection()[0])
        order = self.orders[w.get(i)]
        self.info.set(self.orderToString(order))

    def createInfoWidget(self):
        self.infoframe = Frame(self.main)
        self.infoframe.pack({"side": "left"})

        self.INFOLABEL = Label(self.main, width=30, bd=1, relief="solid", text="Order Detail", justify=LEFT)
        self.INFOLABEL.pack({"side": "top"})

        self.INFO = Label(self.main, textvariable=self.info, justify=LEFT)
        self.INFO.pack({"side": "top"})

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
        self.stages = ["idle", "prep", "cook", "assemble", "complete"]
        self.populateOrders()
        self.info = StringVar()
        self.info.set("Order Info Display")

        self.createWidgets()

        self.root.mainloop()


app = Application()
