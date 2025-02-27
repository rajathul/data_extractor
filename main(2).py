from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import tempfile
import os
import io
from fastapi.responses import StreamingResponse

from extract_text import extract_text
from validation_check import is_valid_document
from extract_info import extract_info
from save_data import save_to_csv, save_to_txt


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract/")
async def extract_pdf(file: UploadFile = File(...)):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        # Write the uploaded file content to the temp file
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name
    
    try:
        # Extract text from PDF using your existing function
        document = extract_text(temp_path)
        
        # Validate the document
        status, document_type, message = is_valid_document(document)
        
        if not status:
            # Clean up the temp file
            os.unlink(temp_path)
            return {"error": message, "document_type": document_type}
        
        # Extract information from the document
        info = extract_info(document)
        
        # Convert dictionary to DataFrame for table display
        df = pd.DataFrame(list(info.items()), columns=["Field", "Value"])
        
        # Clean up the temp file
        os.unlink(temp_path)
        
        return {
            "data": {
                "Field": df["Field"].tolist(),
                "Value": df["Value"].tolist()
            },
            "columns": ["Field", "Value"],
            "document_type": document_type,
            "message": message
        }
    except Exception as e:
        # Clean up the temp file
        os.unlink(temp_path)
        return {"error": str(e)}

@app.post("/download/")
async def download_excel(file: UploadFile = File(...)):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        # Write the uploaded file content to the temp file
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name
    
    try:
        # Extract text from PDF
        document = extract_text(temp_path)
        
        # Validate the document
        status, document_type, message = is_valid_document(document)
        
        if not status:
            # Clean up the temp file
            os.unlink(temp_path)
            raise HTTPException(status_code=400, detail=message)
        
        # Extract information from the document
        info = extract_info(document)
        
        # Convert to DataFrame for Excel
        df = pd.DataFrame(list(info.items()), columns=["Field", "Value"])
        
        # Convert DataFrame to Excel
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        
        # Clean up the temp file
        os.unlink(temp_path)
        
        # Return Excel file as a downloadable response
        return StreamingResponse(
            excel_buffer, 
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=loan_details.xlsx"}
        )
    except Exception as e:
        # Clean up the temp file
        os.unlink(temp_path)
        return {"error": str(e)}

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

# Run with: uvicorn main:app --reload