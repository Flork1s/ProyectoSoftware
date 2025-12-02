from fastapi import APIRouter, UploadFile, File, HTTPException
from services.cloudinary_service import upload_image

upload_router = APIRouter()

@upload_router.post("/", response_model=dict)
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads an image to Cloudinary and returns the URL.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    image_url = upload_image(file)
    return {"url": image_url}
