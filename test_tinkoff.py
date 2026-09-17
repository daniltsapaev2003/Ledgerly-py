from tinkoff import get_shares


shares = get_shares()

print(f"Торгуемых акций: {len(shares)}")
print()

for share in shares[:10]:
    print(share.ticker, "—", share.name)