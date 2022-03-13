import os
from backtesting import Backtest, Strategy
from backtesting import Strategy
import pandas as pd
from app.utils.util import data_loader
from app.utils.strategies import *
from app.schemas.base import *
from app.utils.config import configs
# TODO: require to finish flexible testing 
class TestStrategy(Strategy):
    max_num_trade = 9
    price_mul_factor = 0.02
    money_mul_factor = 1.4
    profit = 0.011

    def init(self):
        parm = MartinV1Parm(
            max_num_trade=self.max_num_trade,
            price_mul_factor=self.price_mul_factor,
            money_mul_factor=self.money_mul_factor,
            profit=self.profit
        )
        self.strategy = MartinV1(MartinV1State(), parm)
        self.martin_indicator = self.I(self._back_compute)
    
    def next(self):
        if self.martin_indicator[-1] == 1 or self.martin_indicator[-1] == -1:
            self.position.close()
        elif self.martin_indicator[-1] > 0:
            self.buy(size=self.martin_indicator[-1])
        elif self.martin_indicator[-1] < 0:
            self.sell(size=-self.martin_indicator[-1])
    
    def _back_compute(self) -> pd.Series:
        steps = []
        for i in range(len(self.data.Close)):
            binance_info = BinanceInfo(open=0,close=self.data.Close[i],high=0,low=0,volume=0)
            steps.append(self.strategy.next(binance_info))
        return pd.Series(steps)
def maximize(stats: pd.Series):
    #TODO
    # return stats["Return [%]"]
    return stats["Return [%]"] + stats["Max. Drawdown [%]"] * 12
if __name__ == "__main__":
    file_path = os.path.join(configs.DATA_PATH, configs.DATA_TYPE, configs.DATA_INTERVAL)
    data = data_loader(file_path)
    bt = Backtest(data, TestStrategy, commission=.0005,
                    exclusive_orders=False,
                    cash=5000000000)
                    
    stats = bt.run()
    # stats = bt.optimize(max_num_trade=range(3, 10, 1),
    #                     price_mul_factor=[0.02 + 0.005 * i for i in range(3)],
    #                     money_mul_factor=[1.1 + 0.1 * i for i in range(9)],
    #                     profit=[0.005 + 0.002 * i for i in range(5)],
    #                     maximize=maximize)
    print(stats)
    print(stats.tail())
    print(stats["Max. Drawdown [%]"])
    print(stats['_trades'])
    print(stats["_strategy"])
    print(stats["Return (Ann.) [%]"])
    bt.plot()