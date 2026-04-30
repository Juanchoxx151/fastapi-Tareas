#Proyecto 2 - Negocio: Venta de ropa
from fastapi import FastAPI, Body, Path

Ropa = [
    {"id": 1, "nombre": "Jean cargo", "precio": 2000},
    {"id": 2, "nombre": "Baggy", "precio": 3000},
    {"id": 3, "nombre": "Musculosa", "precio": 1500},
    {"id": 4, "nombre": "Remera con diseño", "precio": 2000},
    {"id": 5, "nombre": "Bermuda 3/4", "precio": 3000},
    {"id": 6, "nombre": "Buzo frizz", "precio": 1500},
    {"id": 7, "nombre": "Campera de cuero de hombre", "precio": 2000},
    {"id": 8, "nombre": "Blusa de mujer", "precio": 3000},
    {"id": 9, "nombre": "Remera de mujer", "precio": 1500},
    {"id": 10, "nombre": "Medias unisex", "precio": 2000},
    {"id": 11, "nombre": "Boxers", "precio": 3000},
    {"id": 12, "nombre": "Corpiños", "precio": 1500},
    {"id": 13, "nombre": "Zapatillas", "precio": 2000},
    {"id": 14, "nombre": "Camisas de varios colores", "precio": 3000},
    {"id": 15, "nombre": "Vaqueros", "precio": 1500},
    {"id": 16, "nombre": "pullover", "precio": 2000},
    {"id": 17, "nombre": "Gorros de invierno", "precio": 3000},
    {"id": 18, "nombre": "Remeras de fútbol", "precio": 1500}
]


app = FastAPI()

@app.get("/Ropa")
async def get_ropa():
	return Ropa

@app.get("/Ropa/{id}")
async def get_ropa_by_id(id: int = Path(..., gt = 0)):
	for r in Ropa:
		if r.get("id") == id:
			return r
	return{"Error": "No se encontró el id de la ropa, vuelva a intentar."}

@app.post("/Ropa")
async def crear_ropa(id: int = Body(...), nombres: str = Body(...), precio: int = Body(..., ge = 100)):
	for r in Ropa:
		if r.get("id") == id:
			return{"Error": "Ese id ya está ocupado, intente con un id superior a ese número."}
	nueva_ropa = {
		"id": id,
		"nombre": nombres,
		"precio": precio
    }
	Ropa.append(nueva_ropa)
	return nueva_ropa


@app.put("/Ropa/{id}")
async def editar_ropa(id: int = Path(..., gt = 0), nombre: str = Body(..., max_length = 50), precio: int = Body(..., ge = 500)):
	for ropa in Ropa:
		if ropa.get("id") == id:
			ropa["nombre"] = nombre
			ropa["precio"] = precio
			return ropa
	return{"detail": "Not Found"}

@app.delete("/Ropa/{id}")
async def borrar_ropa(id: int = Path(..., gt = 0)):
	for ropa in Ropa:
		if ropa.get("id") == id:
			Ropa.remove(ropa)
			return {"detail": "Artículo borrado correctamente."}
		
	return {"Error": "Ese artículo ya no existe."}
