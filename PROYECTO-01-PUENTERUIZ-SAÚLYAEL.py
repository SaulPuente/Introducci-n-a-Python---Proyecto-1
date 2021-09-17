import lifestore_file as LSF
import pandas as pd
import os

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

"""
This is the LifeStore_SalesList data:

lifestore_searches = [id_search, id product]
lifestore_sales = [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)]
lifestore_products = [id_product, name, price, category, stock]
"""
# Vamos a importar las listas de datos del archivo 'lifestore_file'
products = LSF.lifestore_products
sales = LSF.lifestore_sales
searches = LSF.lifestore_searches




# Sólo nos interesan las ventas en el año 2020, así que eliminamos las demás

def limpieza(año):
    global sales
    año = str(año)
    ventas = sales.copy()

    for venta in ventas:
        venta[3] = venta[3].split("/")

    i = 0
    n = len(sales)
    while i < n:
        if ventas[i][3][2] != año:
            ventas.pop(i)
            sales.pop(i)
            i -= 1
            n = len(sales)
        i += 1
    return ventas

# Definimos una función que toma el n-esimo elemento de una lista
# Nos será útil para ordenar las listas más adelante

# 1.- Productos más vendidos y productos rezagados

def ventasPorProducto(products, sales):
    # Creamos una lista con las ventas por producto
    ventas_por_producto = [[i+1,0,0] for i in range(len(products))]

    # Contamos las ventas que obtuvo cada producto
    i = 1
    for sale in sales:
        while sale[1] != i:
            i += 1
        ventas_por_producto[i-1][1] += 1
        if sale[3] == 1:
            ventas_por_producto[i-1][2] += 1
    # Ordenamos la lista usando la función previamente definida
    ventas_por_producto.sort(key = lambda x: x[1], reverse = True)
    
    return ventas_por_producto



# Repetimos el proceso anterior, pero ahora para el caso de las búsquedas

def busquedasPorProducto(products,searches):
    # Creamos una lista con las búsquedas por producto
    busquedas_por_producto = [[i+1,0] for i in range(len(products))]

    # Contamos las búsquedas que obtuvo cada producto
    i = 1
    for search in searches:
        while search[1] != i:
            i += 1
        busquedas_por_producto[i-1][1] += 1
    # Ordenamos la lista usando la función previamente definida
    busquedas_por_producto.sort(key = lambda x: x[1], reverse = True)
    
    return busquedas_por_producto



def imprimirProductosPorVentas(ventas_por_producto):
    pd.options.display.max_colwidth = 70 #-------------------

    print("\n Productos más vendidos\n")
    # Obtenemos el nombre da cada uno de los primeros productos y los guardamos en una lista
    productosMasVendidos = [[ventas_por_producto[i][0],products[ventas_por_producto[i][0]-1][1],ventas_por_producto[i][1]] for i in range(10)]
    # Le damos formato de tabla a la lista
    productosMasVendidos = pd.DataFrame(productosMasVendidos)
    productosMasVendidos.columns = ["ID","Productos","Ventas"]
    productosMasVendidos = productosMasVendidos.set_index("ID")
    # Imprimmos
    print(productosMasVendidos)
    # Guardamos el dataframe en un archivo csv
    productosMasVendidos.to_csv("productosMasVendidos.csv")
    
    print("\n Productos menos vendidos\n")
    # Obtenemos el nombre da cada uno de los últimos productos y los guardamos en una lista
    productosMenosVendidos = [[ventas_por_producto[i][0],products[ventas_por_producto[i][0]-1][1],ventas_por_producto[i][1]] for i in range(-1,-11,-1)]
    # Le damos formato de tabla a la lista
    productosMenosVendidos = pd.DataFrame(productosMenosVendidos)
    productosMenosVendidos.columns = ["ID","Productos","Ventas"]
    productosMenosVendidos = productosMenosVendidos.set_index("ID")
    # Imprimmos
    print(productosMenosVendidos)
    # Guardamos el dataframe en un archivo csv
    productosMenosVendidos.to_csv("productosMenosVendidos.csv", encoding='utf-8')


    
def imprimirProductosPorBusquedas(busquedas_por_producto):
    pd.options.display.max_colwidth = 70 #-------------------
    
    
    print("\n Productos más buscados\n")
    # Obtenemos el nombre da cada uno de los últimos productos y los guardamos en una lista
    productosMasBuscados = [[busquedas_por_producto[i][0],products[busquedas_por_producto[i][0]-1][1],busquedas_por_producto[i][1]] for i in range(10)]
    # Le damos formato de tabla a la lista
    productosMasBuscados= pd.DataFrame(productosMasBuscados)
    productosMasBuscados.columns = ["ID","Producto","Busquedas"]
    productosMasBuscados = productosMasBuscados.set_index("ID")
    # Imprimmos
    print(productosMasBuscados)
    # Guardamos el dataframe en un archivo csv
    productosMasBuscados.to_csv("productosMasBuscados.csv")
    
    print("\n Productos menos buscados\n")
    # Obtenemos el nombre da cada uno de los últimos productos y los guardamos en una lista
    productosMenosBuscados = [[busquedas_por_producto[i][0],products[busquedas_por_producto[i][0]-1][1],busquedas_por_producto[i][1]] for i in range(-1,-11,-1)]
    # Le damos formato de tabla a la lista
    productosMenosBuscados = pd.DataFrame(productosMenosBuscados)
    productosMenosBuscados.columns = ["ID","Producto","Busquedas"]
    productosMenosBuscados = productosMenosBuscados.set_index("ID")
    # Imprimmos
    print(productosMenosBuscados)
    # Guardamos el dataframe en un archivo csv
    productosMenosBuscados.to_csv("productosMenosBuscados.csv")
    



# 2.- Productos por reseña en el servicio

def reseñasPorProducto(products, sales):
    # Creamos una lista con las ventas por producto
    reseñas_por_producto = [[i+1,0] for i in range(len(products))]

    # Contamos las ventas que obtuvo cada producto y obtenemos el promedio de calificación que recibió cada uno
    i = 1
    n = 0
    for sale in sales:
        while sale[1] != i:
            if n != 0:
                reseñas_por_producto[i-1][1] = round(reseñas_por_producto[i-1][1]/n,2)
      
            n = 0
            i += 1
        reseñas_por_producto[i-1][1] += sale[2]
        n += 1
    # Ordenamos la lista usando la función previamente definida
    reseñas_por_producto.sort(key = lambda x: x[1], reverse = True)
    
    return reseñas_por_producto



def imprimirProductosPorReseñas(reseñas_por_producto):
    pd.options.display.max_colwidth = 70 #-------------------
    
    print("\n Productos mejor calificados\n")   
    # Obtenemos el nombre da cada uno de los primeros productos y los guardamos en una lista
    productosMejorCalificados = [[reseñas_por_producto[i][0],products[reseñas_por_producto[i][0]-1][1],reseñas_por_producto[i][1]] for i in range(20)]
    # Le damos formato de tabla a la lista
    productosMejorCalificados = pd.DataFrame(productosMejorCalificados)
    productosMejorCalificados.columns = ["ID","Productos","Calificación"]
    productosMejorCalificados = productosMejorCalificados.set_index("ID")
    # Imprimmos
    print(productosMejorCalificados)
    # Guardamos el dataframe en un archivo csv
    productosMejorCalificados.to_csv("productosMejorCalificados.csv")
    
    print("\n Productos peor calificados\n")
    # Obtenemos el nombre da cada uno de los últimos productos y los guardamos en una lista
    productosPeorCalificados = [[reseñas_por_producto[i][0],products[reseñas_por_producto[i][0]-1][1],reseñas_por_producto[i][1]] for i in range(-1,-21,-1)]
    # Le damos formato de tabla a la lista
    productosPeorCalificados = pd.DataFrame(productosPeorCalificados)
    productosPeorCalificados.columns = ["ID","Productos","Calificación"]
    productosPeorCalificados = productosPeorCalificados.set_index("ID")
    # Imprimmos
    print(productosPeorCalificados)
    # Guardamos el dataframe en un archivo csv
    productosPeorCalificados.to_csv("productosPeorCalificados.csv")



# 3.- Total de ingresos y ventas promedio mensuales, total anual y meses con más ventas al año

def obtenerVentasAnuales(ventas):
    # Ordenamos las ventas por año
    ventas.sort(key = lambda x: x[3][2])
            
    ventas_anuales = []
    venta_anual = []
    año = ventas[0][3][2]
    
    # Iteramos las ventas y agrupamos por año
    for venta in ventas:
        if venta[3][2] != año:
            ventas_anuales.append(venta_anual)
            venta_anual = []
            año = venta[3][2]
        venta_anual.append(venta)
    ventas_anuales.append(venta_anual)

    del(venta_anual)
    # Ordenamos las ventas en cada año por mes
    for venta_anual in ventas_anuales:
        venta_anual.sort(key = lambda x: x[3][1])
    return ventas_anuales



def obtenerVentasMensuales(ventas_anuales):
    ventas_mensuales = []
    venta_mensual = []
    año = ventas_anuales[0][0][3][2]
    mes = ventas_anuales[0][0][3][1]
    
    # Iteramos en cada año
    for venta_anual in ventas_anuales:
        # Iteramos en cada elemento de la lista anual para ordenar y agrupar por mes
        for venta in venta_anual:
            if venta[3][2] != año or venta[3][1] != mes:
                ventas_mensuales.append(venta_mensual)
                venta_mensual = []
                año = venta[3][2]
                mes = venta[3][1]
            venta_mensual.append(venta)
        ventas_mensuales.append(venta_mensual)
        
    return ventas_mensuales



def obtenerIngresosAnuales(ventasAnuales):
    # Calculamos los ingresos obtenidos en cada año
    # Iteramos por cada año
    for i in range(len(ventas_anuales)):
        venta_anual = ventas_anuales[i]
        ventas = len(venta_anual)
        año = venta_anual[0][3][2]
        ingresos = 0
        reembolsos = 0
        perdidas = 0
        # Iteramos por cada venta en el año y sumamos ventas y reembolsos
        for venta in venta_anual:
            ingresos += products[venta[1]-1][2]
            if venta[-1] == 1:
                reembolsos += 1
                perdidas += products[venta[1]-1][2]
            ventas_anuales[i] = [año,ventas,ingresos,reembolsos,perdidas] + venta_anual
            
        return ventas_anuales


def obtenerIngresosMensuales(ventas_mensuales):
    # Variables para guardar promedios
    promedio_ingreso_mensual = 0
    promedio_venta_mensual = 0
    promedio_perdida_mensual = 0
    promedio_reembolso_mensual = 0
    
    # iteramos por cada mes
    for i in range(len(ventas_mensuales)):
        venta_mensual = ventas_mensuales[i]
        ventas = len(venta_mensual)
        año = venta_mensual[0][3][2]
        mes = venta_mensual[0][3][1]
        ingresos = 0
        reembolsos = 0
        perdidas = 0
        # Iteramos por cada venta en el mes
        for venta in venta_mensual:
            # Calculamos los ingresos y reembolsos
            ingresos += products[venta[1]-1][2]
            if venta[-1] == 1:
                reembolsos += 1
                perdidas += products[venta[1]-1][2]
        # Calculamos los promedios por cada mes
        promedio_ingreso_mensual += ingresos
        promedio_venta_mensual += ventas
        promedio_perdida_mensual += perdidas
        promedio_reembolso_mensual += reembolsos
        ventas_mensuales[i] = [mes,año,ventas,ingresos,reembolsos,perdidas] + venta_mensual
    
    # Terminamos de calcular los promedios e imprimos los resultados
    print("")
    print("Total de ingresos: $" + str(promedio_ingreso_mensual))
    promedio_ingreso_mensual /= len(ventas_mensuales)
    promedio_venta_mensual /= len(ventas_mensuales)
    promedio_perdida_mensual /= len(ventas_mensuales)
    promedio_reembolso_mensual /= len(ventas_mensuales)
    print("Ingreso promedio mensual: $" + str(round(promedio_ingreso_mensual,2)))
    print("Ventas promedio mensual: " + str(round(promedio_venta_mensual,2)))
    print("Perdida promedio mensual: $" + str(round(promedio_perdida_mensual,2)))
    print("Reembolso promedio mensual: " + str(round(promedio_reembolso_mensual,2)))
    
    return ventas_mensuales



def imprimirIngresosAnuales(ventas_anuales):
    for venta_anual in ventas_anuales:
        print("\nIngresos en " + str(venta_anual[0]) + ": $" + str(venta_anual[2]))



def imprimirIngresosMensuales(ventas_mensuales):
    ventas_mensuales.sort(key = lambda x: x[2]-x[4], reverse = True)
    def format(x):
        return "${:.2f}".format(x)

    print("\n Meses con más ventas al año\n")
    mesesMasVentas = [[ventas_mensuales[i][0],ventas_mensuales[i][2],ventas_mensuales[i][3], ventas_mensuales[i][4], ventas_mensuales[i][5]] for i in range(len(ventas_mensuales))]
    mesesMasVentas = pd.DataFrame(mesesMasVentas)
    mesesMasVentas.columns = ["Mes","Ventas","Ingresos","Reembolsos","Perdidas"]
    mesesMasVentas = mesesMasVentas.set_index("Mes")
    mesesMasVentas['Ingresos'] = mesesMasVentas['Ingresos'].apply(format)
    mesesMasVentas['Perdidas'] = mesesMasVentas['Perdidas'].apply(format)
    print(mesesMasVentas)
    mesesMasVentas.to_csv("mesesMasVentas.csv")
    


users = {"Juan":{"Contraseña": "aidie1",
                 "Nivel": "Admin"},
         "Jose":{"Contraseña": "mdaiu",
                 "Nivel": "Lector"},
         "Jesus":{"Contraseña": "ksmaifi",
                  "Nivel": "Lector"}}
clearConsole()
print("\nSea bienvenido a mi proyecto 1 del curso Fundamentos de Programación con Python")
print("\nPara comenzar debe iniciar sesión")
print("\nSi desea salir del programa escriba \'Salir\', si no es así escriba \'continuar\' \n")
continuar = input()
login = False

while continuar == "continuar" or continuar == "Si" or continuar == "si":
    new_user = input("\n¿Es un nuevo usuario? Si es un nuevo usuario puede registrarse escribiendo \'Si\' ")
    if new_user == "Si" or new_user == "si":
        print("\nIngrese su nuevo usuario y contraseña")
    else:
        print("\nMuy bien, acceda con su usuario y contraseña")
    login = False
    user = input("Usuario: ")
    password = input("Contraseña: ")
    if new_user == "Si" or new_user == "si":
        print("\nConfirme su contraseña: ")
        if password == input():
            users[user] = {"Contraseña": password, "Nivel": "Lector"}
            continuar = "No"
            login = True
        else:
            print("\nError, vuelva a introducir sus datos.")
    elif users[user]["Contraseña"] == password:
        print("\nDatos ingresados correctamente, su nivel de permisos es \'" + users[user]["Nivel"] +"\'.")
        nivel = users[user]["Nivel"]
        continuar = "No"
        login = True
    else:
        print("\nIngrese sus datos nuevamente")
        
        
if login:
    print("\n")
    print("***************************************************************")
    print("\n")
    input()
    print("\nA continuación se muestran los resultados obtenidos de los datos proporcionados en el año 2020.")
    ventas = limpieza(2020)
    ventas_por_producto = ventasPorProducto(products,sales)
    busquedas_por_producto = busquedasPorProducto(products,searches)
    imprimirProductosPorVentas(ventas_por_producto)
    input()
    imprimirProductosPorBusquedas(busquedas_por_producto)
    input()
    reseñas_por_producto = reseñasPorProducto(products,sales)
    imprimirProductosPorReseñas(reseñas_por_producto)
    input()
    ventas_anuales = obtenerVentasAnuales(ventas)
    ventas_mensuales = obtenerVentasMensuales(ventas_anuales)
    ingresos_anuales = obtenerIngresosAnuales(ventas_anuales)
    imprimirIngresosAnuales(ingresos_anuales)
    input()
    ingresos_mensuales = obtenerIngresosMensuales(ventas_mensuales)
    imprimirIngresosMensuales(ingresos_mensuales)
    input()
    print("\nEso fue todo, muchas gracias por usar este programa. :)")
