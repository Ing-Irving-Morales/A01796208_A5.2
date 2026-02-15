import json
import sys
import time
import os

def load_json(filename):
    """Carga el archivo JSON y maneja errores del archivo"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no fue encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo '{filename}' no tiene un formato JSON válido.")
        return None
    except Exception as e:
        print(f"Error desconocido al leer '{filename}': {e}")
        return None

def json_to_dic(catalogue):
    """
    Convierte el json en un diccionario
    """
    catalogue_dict = {}
    for item in catalogue:
        # Se itera sobre el catálogo para obtener el producto y el precio
        name = item.get("title")
        price = item.get("price")

        if name and price is not None:
            catalogue_dict[name] = price
    return catalogue_dict

def cal_sales(catalogue_dic, sales):
    """Calcula el costo total de cada registro"""
    total_cost = 0.0

    # Se itera sobre los registros de ventas
    for sale in sales:
        product_name = sale.get("Product")
        quantity = sale.get("Quantity")

        if not product_name or quantity is None:
            print(f"Error: Registro de venta inválido o incompleto: {sale}")
            continue

        if product_name not in catalogue_dic:
            print(f"Error: El producto '{product_name}' no existe en el catálogo de precios.")
            continue

        try:
            qty = int(quantity) #Se asume que las cantidades son enteras
            price = float(catalogue_dic[product_name])
            total_cost += qty * price
        except ValueError:
            print(f"Error: Cantidad o precio no numérico para '{product_name}'.")
            continue

    return total_cost

#Programa Principal

if len(sys.argv) != 2:
    print("El formato de solicitud es incorrecto, " \
    "deberia ser: python *Nombre del script*.py *Archivo a leer 1 *.json *Archivo a leer 2 *.json")
    sys.exit(1)

else:
    start_time = time.time()
    OUTPUT_FILE = "SalesResults.txt"
    catalogue_file = sys.argv[1]
    sales_file = sys.argv[2]

    catalogue_data = load_json(catalogue_file)
    sales_data = load_json(sales_file)

    if catalogue_data is None:
        print("\n*** El archivo del catálogo está vacío ***")
        sys.exit(1)
    if sales_data is None:
        print("\n*** El archivo de las ventas está vacío ***")
        sys.exit(1)

    catalogue_dic = json_to_dic(catalogue_data)

    total_sales = cal_sales(catalogue_dic, sales_data)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Se le da formato a la salida
    result = []
    result.append("Calculo de ventas\n")
    result.append(f"El precio total para {sales_file} es:\n")
    result.append(f"${total_sales:,.2f} USD\n")
    result.append(f"Tiempo de ejecucción: {elapsed_time:.6f} segundos")

    OUT_STRING = "\n".join(result)

    #Mostrar en la terminal
    print(OUT_STRING)

    #Se guarda en archivo externo
    try:
        with open(OUTPUT_FILE, "w", encoding='utf-8') as file:
            file.write(OUT_STRING)
        print(F"\nResultados guardados exitosamente en {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error escribiendo el archivo de resultados: {e}")