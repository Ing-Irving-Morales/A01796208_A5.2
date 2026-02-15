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

def main():
    # Req 7: Iniciar conteo de tiempo
    start_time = time.time()

    # Req 5: Validación de argumentos de línea de comandos
    if len(sys.argv) != 3:
        print("Uso incorrecto. Formato requerido:")
        print("python computeSales.py priceCatalogue.json salesRecord.json")
        sys.exit(1)

    price_file = sys.argv[1]
    sales_file = sys.argv[2]

    # Req 1: Cargar archivos
    print("--- Iniciando Proceso ---")
    catalogue_data = load_json_file(price_file)
    sales_data = load_json_file(sales_file)

    if catalogue_data is None or sales_data is None:
        sys.exit(1)

    # Convertir catálogo a diccionario para eficiencia (Req 6)
    price_lookup = create_price_lookup(catalogue_data)

    # Req 2: Calcular costos
    total_sales = compute_sales(price_lookup, sales_data)

    # Req 7: Calcular tiempo transcurrido
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Formateo de salida (Req 2 - Human Readable)
    output_lines = [
        "TOTAL SALES REPORT",
        "------------------",
        f"Processing Date: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Price Catalogue: {price_file}",
        f"Sales Record:    {sales_file}",
        "",
        f"Total Cost:      ${total_sales:,.2f}",
        f"Execution Time:  {elapsed_time:.4f} seconds",
        "------------------"
    ]
    
    result_text = "\n".join(output_lines)

    # Req 2: Imprimir en pantalla
    print("\n" + result_text)

    # Req 2: Guardar en archivo
    try:
        with open("SalesResults.txt", "w", encoding='utf-8') as f:
            f.write(result_text)
        print("\nResultados guardados en 'SalesResults.txt'.")
    except Exception as e:
        print(f"Error al escribir el archivo de resultados: {e}")

if __name__ == "__main__":
    main()