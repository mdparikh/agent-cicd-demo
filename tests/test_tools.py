from agent_app import lookup_order, search_faq

def test_existing_order():
    result = lookup_order.invoke("1001")
    assert "shipped" in result
    assert "August 16, 2026" in result

def test_missing_order():
    result = lookup_order.invoke("9999")
    assert "No order was found" in result

def test_return_faq():
    result = search_faq.invoke("return")
    assert "30 days" in result
