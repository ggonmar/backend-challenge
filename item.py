

# Item:
# The definition of a certain item. Its price, its promotions (if any), and its quantity within the cart.
class Item:
    items_not_in_promo: int
    items_in_promo: int
    number_in_cart: int
    cost_of_all_items: int

    # Initialize the item with its name, its price, and its promotion if it has one
    def __init__(self, name: str, price: float, promo=None) -> None:
        self.price = price
        self.name = name
        self.number_in_cart = 0
        self.cost_of_all_items = 0
        self.promo = promo
        self.items_in_promo = 0
        self.items_not_in_promo = 0

    # Method that adds a certain number of this item
    def add(self, n) -> None:
        self.number_in_cart = self.number_in_cart + n
        self.recalculate()

    # Method that considers if a recalculation of the price is needed due to possible existing promotions
    # If not, we just obtain the product qty * price.
    # Otherwise, we apply some logic to obtain total price of all the acquired items.
    def recalculate(self) -> None:
        if self.promo is None:
            self.cost_of_all_items = self.number_in_cart * self.price
            self.items_not_in_promo = self.number_in_cart
        else:
            self.apply_valid_promotion()

    # If a Promo is in place, we need to assess
    #   - how many items the promo applies onto
    #      - what discount is applied to said items
    #   - how many items are left to have standard price applied
    #
    def apply_valid_promotion(self) -> None:
        self.cost_of_all_items = 0

        # Items in promo: natural division of the total included by the number needed to apply the promo.
        self.items_in_promo = int(self.number_in_cart / self.promo.promo_divider) * self.promo.promo_divider

        # Items not in promo: could apply Modulo function, but subtraction is more straightforward now
        self.items_not_in_promo = self.number_in_cart - self.items_in_promo

        print(f'\t{self.name} with promo applied: {self.items_in_promo:d}')
        print(f'\t{self.name} without promo applied: {self.items_not_in_promo:d}')

        # "Cost of all" (C) is "items without promotion" (Q1) x  "Price" (P),
        #                 plus "items with promotion" (Q2)   x  "Discounted Price" (DP)
        #   Taking into consideration that DP = P * (1 - dc) and Q = Q1 + Q2
        #    C = (Q1 * P) + (Q2 * P * dc)
        #    C = P * ( Q1 + Q2 * ( 1 - dc ))
        #    C = P * ( Q - Q2*dc )
        #    C = P * Q - Q2*P*dc
        self.cost_of_all_items = self.price * self.number_in_cart - \
                                 (self.price * self.promo.percentage_off_per_item * self.items_in_promo)

    # Method that fills the invoice lines for this item, making the differenciation between promo and standard
    def provide_bill_lines(self, verbose) -> str:
        s = ""
        s = f'{self.name}\t\t{self.number_in_cart}\t{self.cost_of_all_items:.2f}\n'
        if verbose:
            s += f'  Standard\t\t{self.items_not_in_promo}\t{self.items_not_in_promo*self.price:.2f}\n'
            if self.items_in_promo != 0:
                s += f'  {self.promo.promo_name}\t\t{self.items_in_promo}\t' \
                     f'{self.items_in_promo*self.price*(1-self.promo.percentage_off_per_item):.2f}\n'
        return s
