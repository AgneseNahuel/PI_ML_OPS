Transformaciones:
	El primer error que me surgio fue la lectura de archivos .json, por alguna razon pandas no me funcionaba
termine optando por leer sin pandas, el encoding use "Latin" y como tuve que hacer movimientos por errores de librerias al
intentar instalarlas lo deje en "utf-8", ya sabia el numero de las primeras lineas que eran Nan, en el codigo pasado asique las borre nomas.
Luego de leer los archivos .json los elimine, tuve problemas con archivos que son grandes para subirlos al github y use TFS, no queria tener problemas

Hice transformaciones basicas, borrar columnas que no me servian (eso pensaba, tuve que volver a meter un .json para las variables dummies
en una API), que las columnas donde eran fechas que sean de tipo fecha, borrar nulos por columna para tenerlo mas controlado y renombrar columnas

En el ETL al final de todo codie un nuevo .csv para los generos, esto me va a ayudar mas adelante en la creacion de la funcion de API. Ya habia borrardo los
.json, toco volverlos para poder hacer esto.

Guarde todos los .csv en una carpeta llamada CSV...
--------------------------------------------------------------------------------

Feature Engineering:
	Con el "Sentiment_analysis" estaba usando otra libreria que no me daba llamada SentimentIntensityAnalyzer(), cambie muchas cosas y alfinal buscando con ChatGPT,
Google y compañeros me recomendaron TextBlob(), super facil de usar, hice una funcion y listo, esta en ETL.ipynb.
--------------------------------------------------------------------------------

Desarrollo API:
	La funcion  UserForGenre(), me hizo darme cuenta que necesitaba la columna de generos, tuve que volver a meter los .json y crear un csv que me ayude con variables dummies de los 
generos, las transformaciones estan en el archivo ETL. Las otras funciones me costaron pero les agarre la mano y manejar FastAPI es facil.
--------------------------------------------------------------------------------

Deployment: 
	Render nunca lo habia visto, me daba error no recuerdo que libreria, yo queria instalarla en mi entorno virtual, hasta que me di cuenta que podia borrarla del .txt, se me facilito 
la vida, tuve que sacar librerias porque tenia miedo que tarde mucho, deje bastante, pero saque otras, muchos nombres que nunca habia visto, pienso yo que el entorno instala muchas librerias 
por las dudas, deje algunas y me funcionaba bien. si funciona no lo toco...
--------------------------------------------------------------------------------

Análisis exploratorio de los datos:
	Lo hice antes que el Desarrollo de la API y el Deployment saque informacion basica estadistica, y despues me puse a experimentar con los graficos, si sigo con tiempo despues de terminar el proyecto
puede que busque mas informacion para que los graficos esten mas completos.
Los valores duplicados y nulos los elimine en el ETL.
--------------------------------------------------------------------------------

Modelo de aprendizaje automático:
	Intente primero hacer la primera, no me salio y fui por la segunda, tarde mucho en estudiar bien lo que me pedia..., que sea item-item, la similitud del coseno que use cosine_similarity()
en la funcion de recommend_games()
-----------------------------------------------------------------------------------	

		LINK GITHUB
https://github.com/AgneseNahuel/PI_ML_OPS

		LINK PAGINA RENDER
https://proyectoindividual-0dgz.onrender.com/docs

		LINK PAGINA DE YOUTUBE
https://www.youtube.com/watch?v=-hDX5ZSrDDs














