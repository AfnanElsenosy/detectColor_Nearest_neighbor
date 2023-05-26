import cv2
import csv
import pandas as pd
import knn_classifier as knn
#---------------------------------------------------------------#
click=False
r = g = b = 0

testData='test.csv'

trainingData='file.csv'

colors = []

colors_band = {"Red": 2, "Black": 0,
                "Brown": 1, "Orange": 3, "Yellow": 4,
                "Green": 5, "Blue": 6, "Violet": 7,
                "Grey": 8, "White": 9, "Silver": -2,
                "Gold": -1, "Pink": -3}

colors_tolerance = {"Red": .02, "Black": 0,
                    "Brown": .01, "Orange": 0.0005,
                    "Yellow": 0.0002, "Green": 0.05, 
                    "Blue": 0.0025, "Violet": 0.01,
                    "Grey": .01, "White": 0, "Silver":.01,
                    "Gold": 0.05, "Pink": 0}

colorlist=["Red", "Black", "Brown",
            "Orange", "Yellow", "Green",
            "Blue", "Violet", "Grey",
            "White","Silver","Gold", "Pink"]

#---------------------------------------------------------------#
#Do you want just detect color or calculate Rsistace value??
read_inputx = input("If you want to detect color press Y")

global flag
if read_inputx == 'Y':
    flag = 1
    img_path = r'colorpic.jpg'
    img = cv2.imread(img_path)
else:
    flag = 2
    img_path = r'fourBandResistance.png'
    img = cv2.imread(img_path)
#---------------------------------------------------------------#
def save_data(r,g,b):#save r,g,b after click in testData.csv
    with open(testData, mode='w', newline='') as file:
        color = csv.writer(file)
        color.writerow([r, g, b])

#---------------------------------------------------------------#
def get_xy(event,x,y, flags, param):#with click get r,g,b for clicked pixel
    if event==cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r,click 
        click=True
        b, g, r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
        save_data(r,g,b)
#---------------------------------------------------------------#

cv2.namedWindow('image')
cv2.setMouseCallback('image', get_xy)


#---------------------------------------------------------------#
#for calculate Resistace value :
def funColor(prediction): 
    for i in range(len(colorlist)):
        if prediction==colorlist[i]:
            colors.append(prediction)

#---------------------------------------------------------------#

while True:
    cv2.imshow("image", img)

    if click:
            if flag == 1:
                prediction = knn.main(trainingData, testData)
                cv2.rectangle(img, (20, 20), (550, 60), (0, 0, 0), -1)
                text =prediction  + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
                cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                print('Detected color is:', prediction)
            elif flag == 2:
                prediction = knn.main(trainingData, testData)
                funColor(prediction)
                cv2.rectangle(img, (20, 20), (550, 60), (0, 0, 0), -1)
                text =prediction  + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
                cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                print('Detected color is:', prediction)
            click = False
    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

#---------------------------------------------------------#
#calculate Rasistance value:
if flag == 2:
    print(colors)
    band =len(colors)
    if band < 3 or band > 5:
        print("There are no resistors of band" + " " + str(band))

    if band == 3:
        total_r = (colors_band[colors[0]] * 10 + colors_band[colors[1]]) * (10 ** colors_band[colors[2]])
        print(total_r)
    if band == 4:
        total_r = (colors_band[colors[0]] * 10 + colors_band[colors[1]]) * (10 ** colors_band[colors[2]])
        total_r1 = total_r + total_r * colors_tolerance[colors[3]]
        total_r2 = total_r - total_r * colors_tolerance[colors[3]]
        print(total_r)
        print(total_r1)
        print(total_r2)
    if band == 5:
        total_r = (colors_band[colors[0]] * 100 + colors_band[colors[1]] * 10 + colors_band[colors[2]]) * (10 ** colors_band[colors[3]])
        total_r1 = total_r + total_r * colors_tolerance[colors[4]]
        total_r2 = total_r - total_r * colors_tolerance[colors[4]]
        print(total_r)
        print(total_r1)
        print(total_r2)

#---------------------------------------------------------#
cv2.destroyAllWindows()


