import pandas as pd
import argparse
import os

def process_file(file_path):
    # Load file
    df = pd.read_excel(file_path, sheet_name=0)

    # Mapping kolom lama → kolom baru
    column_mapping = {
        "Nomor Pokok": "NP",
        "Nama Lengkap": "Full Name",
        "Nomor WhatsApp": "WhatsApp Number",
        "Unit Kerja": "Unit Kerja",
        "Email": "Email"
    }

    # Pilih hanya kolom yang ada di mapping
    missing_cols = [col for col in column_mapping.keys() if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Kolom berikut tidak ditemukan di file: {missing_cols}")

    new_df = df[list(column_mapping.keys())].rename(columns=column_mapping)

    # Buat nama file output
    base_name, ext = os.path.splitext(file_path)
    output_file = f"{base_name}_transform{ext}"

    # Simpan hasil
    new_df.to_excel(output_file, index=False)

    print(f"File transform disimpan: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform kolom Excel sesuai mapping.")
    parser.add_argument("--file", required=True, help="Path ke file Excel (.xls/.xlsx)")
    args = parser.parse_args()

    process_file(args.file)
