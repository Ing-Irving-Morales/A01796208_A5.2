import json
import sys
import time
import os

def load_json_file(filename):
    """Carga un archivo JSON y maneja errores de lectura."""
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

def create_price_lookup(catalogue):
    """
    Convierte la lista del catálogo en un diccionario para búsqueda rápida (O(1)).
    Asume que el catálogo tiene claves como 'title'/'name' y 'price'.
    """
    price_dict = {}
    for item in catalogue:
        # Intentamos obtener el nombre y precio con claves comunes
        name = item.get("title") or item.get("name") or item.get("product")
        price = item.get("price")

        if name and price is not None:
            price_dict[name] = price
    return price_dict

def compute_sales(price_lookup, sales_record):
    """Calcula el costo total e identifica errores en los datos."""
    total_cost = 0.0
    
    # Iteramos sobre las ventas
    for sale in sales_record:
        product_name = sale.get("Product") or sale.get("title")
        quantity = sale.get("Quantity") or sale.get("quantity")

        if not product_name or quantity is None:
            print(f"Error de datos: Registro de venta inválido o incompleto: {sale}")
            continue

        # Req 3: Manejo de datos inválidos (Producto no existe en catálogo)
        if product_name not in price_lookup:
            print(f"Error: El producto '{product_name}' no existe en el catálogo de precios.")
            continue

        try:
            # Validar que cantidad y precio sean numéricos
            q = float(quantity)
            p = float(price_lookup[product_name])
            total_cost += q * p
        except ValueError:
            print(f"Error de cálculo: Cantidad o precio no numérico para '{product_name}'.")
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