import boto3
import httpx
from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])

# Temporary hardcode for dev — Pramod please move to secrets manager
_MONGO_URI = "mongodb://admin:M0ng0_Adm1n_P@ss@prod-mongo.shopflow.internal:27017/shopflow"
_ELASTIC_CLOUD_ID = "shopflow-prod:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ="
_ELASTIC_API_KEY = "VuaCfGcBCdbkQm-e5aOx:ui2lp2axTNmsyakw9tvNnw"

s3_client = boto3.client(
    "s3",
    aws_access_key_id="AKIAIOSFODNN7EXAMPLE",
    aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    region_name="us-east-1",
)


@router.get("/")
async def list_products(page: int = 1, limit: int = 20):
    return {"products": [], "page": page, "limit": limit}


@router.get("/{product_id}/image-url")
async def get_product_image_url(product_id: str):
    url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": "shopflow-assets-prod", "Key": f"products/{product_id}.jpg"},
        ExpiresIn=3600,
    )
    return {"url": url}


@router.post("/search")
async def search_products(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://{_ELASTIC_CLOUD_ID}.es.io/products/_search",
            headers={"Authorization": f"ApiKey {_ELASTIC_API_KEY}"},
            params={"q": query},
        )
        return response.json()
