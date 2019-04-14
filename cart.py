from item import Item
from promo import promo2x1, promo3for19


# Cart:
# This class will handle the logic of the amount of items that the client has requested,
# and the promotions that should be applied if any.
# Since promotions are applied on this step, the invoicing and billing is taken care of in here

class Cart:
    # The Cart is initialized empty, and thus the total bill is initially zero.
    def __init__(self):
        print('[Server]\tStarted new empty cart')
        self.items_in_cart = {}
        self.bill: float = 0

    # Initial logic to decide if the request requires cart addition, or it is an invoice what should be processed
    def process_request(self, i, verbose):
        if i in ('1', '2', '3', '8', '9'):
            return {"response": self.add_to_cart(i),
                    "current_cart": self.current_shopping_cart()}

        else:
            return {"response": self.generate_invoice(verbose),
                    "current_cart": self.current_shopping_cart()}

    # The logic of adding items to the cart is mapped in relation to the menu the Client encounters.
    # For each request, if the specific Item object is not present in the items_in_cart dict, we create the item
    # Then, in any case, we add the number of items requested.
    # At the end, we recalculate the bill of the whole cart and return the notification of the successful addition
    def add_to_cart(self, i):
        item_code = ""
        if i == '1':
            item_code = "VOUCHER"
            if item_code not in self.items_in_cart:
                self.items_in_cart[item_code] = Item("Vouchers", 5, promo2x1)
            self.items_in_cart[item_code].add(1)
        elif i == '2':
            item_code = "SHIRT"
            if item_code not in self.items_in_cart:
                self.items_in_cart[item_code] = Item("T-Shirts", 20, promo3for19)
            self.items_in_cart[item_code].add(1)
        elif i == '3':
            item_code = "MUG"
            if item_code not in self.items_in_cart:
                self.items_in_cart[item_code] = Item("Mugs    ", 7.5)
            self.items_in_cart[item_code].add(1)

        elif i == '8':
            item_code = "VOUCHER"
            if item_code not in self.items_in_cart:
                self.items_in_cart[item_code] = Item("Vouchers ", 5, promo2x1)
            self.items_in_cart[item_code].add(2)
        elif i == '9':
            item_code = "SHIRT"
            if item_code not in self.items_in_cart:
                self.items_in_cart[item_code] = Item("T-Shirts", 20, promo3for19)
            self.items_in_cart[item_code].add(3)

        self.recalculate_bill()
        return f"Succesfully added {item_code} to the Cart"

    # Method that pretty-prints a quick summary that is displayed on every menu print on client-side.
    def current_shopping_cart(self):
        current_cart = ''
        for i in self.items_in_cart:
            current_cart += f"{self.items_in_cart[i].name.strip()} x{self.items_in_cart[i].number_in_cart}, "
        current_cart = current_cart[:-2]
        return f"{current_cart} | {self.bill:.2f}€"

    # Method that loops through every Item in the cart, and adds up the cost of them.
    def recalculate_bill(self):
        self.bill = 0
        for i in self.items_in_cart:
            self.bill += self.items_in_cart[i].cost_of_all_items
        print(f"\tCurrent bill: {self.bill:.2f}")

    # Method that pretty-prints an invoice with the purchase lines, promos applied and total price
    def generate_invoice(self, verbose):
        invoice = '\n---------------------------------------\n'
        invoice += 'Item Code\t\tQty\tTotal\n'
        if verbose:
            for n, i in enumerate(self.items_in_cart, start=1):
                invoice += self.items_in_cart[i].provide_bill_lines(verbose)
                invoice += '  - - - - - - - - - - - - - - - - - - -\n'
        invoice += f'TOTAL\t\t\t\t{self.bill:.2f}€\n'
        invoice += '---------------------------------------\n'
        return invoice


