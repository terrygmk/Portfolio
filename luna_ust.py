from models import Market,Account,Accounts,Asset

proxies = {
        'http': 'http://127.0.0.1:4780',
        'https':'http://127.0.0.1:4780'
    } 

if Market.getPrices(proxies):
    luna_busd = Market.getPrice('LUNA','BUSD')
    ust_busd = Market.getPrice('UST','BUSD')
    luna_ust = luna_busd / ust_busd
    ust_luna = ust_busd / luna_busd
    print(luna_busd, ust_busd, luna_ust, ust_luna)