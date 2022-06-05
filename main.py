
from models import Market,Account,Accounts,Asset

ver = 0.02
assets = {
    'binance' : {
        'BTC'   : 0.7,
        'USD'   : 22659+2705,
        'ETH'   : 0,       
        # 'BNB'   : 0.317,
    },
    'ftx' : {
        'USD'   : 193,
        'ETH'   : 0.113,       
        # 'BNB'   : 0.317,
    },
    'mt1_ethereum' : {
        'ETH'   : 0,
    },
    'trezor1_ethereum' : {
        'ETH'   : 3.2,
        'BTC'   : 0.999,
    },
    'ledger_bitcoin' : {
        'BTC'   : 0.3,
    },
    'aridrop' : {
        'USD'   : 7000,
    },
}

# 美元对人民币汇率
Asset.USD_TO_RMB = 6.79
Asset.TOTAL_COST_RMB = 930000
# 使用代理
# proxies = None
proxies = {
        'http': 'http://127.0.0.1:4780',
        'https':'http://127.0.0.1:4780'
    }  

if __name__ == '__main__':
    print('ver:',ver)
    while True:
        if Market.getPrices(proxies):
            Accounts._accountList = []
            for key in assets:
                Accounts.addAccount(Account(key, assets[key]))       
            Accounts.show_by_account()    
            Accounts.show_by_crypto_name()    
        else:
            print('Fail to get prices.')
        s = input('输入回车刷新,其它退出，请输入:')
        if s != '':
            break
