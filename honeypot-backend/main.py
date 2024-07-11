from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import logging

from routers.router import router  # Ensure correct import
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware to check the referer
class RefererCheckMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        referer = request.headers.get('referer')
        origin = request.headers.get('origin')
        client_host = request.client.host
        client_port = request.client.port

        logger.info(f"Received request from {client_host}:{client_port}, Referer: {referer}, Origin: {origin}")

        if referer != "http://localhost:9000" and origin != "http://localhost:9000":
            logger.warning(f"Forbidden request from {client_host}:{client_port}")
            return JSONResponse(
                status_code=403,
                content={"detail": "Forbidden"},
            )

        response = await call_next(request)
        return response

app.add_middleware(RefererCheckMiddleware)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)
