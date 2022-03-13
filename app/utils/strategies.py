#只買
import math

from sqlalchemy import false
from app.schemas.base import *

class MartinV1():
    """只做買"""
    def __init__(self, state: MartinV1State, parm: MartinV1Parm):
        self.state = state
        self.parm = parm
        self.martin = self._martin_money_generator(self.parm.max_num_trade, self.parm.money_mul_factor)

    def _martin_money_generator(self, max_num_trade, money_mul_factor):
        if money_mul_factor < 1:
            raise ValueError("money_mul_factor must larger than 1")
        total_money = (math.pow(money_mul_factor, max_num_trade + 1) - 1) / (money_mul_factor - 1)
        money = [math.pow(money_mul_factor, i) / total_money for i in range(max_num_trade + 1)]
        return money
    
    def get_state(self) -> dict:
        # print(self.state.__dict__)
        return self.state

    def next(self, binance_info: BinanceInfo) -> float:
        ans = 0
        if self.state.index == 0:
            self.state.total_money = 0
            self.state.total_coin = 0
            self.state.next_price = binance_info.close
        if self.state.index > 0 and \
            binance_info.close > (self.state.total_money / self.state.total_coin) * (1 + self.parm.profit):
            ans = -1
            self.state.index = 0
        elif self.state.index < len(self.martin) and binance_info.close <= self.state.next_price:
            ans = self.martin[self.state.index]
            self.state.total_money += self.martin[self.state.index]
            self.state.total_coin += (self.martin[self.state.index] / binance_info.close)
            self.state.next_price = self.state.next_price * (1 - self.parm.price_mul_factor)
            self.state.index += 1
        else:
            ans = 0
        return ans

class MartinV2():
    """上下都有"""
    def __init__(self, state: MartinV2State, parm: MartinV2Parm):
        self.state = state
        self.parm = parm
        self.martin = self._martin_money_generator(self.parm.max_num_trade, self.parm.money_mul_factor)

    def _martin_money_generator(self, max_num_trade, money_mul_factor):
        if money_mul_factor < 1:
            raise ValueError("money_mul_factor must larger than 1")
        total_money = (math.pow(money_mul_factor, max_num_trade + 1) - 1) / (money_mul_factor - 1)
        money = [math.pow(money_mul_factor, i) / total_money for i in range(max_num_trade + 1)]
        return money
    
    def get_state(self) -> dict:
        return self.state

    def next(self, binance_info: BinanceInfo) -> float:
        next_step = 0
        if self.state.trade_state == 0:
            self.state.total_money = 0
            self.state.total_coin = 0
            self.state.start_sell_price = binance_info.close * (1 + self.parm.price_range)
            self.state.start_buy_price = binance_info.close * (1 - self.parm.price_range)
            self.state.trade_state = 1
            self.state.index = 0
        elif self.state.trade_state == 1:
            if binance_info.close <= self.state.start_buy_price:
                self.state.trade_state = 2
                self.state.next_price = binance_info.close
            elif binance_info.close >= self.state.start_sell_price:
                self.state.trade_state = 3
                self.state.next_price = binance_info.close

        if self.state.trade_state == 2:
            if self.state.index < len(self.martin) and binance_info.close <= self.state.next_price:
                next_step = self.martin[self.state.index]
                self.state.total_money += self.martin[self.state.index]
                self.state.total_coin += (self.martin[self.state.index] / binance_info.close)
                self.state.next_price = self.state.next_price * (1 - self.parm.price_mul_factor)
                self.state.index += 1
            elif binance_info.close > (self.state.total_money / self.state.total_coin) * (1 + self.parm.profit):
                next_step = -1
                self.state.trade_state = 0
        elif self.state.trade_state == 3:
            if self.state.index < len(self.martin) and binance_info.close >= self.state.next_price:
                next_step = -self.martin[self.state.index]
                self.state.total_money += self.martin[self.state.index]
                self.state.total_coin += (self.martin[self.state.index] / binance_info.close)
                self.state.next_price = self.state.next_price * (1 + self.parm.price_mul_factor)
                self.state.index += 1
            elif binance_info.close < (self.state.total_money / self.state.total_coin) * (1 - self.parm.profit):
                next_step = 1
                self.state.trade_state = 0
        return next_step

class MartinV3():
    """止損"""
    def __init__(self, state: MartinV2State, parm: MartinV2Parm):
        self.state = state
        self.parm = parm
        self.martin = self._martin_money_generator(self.parm.max_num_trade, self.parm.money_mul_factor)

    def _martin_money_generator(self, max_num_trade, money_mul_factor):
        if money_mul_factor < 1:
            raise ValueError("money_mul_factor must larger than 1")
        total_money = (math.pow(money_mul_factor, max_num_trade + 1) - 1) / (money_mul_factor - 1)
        money = [math.pow(money_mul_factor, i) / total_money for i in range(max_num_trade + 1)]
        return money
    
    def get_state(self) -> dict:
        return self.state

    def next(self, binance_info: BinanceInfo) -> float:
        next_step = 0
        if self.state.trade_state == 0:
            self.state.total_money = 0
            self.state.total_coin = 0
            self.state.start_sell_price = binance_info.close * (1 + self.parm.price_range)
            self.state.start_buy_price = binance_info.close * (1 - self.parm.price_range)
            self.state.trade_state = 1
            self.state.index = 0
        elif self.state.trade_state == 1:
            if binance_info.close <= self.state.start_buy_price:
                self.state.trade_state = 2
                self.state.next_price = binance_info.close
            elif binance_info.close >= self.state.start_sell_price:
                self.state.trade_state = 3
                self.state.next_price = binance_info.close

        if self.state.trade_state == 2:
            if self.state.index < len(self.martin) and binance_info.close <= self.state.next_price:
                next_step = self.martin[self.state.index]
                self.state.total_money += self.martin[self.state.index]
                self.state.total_coin += (self.martin[self.state.index] / binance_info.close)
                self.state.next_price = self.state.next_price * (1 - self.parm.price_mul_factor)
                self.state.index += 1
            elif binance_info.close > (self.state.total_money / self.state.total_coin) * (1 + self.parm.profit):
                next_step = -1
                self.state.trade_state = 0
            elif self.state.index == len(self.martin) and binance_info.close <= self.state.next_price:
                next_step = -1
                self.state.trade_state = 0
        elif self.state.trade_state == 3:
            if self.state.index < len(self.martin) and binance_info.close >= self.state.next_price:
                next_step = -self.martin[self.state.index]
                self.state.total_money += self.martin[self.state.index]
                self.state.total_coin += (self.martin[self.state.index] / binance_info.close)
                self.state.next_price = self.state.next_price * (1 + self.parm.price_mul_factor)
                self.state.index += 1
            elif binance_info.close < (self.state.total_money / self.state.total_coin) * (1 - self.parm.profit):
                next_step = 1
                self.state.trade_state = 0
            elif self.state.index == len(self.martin) and binance_info.close >= self.state.next_price:
                next_step = 1
                self.state.trade_state = 0
        return next_step