from fastapi import FastAPI
from api.routes.doc_upload import router as doc_upload_router
from api.routes.user_query import router as user_query_router

app = FastAPI()

app.include_router(doc_upload_router, prefix='/api')
app.include_router(user_query_router, prefix='/api')

