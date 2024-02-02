from fastapi import FastAPI,HTTPException
from typing import Union
from funciones import developer
from funciones import *
from fastapi.responses import JSONResponse
from typing import List, Dict, Tuple, Sequence, Any, Union, Optional, Callable


app = FastAPI()

@app.get("/developer/{desarrollador}")
async def desarrollador(desarrollador:str):
    try:
        resultado = developer(desarrollador)
        return resultado
    except Exception as e:
        return {"error": str(e)} 
    
@app.get("/userdata/{User_id}")
async def User_id(User_id:str):
    try:
        resultado = userdata(User_id)
        return resultado
    except Exception as e:
        return {"error": str(e)} 
    
@app.get("/UserForGenre/{genero}")
async def genero(genero: str):
    try:
        user_and_hours = UserForGenre(genero)
        return user_and_hours
    except Exception as e:
        return {"error": str(e)}
        
@app.get("/best_developer_year/{año}")
async def Best_developer_year(year: int):
    try:
        year_int = int(year)  # Convertir el año a un entero
        result2 = best_developer_year(year_int)
        return result2
    except Exception as e:
        return {"error": str(e)}  

@app.get("/developer_reviews_analysis/{desarrolladora}") 
async def get_developer(desarrolladora: str):
    try:
        resultado= developer_reviews_analysis(desarrolladora)
        return resultado
    except Exception as e:
        return {"error":str(e)}


@app.get("/recomendacion_usuario/{user_id}")
async def get_recomendacion(user_id: str):
    try:
        resultado= recomendacion_usuario(user_id)
        return resultado
    except Exception as e:
        return {"error":str(e)}
    
    
@app.get("/recomendacion_juego/{item_id}")
def recomendacion_juego(item_id: int):
    try:
        recommended_games = recommend_games(item_id)
        return {"Recomendaciones": recommended_games}
    except HTTPException as e:
        return {"Error": e.detail}