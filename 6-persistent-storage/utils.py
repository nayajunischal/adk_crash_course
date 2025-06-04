from google.genai import types


async def _process_event_response(event) -> str | None:
    agent_response = None
    if event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            agent_response = event.content.parts[0].text.strip()
        elif event.actions and event.actions.escalate:
            # Handle potential errors/escalations
            agent_response = (
                f"Agent escalated: {event.error_message or 'No specific message.'}"
            )
    return agent_response


async def call_agent_async(
    user_input: str, runner, user_id: str, session_id: str
) -> str:
    content = types.Content(
        role="user",
        parts=[types.Part(text=user_input)],
    )

    final_response_text = "Agent failed to process your request."  # Default

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        response = await _process_event_response(event)
        if response:
            final_response_text = response

    return final_response_text


def format_order_state_for_display(order_state: dict[str, any]) -> str:
    """
    Format the current order state for display to the user
    """
    if not order_state:
        return "Your order is empty."

    output = "\n🛒 **CURRENT ORDER:**\n"

    # Pizza details
    pizza_type = order_state.get("pizza_type")
    if pizza_type:
        output += f"Pizza: {pizza_type.replace('_', ' ').title()}\n"
    else:
        output += "Pizza: Not selected\n"

    # Size
    size = order_state.get("size")
    if size:
        output += f"Size: {size.replace('_', ' ').title()}\n"
    else:
        output += "Size: Not selected\n"

    # Toppings
    toppings = order_state.get("toppings", [])
    if toppings:
        toppings_str = ", ".join([t.replace("_", " ").title() for t in toppings])
        output += f"Extra Toppings: {toppings_str}\n"

    # Quantity
    quantity = order_state.get("quantity", 1)
    output += f"Quantity: {quantity}\n"

    # Delivery info
    address = order_state.get("address")
    if address:
        output += f"Delivery Address: {address}\n"

    phone = order_state.get("phone_number")
    if phone:
        output += f"Phone: {phone}\n"

    # Price
    total_price = order_state.get("total_price", 0.0)
    if total_price > 0:
        output += f"\n**Total: ${total_price:.2f}**\n"

    return output


def get_order_status_message(order_state: dict[str, any]) -> str:
    """
    Get a status message based on the current order state
    """
    if not order_state:
        return "👋 Welcome! Ready to order some delicious pizza?"

    status = order_state.get("status", "START")

    status_messages = {
        "START": "👋 Welcome! Ready to order some delicious pizza?",
        "PIZZA_SELECTED": "🍕 Great choice! Now let's pick a size.",
        "SIZE_SELECTED": "📏 Perfect! Want to add any extra toppings?",
        "TOPPINGS_ADDED": "🧀 Awesome toppings! Ready for delivery details?",
        "DELIVERY_INFO_SET": "📍 All set! Let me calculate your total.",
        "ORDER_COMPLETE": "✅ Order ready! Confirm to place your order.",
    }

    return status_messages.get(status, "Let me help you with your pizza order!")


def is_order_complete(order_state: dict[str, any]) -> bool:
    """
    Check if an order has all required information
    """
    if not order_state:
        return False

    return (
        bool(order_state.get("pizza_type"))
        and bool(order_state.get("size"))
        and bool(order_state.get("address"))
        and bool(order_state.get("phone_number"))
    )


def get_order_progress(order_state: dict[str, any]) -> str:
    """
    Get a progress indicator for the current order
    """
    if not order_state:
        return "⭕ ⭕ ⭕ ⭕ ⭕"

    progress = ""

    # Pizza type selected
    if order_state.get("pizza_type"):
        progress += "✅ "
    else:
        progress += "⭕ "

    # Size selected
    if order_state.get("size"):
        progress += "✅ "
    else:
        progress += "⭕ "

    # Toppings (optional but show if any)
    if order_state.get("toppings"):
        progress += "✅ "
    else:
        progress += "➖ "

    # Address provided
    if order_state.get("address"):
        progress += "✅ "
    else:
        progress += "⭕ "

    # Phone provided
    if order_state.get("phone_number"):
        progress += "✅"
    else:
        progress += "⭕"

    return progress


def calculate_order_price(order_state: dict[str, any]) -> float:
    """
    Calculate the total price based on current order state
    """
    if (
        not order_state
        or not order_state.get("pizza_type")
        or not order_state.get("size")
    ):
        return 0.0

    # Pizza menu (simplified version for calculation)
    pizza_prices = {
        "margherita": 12.99,
        "pepperoni": 14.99,
        "supreme": 18.99,
        "hawaiian": 16.99,
        "meat_lovers": 19.99,
        "veggie": 15.99,
    }

    size_multipliers = {"small": 0.8, "medium": 1.0, "large": 1.3, "extra_large": 1.6}

    topping_prices = {
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

    # Base calculation
    base_price = pizza_prices.get(order_state["pizza_type"], 0)
    size_multiplier = size_multipliers.get(order_state["size"], 1.0)
    pizza_price = base_price * size_multiplier

    # Toppings
    toppings = order_state.get("toppings", [])
    toppings_price = sum(topping_prices.get(topping, 0) for topping in toppings)

    # Quantity
    quantity = order_state.get("quantity", 1)

    # Calculate total
    subtotal = (pizza_price + toppings_price) * quantity
    tax = subtotal * 0.08  # 8% tax
    total = subtotal + tax

    return round(total, 2)
