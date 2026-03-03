from pathlib import Path
import pandas as pd

from cleaning import basic_clean_pipeline


def main() -> None:
    # Rutas del proyecto
    base_dir = Path(__file__).resolve().parent
    raw_path = base_dir / "olympics_athletes_dataset.csv"
    out_path = base_dir / "data" / "processed" / "olympics_athletes_clean.csv"

    print("Leyendo:", raw_path)
    df_raw = pd.read_csv(raw_path)

    print("Filas/Columnas (raw):", df_raw.shape)

    df_clean = basic_clean_pipeline(df_raw)

    print("Filas/Columnas (clean):", df_clean.shape)
    print("Nulos por columna (top 10):")
    print(df_clean.isna().sum().sort_values(ascending=False).head(10))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(out_path, index=False)

    print("Guardado en:", out_path)


if __name__ == "__main__":
    main()