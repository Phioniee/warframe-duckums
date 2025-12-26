import wfm_api

def run_duckums():
    prime_parts = wfm_api.get_prime_parts_list()
    if prime_parts is None:
        return
    
    user_input = input("\nEnter the prime part: ").strip()

    found_item = None
    for item in prime_parts:
        if item.get("i18n", {}).get("en", {}).get("name", "").lower() == user_input.lower():
            found_item = item
            break
    
    if not found_item:
        print(f"Item '{user_input}' not found among prime parts.")
        return
    
    item_slug = found_item.get("url_name")
    ducat_value = found_item.get("ducats", 0)
    average_price = wfm_api.get_price(item_slug)

    print("\n--- Duckums Result ---")
    print(f"Item: {user_input}")
    print(f"Ducat Value: {ducat_value}")
    print(f"Average Market Price: {average_price}")

if __name__ == "__main__":
    run_duckums()
