from os import remove
from re import L
from PIL.ImageOps import grayscale
import pyautogui
import cv2
import numpy as np
import random

from pymsgbox import NO_ICON

class Location:
    x, y = 0, 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Config:
    interval_use_item = 0.01
    interval_throw = 0.01
    throw = Location(272, 219)

class GuLong:
    def __init__(self):
        self.Items = {
            "TuiHoangKim": "./Resource/TuiHoangKim.png",
            "NganLuong": "./Resource/NganLuong.png",
            "TheCuongHoa": "./Resource/TheCuongHoa.png",
            "x10CHB":"./Resource/x10CHB.png",
            "LongLe":"./Resource/LongLe.png",
            "KimToa":"./Resource/KimToa.png",
            "SachXuyenGiap":"./Resource/SachXuyenGiap.png",
            "SachDaiHiep": "./Resource/SachDaiHiep.png",
            "PhuTangToc": "./Resource/PhuTangToc.png"
        }

        self.Trash = [
            "LongLe", "KimToa", "TheCuongHoa", "x10CHB",
            "PhuTangToc", "SachDaiHiep", "SachXuyenGiap"
        ]
        self.Accept = "./Resource/XacNhan.png"
        self.Max = "./Resource/Max.png"
        self.DonDep = "./Resource/DonDep.png"
        self.Empty = "./Resource/Empty.png"
        self.Opened = "./Resource/Opened.png"
        self.Config = Config()
    
    def find_and_click(self, img, button = 'left', confidence = 0.9, clicks=1, interval=0.15):
        x, y = pyautogui.locateCenterOnScreen(img, confidence=confidence, region=(0,0,900,700))
        pyautogui.click(x, y, clicks=clicks, button=button, interval=interval)

    def use_item(self, item_name, clicks=1):
        # print("trying use %s" % (item_name))
        try:
            self.find_and_click(self.Items[item_name], clicks = clicks, button="right")
            return True
        except (pyautogui.ImageNotFoundException, TypeError):
            print("Not found: %s" % (item_name))
            return False
    
    def remove_dup(self, locs):
        if(len(locs) <= 1):
            return locs
        ans = []
        for l in locs:
            if(len(ans) == 0):
                ans.append(l)
            else:
                for j in ans:
                    if(abs(j.top - l.top) == 0 and abs(j.left - l.left) == 0):
                        del j
                    else:
                        if(abs(j.top - l.top) > 5 and abs(j.left - l.left) > 5):
                            ans.append(l)
        return ans

    def throw_item_type_2(self, item_name, im):
        print("trying throw %s" % (item_name))
        try:
            locs = list(pyautogui.locateAll(self.Items[item_name], im, confidence = 0.95))
            locs = self.remove_dup(locs)
            print(locs)
            for (x, y, w, h) in locs:
                pyautogui.click(x + w/2, y + h/2, button='left', interval=0.1)
                pyautogui.click(Config.throw.x, Config.throw.y, button='left', interval=0.1)
                try:
                    self.find_and_click(self.Max)
                    self.find_and_click(self.Accept)
                except (pyautogui.ImageNotFoundException, TypeError):
                    pass

                self.find_and_click(self.Accept)

            return True
        except (pyautogui.ImageNotFoundException, TypeError):
            # print("Not found: %s" % (item_name))
            return False

    def throw_item(self, item_name):
        print("trying throw %s" % (item_name))
        try:
            self.find_and_click(self.Items[item_name])
            pyautogui.click(Config.throw.x, Config.throw.y, button='left')

            try:
                self.find_and_click(self.Max, grayscale=True)
                self.find_and_click(self.Accept, grayscale=True)
            except (pyautogui.ImageNotFoundException, TypeError):
                pass

            self.find_and_click(self.Accept, confidence=0.85)

            return True
        except (pyautogui.ImageNotFoundException, TypeError):
            # print("Not found: %s" % (item_name))
            return False
    
    def clean_bag(self, require_full = False):
        print("trying clean bag")
        if(self.check_bag_is_full() or require_full == False):
            print("Full, start clean bag")
            im = pyautogui.screenshot()
            for trash in self.Trash:
                x = self.throw_item_type_2(trash, im)
                if(x == False):
                    if(not self.check_bag_is_opened()):
                        self.open_bag()
                    self.throw_item_type_2(trash, im)
        else:
            print("Not full, continue")

    
    def check_bag_is_opened(self):
        print("trying check bag is opened")
        try:
            x, y, w, h = pyautogui.locateOnScreen(self.Opened, confidence = 0.9)
        except (pyautogui.ImageNotFoundException, TypeError):
            return False
        return True

    def open_bag(self):
        print("trying open bag")
        pyautogui.hotkey("alt", "e")
    
    def check_bag_is_full(self):
        print("trying check bag is full")
        try:
            x, y, w, h = pyautogui.locateOnScreen(self.Empty, confidence = 0.9)
        except (pyautogui.ImageNotFoundException, TypeError):
            return True
        return False
    
    def use_all_item(self, item_name):
        for i in range(0, 300):
            x = self.use_item(item_name, clicks=1)
            if(x == False):
                if(not self.check_bag_is_opened()):
                    self.open_bag()
                else:
                    break
            if(i % 60 == 0 and i != 0):
                self.clean_bag()

def main():
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.08
    Client = GuLong()
    Client.clean_bag(require_full=False)
    Client.use_all_item("TuiHoangKim")
    

if __name__ == '__main__':
    main()