from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from models import Order


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error((exc.errors(), exc.body))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.post("/discounts/")
async def discounts(order: Order):
    """ Do some custom discount logic there """
    return JSONResponse(
        content=jsonable_encoder({
            "discount": 0,
            "discount_type": "MONEY",
            "title": "Это сообщение будет отображено в корзине"
        }), status_code=200, headers={'Content-Type': 'application/json; charset=utf-8'}
    )
