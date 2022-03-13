import json
import os
from xml.dom import ValidationErr
from app.utils.config import configs
from app.utils.logging import logger
from app.utils.util import data_loader
from app.schemas.base import *
from app.utils.strategies import *
from binance.futures import Futures

class BinanceHandler(object):
    def __init__(self):
        """Init"""
        self.state = self._get_state_from_db()
        self.parm = eval(configs.STRATEGY + "Parm")()
        logger.info(self.parm.__dict__)
        self.strategy_operator = eval(configs.STRATEGY)(self.state, self.parm)
        self.client = self._get_binance_client()
        if configs.MODE == "test":
            self.index =  0
            file_path = os.path.join(configs.DATA_PATH, configs.DATA_TYPE, configs.DATA_INTERVAL)
            self.data = data_loader(file_path)

    def _get_binance_client(self) -> Futures:
        file_path = os.path.join(configs.DBFILE_PATH, configs.APIKEY_PATH)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                key_secret = json.load(f)
                return Futures(key=key_secret["key"], secret=key_secret["secret"])
        else:
            raise ValidationErr(f"could not open apikey file: {configs.APIKEY_PATH}")
    def search_balance(self) -> float:
        # TODO
        return 700
    def trade(self) -> None:
        binance_info = self.get_info_from_binance()
        next_step = self.strategy_operator.next(binance_info)
        if abs(next_step) == 1:
            self._close_position(next_step=next_step)
        elif next_step > 0:
            self._buy(size=next_step, binance_info=binance_info)
        elif next_step < 0:
            self._sell(size=-next_step, binance_info=binance_info)
        self.state = self.strategy_operator.get_state()
        self._save_state_to_db()
    
    def get_info_from_binance(self) -> BinanceInfo:
        if configs.MODE == "test":
            close = self.data.Close[self.index]
            self.index += 1
        else:
            price = self.client.mark_price(configs.DATA_TYPE)
            close = price["indexPrice"]
        logger.info("price = %s", close)
        return BinanceInfo(open=0,close=close,high=0,low=0,volume=0)

    def _close_position(self, next_step: float):
        params = {
            'symbol': configs.DATA_TYPE,
            'side': 'BUY' if next_step == 1 else 'SELL',
            'type': 'MARKET',
            'quantity': 10,
            'reduceOnly': 'true',
        }
        logger.info('_close_position')
        if configs.MODE == "production":
            response = self.client.new_order(**params)
            logger.info(response)
    
    def _buy(self, size: float, binance_info: BinanceInfo):
        # Post a new order
        quantity = self.search_balance() * configs.LEVERAGE * size / binance_info.close
        params = {
            'symbol': configs.DATA_TYPE,
            'side': 'BUY',
            'type': 'MARKET',
            'quantity': float(round(quantity,3))
        }
        logger.info("_buy: %s, real quantity %s", params, quantity)
        if configs.MODE == "production":
            response = self.client.new_order(**params)
            logger.info(response)
    
    def _sell(self, size: float, binance_info: BinanceInfo):
        # Post a new order
        quantity = self.search_balance()* configs.LEVERAGE * size / binance_info.close
        params = {
            'symbol': configs.DATA_TYPE,
            'side': 'SELL',
            'type': 'MARKET',
            'quantity': float(round(quantity,3))
        }
        logger.info("_sell: %s, real quantity %s", params, quantity)
        if configs.MODE == "production":
            response = self.client.new_order(**params)
            logger.info(response)

    def _get_state_from_db(self):
        file_path = os.path.join(configs.DBFILE_PATH, configs.STRATEGY + ".json")
        if os.path.isfile(file_path):
            logger.info("using dbfile state: %s", file_path)
            with open(file_path, 'r') as f:
                state_json = json.load(f)
                return eval(configs.STRATEGY + "State")(**state_json)
        else:
            logger.info("using default state")
            return eval(configs.STRATEGY + "State")()
    def _save_state_to_db(self):
        file_path = os.path.join(configs.DBFILE_PATH, configs.STRATEGY + ".json")
        with open(file_path, 'w') as f:
            json.dump(self.state.__dict__, f)
binance_handler = BinanceHandler()