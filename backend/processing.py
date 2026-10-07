# Pipeline Coordinator Module
from backend.ingestion import parse_transaction_data
from backend.pricing import calculate_transaction_value, format_currency
from backend.validation import validate_transaction
from security.inventory import update_inventory


def run_pipeline(coin: str, quantity: float, price: float, side: str, current_inventory: dict) -> dict:
    """
    Executes the end-to-end crypto transaction data pipeline.
    """
    # Step 1: Ingestion
    tx_data = parse_transaction_data(coin, quantity, price, side)

    # Step 2: Pricing
    total_value = calculate_transaction_value(tx_data["quantity"], tx_data["price"])
    formatted_value = format_currency(total_value)
    tx_data["total_value"] = total_value
    tx_data["formatted_value"] = formatted_value

    # Step 3: Validation
    validation_result = validate_transaction(tx_data)
    tx_data["validation"] = validation_result

    # Step 4: Security Inventory Update (only if transaction is APPROVED)
    if validation_result["is_valid"]:
        new_inventory = update_inventory(
            current_inventory,
            tx_data["coin"],
            tx_data["quantity"],
            tx_data["side"]
        )
    else:
        new_inventory = current_inventory

    return {
        "transaction": tx_data,
        "new_inventory": new_inventory
    }
