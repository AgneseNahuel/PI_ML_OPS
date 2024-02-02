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
















