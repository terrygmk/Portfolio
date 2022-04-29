
from models import Market,Account,Accounts,Asset

ver = 0.02

binance_asset = {
    'BTC'   : 0.952,
    'USD'   : 13774,
    'ETH'   : 4.024,
    'ATOM'  : 97.49,
    'UNI'   : 162.77,
    'LOKA'  : 154.6,
    'BNB'   : 0.850,
    'LUNA'  : 1.08,
    'GMT'   : 22.10,
}

mt1_ethereum_asset = {
    'ETH'   : 0.394,
}

mt1_polygon_asset = {
    'ETH'       : 0.155,
    'MATIC'     : 246,
}

trezor1_ethereum_asset = {
    'ETH'   : 2.368,
}

trezor1_aava_aavx_asset = {
    'BTC'   : 1,
    'ETH'   : 1,
}

ledger_bitcoin_asset = {
    'BTC'   : 0.3,
}

# 美元对人民币汇率
Asset.USD_TO_RMB = 6.4
# 使用代理
# proxies = None
proxies = {
        'http': 'http://127.0.0.1:4780',
        'https':'http://127.0.0.1:4780'
    }  

if __name__ == '__main__':
    print('ver:',ver)
    if Market.getPrices(proxies):
        Accounts.addAccount(Account('binance', binance_asset))
        Accounts.addAccount(Account('mt1_ethereum', mt1_ethereum_asset))
        Accounts.addAccount(Account('mt1_polygon', mt1_polygon_asset))
        Accounts.addAccount(Account('trezor1_ethereum', trezor1_ethereum_asset))
        Accounts.addAccount(Account('trezor1_aava_aavx', trezor1_aava_aavx_asset))
        Accounts.addAccount(Account('ledger_bitcoin', ledger_bitcoin_asset))
        Accounts.show_by_crypto_name()
        Accounts.show_by_account()        
    else:
        print('Fail to get prices.')
