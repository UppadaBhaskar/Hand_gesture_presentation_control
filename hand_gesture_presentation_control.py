from cvzone.HandTrackingModule import HandDetector
import os
import cv2
import numpy as np



width=1280
height=720

folderpath='presentation'

cap=cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4,height)

pathimages=sorted(os.listdir(folderpath),key=len)

#dictionary of image to drawing points
drawDict={}
drawFlag=[]
for i in range(len(pathimages)):
    drawFlag.append(True)
for i in range(len(pathimages)):
    drawDict[i]=[]


#dictionary to store undo values
drawDict1={}
for i in range(len(pathimages)):
    drawDict1[i]=[]

print(pathimages)

hs,ws=int(120*1),int(213*1) #height and width of small image on right top corner

imgnumber=0 #used for changing slide by inc/dec

#pressing time
pressed=False
presscounter=0
delay=5

#setting border line for means face line
gestureThreshold=300

#hand detector
detector=HandDetector(detectionCon=0.8,maxHands=1)

'''#colors of pointer and lines
colors=[(0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255)]'''

#pensize
penSize=15

while True:
    success,img=cap.read()
    pathfullimage=os.path.join(folderpath,pathimages[imgnumber]) #we are just getting the path of slide image
    imgcurrent=cv2.imread(pathfullimage) #reading image from that path
    img=cv2.flip(img,1) #flipping the images
    hands,img=detector.findHands(img)    #finding the hand and plotting the points on it and fliptype will say that the image is flipped or not
    

    #Drawing a line of Threshold
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(255,0,0),10)

    #sizing and showing images
    imagesmall=cv2.resize(img,(ws,hs))
    imgcurrent=cv2.resize(imgcurrent,(width,height))

    if hands and pressed is False:
        hand=hands[0]
        fingers=detector.fingersUp(hand)
        
        cx,cy=hand['center']  #this is to check that the center of hand is above line or not.
        lmlist=hand['lmList'] #taking the landmarks of the fingers points

        #scaling the area with the whole screen
        xval=int(np.interp(lmlist[8][0],[width//2,width],[0,width]))
        yval=int(np.interp(lmlist[8][1],[150,height-150],[0,height]))
        indexFinger=xval+70,yval

        #print(fingers)

        if cy<=gestureThreshold:  #if the hand above the line

            #gesture-1  -left

            if fingers==[1,0,0,0,0] and imgnumber>0:
                print("left")
                pressed=True
                imgnumber-=1

            #gesture-2  -right

            if fingers==[0,0,0,0,1] and imgnumber<len(pathimages)-1:
                print("right")
                pressed=True
                imgnumber+=1
        #gesture-3 (showing cursor)
        if fingers==[0,1,1,0,0] :
            cv2.circle(imgcurrent,indexFinger,12,(0,0,255),cv2.FILLED)

        #Gesture-4 (drawing)
        if fingers==[0,1,0,0,0]:
            
            cv2.circle(imgcurrent,indexFinger,penSize+8,(0,0,255),cv2.FILLED) 
            drawDict[imgnumber].append(indexFinger)
            drawFlag[imgnumber]=True
        elif drawFlag[imgnumber]==True:
            drawDict[imgnumber].append(-1)
            drawFlag[imgnumber]=False
        
        #gesture-5 (undo)
        if fingers==[0,0,1,1,1]:
            
            pressed=True
            while (True and drawDict[imgnumber]) :
                if drawDict[imgnumber][-1]!=-1:
                    drawDict1[imgnumber].append(drawDict[imgnumber].pop())

                else:
                    drawDict1[imgnumber].append(drawDict[imgnumber].pop())
                    break
        #gesture-6 (Redo)
        if fingers==[0,1,1,1,1]:
            pressed=True
            if drawDict1[imgnumber]:
                drawDict[imgnumber].append(drawDict1[imgnumber].pop())
            while (True and drawDict1[imgnumber]):
                if drawDict1[imgnumber][-1]!=-1:
                    drawDict[imgnumber].append(drawDict1[imgnumber].pop())
                else:
                    break

    #wait for some timedelay and recheck if the finger raised           
    if pressed:  
        presscounter+=1
        if presscounter>delay:
            presscounter=0
            pressed=False

    #drawing line from previously drawn points
    for i in range(1,len(drawDict[imgnumber])):
        if drawDict[imgnumber][i]==-1 or drawDict[imgnumber][i-1]==-1:
            continue

        cv2.line(imgcurrent,drawDict[imgnumber][i-1],drawDict[imgnumber][i],(0,0,200),penSize)      
    


    '''#setting the size of slide TO BE CHANGED
    h,w,_=imgcurrent.shape'''
    '''wc,hc=width-20,180
    for i in range(len(colors)):
        cv2.circle(imgcurrent,(wc,hc+(i*50)),16,colors[i],cv2.FILLED)
    wp,hp=width-60,hc
    for i in range(len(colors)):
        cv2.circle(imgcurrent,(wp,hp+(i*50)),16,colors[i],cv2.FILLED)'''
    
    
    imgcurrent[0:hs,width-ws:width]=imagesmall
    #cv2.imshow('image',img) #displaying
    cv2.imshow('slides',imgcurrent)

    key=cv2.waitKey(1)

    #pensize setting
    if penSize<=22 and penSize>=2  :
        
        if penSize<22 and (key==ord('b') or key==ord('B')):
            penSize+=1
        elif penSize>2 and (key==ord('s') or key==ord('S')):
            penSize=penSize-1

    if key==ord('q'):
        break
