"""
Este módulo calcula el total de ventas a partir de un catálogo de precios
y un archivo de registro de ventas en formato JSON.
"""

import json
import sys
import time


def load_json_file(filename):
    """Carga un archivo JSON y maneja errores en caso de fallo."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {filename}.")
    except json.JSONDecodeError:
        print(f"Error: El archivo {filename} no tiene un formato JSON válido.")
    return None


def compute_total_sales(price_catalogue, sales_record):
    """
    Calcula el costo total de las ventas basándose en el catálogo de precios.
    Maneja errores de datos inválidos en el archivo de ventas.
    """
    total_sales = 0.0
    errors = []

    for sale in sales_record:
        product = sale.get("product")
        quantity = sale.get("quantity")

        if product not in price_catalogue:
            errors.append(
                f"Error: Producto '{product}' no encontrado en el catálogo."
            )
            continue
        if not isinstance(quantity, (int, float)) or quantity < 0:
            errors.append(
                f"Error: '{quantity}' para el producto '{product}'."
            )
            continue

        total_sales += price_catalogue[product] * quantity

    return total_sales, errors


def main():
    """Función principal para ejecutar el programa."""
    if len(sys.argv) != 3:
        sys.exit(1)

    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]

    # Cargar archivos JSON
    price_catalogue = load_json_file(price_catalogue_file)
    sales_record = load_json_file(sales_record_file)

    if price_catalogue is None or sales_record is None:
        print("No se puede continuar debido a errores en los archivos JSON.")
        sys.exit(1)

    start_time = time.time()

    # Calcular total de ventas
    total_sales, errors = compute_total_sales(price_catalogue, sales_record)

    elapsed_time = time.time() - start_time

    # Generar salida
    result_output = (
        f"Total de ventas: ${total_sales:.2f}\n"
        f"Tiempo de ejecución: {elapsed_time:.4f} segundos\n"
    )

    # Imprimir errores si los hay
    if errors:
        error_output = "\n".join(errors) + "\n"
        print(error_output)
        result_output += f"\nErrores encontrados:\n{error_output}"

    # Guardar en archivo
    with open("SalesResults.txt", "w", encoding="utf-8") as result_file:
        result_file.write(result_output)

    print(result_output)


if __name__ == "__main__":
    main()
