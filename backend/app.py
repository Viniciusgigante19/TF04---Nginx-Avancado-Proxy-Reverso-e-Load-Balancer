from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_products():
    products = [
        {
            "id": 1,
            "name": "Camiseta Básica",
            "price": 49.90,
            "stock": 120
        },
        {
            "id": 2,
            "name": "Tênis Esportivo",
            "price": 199.90,
            "stock": 45
        },
        {
            "id": 3,
            "name": "Mochila Casual",
            "price": 89.90,
            "stock": 60
        },
        {
            "id": 4,
            "name": "Relógio Digital",
            "price": 149.90,
            "stock": 30
        }
    ]

    return {
        "status": "success",
        "total": len(products),
        "products": products
    }