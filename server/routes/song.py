import cloudinary.uploader
from fastapi import HTTPException, Depends, APIRouter, Form, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from database import get_db
from middleware.auth_middleware import auth_middleware
import cloudinary
import uuid
from models.song import Song
from config import settings
from pydantic_schemas.favourite_song import FavouriteSong
from models.favourites import Favourite

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

@router.post("/favourite")
def favourite_songs(song: FavouriteSong,
                    db: Session = Depends(get_db),
                    auth_dict=Depends(auth_middleware)):
    # get user id from auth_dict
    user_id = auth_dict["uid"]
    # check if song already exists in favourites
    existing_fav = db.query(Favourite).filter(Favourite.song_id == song.song_id, Favourite.user_id == user_id).first()
    if existing_fav:
        db.delete(existing_fav)
        db.commit()
        return {"message": False}
    # if not, add to favourites
    else:
        new_fav = Favourite(id = str(uuid.uuid4()), user_id=user_id, song_id=song.song_id)
        db.add(new_fav)
        db.commit()
        return {"message": True}
    
@router.get("/list/favourites")
def list_fav_songs(db: Session = Depends(get_db),
               auth_dict=Depends(auth_middleware)):
    user_id = auth_dict["uid"]
    fav_songs = db.query(Favourite).filter(Favourite.user_id == user_id).options(
        joinedload(Favourite.song),
        joinedload(Favourite.user)
    ).all()
    if not fav_songs:
        return {"message": "No favourite songs found."}
    return fav_songs