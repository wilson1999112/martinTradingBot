""" Schemas for the API """
from pydantic import BaseModel
from typing import Dict, List, Optional
class BalanceResult(BaseModel):
    """Balance Output Schemas"""
    result: float

class TradeResult(BaseModel):
    """Trade Output Schemas"""
    result: str

class BinanceInfo(BaseModel):
    """Binance price information"""
    open: float
    close: float
    high: float
    low: float
    volume: float

class MartinV1State(BaseModel):
    index: int = 0
    total_money:float = 0
    total_coin: float = 0
    next_price: float = 0

class MartinV1Parm(BaseModel):
    max_num_trade: int = 7
    price_mul_factor:float = 0.02
    money_mul_factor: float = 1.7
    profit: float = 0.013

class MartinV2State(BaseModel):
    index: int = 0
    total_money:float = 0
    total_coin: float = 0
    next_price: float = 0
    trade_state: int = 0
    start_sell_price: float = 0
    start_buy_price: float = 0

class MartinV2Parm(BaseModel):
    max_num_trade: int = 8
    price_mul_factor:float = 0.025
    money_mul_factor: float = 1.3
    profit: float = 0.004
    price_range: float = 0.01