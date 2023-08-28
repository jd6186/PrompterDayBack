from fastapi import FastAPI, APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.core.dto.response_dto import ResponseDTO
from src.core.error.error_type_code import EXCEPTION_TYPE
from src.core.security import jwt_token_config
from src.core.util import http_util


############################## App & CORS Setting ##############################
app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi", redoc_url=None)
http_util.cors_setting(app, CORSMiddleware)


############################## Router 관리 ##############################
# API Health Check
@app.get("/api/health-check")
async def health_check():
    return "health check success"

# master router
master_router = APIRouter(
    prefix='/api',
    responses={404: {"description": "Page Not Found"}},
)
# my page router
guest_router = APIRouter(prefix='/guest')
user_router = APIRouter(prefix='/user', dependencies=[Depends(jwt_token_config.verify_token)])
http_util.router_setting(app, master_router, guest_router, user_router)


############################## Global Exception Handler ##############################
@app.exception_handler(HTTPException)
async def http_exception_handler(request, error_object):
    print(f"시스템 오류가 발생했습니다. Error status_code: {error_object.status_code}, Message : {error_object.detail}")
    dto = ResponseDTO(
        result_data="시스템 오류 발생",
        status_code=error_object.status_code,
        status_message=error_object.detail
    )
    return JSONResponse(
        content=dto.dict()
    )


@app.exception_handler(Exception)
async def global_exception_handler(request, error_object):
    print(f"예상하지 못한 오류가 발생했습니다.")
    dto = ResponseDTO(
        result_data="시스템 오류 발생",
        status_code=EXCEPTION_TYPE.ERROR_500.value["code"],
        status_message=EXCEPTION_TYPE.ERROR_500.value["message"]
    )
    return JSONResponse(
        content=dto.dict()
    )



############################## Filter ##############################
@app.middleware("http")
async def application_filter(request: Request, call_next):
    http_util.url_routing_check(request)
    response = await call_next(request)
    return response
