from pathlib import Path
import pandas as pd

# --------------------------------------------------
# 1. Define dataset locations
# --------------------------------------------------

videos_folder = Path("Videos")
file_list_path = Path("FileList.csv")
tracings_path = Path("VolumeTracings.csv")

# --------------------------------------------------
# 2. Load the two CSV files
# --------------------------------------------------

file_list = pd.read_csv(file_list_path)
tracings = pd.read_csv(tracings_path)

# --------------------------------------------------
# 3. Find all AVI files
# --------------------------------------------------

avi_files = sorted(videos_folder.glob("*.avi"))

print("Dataset loaded successfully!")
print(f"AVI files: {len(avi_files)}")
print(f"FileList rows: {len(file_list)}")
print(f"VolumeTracings rows: {len(tracings)}")

# --------------------------------------------------
# 4. Create fast lookup for number of tracing rows
# --------------------------------------------------

tracing_counts = tracings.groupby("FileName").size()

# --------------------------------------------------
# 5. Link every AVI file to both CSV files
# --------------------------------------------------

results = []

for avi_file in avi_files:

    # Filename WITH .avi
    # Example: 0X100009310A3BD7FC.avi
    avi_name = avi_file.name

    # Filename WITHOUT .avi
    # Example: 0X100009310A3BD7FC
    file_id = avi_file.stem


    # --------------------------------------------------
    # Find matching row in FileList.csv
    # --------------------------------------------------

    file_match = file_list[
        file_list["FileName"] == file_id
    ]


    # --------------------------------------------------
    # Find number of matching rows in VolumeTracings.csv
    # --------------------------------------------------

    number_of_tracing_rows = int(
        tracing_counts.get(avi_name, 0)
    )


    # --------------------------------------------------
    # Check whether FileList match exists
    # --------------------------------------------------

    if file_match.empty:

        results.append({
            "AVIFile": avi_name,
            "VideoPath": str(avi_file),
            "FoundInFileList": False,
            "FoundInVolumeTracings": number_of_tracing_rows > 0,
            "TracingRows": number_of_tracing_rows,
            "EF": None,
            "ESV": None,
            "EDV": None,
            "FrameHeight": None,
            "FrameWidth": None,
            "FPS": None,
            "NumberOfFrames": None,
            "Split": None
        })

    else:

        row = file_match.iloc[0]

        results.append({
            "AVIFile": avi_name,
            "VideoPath": str(avi_file),
            "FoundInFileList": True,
            "FoundInVolumeTracings": number_of_tracing_rows > 0,
            "TracingRows": number_of_tracing_rows,
            "EF": row["EF"],
            "ESV": row["ESV"],
            "EDV": row["EDV"],
            "FrameHeight": row["FrameHeight"],
            "FrameWidth": row["FrameWidth"],
            "FPS": row["FPS"],
            "NumberOfFrames": row["NumberOfFrames"],
            "Split": row["Split"]
        })

# --------------------------------------------------
# 6. Convert results to a DataFrame
# --------------------------------------------------

linked_data = pd.DataFrame(results)

# --------------------------------------------------
# 7. Save the linked data
# --------------------------------------------------

output_file = "LinkedData.csv"

linked_data.to_csv(
    output_file,
    index=False
)

# --------------------------------------------------
# 8. Print summary
# --------------------------------------------------

print("\nLinking complete!")

print(f"Videos processed: {len(linked_data)}")

print(
    f"Matched to FileList.csv: "
    f"{linked_data['FoundInFileList'].sum()}"
)

print(
    f"Matched to VolumeTracings.csv: "
    f"{linked_data['FoundInVolumeTracings'].sum()}"
)

print(
    f"Missing from FileList.csv: "
    f"{(~linked_data['FoundInFileList']).sum()}"
)

print(
    f"Missing from VolumeTracings.csv: "
    f"{(~linked_data['FoundInVolumeTracings']).sum()}"
)
print(f"\nResults saved to: {output_file}")