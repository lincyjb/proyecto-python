import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("olympics_athletes_dataset.csv")

print(df.shape)        # (filas, columnas)
print(df.columns)      # nombres de columnas
df.head(10)            # primeras 10 filas

df.info()              # tipos de datos y nulos
df.describe()          # resumen numérico
df.describe(include="object")  # resumen categórico (texto)

missing = df.isna().sum().sort_values(ascending=False)
missing_pct = (missing / len(df) * 100).round(2)

tabla_missing = pd.DataFrame({"missing": missing, "missing_%": missing_pct})
tabla_missing
df.duplicated().sum()

df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], errors="coerce")

plt.figure()
df["age"].dropna().plot(kind="hist", bins=20, title="Distribución de edad")
plt.xlabel("Edad")
plt.ylabel("Frecuencia")
plt.show()

plt.figure()
df["medal"].value_counts().plot(kind="bar", title="Conteo por tipo de medalla (medal)")
plt.xlabel("Medalla")
plt.ylabel("Conteo")
plt.show()

plt.figure()
df["sport"].value_counts().head(10).plot(kind="bar", title="Top 10 deportes por conteo")
plt.xlabel("Deporte")
plt.ylabel("Conteo")
plt.show()

plt.figure()
df.plot(kind="scatter", x="height_cm", y="weight_kg", title="Altura vs peso")
plt.xlabel("Altura (cm)")
plt.ylabel("Peso (kg)")
plt.show()

df["has_medal"] = df["medal"].ne("No Medal") & df["medal"].notna()

medals_by_gender = (
    df.groupby("gender")["has_medal"]
      .agg(total_rows="size", medalistas="sum")
      .assign(pct_medalistas=lambda x: (x["medalistas"]/x["total_rows"]*100).round(2))
      .sort_values("pct_medalistas", ascending=False)
)
medals_by_gender

medals_by_year = (
    df.groupby("year")["has_medal"]
      .agg(total_rows="size", medalistas="sum")
      .assign(pct_medalistas=lambda x: (x["medalistas"]/x["total_rows"]*100).round(2))
      .sort_index()
)
medals_by_year

plt.figure()
medals_by_year["medalistas"].plot(kind="line", title="Medallistas por año (conteo)")
plt.xlabel("Año")
plt.ylabel("Medallistas (conteo)")
plt.show()

