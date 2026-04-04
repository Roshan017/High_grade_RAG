from fastapi import FastAPI
from api.routes.doc_upload import router as doc_upload_router

app = FastAPI()

app.include_router(doc_upload_router, prefix='/api')

