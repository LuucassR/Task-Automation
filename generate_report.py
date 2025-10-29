import csv
import os
import sys
from datetime import datetime

# Archivos
INPUT_FILE = "data/input_data.csv"
REPORT_DIR = "data/reports/"

# --- Funciones ---
def create_sample_csv(file_path):
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["name","department","sales"])
            writer.writerow(["Alice","Marketing","1200"])
            writer.writerow(["Bob","Sales","1500"])
            writer.writerow(["Charlie","Sales","800"])
            writer.writerow(["Diana","HR","600"])
            writer.writerow(["Eve","Marketing","700"])
        print(f"📄 CSV de ejemplo creado en {file_path}\n")

def add_entry_to_csv(file_path, name, department, sales):
    with open(file_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([name, department, sales])
    print(f"✅ Nuevo registro agregado: {name} | {department} | {sales}\n")

def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def summarize_data(data):
    summary = {}
    for row in data:
        dept = row["department"]
        name = row["name"]
        sales = int(row["sales"])

        if dept not in summary:
            summary[dept] = {
                "employees": 0,
                "total_sales": 0,
                "max_sale": 0,
                "min_sale": sales,
                "best_seller": {"name": "", "sales": 0},
                "sellers": []  # lista de vendedores para ranking
            }

        summary[dept]["employees"] += 1
        summary[dept]["total_sales"] += sales
        if sales > summary[dept]["max_sale"]:
            summary[dept]["max_sale"] = sales
        if sales < summary[dept]["min_sale"]:
            summary[dept]["min_sale"] = sales
        if sales > summary[dept]["best_seller"]["sales"]:
            summary[dept]["best_seller"] = {"name": name, "sales": sales}
        summary[dept]["sellers"].append({"name": name, "sales": sales})

    # Ordenar vendedores dentro de cada departamento de mayor a menor
    for dept in summary:
        summary[dept]["sellers"].sort(key=lambda x: x["sales"], reverse=True)

    return summary

def sort_departments(summary):
    return sorted(summary.items(), key=lambda x: x[1]["total_sales"], reverse=True)

def print_summary(sorted_summary):
    print("\n" + "="*50)
    print("📊 RESUMEN DE VENTAS POR DEPARTAMENTO")
    print("="*50)
    total_employees = 0
    total_sales = 0
    for dept, stats in sorted_summary:
        avg_sale = stats["total_sales"] / stats["employees"]
        best_seller = f"{stats['best_seller']['name']} ({stats['best_seller']['sales']})"
        alert = "⚠️ PROMEDIO BAJO!" if avg_sale < 1000 else ""
        print(f"Departamento: {dept}")
        print(f" - Empleados: {stats['employees']}")
        print(f" - Total ventas: {stats['total_sales']}")
        print(f" - Promedio ventas: {avg_sale:.2f} {alert}")
        print(f" - Venta máxima: {stats['max_sale']}")
        print(f" - Venta mínima: {stats['min_sale']}")
        print(f" - Mejor vendedor: {best_seller}")
        print(" - Ranking de vendedores:")
        for i, seller in enumerate(stats["sellers"], 1):
            print(f"    {i}. {seller['name']} ({seller['sales']})")
        print("-"*50)
        total_employees += stats["employees"]
        total_sales += stats["total_sales"]

    print(f"📈 ESTADÍSTICAS GLOBALES")
    print(f" - Total empleados: {total_employees}")
    print(f" - Total ventas: {total_sales}")
    print("="*50 + "\n")

def write_report(sorted_summary):
    os.makedirs(REPORT_DIR, exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORT_DIR + f"report_summary_{now}.csv"

    with open(report_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Department","Employees","Total Sales","Average Sales","Max Sale","Min Sale","Best Seller"])
        for dept, stats in sorted_summary:
            avg_sale = stats["total_sales"] / stats["employees"]
            best_seller = f"{stats['best_seller']['name']} ({stats['best_seller']['sales']})"
            writer.writerow([dept, stats["employees"], stats["total_sales"], round(avg_sale, 2), stats["max_sale"], stats["min_sale"], best_seller])
    print(f"✅ Reporte generado: {report_file}\n")

def prompt_new_entry():
    print("💡 Agregar nuevo registro al CSV")
    name = input("Nombre: ").strip()
    department = input("Departamento: ").strip()
    while True:
        sales = input("Ventas: ").strip()
        if sales.isdigit() and int(sales) >= 0:
            sales = int(sales)
            break
        else:
            print("⚠️ Ventas debe ser un número entero positivo. Intenta de nuevo.")
    add_entry_to_csv(INPUT_FILE, name, department, sales)

# --- Programa principal ---
create_sample_csv(INPUT_FILE)

if len(sys.argv) == 4:
    name, department, sales = sys.argv[1], sys.argv[2], sys.argv[3]
    if sales.isdigit() and int(sales) >= 0:
        add_entry_to_csv(INPUT_FILE, name, department, int(sales))
    else:
        print("⚠️ Ventas debe ser un número entero positivo. Ignorando entrada CLI.")
elif len(sys.argv) == 1:
    respuesta = input("¿Deseas agregar un nuevo registro al CSV? (s/n): ").strip().lower()
    if respuesta == 's':
        prompt_new_entry()
elif len(sys.argv) > 1:
    print("⚠️ Uso incorrecto: python generate_report.py [name department sales]\n")

data = read_csv(INPUT_FILE)
summary = summarize_data(data)
sorted_summary = sort_departments(summary)
print_summary(sorted_summary)
write_report(sorted_summary)
