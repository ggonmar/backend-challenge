import unittest
from cart import Cart

# Defining some unit tests to validate my cart behavior.
class TestStringMethods(unittest.TestCase):

    # GIVEN a Cart has been set up
    # WHEN a request for adding item A to the cart is received
    # THEN said item A is included to the cart
    #   AND the price is updated accordingly
    #   AND no promotion is applied
    def check_item(self, i):

        # GIVEN
        cart = Cart()

        # WHEN
        cart.process_request(i['code'], True)

        # THEN
        self.assertIn(i['item'], cart.items_in_cart)
        self.assertEqual(cart.items_in_cart[i['item']].items_in_promo, i['in'])
        self.assertEqual(cart.items_in_cart[i['item']].items_not_in_promo, i['not'])
        self.assertEqual(cart.items_in_cart[i['item']].number_in_cart, i['total'])
        self.assertEqual(cart.items_in_cart[i['item']].cost_of_all_items, i['price'])
        self.assertEqual(cart.bill, i['price'])


    # Parametrization to execute the test with all the items
    def test_items_load(self):
        values=[ {'item': 'MUG', 'price': 7.5, 'code':'3', 'in':0, 'not':1, 'total':1},
                 {'item': 'VOUCHER', 'price': 5, 'code': '1', 'in': 0, 'not': 1, 'total': 1},
                 {'item': 'SHIRT', 'price': 20, 'code': '2', 'in': 0, 'not': 1, 'total': 1}
                ]

        for i in values:
            self.check_item(i)


    # GIVEN a Cart has been set up
    # WHEN several requests are received
    # THEN all corresponding items are included to the cart
    #   AND price is updated accordingly
    #   AND promotions are applied accordingly
    def check_complex(self, t):
        # GIVEN
        cart=Cart()

        # WHEN
        for i in t['input']:
            cart.process_request(i, True)

        print(cart.generate_invoice(True))
        # THEN
        self.assertEqual(cart.bill, t['expected'])


    # This test corresponds to the exact requests stated on the challenge
    # I'm treating all the examples as parametrized tests to be ran
    def test_complex_carts(self):
        values=[{"input": self.parse_request('VOUCHER, TSHIRT, MUG'), "expected":32.50},
                {"input": self.parse_request('VOUCHER, TSHIRT, VOUCHER'), "expected": 25},
                {"input": self.parse_request('TSHIRT, TSHIRT, TSHIRT, VOUCHER, TSHIRT'), "expected": 82},
                {"input": self.parse_request('VOUCHER, TSHIRT, VOUCHER, VOUCHER, MUG, TSHIRT, TSHIRT'), "expected": 74.5}
                ]
        for i in values:
            self.check_complex(i)

    # Tools to parse the input and adapt it to my cart setup
    def parse_request(self, s):
        return map(self.sort_requests, s.split(', '))

    def sort_requests(self, s):
            if s== 'VOUCHER':
                return '1'
            elif s== 'TSHIRT':
                return '2'
            elif s== 'MUG':
                return '3'

if __name__ == '__main__':
    unittest.main()
