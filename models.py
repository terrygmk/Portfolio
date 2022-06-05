
from typing import Dict
import requests

class Market():

    _priceList = []

    @staticmethod
    def getPrices(proxies=None):
        b_req = False
        url = 'https://api.binance.com/api/v3/ticker/price'                 
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
    def getPrice(asset_name:str, USD_TYPE='USDT'):
        symbol = asset_name + USD_TYPE
        if symbol == 'USD' + USD_TYPE:
            return 1
        for dt in Market.priceList:
            if dt.get('symbol') == symbol:
                return eval(dt.get('price'))
        return 0

class Asset():

    USD_TO_RMB = 6.4
    TOTAL_COST_RMB = 930000

    def __init__(self, name:str, amount:float) -> None:
        self.name   = name
        self.amount = amount
        self.price  = Market.getPrice(self.name)

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
    def get_total_asset_list():
        # 汇总各个账号总资源，并按资产价值倒序
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
        return total_value,asset_list

    @staticmethod
    def show_by_crypto_name():        
        total_value, asset_list = Accounts.get_total_asset_list()               
        lines = '{}{:<8s} {:>12s} {:>12s} {:>8s} {:>8s} {:>6s}%\n'.format('', 'name', 'price', 'amount', 'usd', 'rmb','')
        usd_value = 0
        for asset in asset_list:
            per_total = asset.getValue() / total_value
            if asset.name == 'USD':
                usd_value = asset.getValue()
            lines = '{}{:<8s} {:>12.02f} {:>12.03f} {:>8.0f} {:>8.0f} {:>6.02f}%\n'.format(lines, asset.name, asset.price, asset.amount, asset.getValue(), asset.getRmbValue(), per_total*100)
        lines     = '{}{:<8s} {:>12.02f} {:>12.03f} {:>8.0f} {:>8.0f} {:>6.02f}%\n'.format(lines, 'total', 1, total_value, total_value, total_value * Asset.USD_TO_RMB ,100)
        lines = '{}{:<12s}:{:>12.02f}\n'.format(lines, 'total => USD', total_value/Market.getPrice('USD'))
        total_value_rmb = total_value * Asset.USD_TO_RMB
        profit = total_value_rmb - Asset.TOTAL_COST_RMB
        per_profit = profit / Asset.TOTAL_COST_RMB
        lines = '{}{:<12s}:{:>12.02f}{:>12.02f}{:>8.02f}%\n'.format(lines, 'total => RMB', total_value_rmb, profit, per_profit*100)
        lines = '{}{:<12s}:{:>12.02f}\n'.format(lines, 'total => BTC', total_value/Market.getPrice('BTC'))
        lines = '{}{:<12s}:{:>12.02f}\n'.format(lines, 'total => ETH', total_value/Market.getPrice('ETH'))
        rate = 1-usd_value/total_value
        lines = '{}{:<12s}:{:>11.02f}%\n'.format(lines, 'Rate', rate*100)
        print(lines)

    

    @staticmethod
    def show_by_account():
        lines = '{}{:<20} {:>8} {:>8} {:>6s}%\n'.format('', 'account', 'usd', 'rmb', '')
        total_value = 0
        for account in Accounts._accountList:
            total_value += account.getValue()
        for account in Accounts._accountList:
            per_total = account.getValue() / total_value
            lines = '{}{:<20} {:>8.0f} {:>8.0f} {:>6.02f}%\n'.format(lines, account.name,  account.getValue(), account.getRmbValue(), per_total* 100)
        lines     = '{}{:<20} {:>8.0f} {:>8.0f} {:>6.02f}%\n'.format(lines, 'total', total_value, total_value * Asset.USD_TO_RMB, 100)
        print(lines)

