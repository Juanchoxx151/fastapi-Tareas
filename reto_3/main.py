# En el práctico anterior dejamos un crud funcional en memoria, guardando datos en un diccionario. 
# Para este práctico vamos a seguir por las mismas líneas, pero agregando pydantic
# para la validación de tipos y restricciones. Para este tercer práctico será necesario 
# que me entreguen una aplicación de FastAPI con un crud en memoria que incluya:

# * Esquemas de pydantic para la estructura de los diccionarios (equivalente a la tabla en db).
# * Parámetros definidos con metadatos usando Annotated junto con Path() o Query(). 
#   Los mismos deben incluir restricciones (mayor que, longitud máxima, etc...).
# * Asimismo, los esquemas de pydantic también deben estar definidos con Annotated y usar Field().
# * Los endpoints que reciban id como parámetro de ruta (path()) deben levantar un HTTPException()
#   si no se encuentra coincidencia por id.
# * Finalmente, los path operations deben incluir un response_model y, si aplicase, un responses.

# Pueden trabajar a partir de lo que entregaron en el práctico anterior, sumandole todas estas features.
# La entrega será preferentemente por Github, en la medida de lo posible. Se usarán las horas de hoy (jueves) para realizar este práctico. Éxitos!!

from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.title = "Mi primera API"

app.add_middleware(
	CORSMiddleware,
	allow_origins=[
        "http://127.0.0.1:8000"
		"https://juanchoxx151.github.io/front",
    ],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

Ropa = [
    {"id": 1, "nombre": "Jean cargo", "precio": 2000, "activo": True},
    {"id": 2, "nombre": "Baggy", "precio": 3000, "activo": True},
    {"id": 3, "nombre": "Musculosa", "precio": 1500, "activo": True},
    {"id": 4, "nombre": "Remera con diseño", "precio": 2000, "activo": True},
    {"id": 5, "nombre": "Bermuda 3/4", "precio": 3000, "activo": True},
    {"id": 6, "nombre": "Buzo frizz", "precio": 1500, "activo": True},
    {"id": 7, "nombre": "Campera de cuero de hombre", "precio": 2000, "activo": True},
    {"id": 8, "nombre": "Blusa de mujer", "precio": 3000, "activo": True},
    {"id": 9, "nombre": "Remera de mujer", "precio": 1500, "activo": True},
    {"id": 10, "nombre": "Medias unisex", "precio": 2000, "activo": True},
    {"id": 11, "nombre": "Boxers", "precio": 3000, "activo": True},
    {"id": 12, "nombre": "Corpiños", "precio": 1500, "activo": True},
    {"id": 13, "nombre": "Zapatillas", "precio": 2000, "activo": True},
    {"id": 14, "nombre": "Camisas de varios colores", "precio": 3000, "activo": True},
    {"id": 15, "nombre": "Vaqueros", "precio": 1500, "activo": True},
    {"id": 16, "nombre": "pullover", "precio": 2000, "activo": True},
    {"id": 17, "nombre": "Gorros de invierno", "precio": 3000, "activo": True},
    {"id": 18, "nombre": "Remeras de fútbol", "precio": 1500, "activo": True}
]

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Artículo no encontrado",
                }
            }
        },
    },
}

CaracterRopa = Annotated[str, Field(max_length=50)]
PrecioVenta = Annotated[int, Field(gt=500, le= 10000)]
BoolActivo = Annotated[bool, Field(description= "¿Hay stock?")]
IdRopa = Annotated[int, Path(..., gt=0)]

class RopaSchema(BaseModel):
  id: Annotated[int, Field(gt=0, description="ID del articulo", deprecated=True)]
  nombre: CaracterRopa
  precio: PrecioVenta
  activo: BoolActivo = True

class ArticuloUpdateSchema(BaseModel):
    nombre: CaracterRopa
    precio: PrecioVenta
    activo: BoolActivo = True


@app.get("/Ropa", response_model=list[RopaSchema])
async def get_ropa():
	return Ropa

@app.get("/Ropa/{id}", responses=NOT_FOUND_RESPONSE, response_model=RopaSchema)
async def get_ropa_by_id(id: IdRopa):
	for r in Ropa:
		if r.get("id") == id:
			return r
	raise HTTPException(status_code=404, detail="No se encontró el ID de la ropa, intente con otro.")

@app.post("/Ropa", response_model=RopaSchema)
async def crear_ropa(nueva_ropa:RopaSchema):
	for r in Ropa:
		if r.get("id") == nueva_ropa.id:
			raise HTTPException(status_code=400, detail="Ese id ya está ocupado.")

	Ropa.append(nueva_ropa.model_dump())
	return nueva_ropa


@app.put("/Ropa/{id}", response_model=RopaSchema)
async def editar_ropa(
	id: IdRopa, 
	edit_ropa:ArticuloUpdateSchema):
	
	for ropa in Ropa:
		if ropa.get("id") == id:
			ropa["nombre"] = edit_ropa.nombre
			ropa["precio"] = edit_ropa.precio
			ropa["activo"] = edit_ropa.activo
			return ropa
	raise HTTPException(status_code=404, detail="El artículo no fue encontrado.")

@app.delete("/Ropa/{id}", responses=NOT_FOUND_RESPONSE)
async def borrar_ropa(id: IdRopa):
	for ropa in Ropa:
		if ropa.get("id") == id:
			Ropa.remove(ropa)
			return {"detail": "Artículo borrado correctamente."}
	raise HTTPException(status_code=404, detail="El artículo no existe.")