from flask import Flask, request, jsonify
import pandas as pd
import io

from cleaning import basic_clean_pipeline

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "mensaje": "API de limpieza de datos olímpicos",
        "autora": "Lincy",
        "endpoints": {
            "/clean": "POST - Sube un CSV y recibe los datos limpios"
        }
    })


# ── ENDPOINT /clean ──────────────────────────────────────────────────────────

@app.route("/clean", methods=["POST"])
def clean():
    """
    Recibe un archivo CSV, aplica basic_clean_pipeline y devuelve
    los datos limpios en formato JSON.
    """

    # 1. Verificar que se envió un archivo
    if "file" not in request.files:
        return jsonify({"error": "No se envió ningún archivo. Usa el campo 'file'."}), 400

    file = request.files["file"]

    # 2. Verificar que el archivo es un CSV
    if not file.filename.endswith(".csv"):
        return jsonify({"error": "El archivo debe ser un CSV."}), 400

    # 3. Leer el CSV
    try:
        contenido = file.read().decode("utf-8")
        df_raw = pd.read_csv(io.StringIO(contenido))
    except Exception as e:
        return jsonify({"error": f"No se pudo leer el archivo: {str(e)}"}), 400

    # 4. Aplicar limpieza
    try:
        df_clean = basic_clean_pipeline(df_raw)
    except Exception as e:
        return jsonify({"error": f"Error durante la limpieza: {str(e)}"}), 500

    # 5. Convertir fechas a string para poder enviarlas en JSON
    df_clean = df_clean.copy()
    for col in df_clean.columns:
        if pd.api.types.is_datetime64_any_dtype(df_clean[col]):
            df_clean[col] = df_clean[col].astype(str)
        if pd.api.types.is_object_dtype(df_clean[col]):
            df_clean[col] = df_clean[col].where(df_clean[col].notna(), other=None)

    # 6. Devolver resultado
    return jsonify({
        "mensaje": "Limpieza exitosa",
        "filas_originales": len(df_raw),
        "filas_limpias": len(df_clean),
        "columnas": list(df_clean.columns),
        "muestra": df_clean.head(5).to_dict(orient="records")
    })


# ── EJECUTAR ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
