from fastapi import FastAPI
from Tracker.Routes import trans_router, cat_router

main_app = FastAPI()

main_app.include_router(trans_router,prefix="/transactions")
main_app.include_router(cat_router,prefix="/transactions")