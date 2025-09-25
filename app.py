import pandas as pd
import re
import argparse
from geopy.distance import geodesic
import os

def extract_long_lat(location_str):
    """Ekstrak longitude dan latitude dari string Location Coordinates"""
    if pd.isna(location_str):
        return None, None
    lon_match = re.search(r"Longitude:\s*([-\d.]+)", location_str)
    lat_match = re.search(r"Latitude:\s*([-\d.]+)", location_str)
    lon = float(lon_match.group(1)) if lon_match else None
    lat = float(lat_match.group(1)) if lat_match else None
    return lon, lat

def calc_distance(lat, lon, ref_point):
    """Hitung jarak dari titik (lat, lon) ke ref_point (dalam meter)"""
    if pd.isna(lat) or pd.isna(lon):
        return None
    return geodesic((lat, lon), ref_point).meters

def process_file(file_path):
    # Load file Excel
    df = pd.read_excel(file_path, sheet_name=0)

    # Ekstrak longitude dan latitude
    df[["Longitude", "Latitude"]] = df["Location Coordinates"].apply(
        lambda x: pd.Series(extract_long_lat(x))
    )

    # Titik referensi
    ref_point_jakarta = (-6.24068534180811, 106.7993318802972)
    ref_point_karawang = (-6.360620063697015, 107.30800526276006)

    # Hitung jarak ke Jakarta & Karawang
    df["Jarak Jakarta (m)"] = df.apply(
        lambda row: calc_distance(row["Latitude"], row["Longitude"], ref_point_jakarta), axis=1
    )
    df["Jarak Karawang (m)"] = df.apply(
        lambda row: calc_distance(row["Latitude"], row["Longitude"], ref_point_karawang), axis=1
    )

    # Kolom Masuk Undian
    df["Masuk Undian"] = df.apply(
        lambda row: True if (
            (row["Jarak Karawang (m)"] is not None and row["Jarak Karawang (m)"] < 6000) or
            (row["Jarak Jakarta (m)"] is not None and row["Jarak Jakarta (m)"] < 3000)
        ) else False,
        axis=1
    )

    # Filter untuk file kedua (hanya yang masuk undian)
    filtered_df = df[df["Masuk Undian"] == True]

    # Nama file output
    base_name, ext = os.path.splitext(file_path)
    output_full = f"{base_name}_processed.xlsx"
    output_filtered = f"{base_name}_undian.xlsx"

    # Simpan ke Excel
    df.to_excel(output_full, index=False)
    filtered_df.to_excel(output_filtered, index=False)

    print(f"File dengan semua data + kolom tambahan disimpan: {output_full}")
    print(f"File dengan data 'Masuk Undian = True' disimpan: {output_filtered}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Proses file Excel dan hitung jarak Jakarta & Karawang.")
    parser.add_argument("--file", required=True, help="Path ke file Excel (.xls/.xlsx)")
    args = parser.parse_args()

    process_file(args.file)
