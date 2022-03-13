"""app server start here"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.utils.logging import logger
from app.routes.bot import router
from app.core.errors.exception import UserInputError
from app.core.binance_api import binance_handler
from fastapi_utils.tasks import repeat_every
from datetime import datetime
from time import time 
def create_app():

    main_app = FastAPI()

    main_app.include_router(router, tags=["Binance"])
    return main_app

app = create_app()
@app.exception_handler(UserInputError)
async def user_input_exception_handler(request: Request, exc: UserInputError):
    return JSONResponse(
        status_code=406,
        content={"error": exc.err},
    )

@app.on_event("startup")
@repeat_every(seconds=60, logger=logger)
def periodic():
    cur = datetime.fromtimestamp(time())
    if cur.hour % 4 == 0 and cur.minute == 0:
        try:
            global binance_handler
            binance_handler.trade()
            logger.info("trade OK")
        except Exception as e:
            logger.exception("trade fail")