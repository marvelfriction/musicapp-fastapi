from fastapi import HTTPException, Depends, APIRouter

router = APIRouter()

@router.post("/upload", status_code=201)
def upload_song():
    pass