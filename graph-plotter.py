import os
import csv
import matplotlib.pyplot as plt

output_dir = "grafico"
os.makedirs(output_dir, exist_ok=True)

files = [
    "tables_csv/nobg/TM_CCOEFF_NORMED_matching_results.csv",
    "tables_csv/nobg/TM_CCORR_NORMED_matching_results.csv",
    "tables_csv/withbg/TM_CCOEFF_NORMED_matching_results.csv",
    "tables_csv/withbg/TM_CCORR_NORMED_matching_results.csv",
]

def extract_frame_number(frame_name):
    return int(frame_name.split("_")[1])  # Extrai o número após "frame_"

def plot_graph(file, label):
    frames = []
    min_vals = []
    max_vals = []

    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Pula o cabeçalho
        data = []
        for row in reader:
            frame_number = extract_frame_number(row[0])  # Extrai o número do frame
            min_val = float(row[1])
            max_val = float(row[2])
            data.append((frame_number, min_val, max_val))
        
        data.sort()

        for frame_number, min_val, max_val in data:
            frames.append(frame_number)
            min_vals.append(min_val)
            max_vals.append(max_val)

    plt.figure()
    plt.plot(frames, min_vals, label="min_val", color="blue")
    plt.plot(frames, max_vals, label="max_val", color="orange")
    plt.xlabel("Frames")
    plt.ylabel("Value")
    plt.title(label)
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(output_dir, f"{label}.png"))
    plt.close()

labels = [
    "TM_CCOEFF_NORMED (No Background)",
    "TM_CCORR_NORMED (No Background)",
    "TM_CCOEFF_NORMED (With Background)",
    "TM_CCORR_NORMED (With Background)",
]

for file, label in zip(files, labels):
    plot_graph(file, label)
