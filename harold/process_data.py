import pandas as pd

# Cargar el archivo Excel
df = pd.read_excel("harold/sample_data.xlsx")

# Definir palabras clave para la preparación
preparation_keywords = ['dry yeast', 'prepared mustard', 'chopped', 'smooth']

# Definir una función para dividir las celdas de Ingredients
def split_ingredients(row):
    ingredients = []
    for col in df.columns:
        if col.startswith("Ingredients-"):
            ingredient = row[col]
            if not pd.isna(ingredient):
                parts = ingredient.split()
                quantity = parts[0] if parts[0].isdigit() else ""
                unit = parts[1] if len(parts) > 1 and not parts[1].isdigit() else ""
                name = " ".join(parts[1:]) if len(parts) > 1 else parts[0]
                # Agregar preparación basada en palabras clave
                preparation = ""
                for keyword in preparation_keywords:
                    if keyword in name.lower():
                        preparation = keyword
                        break
                results = [quantity, unit, name, preparation]
                ingredients.append(results)
    return pd.Series([ingredients]) if ingredients else pd.Series([["", "", "", ""]])

# Aplicar la función a cada fila del DataFrame
new_columns = df.apply(split_ingredients, axis=1)

# Concatenar las nuevas columnas al DataFrame original
df = pd.concat([df, new_columns], axis=1)

# Expandir la lista de ingredientes en filas separadas
df = df.explode(0)

# Renombrar las columnas generadas
df.columns = list(df.columns[:-1]) + ["Ingredients"]

# Crear las nuevas columnas 'QUANTITY', 'UNIT', 'NAME', 'PREPARATION'
df['QUANTITY'] = df['Ingredients'].apply(lambda x: x[0] if x else "")
df['UNIT'] = df['Ingredients'].apply(lambda x: x[1] if x else "")
df['NAME'] = df['Ingredients'].apply(lambda x: x[2] if x else "")
df['PREPARATION'] = df['Ingredients'].apply(lambda x: x[3] if x else "")

# Eliminar las columnas Ingredients-1, Ingredients-2, ..., Ingredients-n
for col in df.columns:
    if col.startswith("Ingredients-"):
        df.drop(columns=[col], inplace=True)

# Eliminar la columna 'Ingredients'
df.drop(columns=['Ingredients'], inplace=True)

# Guardar el DataFrame en un nuevo archivo Excel
df.to_excel("harold/sample_data_processed.xlsx", index=False)
