"""Router for Development"""
from fastapi import APIRouter
from app.schemas.base import BalanceResult, TradeResult
from app.core.binance_api import binance_handler
from app.utils.logging import logger
router = APIRouter()

@router.get("/search/balance", response_model=BalanceResult)
def search_balance() -> BalanceResult:
    """
    Get balance of my account

    Returns:
     - **BalanceResult**: balance result.
    """
    logger.info("Get balance of my account")
    return BalanceResult(result=binance_handler.search_balance())

@router.get("/trade", response_model=TradeResult)
def trade() -> TradeResult:
    """
    make a trade

    # TODO
    Returns:
     - **TradeResult**: trade result.
    """
    logger.info("try to make a trade")
    binance_handler.trade()
    return TradeResult(result='ok')