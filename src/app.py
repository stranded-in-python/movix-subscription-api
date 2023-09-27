from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import account, account_payment, billing_webhooks, subscriptions, tariff
from core.config import settings

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


app.include_router(
    billing_webhooks.router, prefix="/api/v1", tags=["Webhooks", "Billing"]
)
app.include_router(subscriptions.router, prefix="/api/v1", tags=["Subscription"])
app.include_router(account.router, prefix="/api/v1", tags=["Account"])
app.include_router(
    account_payment.router, prefix="/api/v1", tags=["Account", "Payment"]
)
app.include_router(tariff.router, prefix="/api/v1", tags=["Subscription", "Tariff"])
