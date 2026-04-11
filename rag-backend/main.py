from fastapi import FastAPI
from api.routes.doc_upload import router as doc_upload_router
from api.routes.user_query import router as user_query_router
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from llm.langfuse import init_langfuse

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_langfuse()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(doc_upload_router, prefix='/api')
app.include_router(user_query_router, prefix='/api')

