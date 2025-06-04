from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

PIZZA_MENU = {
    "margherita": {
        "base_price": 12.99,
        "description": "Classic tomato sauce, mozzarella, and basil",
    },
    "pepperoni": {
        "base_price": 14.99,
        "description": "Tomato sauce, mozzarella, and pepperoni",
    },
    "supreme": {
        "base_price": 18.99,
        "description": "Tomato sauce, mozzarella, pepperoni, sausage, peppers, onions, mushrooms",
    },
    "hawaiian": {
        "base_price": 16.99,
        "description": "Tomato sauce, mozzarella, ham, and pineapple",
    },
    "meat_lovers": {
        "base_price": 19.99,
        "description": "Tomato sauce, mozzarella, pepperoni, sausage, ham, and bacon",
    },
    "veggie": {
        "base_price": 15.99,
        "description": "Tomato sauce, mozzarella, peppers, onions, mushrooms, and olives",
    },
}

SIZE_MULTIPLIERS = {"small": 0.8, "medium": 1.0, "large": 1.3, "extra_large": 1.6}

AVAILABLE_TOPPINGS = {
    "pepperoni": 2.00,
    "sausage": 2.00,
    "mushrooms": 1.50,
    "peppers": 1.50,
    "onions": 1.50,
    "olives": 1.50,
    "extra_cheese": 2.50,
    "bacon": 2.50,
    "ham": 2.00,
    "pineapple": 1.50,
}


def display_menu(tool_context: ToolContext) -> dict:
    print("--- Tool: display_menu called ---")

    menu_text = "🍕 **PIZZA MENU** 🍕\n\n"

    for pizza_name, details in PIZZA_MENU.items():
        menu_text += f"**{pizza_name.replace('_', ' ').title()}** - ${details['base_price']:.2f}\n"
        menu_text += f"   {details['description']}\n\n"

    menu_text += "\n**SIZES & PRICING:**\n"
    menu_text += "- Small (80% of base price)\n"
    menu_text += "- Medium (base price)\n"
    menu_text += "- Large (130% of base price)\n"
    menu_text += "- Extra Large (160% of base price)\n\n"

    menu_text += "**ADDITIONAL TOPPINGS:**\n"
    for topping, price in AVAILABLE_TOPPINGS.items():
        menu_text += f"- {topping.replace('_', ' ').title()}: +${price:.2f}\n"

    return {"action": "display_menu", "menu": menu_text}


def set_pizza_type(pizza_type: str, tool_context: ToolContext) -> dict:
    print(f"--- Tool: set_pizza_type called with '{pizza_type}' ---")

    pizza_type_lower = pizza_type.lower()

    if pizza_type_lower not in PIZZA_MENU:
        available_pizzas = ", ".join(
            [p.replace("_", " ").title() for p in PIZZA_MENU.keys()]
        )
        return {
            "action": "set_pizza_type",
            "status": "error",
            "message": f"Pizza type '{pizza_type}' is not available. Available pizzas: {available_pizzas}",
        }

    tool_context.state["pizza_type"] = pizza_type_lower
    tool_context.state["status"] = "PIZZA_SELECTED"

    pizza_info = PIZZA_MENU[pizza_type_lower]

    return {
        "action": "set_pizza_type",
        "pizza_type": pizza_type_lower,
        "description": pizza_info["description"],
        "base_price": pizza_info["base_price"],
        "message": f"Great choice! Selected {pizza_type.title()} pizza (${pizza_info['base_price']:.2f}). {pizza_info['description']}",
    }


def set_pizza_size(size: str, tool_context: ToolContext) -> dict:
    print(f"--- Tool: set_pizza_size called with '{size}' ---")

    size_lower = size.lower()

    if size_lower not in SIZE_MULTIPLIERS:
        available_sizes = ", ".join(
            [s.replace("_", " ").title() for s in SIZE_MULTIPLIERS.keys()]
        )
        return {
            "action": "set_pizza_size",
            "status": "error",
            "message": f"Size '{size}' is not available. Available sizes: {available_sizes}",
        }

    tool_context.state["size"] = size_lower
    tool_context.state["status"] = "SIZE_SELECTED"

    multiplier = SIZE_MULTIPLIERS[size_lower]

    return {
        "action": "set_pizza_size",
        "size": size_lower,
        "multiplier": multiplier,
        "message": f"Perfect! Selected {size.replace('_', ' ').title()} size (price multiplier: {multiplier}x)",
    }


def add_toppings(toppings: list[str], tool_context: ToolContext) -> dict:
    print(f"--- Tool: add_toppings called with {toppings} ---")

    # Get current toppings from state
    current_toppings = tool_context.state.get("toppings", [])

    # Validate toppings
    invalid_toppings = []
    valid_toppings = []

    for topping in toppings:
        topping_lower = topping.lower()
        if topping_lower in AVAILABLE_TOPPINGS:
            if topping_lower not in current_toppings:
                valid_toppings.append(topping_lower)
        else:
            invalid_toppings.append(topping)

    if invalid_toppings:
        available_toppings = ", ".join(
            [t.replace("_", " ").title() for t in AVAILABLE_TOPPINGS.keys()]
        )
        return {
            "action": "add_toppings",
            "status": "error",
            "invalid_toppings": invalid_toppings,
            "message": f"Invalid toppings: {', '.join(invalid_toppings)}. Available toppings: {available_toppings}",
        }

    current_toppings.extend(valid_toppings)
    tool_context.state["toppings"] = current_toppings

    topping_prices = {
        topping: AVAILABLE_TOPPINGS[topping] for topping in valid_toppings
    }
    total_topping_cost = sum(topping_prices.values())

    return {
        "action": "add_toppings",
        "added_toppings": valid_toppings,
        "topping_prices": topping_prices,
        "total_topping_cost": total_topping_cost,
        "all_toppings": current_toppings,
        "message": f"Added toppings: {', '.join([t.replace('_', ' ').title() for t in valid_toppings])}. Extra cost: ${total_topping_cost:.2f}",
    }


def remove_toppings(toppings: list[str], tool_context: ToolContext) -> dict:
    print(f"--- Tool: remove_toppings called with {toppings} ---")

    # Get current toppings from state
    current_toppings = tool_context.state.get("toppings", [])

    removed_toppings = []
    not_found_toppings = []

    for topping in toppings:
        topping_lower = topping.lower()
        if topping_lower in current_toppings:
            current_toppings.remove(topping_lower)
            removed_toppings.append(topping_lower)
        else:
            not_found_toppings.append(topping)

    # Update state
    tool_context.state["toppings"] = current_toppings

    message = ""
    if removed_toppings:
        message += f"Removed toppings: {', '.join([t.replace('_', ' ').title() for t in removed_toppings])}. "
    if not_found_toppings:
        message += (
            f"Could not find these toppings to remove: {', '.join(not_found_toppings)}"
        )

    return {
        "action": "remove_toppings",
        "removed_toppings": removed_toppings,
        "not_found_toppings": not_found_toppings,
        "remaining_toppings": current_toppings,
        "message": message.strip(),
    }


def set_quantity(quantity: int, tool_context: ToolContext) -> dict:
    print(f"--- Tool: set_quantity called with {quantity} ---")

    if quantity < 1 or quantity > 20:
        return {
            "action": "set_quantity",
            "status": "error",
            "message": "Quantity must be between 1 and 20 pizzas",
        }

    tool_context.state["quantity"] = quantity

    return {
        "action": "set_quantity",
        "quantity": quantity,
        "message": f"Set quantity to {quantity} pizza{'s' if quantity > 1 else ''}",
    }


def set_delivery_info(
    address: str, phone_number: str, tool_context: ToolContext
) -> dict:
    print(
        f"--- Tool: set_delivery_info called with address: '{address}', phone: '{phone_number}' ---"
    )

    errors = []

    if not address or len(address.strip()) < 10:
        errors.append("Address must be at least 10 characters long")

    phone_clean = "".join(filter(str.isdigit, phone_number))
    if len(phone_clean) not in [10, 11]:
        errors.append("Phone number must be 10 or 11 digits")

    if errors:
        return {
            "action": "set_delivery_info",
            "status": "error",
            "errors": errors,
            "message": f"Validation failed: {'; '.join(errors)}",
        }

    tool_context.state["address"] = address.strip()
    tool_context.state["phone_number"] = phone_clean
    tool_context.state["status"] = "DELIVERY_INFO_SET"

    return {
        "action": "set_delivery_info",
        "address": address.strip(),
        "phone_number": phone_clean,
        "message": f"Delivery info set! Address: {address.strip()}, Phone: {phone_clean}",
    }


def calculate_total_price(tool_context: ToolContext) -> dict:
    print("--- Tool: calculate_total_price called ---")

    # Get order details from state
    pizza_type = tool_context.state.get("pizza_type")
    size = tool_context.state.get("size")
    toppings = tool_context.state.get("toppings", [])
    quantity = tool_context.state.get("quantity", 1)

    if not pizza_type or not size:
        return {
            "action": "calculate_total_price",
            "status": "error",
            "message": "Cannot calculate price: Pizza type and size must be selected first",
        }

    base_price = PIZZA_MENU[pizza_type]["base_price"]
    size_multiplier = SIZE_MULTIPLIERS[size]
    pizza_price = base_price * size_multiplier

    toppings_price = sum(AVAILABLE_TOPPINGS[topping] for topping in toppings)

    price_per_pizza = pizza_price + toppings_price
    subtotal = price_per_pizza * quantity
    tax = subtotal * 0.08  # 8% tax
    total_price = subtotal + tax

    tool_context.state["total_price"] = total_price

    return {
        "action": "calculate_total_price",
        "pizza_type": pizza_type,
        "size": size,
        "toppings": toppings,
        "quantity": quantity,
        "base_price": base_price,
        "size_multiplier": size_multiplier,
        "pizza_price": pizza_price,
        "toppings_price": toppings_price,
        "price_per_pizza": price_per_pizza,
        "subtotal": subtotal,
        "tax": tax,
        "total_price": total_price,
        "message": f"Order total: ${total_price:.2f} (Subtotal: ${subtotal:.2f} + Tax: ${tax:.2f})",
    }


def view_current_order(tool_context: ToolContext) -> dict:
    print("--- Tool: view_current_order called ---")

    state = tool_context.state

    # Build order summary
    order_summary = "🍕 **CURRENT ORDER SUMMARY** 🍕\n\n"

    pizza_type = state.get("pizza_type")
    if pizza_type:
        pizza_info = PIZZA_MENU[pizza_type]
        order_summary += f"Pizza: {pizza_type.replace('_', ' ').title()}\n"
        order_summary += f"Description: {pizza_info['description']}\n"
    else:
        order_summary += "Pizza: Not selected\n"

    size = state.get("size")
    if size:
        order_summary += f"Size: {size.replace('_', ' ').title()}\n"
    else:
        order_summary += "Size: Not selected\n"

    toppings = state.get("toppings", [])
    if toppings:
        toppings_str = ", ".join([t.replace("_", " ").title() for t in toppings])
        order_summary += f"Extra Toppings: {toppings_str}\n"
    else:
        order_summary += "Extra Toppings: None\n"

    quantity = state.get("quantity", 1)
    order_summary += f"Quantity: {quantity}\n"

    address = state.get("address")
    if address:
        order_summary += f"Delivery Address: {address}\n"
    else:
        order_summary += "Delivery Address: Not provided\n"

    phone = state.get("phone_number")
    if phone:
        order_summary += f"Phone Number: {phone}\n"
    else:
        order_summary += "Phone Number: Not provided\n"

    total_price = state.get("total_price", 0.0)
    if total_price > 0:
        order_summary += f"\n**Total Price: ${total_price:.2f}**\n"

    status = state.get("status", "START")
    order_summary += f"\nOrder Status: {status}\n"

    return {
        "action": "view_current_order",
        "order_summary": order_summary,
        "order_complete": bool(pizza_type and size and address and phone),
        "status": status,
    }


pizza_order_agent = Agent(
    name="pizza_order_agent",
    model="gemini-2.0-flash",
    description="A specialized assistant for taking pizza orders with persistent state management",
    instruction="""
    You are a friendly pizza ordering assistant that helps customers build their perfect pizza order.
    
    The order state contains:
    - status: Current order status (START, PIZZA_SELECTED, SIZE_SELECTED, etc.)
    - pizza_type: Selected pizza type
    - size: Selected pizza size  
    - toppings: list of additional toppings
    - quantity: Number of pizzas
    - address: Delivery address
    - phone_number: Contact phone number
    - total_price: Calculated total price
    
    **ORDER PROCESS GUIDELINES:**
    
    1. **Menu Display**: Use display_menu when customers ask about available options
    
    2. **Pizza Selection**: Use set_pizza_type when customers choose a pizza
    
    3. **Size Selection**: Use set_pizza_size when customers specify size
    
    4. **Toppings Management**: 
       - Use add_toppings to add extra toppings
       - Use remove_toppings to remove toppings
       - Be smart about interpreting customer requests
    
    5. **Quantity**: Use set_quantity when customers specify how many pizzas
    
    6. **Delivery Info**: Use set_delivery_info to collect address and phone
    
    7. **Price Calculation**: Use calculate_total_price to show pricing breakdown
    
    8. **Order Review**: Use view_current_order to show complete order summary
    
    **SMART INTERACTION RULES:**
    
    - Always be friendly and conversational
    - Guide customers through the ordering process naturally
    - Use your best judgment to interpret customer requests
    - Don't ask for clarification unless absolutely necessary
    - Automatically calculate prices when order details change
    - Suggest popular combinations or upsells appropriately
    - Confirm important details before finalizing
    
    **AVAILABLE PIZZAS:** margherita, pepperoni, supreme, hawaiian, meat_lovers, veggie
    **AVAILABLE SIZES:** small, medium, large, extra_large  
    **AVAILABLE TOPPINGS:** pepperoni, sausage, mushrooms, peppers, onions, olives, extra_cheese, bacon, ham, pineapple
    
    Remember to keep the conversation natural and helpful while ensuring all order details are captured accurately.
    """,
    tools=[
        display_menu,
        set_pizza_type,
        set_pizza_size,
        add_toppings,
        remove_toppings,
        set_quantity,
        set_delivery_info,
        calculate_total_price,
        view_current_order,
    ],
)
