from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int

class ProductToRemove(BaseModel):
    id: int
    name: str

products = [
    {"id": 1, "name": "Camiseta Básica", "price": 49.90, "stock": 120},
    {"id": 2, "name": "Tênis Esportivo", "price": 199.90, "stock": 45},
    {"id": 3, "name": "Mochila Casual", "price": 89.90, "stock": 60},
    {"id": 4, "name": "Relógio Digital", "price": 149.90, "stock": 30}
]
next_id = 5

@app.get("/health")
def amIhealth():
    return {"ok": True}

@app.get("/products")
def get_products():
    return {"products": products}

@app.post("/products")
def add_products(product: Product):
    global next_id
    product.id = next_id
    next_id += 1
    products.append(product.dict())
    return {"message": f"Produto {product.name} cadastrado!"}

@app.delete("/products")
def remove_products(product: ProductToRemove):
    global products
    products = [p for p in products if p["id"] != product.id]
    return {"message": f"Produto {product.name} removido!"}