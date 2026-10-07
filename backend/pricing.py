# Pricing Module - Dev 2 Feature Branch (feature/pricing)

def calculate_transaction_value(quantity: float, price: float) -> float:
    """
    Calculates the total monetary value of a transaction.
    """
    return quantity * price


def format_currency(amount: float, currency_symbol: str = "$") -> str:
    """
    Formats numeric amounts into currency string representation.
    """
    return f"{currency_symbol}{amount:,.2f}"
