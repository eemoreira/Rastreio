import cv2 as cv
import os

# best 2 mathods from previous part
methods = ['TM_CCOEFF_NORMED', 'TM_CCORR_NORMED']

template_bg = "MonsterTemplateBG.jpg"
template_nobg = "MonsterTemplateNOBG.png"
template = cv.imread(template_bg, cv.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]
frames_dir = "frames"
output_dir = "VideoFrameMatchingWithBackground"

def getMatchings(img, name):
    for meth in methods:
        method = getattr(cv, meth)

        res = cv.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        matched_img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)  # Convert to BGR for colored rectangle
        cv.rectangle(matched_img, top_left, bottom_right, (0, 255, 0), 2)

        output_path = os.path.join(output_dir, f"{meth}/{name}_{meth}_WithBackground.jpg")
        cv.imwrite(output_path, matched_img)

for filename in os.listdir(frames_dir):
    if filename.endswith(".jpg"):
        print(filename)
        img = cv.imread(f'frames/{filename}', cv.IMREAD_GRAYSCALE)
        getMatchings(img, filename[:-4])
    else:
        exit(1)
