from pydantic import BaseModel

class EcommerceAgentContext(BaseModel):
    customer_name: str | None = None
    customer_email: str | None = None
    order_number: str | None = None
    product_id: str | None = None
    return_reason: str | None = None
    tracking_number: str | None = None

