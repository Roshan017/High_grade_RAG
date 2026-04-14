from fastapi import FastAPI
from api.routes.doc_upload import router as doc_upload_router
from api.routes.user_query import router as user_query_router
from api.routes.auth import router as auth_router
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from llm.langfuse import init_langfuse
from api.routes.ragas_analysis import router as ragas_analysis_router

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_langfuse()
    yield

app = FastAPI(lifespan=lifespan)

# Add CORS Middleware to allow frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with the exact frontend domain (e.g. https://my-frontend.com)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import Depends
from api.middlewares.Get_user import get_current_user

app.include_router(auth_router, prefix='/api/auth')
app.include_router(doc_upload_router, prefix='/api', dependencies=[Depends(get_current_user)])
app.include_router(user_query_router, prefix='/api', dependencies=[Depends(get_current_user)])
app.include_router(ragas_analysis_router, prefix='/api', dependencies=[Depends(get_current_user)])
