
from typing import Dict
import requests

class Market():

    _priceList = []

    @staticmethod
    def getPrices():
        b_req = False
        url = 'https://api.binance.com/api/v3/ticker/price'
        proxies = {
            'http': 'http://127.0.0.1:4780',
            'https':'http://127.0.0.1:4780'
        }           
        try:
            req = requests.get(url, timeout=10, proxies=proxies)
            # req = requests.get(url, timeout=10)
            if req.status_code == 200:
                b_req = True
                Market.priceList = req.json()
        except Exception as e :
            print('getPrices:',str(e))
        return b_req

    @staticmethod
    def getPrice(symbol:str):
        if symbol == 'USDUSDT':
            return 1
        for dt in Market.priceList:
            if dt.get('symbol') == symbol:
                return eval(dt.get('price'))
        return None

class Asset():

    USD_TO_RMB = 6.4

    def __init__(self, name:str, amount:float) -> None:
        self.name   = name
        self.amount = amount
        self.price  = Market.getPrice(self.name + 'USDT')

    def getValue(self):
        return self.amount * self.price

    def getRmbValue(self):
        return self.getValue() * Asset.USD_TO_RMB

    def __str__(self) -> str:
        return '{} {} {} '.format(self.name, self.amount, self.price)


class Account():

    def __init__(self, name:str, assetDt:Dict) -> None:
        self.name           = name
        self.assetList      = []
        for asset_name in assetDt:
            asset = Asset(asset_name, assetDt[asset_name])
            self.assetList.append(asset)

    def getValue(self):
        total = 0
        for asset in self.assetList:
            total += asset.getValue()
        return total
    
    def getRmbValue(self):
        return self.getValue() * Asset.USD_TO_RMB


class Accounts():
        
    _accountList    = []

    @staticmethod
    def addAccount(account):        
        Accounts._accountList.append(account)

    @staticmethod
    def show_by_account():
        lines = '{}{:<20} {:>8} {:>8} {:>6s}%\n'.format('', 'account', 'usd', 'rmb', '')
        total_value = 0
        for account in Accounts._accountList:
            total_value += account.getValue()
        for account in Accounts._accountList:
            per_total = account.getValue() / total_value
            lines = '{}{:<20} {:>8.0f} {:>8.0f} {:>6.02f}%\n'.format(lines, account.name, account.getValue(), account.getRmbValue(), per_total* 100)
        lines = '{}{:<20} {:>8.0f} {:>8.0f} {:>6.02f}%\n'.format(lines, 'total', total_value, total_value * Asset.USD_TO_RMB, 100)
        print(lines)

    @staticmethod
    def show_by_crypto_name():        
        total_value = 0
        asset_dict = {}
        for account in Accounts._accountList:
            for asset in account.assetList:
                if asset_dict.get(asset.name) is None:
                    asset_dict[asset.name] = 0
                asset_dict[asset.name] += asset.amount
            total_value += account.getValue()

        asset_list = []
        for asset_name in asset_dict:
            asset_list.append(Asset(asset_name, asset_dict[asset_name]))

        asset_list.sort(key=lambda y: y.getValue(),reverse=True)
        
        lines = '{}{:<20} {:>8} {:>8} {:>6s}%\n'.format('', 'name', 'usd', 'rmb','')
        for asset in asset_list:
            per_total = asset.getValue() / total_value
            lines = '{}{:<20} {:>8.0f} {:>8.0f} {:>6.02f}%\n'.format(lines, asset.name, asset.getValue(), asset.getRmbValue(), per_total*100)

        lines = '{}{:<20} {:>8.0f} {:>8.0f} {:>6.02f}%\n'.format(lines, 'total', total_value, total_value * Asset.USD_TO_RMB,100)

        print(lines)

