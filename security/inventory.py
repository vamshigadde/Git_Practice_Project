# Inventory Security Module - Dev 4 Feature Branch (feature/inventory)
from config.config import INITIAL_INVENTORY

def get_initial_inventory() -> dict:
    """
    Returns a copy of the default initial holdings inventory.
    """
    return INITIAL_INVENTORY.copy()


def update_inventory(inventory: dict, coin: str, quantity: float, side: str) -> dict:
    """
    Calculates updated inventory holdings based on transaction side.
    """
    updated = inventory.copy()
    current_balance = updated.get(coin, 0.0)

    if side == "BUY":
        updated[coin] = current_balance + quantity
    elif side == "SELL":
        updated[coin] = current_balance - quantity

    return updated
