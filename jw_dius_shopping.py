from decimal import Decimal, ROUND_HALF_UP


class PricingRules:
    """PricingRules contains the prices for the items stocked in inventory
    and any special pricing rules applicable to these items. When apply_rules(cart)
    is called with a cart of items, the prices and special rules are applied and
    a total price is returned for use by a Checkout object.
    """

    def __init__(self):
        self._inventory = {
            "ipd": ("Super iPad", Decimal("549.99")),
            "mbp": ("MacBook Pro", Decimal("1399.99")),
            "atv": ("Apple TV", Decimal("109.50")),
            "vga": ("VGA adapter", Decimal("30.00")),
        }
        self._pricing_rules = {
            "ipd": self._ipd_rule,
            "mbp": self._mbp_rule,
            "atv": self._atv_rule,
            "vga": self._vga_rule,
        }

    def _ipd_rule(self, qty, unit_price, cart):
        """The brand new Super iPad will have a bulk discounted applied,
        where the price will drop to $499.99 each, if someone buys more than 4.
        """
        if qty > 4:
            unit_price = Decimal("499.99")
        return unit_price * qty

    def _mbp_rule(self, qty, unit_price, cart):
        """MacBook Pros do not have a special pricing rule."""
        return unit_price * qty

    def _atv_rule(self, qty, unit_price, cart):
        """We're going to have a 3 for 2 deal on Apple TVs.
        For example, if you buy 3 Apple TVs, you will pay the price of 2 only.
        """
        return unit_price * (2 * (qty // 3) + qty % 3)

    def _vga_rule(self, qty, unit_price, cart):
        """We will bundle in a free VGA adapter free of charge with every MacBook Pro sold.
        Only charge for qty of VGA adapters less qty of MBPs.
        """
        subtotal = Decimal("0.00")
        qty_mbp = cart["mbp"] if "mbp" in cart else 0
        if qty_mbp < qty:
            subtotal = unit_price * (qty - qty_mbp)
        return subtotal

    def apply_rules(self, cart):
        """Apply pricing rules to cart and return sum total."""
        total = Decimal("0.00")
        for sku in cart:
            qty = cart[sku]
            unit_price = self._inventory[sku][1]
            product_rule = self._pricing_rules[sku]
            subtotal = product_rule(qty, unit_price, cart)
            total += subtotal
        # ensure that total is rounded correctly to 2 decimal places
        return total.quantize(Decimal(".01"), rounding=ROUND_HALF_UP)


class Checkout:
    """Checkout allows items to be scanned by their SKU using scan(sku).
    These items are tallied in the cart dict and total() returns the
    cart total with pricing rules applied.
    """

    def __init__(self, pricing_rules):
        self._pricing_rules = pricing_rules
        self._cart = {}

    def scan(self, sku):
        """Scans an item's SKU and adds it to the cart."""
        if sku not in self._cart:
            self._cart[sku] = 1
        else:
            self._cart[sku] += 1

    def total(self):
        """Gets cart total after pricing rules have been applied."""
        return self._pricing_rules.apply_rules(self._cart)
