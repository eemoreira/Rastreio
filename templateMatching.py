import cv2 as cv
import numpy as np
import os
from matplotlib import pyplot as plt

from VideoMatching import output_dir

# All the 6 methods for comparison in a list
methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED', 'TM_CCORR',
            'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED']

template = cv.imread("ursopardoTemplate.pgm", cv.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]
output_dir = "ImgMatchings"

tp = len(methods) * [0]
fp = len(methods) * [0]
tn = len(methods) * [0]
fn = len(methods) * [0]

def getMatchings(img, name, shouldMatch):
    for meth, i in zip(methods, range(len(methods))):
        method = getattr(cv, meth)

        img2 = img.copy()
        res = cv.matchTemplate(img2, template, method)

        # Estatísticas da matriz de correspondência
        res_mean = np.mean(res)
        res_std = np.std(res)

        # Define o limiar como média + desvio padrão
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        matched_img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)  # Convert to BGR for colored rectangle
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:

            top_left = min_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            threshold = res_mean - 2 * res_std
            if min_val <= threshold:
                cv.rectangle(img2,top_left, bottom_right, 255, 2)
                if shouldMatch:
                    tp[i] += 1
                else:
                    fp[i] += 1
            else:
                if shouldMatch:
                    fn[i] += 1
                else:
                    tn[i] += 1
        else:

            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            threshold = res_mean + 2 * res_std
            if max_val >= threshold:
                cv.rectangle(img2,top_left, bottom_right, 255, 2)
                if shouldMatch:
                    tp[i] += 1
                else:
                    fp[i] += 1
            else:
                if shouldMatch:
                    fn[i] += 1
                else:
                    tn[i] += 1



        output_path = os.path.join(output_dir, f"{name}_{meth}_WithBackground.jpg")
        cv.imwrite(output_path, matched_img)

for filename in os.listdir("ursopardo"):
    if filename.endswith(".pgm"):
        img = cv.imread(f'ursopardo/{filename}', cv.IMREAD_GRAYSCALE)
        if filename.startswith("sem"):
            shouldMatch = False
        else:
            shouldMatch = True
        getMatchings(img, filename[:-4], shouldMatch)
        continue
    else:
        exit(1)

print(tp)
print(tn)
print(fp)
print(fn)

accuracy = len(methods) * [0]
for i in range(len(methods)):
    val = (tp[i] + tn[i]) / (tp[i] + tn[i] + fn[i] + fp[i])
    accuracy[i] = (val, i)

accuracy = sorted(accuracy)
print(accuracy)
