from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from database import Database
from csv import writer


db = Database('rest.db')


class App():
    def __init__(self, window):
        self.window = window
        window.title(' Restaurant Management System')
        window.geometry('500x300+500+150')
        window.resizable(0, 0)
        window.iconbitmap('logo/icon.ico')
        self.main_window_layout()
        self.order_total = 0
        window.mainloop()

    def main_window_layout(self):
        self.rest_label = Label(
            self.window, text='Welcome to the restaurant...', font=('verdana', 20, 'italic'), pady=40, padx=50)
        self.rest_label.grid(row=0, column=0)

        self.menu_btn = Button(
            self.window, text='Update Menu', font=('verdana', 15), padx=20, bd=7, command=self.menu_window)
        self.menu_btn.grid(row=1, column=0)

        self.order_btn = Button(
            self.window, text='Place Order', font=('verdana', 15), padx=28, bd=7, command=self.order_window)
        self.order_btn.grid(row=2, column=0)

        self.quit_btn = Button(self.window, text='Quit',
                               font=('verdana', 15), padx=65, bd=7, command=self.window.destroy)
        self.quit_btn.grid(row=3, column=0)

# -----------------------Menu window start-------------------------
    def menu_window(self):
        self.menu = Toplevel()
        self.menu.title(' Menu')
        self.menu.geometry('750x380+400+150')
        self.menu.resizable(0, 0)
        self.menu.iconbitmap('logo/icon.ico')

        self.menu_window_layout()

    def menu_window_layout(self):
        self.dish_label = Label(self.menu, text='Dish Name',
                                font=('verdana', 12, 'bold'), pady=30)
        self.dish_label.grid(row=0, column=0, sticky=E)

        self.dish_name = StringVar()
        self.dish_entry = Entry(self.menu, font=(
            'verdana', 12), bd=4, textvariable=self.dish_name)
        self.dish_entry.grid(row=0, column=1)

        self.price_label = Label(self.menu, text='Price ',
                                 font=('verdana', 12, 'bold'))
        self.price_label.grid(row=0, column=2, sticky=E)

        self.dish_price = StringVar()
        self.price_entry = Entry(self.menu, font=(
            'verdana', 12), bd=4, textvariable=self.dish_price)
        self.price_entry.grid(row=0, column=3)

        self.add_dish_btn = Button(
            self.menu, text='Add Dish', font=('verdana', 12), bd=5, command=self.add_dish)
        self.add_dish_btn.grid(row=1, column=0)

        self.remove_dish_btn = Button(
            self.menu, text='Remove Dish', font=('verdana', 12), bd=5, command=self.remove_dish)
        self.remove_dish_btn.grid(row=1, column=1)
        self.remove_dish_label = Label(self.menu, text='select dish from menu')
        self.remove_dish_label.grid(row=2, column=1)

        self.update_dish_btn = Button(
            self.menu, text='Update Dish', font=('verdana', 12), bd=5, command=self.update_dish)
        self.update_dish_btn.grid(row=1, column=2)
        self.update_dish_label = Label(self.menu, text='select dish from menu')
        self.update_dish_label.grid(row=2, column=2)

        self.clear_btn = Button(
            self.menu, text='Clear Text', font=('verdana', 12), bd=5, command=self.clear_text)
        self.clear_btn.grid(row=1, column=3)

        self.menu_label = Label(self.menu, text='Menu:',
                                font=('verdana', 12, 'italic'), padx=20)
        self.menu_label.grid(row=3, column=0, sticky=W)

        self.back_btn = Button(self.menu, text='Back', font=(
            'verdana', 12), padx=10, bd=5, command=self.menu.destroy)
        self.back_btn.grid(row=5, column=3)

        self.scrollbar = Scrollbar(self.menu)
        self.scrollbar.grid(row=5, column=2, sticky='NSW')

        self.dish_list = Listbox(self.menu, height=10,
                                 width=35, bd=5, font=('verdana', 12), yscrollcommand=self.scrollbar.set)
        self.dish_list.grid(row=4, column=0, columnspan=2,
                            rowspan=6, padx=20)

        self.scrollbar.configure(command=self.dish_list.yview)

        self.dish_list.bind('<<ListboxSelect>>', self.select)
        self.fill_menu()

    def select(self, event):
        index = self.dish_list.curselection()
        try:
            self.selected_item = self.dish_list.get(index).split(',       ')
            self.dish_name.set(self.selected_item[0])
            self.dish_price.set(self.selected_item[1])
        except:
            pass

    def fill_menu(self):
        self.dish_list.delete(0, END)
        rows = db.fetch()
        for row in rows:
            self.dish_list.insert(0, f'{row[0]},       {row[1]}')

    def add_dish(self):
        new_dish = self.dish_entry.get().strip()
        price = self.price_entry.get().strip()
        if new_dish == '' or price == '':
            self.menu.destroy()  # To destroy the previous toplevel window
            messagebox.showerror(
                'Empty fields', 'Please fill in all the fields')
            self.menu_window()  # Display a new toplevel window
        else:
            dishes = self.dish_list.get(0, END)
            for dish in dishes:
                if new_dish.lower() == dish.split(',')[0]:
                    self.menu.destroy()
                    messagebox.showinfo(
                        'Duplicate dish', 'Dish already in menu')
                    self.menu_window()
                    break
            else:
                db.insert(new_dish.lower(), price)
                self.clear_text()
                self.fill_menu()

    def remove_dish(self):
        try:
            db.remove(self.selected_item[0])
            self.clear_text()
            self.fill_menu()
        except:
            pass

    def update_dish(self):
        try:
            db.update(self.selected_item[0],
                      self.dish_entry.get().strip(), self.price_entry.get().strip())
            self.clear_text()
            self.fill_menu()
        except:
            pass

    def clear_text(self):
        self.dish_name.set('')
        self.dish_price.set('')
# -----------------------Menu window end---------------------------

# -----------------------Order window start------------------------
    def order_window(self):
        self.order = Toplevel()
        self.order.title(' Place Order')
        self.order.geometry('630x330+400+150')
        self.order.resizable(0, 0)
        self.order.iconbitmap('logo/icon.ico')

        self.order_window_layout()
        db.create_bill()

    def order_window_layout(self):
        self.search = StringVar()
        self.search_entry = Entry(self.order, font=(
            'verdana', 12), width=27, bd=4, textvariable=self.search)
        self.search_entry.grid(row=0, column=1, pady=15)

        self.search_btn = Button(
            self.order, text='Search', font=('verdana', 10), bd=4, command=self.search_dish)
        self.search_btn.grid(row=0, column=2)

        self.search_price = StringVar()
        self.display_price = Label(
            self.order, font=('verdana', 12), textvariable=self.search_price)
        self.display_price.grid(row=1, column=1)

        self.clear_btn = Button(
            self.order, text='Clear', font=('verdana', 10), bd=4, command=self.clear_entry)
        self.clear_btn.grid(row=1, column=2)

        self.menu_label = Label(self.order, text='Menu:',
                                font=('verdana', 12, 'italic'), padx=20)
        self.menu_label.grid(row=2, column=0, sticky=W)

        self.add_to_bag_btn = Button(self.order, text='Add to bag', font=(
            'verdana', 12), padx=10, bd=5, command=self.add_to_bag)
        self.add_to_bag_btn.grid(row=4, column=3)

        self.total_price = StringVar()
        self.display_total = Label(
            self.order, font=('verdana', 12), pady=10, textvariable=self.total_price)
        self.display_total.grid(row=5, column=3)

        self.bill_btn = Button(self.order, text='To bill', font=(
            'verdana', 12), padx=10, bd=5, command=self.bill_window)
        self.bill_btn.grid(row=6, column=3)

        self.reset_btn = Button(self.order, text='Reset', font=(
            'verdana', 12), padx=10, bd=5, command=self.reset)
        self.reset_btn.grid(row=7, column=3)

        self.back_btn = Button(self.order, text='Back', font=(
            'verdana', 12), padx=10, bd=5)
        self.back_btn.grid(row=8, column=3)

        self.back_btn.bind('<Button-1>', self.destroy_backbtn)

        self.scrollbar = Scrollbar(self.order)
        self.scrollbar.grid(row=5, column=2, sticky='NSW')

        self.dish_list = Listbox(self.order, height=10,
                                 width=35, bd=5, font=('verdana', 12), yscrollcommand=self.scrollbar.set)
        self.dish_list.grid(row=3, column=0, columnspan=2,
                            rowspan=6, padx=20)

        self.scrollbar.configure(command=self.dish_list.yview)
        self.dish_list.bind('<<ListboxSelect>>', self.select2)

        self.fill_menu()

    def destroy_backbtn(self, event):
        self.order_total = 0
        db.drop_bill()
        self.order.destroy()

    def clear_entry(self):
        self.search.set('')
        self.search_price.set('')

    def select2(self, event):
        index = self.dish_list.curselection()
        try:
            self.selected_item = self.dish_list.get(index).split(',       ')
            self.search.set(self.selected_item[0])
            self.search_price.set(f'Price: {self.selected_item[1]}')
        except:
            pass

    def search_dish(self):
        dishes = self.dish_list.get(0, END)
        for dish in dishes:
            if self.search_entry.get().strip().lower() == dish.split(',')[0]:
                self.search_price.set(f"Price: {dish.split(',')[1].strip()}")
                break
            else:
                self.search_price.set('Dish not found')

    def add_to_bag(self):
        try:
            self.calculate_total()
            name = self.search_entry.get()
            price = self.search_price.get().split(': ')[1]
            db.insert_bill(name, price)
        except:
            pass

    def calculate_total(self):
        price_str = self.search_price.get().split(': ')
        self.order_total += float(price_str[1])
        self.total_price.set(f"Total: {'%.2f' % self.order_total}")

    def reset(self):
        db.drop_bill()
        db.create_bill()
        self.order_total = 0
        self.total_price.set('')
        self.clear_entry()
# -----------------------Order window end--------------------------

# -----------------------Bill window start-------------------------
    def bill_window(self):
        if self.order_total > 0:
            self.bill = Toplevel()
            self.bill.title(' Bill')
            self.bill.geometry('630x330+400+150')
            self.bill.resizable(0, 0)
            self.bill.iconbitmap('logo/icon.ico')
            self.bill_window_layout()
            self.fill_bill()
        else:
            self.order.destroy()
            messagebox.showerror(
                'Empty order', 'Please select atleast one dish')
            self.order_window()

    def bill_window_layout(self):
        self.main_bill = ttk.Treeview(
            self.bill, columns=(1, 2, 3), show='headings', height=7)
        self.main_bill.grid(row=0, column=0, padx=10, pady=20)
        self.main_bill.heading(1, text='#')
        self.main_bill.column(1, anchor=CENTER, width=40)
        self.main_bill.heading(2, text='Name')
        self.main_bill.column(2, anchor=CENTER)
        self.main_bill.heading(3, text='Price')
        self.main_bill.column(3, anchor=CENTER)

        self.main_bill.bind('<ButtonRelease-1>', self.select_bill)
        ttk.Style().configure('Treeview', font=('verdana', 10))

        self.remove = Button(self.bill, text='Remove Dish',
                             font=('verdana', 12), bd=5, command=self.remove_item)
        self.remove.grid(row=0, column=2)

        self.bill_total = StringVar()
        self.total_label = Label(
            self.bill, textvariable=self.bill_total, font=('verdana', 12), pady=20)
        self.total_label.grid(row=1, column=0)
        self.bill_total.set(f"Total: {'%.2f' % self.order_total}")

        self.print_bill_btn = Button(self.bill, text='Print bill',
                                     font=('verdana', 12), bd=5, padx=10, command=self.print_bill)
        self.print_bill_btn.grid(row=1, column=2)

        self.back_btn = Button(self.bill, text='Back',
                               font=('verdana', 12), padx=5, bd=5, command=self.bill.destroy)
        self.back_btn.grid(row=3, column=2)

    def fill_bill(self):
        self.main_bill.delete(*self.main_bill.get_children())
        rows = db.fetch_bill()
        for row in rows:
            self.main_bill.insert('', END, values=row)

    def select_bill(self, event):
        self.bill_item = self.main_bill.item(self.main_bill.selection())

    def remove_item(self):
        try:
            dish_id = self.bill_item['values'][0]
            dish_price = self.bill_item['values'][2]
            db.remove_bill(dish_id)
            self.order_total -= float(dish_price)
            self.total_price.set(f"Total: {'%.2f' % self.order_total}")
            self.bill_total.set(f"Total: {'%.2f' % self.order_total}")
            self.fill_bill()
        except:
            pass

    def print_bill(self):
        if self.order_total > 0:
            with open('bill.csv', 'w') as csv_file:
                csv_writer = writer(csv_file)
                csv_writer.writerow(['Bill: '])
                csv_writer.writerow(['Sr No.', 'Name', 'Price'])
                i = 1
                for row in db.fetch_bill():
                    csv_writer.writerow([i, row[1], row[2]])
                    i += 1
                csv_writer.writerow(['', '', 'Total: ', self.order_total])
            self.order.destroy()
            self.bill.destroy()
            messagebox.showinfo('Print', 'Printing bill.....')
            self.order_window()
        else:
            self.bill.destroy()
            self.order.destroy()
            messagebox.showerror('Empty bill', 'Cannot print an empty bill')
            self.order_window()
# -----------------------Bill window end---------------------------


root = Tk()
app = App(root)
