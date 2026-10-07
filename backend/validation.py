# Validation Module - Dev 3 Feature Branch (feature/validation)
from config.config import SUPPORTED_COINS

def validate_transaction(transaction: dict) -> dict:
    """
    Validates ingested transaction parameters.
    """
    errors = []

    if transaction["quantity"] <= 0:
        errors.append("Quantity must be greater than zero.")
        
    if transaction["price"] <= 0:
        errors.append("Price must be greater than zero.")

    if transaction["side"] not in ["BUY", "SELL"]:
        errors.append("Side must be either BUY or SELL.")

    if transaction["coin"] not in SUPPORTED_COINS:
        errors.append(f"Unsupported coin. Allowed: {', '.join(SUPPORTED_COINS)}")

    is_valid = len(errors) == 0

    return {
        "is_valid": is_valid,
        "status": "APPROVED" if is_valid else "REJECTED",
        "errors": errors
    }
