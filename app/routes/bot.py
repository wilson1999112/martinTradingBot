"""Router for Development"""
from fastapi import APIRouter
from app.schemas.base import BalanceResult
from app.core.binance_api import binance_handler
from app.utils.logging import logger
router = APIRouter()

# TODO
@router.get("/search/balance", response_model=BalanceResult)
def search_balance() -> BalanceResult:
    """
    Get balance of my account

    Returns:
     - **BalanceResult**: balance result.
    """
    logger.info("Get balance of my account")
    return BalanceResult(result=binance_handler.search_balance())