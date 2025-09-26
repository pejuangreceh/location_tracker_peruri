import pandas as pd
import argparse
import os

def process_file(file_path, takeout_list):
    # Load file Excel
    df = pd.read_excel(file_path, sheet_name=0)

    # Pastikan kolom NP ada
    if "NP" not in df.columns:
        raise ValueError("Kolom 'NP' tidak ditemukan di file!")

    # Buang baris yang NP-nya ada di list takeout
    filtered_df = df[~df["NP"].astype(str).isin([str(x) for x in takeout_list])]

    # Nama file output
    base_name, ext = os.path.splitext(file_path)
    output_file = f"{base_name}_filtered{ext}"

    # Simpan hasil
    filtered_df.to_excel(output_file, index=False)

    print(f"File hasil takeout disimpan: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Takeout baris berdasarkan NP list.")
    parser.add_argument("--file", required=True, help="Path ke file Excel (.xls/.xlsx)")
    args = parser.parse_args()

    # List NP yang mau di-takeout
    takeout = ["7853", "J974", "K323"]

    process_file(args.file, takeout)
