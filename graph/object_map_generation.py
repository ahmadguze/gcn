import pytesseract
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import image_to_scan as scanimg
def object_map(imgdir,csvdir):

  for file in os.listdir(imgdir):

    csv_file = os.path.join(csvdir, file[:-4] + ".csv")
    img_file = os.path.join(imgdir, file)

    large=cv2.imread(img_file)

    small = cv2.cvtColor(large, cv2.COLOR_BGR2GRAY)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))

    grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

    _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))

    dilate = cv2.dilate(bw, kernel, iterations=1)


    #plt.imshow(dilate)
    #plt.show()



    contours, hierarchy = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    kk=file
    print(contours)
    mask = np.zeros(bw.shape, dtype=np.uint8)
    i=large
    for idx in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[idx])
        mask[y:y+h, x:x+w] = 0
        cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
        r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)

        if r > 0.45 and w > 8 and h > 8:
            cv2.rectangle(large, (x, y), (x+w-1, y+h-1), (0, 255, 0), 1)
            roi=large[y:y+h, x:x+w]
            import csv

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    image = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)

    arr = ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'total', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o',
           'o', 'o',
           'o', 'o', 'o', 'o', 'date', 'o', 'o', 'o', 'ee', 'o']
    count =0
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["xmin", "ymin", "xmax","ymax","Object"])
        for idx in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[idx])
            cv2.rectangle(i, (x, y), (x + w, y + h), (36, 255, 12), 2)
            mask[y:y+h, x:x+w] = 0
            thresh= 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            ROI = thresh[y:y + h, x:x + w]
            cv2.waitKey(0)
            data = pytesseract.image_to_string(ROI, lang='eng', config='--psm 6')
            op='o'
            if(count<len(arr)) :
                op=arr[count]


            writer.writerow([x,y,x+w,y+h,data])
            count+=1
            cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
            r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)
    cv2.imshow('888',i)
    cv2.waitKey(0)
    print(roi)
if __name__ == "__main__":
     object_map('D:\\g-project\\Document_IE-master\\graph\\object test', 'D:\\g-project\\Document_IE-master\\graph\\object testt')
    #__________________________