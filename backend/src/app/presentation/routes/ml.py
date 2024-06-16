import io
from typing import Any
from fastapi.responses import StreamingResponse
import requests
from fastapi import APIRouter, Depends, HTTPException, Request, status

from urllib.parse import quote

from app.shared.config import SERVER_SETTINGS
from app.shared.logger import logger
from app.shared.jwt import JWT


router = APIRouter(prefix="/search")

@router.get("/catalog",
			dependencies=[Depends(JWT.check_access_token)],
			response_model= dict[str, Any],
			summary="Get references to the search query")
async def catalog(prompt: str, *, request: Request) -> dict[str, Any]:
	if not (payload := request.state.token_payload):
		raise HTTPException(500, "Can't find token payload")

	try:
		result = requests.get(f"{SERVER_SETTINGS.ml_uri}/v1/ml/matching/show_reference", params={"prompt": prompt,
																								 "user_id": payload.user_id}).json()

		logger.debug(f"Refereces result: {result}")
		print(f"Refereces result: {result}")

		if "values" in result.keys():
			answer = {prompt: result["values"]}
		else:
			answer = {prompt: []}

		return answer
	except HTTPException as http_err:
		raise http_err
	except Exception as err:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
							detail=err)


@router.get("/remnants_references",
			summary="Remnants of similar products")
async def remnants_references(user_pick: str):
	try:
		result = requests.get(f"{SERVER_SETTINGS.ml_uri}/v1/ml/return_leftovers", params={"user_pick": user_pick}).json()

		logger.debug(f"Refereces result: {result}")
		print(f"Refereces result: {result}")

		return result
	except HTTPException as http_err:
		raise http_err
	except Exception as err:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
							detail=err)


@router.get("/regular",
			summary="Check if purchase is regular")
async def is_regular(user_pick: str):
	try:
		result = requests.get(f"{SERVER_SETTINGS.ml_uri}/v1/ml/check_regular", params={"user_pick": user_pick}).json()

		logger.debug(f"Refereces result: {result}")
		print(f"Refereces result: {result}")

		return result
	except HTTPException as http_err:
		raise http_err
	except Exception as err:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
							detail=err)


@router.get("/purchases_history",
			summary="History of goods purchase")
async def purchases_history(user_pick: str):
	logger.debug(f"query: {user_pick}")
	try:
		result = requests.get(f"{SERVER_SETTINGS.ml_uri}/v1/ml/get_history", params={"user_pick": user_pick})

		print(result.status_code, result.content)

		if result.status_code == 200:
			encoded_filename = quote(f'{user_pick}_history.xlsx')
			return StreamingResponse(
				io.BytesIO(result.content),
				media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
				headers={'Content-Disposition': f'attachment; filename={encoded_filename}; filename*=UTF-8\'\'{encoded_filename}'}

			)
		else:
			raise HTTPException(result.status_code, result.content)

	except HTTPException as http_err:
		raise http_err
	except Exception as err:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
							detail=err)
