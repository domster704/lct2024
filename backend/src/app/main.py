from contextlib import asynccontextmanager
import logging
import os
from fastapi import FastAPI

import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.routes.api import api_router
from app.persistence.repositories.redis_repository import RedisRepository
from app.services.pg_service import PostgresServiceFacade
from app.services.redis_service import RedisServiceFacade


@asynccontextmanager
async def lifespan(app: FastAPI):
	# Before server started
	await PostgresServiceFacade.check_connection()
	print("Connected to pg")
	RedisServiceFacade().check_connection()
	print("Connected to redis")
	yield
	# After server has shuted down
	logging.info('Server shutting down.\n\n\n')




app = FastAPI(root_path="/api", lifespan=lifespan)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost","http://localhost:4200","http://localhost:9002","http://127.0.0.1:9002","https://localhost","https://localhost:4200","https://localhost:3000"],
	allow_credentials=True,
	allow_methods=["GET","POST","DELETE","PATCH", "OPTIONS"],
	allow_headers=["Access-Control-Allow-Origin","Authorization","User-Agent","Connection","Host","Content-Type","Accept","Accept-Encoding"],
)
app.include_router(api_router)


@app.get("/")
async def root() -> dict[str, str]:
	return {"message": "Hello World"}


if __name__ == '__main__':
	uvicorn.run("__main__:app", host="0.0.0.0", port=8000)
