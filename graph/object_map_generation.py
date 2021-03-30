import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import n
import cv2 as cv
def detectObject(csv,raw,name,img):
    df = pd.read_csv(os.path.join(raw, name+'.csv'))

    new_df = pd.DataFrame( columns=[ "xmin", "ymin", "xmax", "ymax", "text",'object'])

    text = ""
    xmin = 0
    xmax = 0
    ymin = df.loc[0, "ymin"]
    ymax = df.loc[0, "ymax"]
    image = Image.open(img)
    imgWidth, imgHeight = image.size

    for i in range(len(df) - 1):
        space = abs(df.loc[i, "xmax"] - df.loc[i + 1, "xmin"]) * 100
        # width = df.loc[i , "xmax"]-df.loc[i , "xmin"]
        # numberOfChar = len(df.loc[i,"Object"])
        # per = width / numberOfChar
        if space == 0:
            continue

        Height = max((ymax - ymin), (df.loc[i, "ymax"] - df.loc[i, "ymin"])) * 100
        rate = (Height / space)
        text += (str)(df.loc[i, "Text"])
        text += " "

        if space < Height:
            ymin = min(ymin, df.loc[i, "ymin"])
            ymax = max(ymax, df.loc[i, "ymax"])
        else:
            xmax = df.loc[i, "xmax"]
            new_df.loc[len(new_df.index)] = [ xmin, ymin, xmax,
                                             ymax, text,'o']
            draw = ImageDraw.Draw(image)

            left = imgWidth * xmin
            top = imgHeight * ymin
            draw.rectangle([left, top, left + (imgWidth * (xmax - xmin)),
                            top + (imgHeight * (ymax - ymin))], outline='red')
            text = ""
            ymin = df.loc[i + 1, "ymin"]
            ymax = df.loc[i + 1, "ymax"]
            xmin = df.loc[i + 1, "xmin"]

    text += (str)(df.loc[i + 1, "Text"])
    xmax = df.loc[i + 1, "xmax"]
    new_df.loc[len(new_df.index)] = [ xmin, ymin, xmax, ymax, text,'o']

    left = imgWidth * xmin
    top = imgHeight * ymin
    draw.rectangle([left, top, left + (imgWidth * (xmax - xmin)),
                    top + (imgHeight * (ymax - ymin))], outline='green')
    new_df.to_csv(os.path.join(csv, name + '.csv'),index=False)
    image.save("./data/showimages/"+name+'.jpg')


def run (img,csv,raw) :
  for file in os.listdir(img):
      name=file[:-4]
      print(name)
      n.process_text_analysis(os.path.join(img, file),name,raw)
      detectObject(csv,raw,name,os.path.join(img, file))


