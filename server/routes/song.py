import cloudinary.uploader
from fastapi import HTTPException, Depends, APIRouter, Form, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import auth_middleware
import cloudinary
import uuid
from models.song import Song
from config import settings

router = APIRouter()

cloudinary.config( 
    cloud_name = settings.cloudinary_cloud_name,
    api_key = settings.cloudinary_api_key, 
    api_secret = settings.cloudinary_api_secret,
    secure=True
)

@router.post("/upload", status_code=201)
def upload_song(song: UploadFile = File(...),
                thumbnail: UploadFile = File(...),
                artist: str = Form(...),
                song_name: str = Form(...),
                hex_code: str = Form(...),
                db: Session = Depends(get_db),
                auth_dict=Depends(auth_middleware)):
    
    try:
        song_id = str(uuid.uuid4())
        song_res = cloudinary.uploader.upload(song.file, resource_type="auto", folder=f"songs/{song_id}")
        thumbnail_res = cloudinary.uploader.upload(thumbnail.file, resource_type="image", folder=f"songs/{song_id}")
        # store in db
        new_song = Song(id=song_id,
                        song_url= song_res["url"],
                        thumbnail_url= thumbnail_res["url"],
                        artist=artist,
                        song_name=song_name,
                        hex_code=hex_code)
        db.add(new_song)
        db.commit()
        db.refresh(new_song)
        return new_song
    
    except Exception as e:
        raise HTTPException(400, f"Error uploading song: {str(e)}")

@router.get("/list")
def list_songs(db: Session = Depends(get_db),
               auth_dict=Depends(auth_middleware)):
    songs = db.query(Song).all()
    return songs