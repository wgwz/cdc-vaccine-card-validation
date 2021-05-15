import base64
from pathlib import Path
import boto3


BYTES_PER_MB = 10 ** 6
MAX_MB = 10
client = boto3.client('textract')
path = Path("~/Downloads/").expanduser()


imgs = list(path.glob("*.jpg")) + list(path.glob("*.JPG"))
for img in sorted(imgs):
    img_raw = img.open("rb").read()
    img_bytes = bytearray(img_raw)
    img_size_mb = img.stat().st_size / BYTES_PER_MB
    if img_size_mb >= MAX_MB:
        print(f"Image: {img.name} is too large to process with AWS Textract")
        continue
    response = client.detect_document_text(
        Document={
            'Bytes': img_bytes,
        }
    )
    for block in response["Blocks"]:
        if block['BlockType'] == 'LINE' and block['Confidence'] > 90:
            if block["Text"] == "COVID-19 Vaccination Record Card":
                print(f"Image: {img.name} is Valid Vaccine Card")
                break
