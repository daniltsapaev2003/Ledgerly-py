from tinkoff import get_shares


shares = get_shares()

print(f"Получено акций: {len(shares)}")
print()

share = shares[0]

print(share)