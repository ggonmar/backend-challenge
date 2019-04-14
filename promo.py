

# Promo:
# Definition of a promotion following patterns that would apply to the requested scenario:
# Promotions have a number of items it applies onto (threshold, so to say), and a discount on each item.
class Promo:
    def __init__(self, promo_name: str, percentage_off_per_item: float, promo_divider: int) -> None:
        self.promo_name = promo_name
        self.percentage_off_per_item = percentage_off_per_item
        self.promo_divider = promo_divider


# For the Vouchers, it's a 50% discount if we buy 2
promo2x1: Promo = Promo("2x1 Promo", 0.5, 2)

# For the T-shirts, it's a 5% off if we buy 3
promo3for19: Promo = Promo("3 for 19€", 0.05, 3)
