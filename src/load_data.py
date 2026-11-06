
# ==========================================
# 1. Import Libraries
# ==========================================

from pathlib import Path
import pandas as pd


# ==========================================
# 2. Define Project Paths
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data" / "genres_original"

OUTPUT_DIR = PROJECT_DIR / "data" / "processed"

OUTPUT_FILE = OUTPUT_DIR / "metadata.csv"


# ==========================================
# 3. Supported Audio Formats
# ==========================================

AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg"}


# ==========================================
# 4. Load Audio File Information
# ==========================================

def load_data():

    records = []

    # Check dataset folder
    if not DATA_DIR.exists():
        print("Error: Dataset folder not found!")
        return

    # Find genre folders
    for genre_folder in sorted(DATA_DIR.iterdir()):

        if not genre_folder.is_dir():
            continue

        genre = genre_folder.name

        print(f"Checking genre: {genre}")

        # Find audio files
        for audio_file in sorted(genre_folder.iterdir()):

            if audio_file.suffix.lower() not in AUDIO_EXTENSIONS:
                continue

            # Save audio information
            records.append({
                "file_name": audio_file.name,
                "file_path": str(audio_file.resolve()),
                "genre": genre
            })

    # ======================================
    # 5. Create Metadata Table
    # ======================================

    df = pd.DataFrame(
        records,
        columns=["file_name", "file_path", "genre"]
    )

    # ======================================
    # 6. Create Output Folder
    # ======================================

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ======================================
    # 7. Save CSV File
    # ======================================

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    # ======================================
    # 8. Display Results
    # ======================================

    print("\nData loading completed!")

    print(f"Total audio files: {len(df)}")

    print("\nFiles per genre:")

    if df.empty:
        print("No audio files found!")
    else:
        print(df["genre"].value_counts().sort_index())

    print(f"\nMetadata saved to: {OUTPUT_FILE}")


# ==========================================
# 9. Run Program
# ==========================================

if __name__ == "__main__":
    load_data()
