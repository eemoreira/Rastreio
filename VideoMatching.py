import cv2 as cv
import os
import csv

# Best 2 methods from previous part
methods = ['TM_CCOEFF_NORMED', 'TM_CCORR_NORMED']

template_bg = "MonsterTemplateBG.jpg"
template_nobg = "MonsterTemplateNOBG.png"
template = cv.imread(template_nobg, cv.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]
frames_dir = "frames"
output_dir = "VideoFrameMatchingNOBackground"
tables_dir = "tables_csv"  

os.makedirs(tables_dir, exist_ok=True)

for meth in methods:
    os.makedirs(os.path.join(output_dir, meth), exist_ok=True)

csv_data = {meth: [] for meth in methods}

def getMatchings(img, name):
    for meth in methods:
        method = getattr(cv, meth)

        res = cv.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        # adicionar os valores min_val e max_val à tabela de resultados
        csv_data[meth].append([name, min_val, max_val])

        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        matched_img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        cv.rectangle(matched_img, top_left, bottom_right, (0, 255, 0), 2)

        output_path = os.path.join(output_dir, meth, f"{name}_{meth}_NoBackground.jpg")
#        cv.imwrite(output_path, matched_img)

for filename in os.listdir(frames_dir):
    if filename.endswith(".jpg"):
        print(f"Processing {filename}")
        img = cv.imread(f'frames/{filename}', cv.IMREAD_GRAYSCALE)
        getMatchings(img, filename[:-4])
    else:
        continue

# Salvar os dados dos CSVs
for meth in methods:
    csv_file_path = os.path.join(tables_dir, f"{meth}_matching_results.csv")
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Frame", "Min_val", "Max_val"])
        writer.writerows(csv_data[meth])

    print(f"CSV saved for {meth} at {csv_file_path}")
