
# ==========================================
# 1. Import Libraries
# ==========================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# 2. Define Project Paths
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

METADATA_FILE = (
    PROJECT_DIR / "data" / "processed" / "metadata.csv"
)

PLOT_DIR = PROJECT_DIR / "reports" / "plots"


# ==========================================
# 3. Load Dataset
# ==========================================

def load_metadata():

    if not METADATA_FILE.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {METADATA_FILE}"
        )

    df = pd.read_csv(METADATA_FILE)

    required_columns = ["file_name", "file_path", "genre"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )

    # Convert empty strings to missing values
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    print("Dataset loaded successfully!")
    print(f"Total records: {len(df)}")

    return df


# ==========================================
# 4. Create Output Folder
# ==========================================

def create_output_folder():

    PLOT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# 5. Plot Genre Distribution (Bar Chart)
# ==========================================

def plot_genre_distribution(df):

    genre_counts = df["genre"].dropna().value_counts().sort_index()

    plt.figure(figsize=(9, 5))

    bars = plt.bar(
        genre_counts.index,
        genre_counts.values
    )

    plt.title("Number of Audio Files per Genre")
    plt.xlabel("Music Genre")
    plt.ylabel("Number of Audio Files")

    plt.bar_label(bars)

    plt.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()

    plt.savefig(
        PLOT_DIR / "genre_distribution.png",
        dpi=300
    )

    plt.show()
    plt.close()


# ==========================================
# 6. Plot Genre Percentages (Pie Chart)
# ==========================================

def plot_genre_pie_chart(df):

    genre_counts = df["genre"].dropna().value_counts()

    if genre_counts.empty:
        print("No genre data available for pie chart.")
        return

    plt.figure(figsize=(8, 8))

    plt.pie(
        genre_counts.values,
        labels=genre_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Music Genre Distribution")

    plt.tight_layout()

    plt.savefig(
        PLOT_DIR / "genre_percentage.png",
        dpi=300
    )

    plt.show()
    plt.close()


# ==========================================
# 7. Plot Audio File Formats
# ==========================================

def plot_audio_formats(df):

    formats = (
        df["file_name"]
        .dropna()
        .astype(str)
        .str.extract(r"(\.[^.]+)$")[0]
        .str.lower()
        .fillna("unknown")
    )

    format_counts = formats.value_counts().sort_index()

    if format_counts.empty:
        print("No audio formats available.")
        return

    plt.figure(figsize=(8, 5))

    bars = plt.bar(
        format_counts.index,
        format_counts.values
    )

    plt.title("Audio File Formats Distribution")
    plt.xlabel("Audio Format")
    plt.ylabel("Number of Files")

    plt.bar_label(bars)

    plt.tight_layout()

    plt.savefig(
        PLOT_DIR / "audio_formats.png",
        dpi=300
    )

    plt.show()
    plt.close()


# ==========================================
# 8. Plot Missing Values
# ==========================================

def plot_missing_values(df):

    columns = ["file_name", "file_path", "genre"]

    missing_counts = df[columns].isnull().sum()

    plt.figure(figsize=(8, 5))

    bars = plt.bar(
        missing_counts.index,
        missing_counts.values
    )

    plt.title("Missing Values per Column")
    plt.xlabel("Dataset Columns")
    plt.ylabel("Number of Missing Values")

    plt.bar_label(bars)

    plt.tight_layout()

    plt.savefig(
        PLOT_DIR / "missing_values.png",
        dpi=300
    )

    plt.show()
    plt.close()


# ==========================================
# 9. Check Duplicate Records
# ==========================================

def check_duplicates(df):

    duplicate_count = df.duplicated(
        subset=["file_path"]
    ).sum()

    print("\nDuplicate Records:")
    print(f"Number of duplicate file paths: {duplicate_count}")


# ==========================================
# 10. Run All EDA Visualizations
# ==========================================

def main():

    print("Starting EDA Visualization...\n")

    df = load_metadata()

    create_output_folder()

    plot_genre_distribution(df)

    plot_genre_pie_chart(df)

    plot_audio_formats(df)

    plot_missing_values(df)

    check_duplicates(df)

    print("\nEDA visualization completed!")

    print(f"Charts saved in: {PLOT_DIR}")


# ==========================================
# 11. Main Program
# ==========================================

if __name__ == "__main__":
    main()
