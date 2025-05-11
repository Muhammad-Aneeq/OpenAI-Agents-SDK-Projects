from agents import function_tool, RunContextWrapper
from models.ecommerce_models import EcommerceAgentContext
import random
from datetime import datetime, timedelta

@function_tool
async def track_order(
    context: RunContextWrapper[EcommerceAgentContext], order_number: str
) -> str:
    """
    Track the status of an order.

    Args:
        order_number: The order number to track.
    """
    # Store the order number in context
    context.context.order_number = order_number

    # Simulate order tracking with randomized results
    statuses = ["Order Processing", "Shipped", "Out for Delivery", "Delivered"]
    status = random.choice(statuses)

    if status == "Shipped" or status == "Out for Delivery":
        tracking_number = f"TRK-{random.randint(1000000, 9999999)}"
        context.context.tracking_number = tracking_number
        delivery_date = (datetime.now() + timedelta(days=random.randint(1, 5))).strftime("%B %d, %Y")
        return f"Your order #{order_number} is {status}. Tracking number: {tracking_number}. Estimated delivery: {delivery_date}."
    elif status == "Delivered":
        delivery_date = (datetime.now() - timedelta(days=random.randint(1, 3))).strftime("%B %d, %Y")
        return f"Your order #{order_number} was delivered on {delivery_date}."
    else:
        return f"Your order #{order_number} is currently being processed. It will ship within 1-2 business days."
