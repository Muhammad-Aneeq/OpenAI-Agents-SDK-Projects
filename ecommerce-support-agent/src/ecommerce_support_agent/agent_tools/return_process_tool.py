from agents import function_tool, RunContextWrapper
from models.ecommerce_models import EcommerceAgentContext
import random

@function_tool
async def process_return(
    context: RunContextWrapper[EcommerceAgentContext],
    order_number: str,
    product_id: str,
    reason: str
) -> str:
    """
    Process a return request.

    Args:
        order_number: The order number for the return.
        product_id: The product ID being returned.
        reason: The reason for the return.
    """
    # Update context with return information
    context.context.order_number = order_number
    context.context.product_id = product_id
    context.context.return_reason = reason

    # Generate a return authorization number
    return_auth = f"RET-{random.randint(10000, 99999)}"

    return (
        f"Return request processed successfully.\n"
        f"Return Authorization Number: {return_auth}\n"
        f"Please print the return label from your account and ship the item back within 14 days."
    )
