# Ingestion Module - Dev 1 Feature Branch (feature/ingestion)
from datetime import datetime

def parse_transaction_data(coin: str, quantity: float, price: float, side: str) -> dict:
    """
    Ingests and normalizes raw transaction inputs.
    """
    return {
        "coin": str(coin).strip().upper(),
        "quantity": float(quantity),
        "price": float(price),
        "side": str(side).strip().upper(),
        "timestamp": datetime.now().isoformat()
    }
