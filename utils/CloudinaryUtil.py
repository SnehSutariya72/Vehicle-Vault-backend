import cloudinary
from cloudinary.uploader import upload

#cloundinary configuration
cloudinary.config(
    cloud_name = "dlehfwb2r",
    api_key="517235419466314",
    api_secret="mRvrUFBTFIbKGs87poGsMFKGQrk"
)

#util functionn...

async def upload_image(image):
    result = upload(image)
    print("cloundianry response,",result)
    return result["secure_url"] #string