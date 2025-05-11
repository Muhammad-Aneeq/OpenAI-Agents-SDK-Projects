from agents import function_tool


@function_tool(
    name_override="product_lookup_tool",
    description_override="Lookup information about products."
)
async def product_lookup_tool(product_query: str) -> str:
    """
    Look up product information based on a query.

    Args:
        product_query: A string describing the product to look up.
    """
    if "headphones" in product_query.lower():
        return (
            "SoundWave Headphones: $99.99\n"
            "Available in black, white, and blue\n"
            "Features: Noise cancellation, Bluetooth 5.0, 24-hour battery life"
        )
    elif "laptop" in product_query.lower():
        return (
            "TechPro Laptop: $899.99\n"
            "Available in silver and space gray\n"
            "Specs: 16GB RAM, 512GB SSD, 15-inch display, Intel i7 processor"
        )
    elif "smartwatch" in product_query.lower():
        return (
            "FitTrack Smartwatch: $149.99\n"
            "Available in black, rose gold, and silver\n"
            "Features: Heart rate monitoring, sleep tracking, water resistant"
        )
    return "I'm sorry, I couldn't find information about that product."
