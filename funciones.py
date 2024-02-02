import pandas as pd
import fastapi
from fastapi import FastAPI, HTTPException
import pyarrow.csv as pq
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

games = pd.read_csv("games.csv")
df_reviews = pd.read_csv("user_reviews.csv")
df_items = pd.read_csv("user_items.csv")
data_steam = pd.read_csv("data_steam.csv")

#1
def developer(desarrollador: str): 
    resultado = []

    # Filtrar el DataFrame por el desarrollador especificado
    df_desarrollador = games[games["developer"] == desarrollador]

    # Obtener la lista única de años
    años = df_desarrollador["release_date"].unique()

    for año in años:
        # Filtrar por año
        df_año = df_desarrollador[df_desarrollador["release_date"] == año]

        # Calcular la cantidad de juegos lanzados en ese año
        cantidad_juegos = len(df_año)

        # Calcular el porcentaje de juegos gratuitos
        porcentaje_gratuito = (df_año["price"] == 0).mean() * 100 if cantidad_juegos > 0 else 0

        # Almacenar resultados en el diccionario
        resultado.append({
            "año": int(año),
            "cantidad_juegos": cantidad_juegos,
            "porcentaje_gratuito": porcentaje_gratuito
        })

    # Ordenar los resultados por año
    resultado = sorted(resultado, key=lambda x: x["año"])

    return resultado

#2
def userdata(user_id: str):
    resultado = {}

    # Filtrar df_reviews por el user_id especificado
    df_usuario = df_reviews[df_reviews["user_id"] == user_id]

    # Calcular el dinero gastado por el usuario
    dinero_gastado = df_usuario.merge(games, on="item_id")["price"].sum()

    # Calcular el porcentaje de recomendación
    porcentaje_recomendacion = (df_usuario["recommend"].mean() * 100) if not df_usuario.empty else 0

    # Calcular la cantidad de items
    cantidad_items = len(df_usuario)

    # Almacenar resultados en el diccionario
    resultado["Usuario"] = user_id
    resultado["Dinero gastado"] = f"{dinero_gastado} USD"
    resultado["% de recomendación"] = f"{porcentaje_recomendacion}%"
    resultado["Cantidad de items"] = cantidad_items

    return resultado
    
    
#No funciona y crashea todo
"""def UserForGenre(genero: str):

    if genero not in games.columns:
        return {"error": f"'{genero}' no es un género válido"}
    
    resultado = {}

    # Filtrar df_reviews por el género especificado
    df_genero = df_reviews.merge(games[games[genero] == 1], on="item_id")
    
    # Fusionar con df_items para obtener el tiempo jugado
    df_genero = df_genero.merge(df_items, on="item_id", how="inner", suffixes=('reviews', 'items'))

    # Encontrar el usuario con más horas jugadas para el género
    usuario_mas_horas = df_genero.groupby("user_id")["playtime_forever"].sum().idxmax()

    # Obtener las horas jugadas por año
    horas_por_año = df_genero.groupby("año_lanzamiento")["playtime_forever"].sum().reset_index()
    horas_por_año = [{"Año": int(año), "Horas": horas} for año, horas in zip(horas_por_año["año_lanzamiento"], horas_por_año["playtime_forever"])]

    # Almacenar resultados en el diccionario
    resultado["Usuario con más horas jugadas para Género X"] = usuario_mas_horas
    resultado["Horas jugadas"] = horas_por_año
    
    return resultado"""
    

#4-------------------------------------------------------------------------------------------------------------
def best_developer_year(año: int):
    # Realizar la unión de los DataFrames
    merged_df = pd.merge(df_reviews, games, on='item_id')
    if año not in merged_df['release_date'].unique():
        return {'error': 'El año especificado no existe.'}

    # Filtrar los juegos por año y por recomendación positiva
    df_year = merged_df[(merged_df['release_date'] == año) & (merged_df['recommend'] == True) & (merged_df['sentiment_analysis'] == 2)]

    # Contar el número de juegos recomendados por desarrollador y devolver los tres primeros desarrolladores
    top_desarrolladores = df_year['developer'].value_counts().head(3).index.tolist()

     # Devolver el top 3 de desarrolladores
    return {"Puesto 1" : top_desarrolladores[0], "Puesto 2" : top_desarrolladores[1], "Puesto 3" : top_desarrolladores[2]}


#5------------------------------------------------------------------------------------------------------------
merged = df_reviews.merge(games[['item_id', 'price',"developer"]], on='item_id')

def developer_reviews_analysis(desarrolladora:str):
    if desarrolladora not in games['developer'].unique():
        return {'error': 'El Desarrollador especificado no existe.'}
    
    #filtrar las columnas a utilizar 
    df = merged[['user_id', 'item_id','developer','year_posted','sentiment_analysis']] 
    #filtrar los datos por desarrolladora
    df_merged = df[df["developer"] == desarrolladora] 

    # Se obtienen la cantidad de reviews positivas y negativas
    reviews_positivas = df_merged[df_merged["sentiment_analysis"] == 2].shape[0] 
    reviews_negativas = df_merged[df_merged["sentiment_analysis"] == 0].shape[0]

    # Se crea un string con el resumen de las reviews
    resumen_reviews = f"[Negative = {reviews_negativas}, Positive = {reviews_positivas}]" 
    # Se crea un diccionario con los resultados obtenidos
    dicc = {desarrolladora : resumen_reviews} 

    # Se devuelve un diccionario con los resultados obtenidos
    return dicc
 

#ML MODELOS---------------------------------------------------------------------------------------------------
def recomendacion_usuario(id_usuario):
    
    #Seleccionar características (X) y la etiqueta (y)
    X = data_steam[['item_id', 'release_date', 'price', 'sentiment_analysis', 'playtime_forever']]
    y = data_steam['recommend']

    #Divide el conjunto de datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #Crea y entrena el modelo
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    
    #------------------------------------------------------------------------------------------------------
    
    # Verifica si el usuario existe en el conjunto de datos
    if id_usuario not in data_steam['user_id'].values:
        print(f'El usuario {id_usuario} no existe en el conjunto de datos.')
        return None

    # Filtra el conjunto de datos para obtener las características de juegos no etiquetados para el usuario
    juegos_sin_etiqueta = data_steam[data_steam['user_id'] == id_usuario][['item_id', 'release_date', 'price', 'sentiment_analysis', 'playtime_forever']]

    # Asegúrate de que haya al menos un juego sin etiquetar para el usuario
    if juegos_sin_etiqueta.empty:
        print(f'No hay juegos sin etiquetar para el usuario {id_usuario}.')
        return None

    # Utiliza el modelo entrenado para predecir las preferencias del usuario para los juegos sin etiquetar
    preferencias_usuario = modelo.predict(juegos_sin_etiqueta)

    # Combina las predicciones con la información del juego y selecciona los 5 mejores
    juegos_sin_etiqueta['recommend'] = preferencias_usuario
    juegos_recomendados = juegos_sin_etiqueta.sort_values(by='recommend', ascending=False).head(5)

    # Realiza una fusión con el conjunto de datos original para obtener el nombre del juego
    juegos_recomendados = pd.merge(juegos_recomendados, data_steam[['item_id', 'title']], on='item_id', how='left')

    # Elimina duplicados basados en 'App_name'
    juegos_recomendados = juegos_recomendados.drop_duplicates(subset='title')

    # Reinicia el índice y luego incrementa en 1
    juegos_recomendados.reset_index(drop=True, inplace=True)
    juegos_recomendados.index += 1
    
    # Suponiendo que 'juegos_recomendados' es un DataFrame con las columnas mencionadas
    datos_dict = juegos_recomendados[['title', 'release_date', 'price', 'sentiment_analysis', 'recommend', 'playtime_forever']].to_dict(orient='records')

    return datos_dict

    

def recommend_games(item_id):
    # se carga los datasets que se va a utilizar para dos dataframes distintos
    data = pd.read_csv('juegos_steam.csv')
    data_juegos_steam = pd.read_csv('juegos_id.csv')

    # crear una matriz de características de los juegos
    tfidv = TfidfVectorizer(min_df=2, max_df=0.7, token_pattern=r'\b[a-zA-Z0-9]\w+\b')
    data_vector = tfidv.fit_transform(data['features'])

    data_vector_df = pd.DataFrame(data_vector.toarray(), index=data['item_id'], columns = tfidv.get_feature_names_out())

    # calcular la similitud coseno entre los juegos en la matriz de características
    vector_similitud_coseno = cosine_similarity(data_vector_df.values)

    cos_sim_df = pd.DataFrame(vector_similitud_coseno, index=data_vector_df.index, columns=data_vector_df.index)

    juego_simil = cos_sim_df.loc[item_id]

    simil_ordenada = juego_simil.sort_values(ascending=False)
    resultado = simil_ordenada.head(6).reset_index()

    result_df = resultado.merge(data_juegos_steam, on='item_id',how='left')

    # La función devuelve una lista de los 6 juegos más similares al juego dado
    juego_title = data_juegos_steam[data_juegos_steam['item_id'] == item_id]['title'].values[0]

    # mensaje que indica el juego original y los juegos recomendados
    mensaje = f"Si te gustó el juego {item_id} : {juego_title}, también te pueden gustar:"

    result_dict = {
        'mensaje': mensaje,
        'juegos recomendados': result_df['title'][1:6].tolist()
    }

    return result_dict