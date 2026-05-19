STOCK_PRICES = {
    "AAPL": 180.0,
    "TSLA": 250.0,
    "GOOGL": 140.0,
    "MSFT": 330.0,
    "AMZN": 145.0,
}


def display_available_stocks():
    print("\nAvailable stocks and prices:")
    for stock_name, price in STOCK_PRICES.items():
        print(f"  {stock_name}: ${price:.2f}")


def get_portfolio():
    portfolio = {}

    while True:
        stock_name = input("\nEnter stock symbol (or 'done' to finish): ").strip().upper()

        if stock_name == "DONE":
            break

        if stock_name not in STOCK_PRICES:
            print("Stock not found in the price list. Try again.")
            continue

        quantity_text = input(f"Enter quantity for {stock_name}: ").strip()

        if not quantity_text.isdigit():
            print("Quantity must be a whole number. Try again.")
            continue

        quantity = int(quantity_text)

        if quantity <= 0:
            print("Quantity must be greater than 0. Try again.")
            continue

        portfolio[stock_name] = portfolio.get(stock_name, 0) + quantity
        print(f"Added {quantity} share(s) of {stock_name}.")

    return portfolio


def calculate_total_investment(portfolio):
    total = 0.0
    lines = []

    for stock_name, quantity in portfolio.items():
        price = STOCK_PRICES[stock_name]
        investment = price * quantity
        total += investment
        lines.append((stock_name, quantity, price, investment))

    return total, lines


def display_summary(total, lines):
    print("\nPortfolio Summary")
    print("-" * 50)
    for stock_name, quantity, price, investment in lines:
        print(
            f"{stock_name:<8} Quantity: {quantity:<4} "
            f"Price: ${price:<8.2f} Value: ${investment:.2f}"
        )
    print("-" * 50)
    print(f"Total Investment Value: ${total:.2f}")


def save_to_txt(total, lines, filename="portfolio_summary.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Portfolio Summary\n")
        file.write("-" * 50 + "\n")
        for stock_name, quantity, price, investment in lines:
            file.write(
                f"{stock_name:<8} Quantity: {quantity:<4} "
                f"Price: ${price:<8.2f} Value: ${investment:.2f}\n"
            )
        file.write("-" * 50 + "\n")
        file.write(f"Total Investment Value: ${total:.2f}\n")

    print(f"Saved summary to {filename}")


def save_to_csv(lines, filename="portfolio_summary.csv"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Stock,Quantity,Price,Investment Value\n")
        for stock_name, quantity, price, investment in lines:
            file.write(f"{stock_name},{quantity},{price:.2f},{investment:.2f}\n")

    print(f"Saved summary to {filename}")


def ask_to_save(total, lines):
    choice = input("\nDo you want to save the result? (yes/no): ").strip().lower()

    if choice != "yes":
        return

    file_type = input("Save as '.txt' or '.csv'?: ").strip().lower()

    if file_type == ".txt" or file_type == "txt":
        save_to_txt(total, lines)
    elif file_type == ".csv" or file_type == "csv":
        save_to_csv(lines)
    else:
        print("Unsupported file type. Skipping save.")


def main():
    print("Stock Portfolio Tracker")
    print("=" * 50)
    display_available_stocks()

    portfolio = get_portfolio()

    if not portfolio:
        print("\nNo stocks entered. Exiting program.")
        return

    total, lines = calculate_total_investment(portfolio)
    display_summary(total, lines)
    ask_to_save(total, lines)


if __name__ == "__main__":
    main()
