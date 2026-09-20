from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

ORDERS = {
    "1001": {"customer": "Priya", "item": "Wireless Headphones", "status": "shipped", "expected_delivery": "August 16, 2026"},
    "1002": {"customer": "Rahul", "item": "Mechanical Keyboard", "status": "delivered", "expected_delivery": "August 10, 2026"},
    "1003": {"customer": "Anita", "item": "USB-C Monitor", "status": "processing", "expected_delivery": "August 20, 2026"},
}

FAQ = {
    "return": "Items can be returned within 30 days of delivery if they are unused and in original packaging.",
    "refund": "Approved refunds are normally processed within 5-7 business days after the returned item is received.",
    "shipping": "Standard shipping normally takes 3-5 business days. Customers receive tracking information after shipment.",
}

@tool
def lookup_order(order_id: str) -> str:
    """Look up an order by order ID."""
    order = ORDERS.get(order_id)
    if not order:
        return f"No order was found for order ID {order_id}."
    return (
        f"Order {order_id}: customer={order['customer']}, item={order['item']}, "
        f"status={order['status']}, expected_delivery={order['expected_delivery']}."
    )

@tool
def search_faq(topic: str) -> str:
    """Find return, refund, or shipping policy information."""
    topic = topic.lower()
    for key, answer in FAQ.items():
        if key in topic:
            return answer
    return "No matching FAQ information was found."

SYSTEM_PROMPT = """
You are an e-commerce customer support agent.
Use lookup_order for specific order questions.
Use search_faq for returns, refunds, and shipping.
Never invent order information.
If an order cannot be found, clearly say so.
Only use information returned by tools for factual claims.
Be concise, helpful, and professional.
"""

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

agent = create_agent(
    model=llm,
    tools=[lookup_order, search_faq],
    system_prompt=SYSTEM_PROMPT,
)

def ask_agent(question: str) -> str:
    result = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })
    return result["messages"][-1].content[0]['text']
