from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from stock import Stock
from cart import Cart
import json
import functions as lib
from main_window import Ui_MainWindow
from add_stock import Ui_Dialog as add_stock_ui
from quantity import Ui_Dialog as quantity_ui
from client_input_dlg import Ui_Dialog as client_input_ui

class ClientInput(QDialog,client_input_ui):
    def __init__(self,parent = None):
        super(ClientInput,self).__init__(parent)
        self.ui = client_input_ui()
        self.ui.setupUi(self)
class Quantity(QDialog,quantity_ui):
    def __init__(self,parent=None):
        super(Quantity,self).__init__(parent)
        self.ui = quantity_ui()
        self.ui.setupUi(self)
class AddStock(QDialog,add_stock_ui):
    def __init__(self,parent=None):
        super(AddStock,self).__init__(parent)
        self.ui = add_stock_ui()
        self.ui.setupUi(self)

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        # item = Stock("1","vodka",450,50)
        # item.to_dict()
        file = open("names.dat","r")
        name_list = json.loads(file.read())
        completer = QCompleter(name_list)
        #initializing the tables(stocks,cart)

        self.load_stocks()
        self.load_cart()
        self.search_input.setCompleter(completer)
        self.add_stock_btn.clicked.connect(lambda: self.show_add_stock())
        self.add_to_cart_btn.clicked.connect(lambda: self.add_quantity(self.available_table))
        self.sell_btn.clicked.connect(lambda: self.sell_cart())
    def add_stock(self,ui):
        stock = {
            'id' : int(lib.assign_valid_id(int(ui.id_input.text()))),
            'name': ui.name_input.text(),
            'price': float(ui.price_input.text()),
            'quantity': int(ui.quantity_input.text())
        }
        lib.add_stock(stock)
        

    def show_add_stock(self):
        add_stock_dlg = AddStock(self)
        add_stock_dlg.ui.buttonBox.accepted.connect(
            lambda: self.add_stock(add_stock_dlg.ui)
        )
        add_stock_dlg.exec()
        self.load_stocks()
    def load_stocks(self):
        stocks = lib.load_stock()
        self.available_table.setRowCount(len(stocks))
        for index,stock in enumerate(stocks):
            stock = stock.to_dict()
            for column_index,attr in enumerate(stock):
                self.available_table.setItem(index,column_index,QTableWidgetItem(str(stock[str(attr)])))
                # table.item(index,column_index).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def add_quantity(self,table):
        selected_row = table.currentRow()
        if selected_row != -1:
            stock_id = int(table.item(selected_row,0).text())
            add_quantity_dlg = Quantity(self)
            add_quantity_dlg.ui.buttonBox.accepted.connect(lambda:self.add_to_cart(stock_id,int(add_quantity_dlg.ui.spinBox.text())))
            add_quantity_dlg.exec()

    def add_to_cart(self,stock_id,quantity):
        stock = lib.find_stock(stock_id)
        total = stock.price * quantity
        cart_stock = Cart(int(stock.Id),str(stock.name),int(quantity),int(stock.price),total)
        lib.save_cart(cart_stock)
        self.load_cart()
    def load_cart(self):
        cart = lib.load_cart()
        self.cart_table.setRowCount(len(cart))
        for index,stock in enumerate(cart):
            stock = Cart.to_dict(stock)
            for column_index,attr in enumerate(stock):
                self.cart_table.setItem(index,column_index,QTableWidgetItem(str(stock[str(attr)])))

    def sell_cart(self):
        
        lib.clear_cart()
        self.load_cart()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
