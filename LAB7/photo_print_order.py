def parse_order(text):
    if not isinstance(text, str):
        return None, 0
    if ':' not in text:
        return None, 0
    parts = text.split(':')
    if len(parts) != 2:
        return None, 0
    size_part, copies_part = parts
    size = size_part.strip().upper()
    try:
        copies = int(copies_part.strip())
        if copies < 0:
            copies = 0
    except (ValueError, TypeError):
        copies = 0
    return size, copies


def file_size_average(sizes_csv):
    if not isinstance(sizes_csv, str):
        return 0
    parts = sizes_csv.split(',')
    values = []
    for r in parts:
        cleaned = r.strip()
        if cleaned:
            try:
                values.append(int(cleaned))
            except (ValueError, TypeError):
                pass
    if not values:
        return 0
    return sum(values) // len(values)


def payable_amount(text):
    if not isinstance(text, str):
        return 0.0
    if '|' not in text:
        return 0.0
    parts = text.split('|')
    if len(parts) != 2:
        return 0.0
    amount_str, discount_str = parts
    try:
        amount = float(amount_str.strip())
    except (ValueError, TypeError):
        amount = 0.0
    try:
        discount = float(discount_str.strip())
    except (ValueError, TypeError):
        discount = 0.0
    total = amount * 1.18 - discount
    return max(total, 0.0)


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter print size:copies (e.g. 4x6:25): ")
    result = parse_order(user_input)
    print("Size and Copies:", result)

    print("\n==== Running file_size_average ====")
    user_input = input("Enter file sizes in MB as CSV (e.g. 4,8,12): ")
    result = file_size_average(user_input)
    print("Average File Size:", result)

    print("\n==== Running payable_amount ====")
    user_input = input("Enter amount|discount (e.g. 450|50): ")
    result = payable_amount(user_input)
    print("Payable Amount:", result)


if __name__ == "__main__":
    main()