from fastapi import APIRouter
from db_config import DB
from fastapi import Depends, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from auth.utils import JWTBearer
from pypdf import PdfReader, PdfWriter 
import os
import tempfile

pdf_resizer_router = APIRouter(
    prefix="/pdf",
    tags=["auth"]
)

@pdf_resizer_router.post("/resize",  dependencies=[Depends(JWTBearer())])
def resize_pdf(file: UploadFile):
    

    if file.content_type != "application/pdf":
        return HTTPException(
            detail="Invalid file type",
            headers={"WWW-Authenticate": "Bearer"},
            status_code=status.HTTP_428_PRECONDITION_REQUIRED
        )
    
    temp_folder = tempfile.gettempdir()
    new_resize_name = "".join(file.filename.split(".")[:-1])+"_resize"+".pdf"


    resize_file_tmp_loc = os.path.join(temp_folder, new_resize_name)


    reader = PdfReader(file.file)
    writer = PdfWriter()

    for i in range(0, len(reader.pages)):

        page_1 = reader.pages[i]

        # get the height of the page
        height = page_1.cropbox.upper_right[1]
        width = page_1.cropbox.upper_right[0]

        page_1.cropbox.lower_left = (0,height - 3740)
        page_1.cropbox.lower_right = (width,height - 3740)

        writer.add_page(page_1)

        reader = PdfReader(file.file)
        page_2 = reader.pages[i]

        page_2.cropbox.upper_left = (0, height - 3740  + 1)
        page_2.cropbox.upper_right = (width, height - 3740  + 1)

        writer.add_page(page_2)


    with open(resize_file_tmp_loc, 'wb') as output_file:
        writer.write(output_file)

    response =  FileResponse(
        resize_file_tmp_loc,
        filename=new_resize_name
    )
    response.headers["Content-Type"] = "application/pdf"

    return response