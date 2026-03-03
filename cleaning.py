from __future__ import annotations
import pandas as pd


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza nombres de columnas: lower, espacios->_, sin dobles __."""
    out = df.copy()
    out.columns = (
        out.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("__", "_", regex=False)
    )
    return out


def parse_dates(df: pd.DataFrame, date_cols: list[str]) -> pd.DataFrame:
    """Convierte columnas de fecha a datetime (NaT si hay errores)."""
    out = df.copy()
    for c in date_cols:
        if c in out.columns:
            out[c] = pd.to_datetime(out[c], errors="coerce")
    return out


def coerce_numeric(df: pd.DataFrame, numeric_cols: list[str]) -> pd.DataFrame:
    """Asegura que columnas numéricas sean numéricas (NaN si hay errores)."""
    out = df.copy()
    for c in numeric_cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


def clean_string_columns(df: pd.DataFrame, string_cols: list[str]) -> pd.DataFrame:
    """Limpia strings: strip y normaliza vacíos a NA."""
    out = df.copy()
    for c in string_cols:
        if c in out.columns:
            out[c] = (
                out[c]
                .astype("string")
                .str.strip()
                .replace({"": pd.NA, "-": pd.NA})
            )
    return out


def drop_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas duplicadas exactas."""
    return df.drop_duplicates().copy()


def add_has_medal(df: pd.DataFrame, medal_col: str = "medal") -> pd.DataFrame:
    """Crea columna booleana has_medal."""
    out = df.copy()
    if medal_col in out.columns:
        out["has_medal"] = out[medal_col].notna() & (out[medal_col] != "No Medal")
    return out


def basic_clean_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pipeline básico de limpieza (puro): no lee ni escribe archivos.
    """
    out = standardize_column_names(df)

    # Ajusta listas a tus columnas reales (con nombres ya estandarizados)
    out = parse_dates(out, ["date_of_birth"])
    out = coerce_numeric(out, ["age", "height_cm", "weight_kg", "year"])
    out = clean_string_columns(out, ["athlete_name", "country_name", "sport", "event", "medal", "notes"])

    out = drop_duplicate_rows(out)
    out = add_has_medal(out, "medal")

    return out

