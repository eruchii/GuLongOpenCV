import cv2
import numpy as np
import pyautogui
import random
import time
import os

methods = ['cv2.TM_CCOEFF',' cv2.TM_CCOEFF_NORMED','cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

def region_grabber(region):
	x1 = region[0]
	y1 = region[1]
	width = region[2]-x1
	height = region[3]-y1

	return pyautogui.screenshot(region=(x1,y1,width,height))

def imagesearcharea(image, x1,y1,x2,y2, precision=0.8, im=None) :
	if im is None :
	   im = region_grabber(region=(x1, y1, x2, y2))

	img_rgb = np.array(im)
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	template = cv2.imread(image, 0)

	res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
	if max_val < precision:
		return (-1, -1)
	return max_loc

def list_searchimage(image, r_image, threshold=0.85):
	ans = []
	print(image)
	img_gray = cv2.imread(image, 0)
	img_rgb = cv2.imread(image, 1)
	template = cv2.imread(r_image,0)
	w, h = template.shape[::-1]
	res = cv2.matchTemplate(img_gray,template,eval(methods[1]))
	loc = np.where( res >= threshold)
	for pt in zip(*loc[::-1]):
		cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
		ans.append(pt)
	print("./out/res_"+image)
	cv2.imwrite("./out/res_"+image.split("/")[-1], img_rgb)

def single_searchimage(image, r_image, threshold=0.85):
	print(image)
	img_gray = cv2.imread(image, 0)
	img_rgb = cv2.imread(image, 1)
	template = cv2.imread(r_image,0)
	w, h = template.shape[::-1]
	res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	print("./out/res_"+image)
	if max_val < threshold:
		return (-1, -1)
	else:
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		cv2.rectangle(img_rgb, (max_loc[0], max_loc[1]) , (max_loc[0] + w, max_loc[1] + h), (0,0,255), 2)
		cv2.imwrite("./out/res_"+image.split("/")[-1].split(".")[0]+"_"+r_image.split("/")[-1], img_rgb)
	# scale = 0.7
	# c, newW, newH = img_rgb.shape[::-1]
	# newW, newH = int(newW*scale), int(newH*scale)
	# img_rgb =  cv2.resize(img_rgb, (newW, newH))
	# cv2.imshow("gg", img_rgb)
	# cv2.waitKey(0)
	return max_loc

def detect(r_image, count,threshold=0.9):
	im = pyautogui.screenshot()
	img_rgb = np.array(im)
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
	template = cv2.imread(r_image,0)
	w, h = template.shape[::-1]
	res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	if max_val < threshold:
		return (-1, -1)
	else:
		im = pyautogui.screenshot()
		img_rgb = np.array(im)
		img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
		print("Gap boss :", r_image.split("/")[-1])
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		cv2.rectangle(img_rgb, (max_loc[0]+20, max_loc[1]), (max_loc[0] + w, max_loc[1] + h), (0,0,255), 2)
		cv2.imwrite("./out/res"+str(count)+".png", img_rgb)
		return max_loc	

def multi_searchimage(image, threshold=0.9):
	print(image)
	r_lst = os.listdir("./r_img")
	img_gray = cv2.imread(image, 0)
	img_rgb = cv2.imread(image, 1)

	for ii in r_lst:
		r_image= "./r_img/"+ii
		# print(ii)
		template = cv2.imread(r_image,0)
		w, h = template.shape[::-1]
		res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		loc = np.where( res >= threshold)
		for pt in zip(*loc[::-1]):
			print(ii,pt[0], pt[1])
			cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
	
	cv2.imwrite("./out/res_"+image.split("/")[-1], img_rgb)

# lst = os.listdir("./img")
# for i in range(0, len(lst)):
# 	os.rename("./img/"+lst[i], "./img/"+str(i)+"."+lst[i].split('.')[-1])
# lst = os.listdir("./img")	
# r_lst = os.listdir("./r_img")
# print(r_lst)
# for img in lst:
# 	multi_searchimage("./img/"+img)

found = False
count = 0
XY = {}
with open("realData.txt","r") as f:
	l = f.readlines()
	for line in l:
		name, x, y = line.strip("\n").split(" ")
		XY[name] = (int(x), int(y))
while 1:
	lst = os.listdir("./boss")
	for img in lst:
		x, y = detect("./boss/"+img,count)
		if(x != -1 and y!=-1):
			count += 1
			try:
				pyautogui.click(x = x+XY[img][0], y = y+XY[img][1],clicks = 2, interval = 0.5)
			except KeyError:
				pass
			print(img, x, y, count)
			found = True
		if(found):
			found = False
			break
	# if(found):
	# 	time.sleep(0)
	# else:
	# 	time.sleep(0)