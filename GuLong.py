from os import remove
from re import L
from PIL.ImageOps import grayscale
import pyautogui
import cv2
import numpy as np
import random

class Location:
    x, y = 0, 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Config:
    interval_use_item = 0.01
    interval_throw = 0.01
    throw = Location(272, 219)
    exchange_nganluong_exp = Location(435, 444)
    accept_exchange = Location(420, 401)
    do_dong_hien = Location(523, 393)
    exp_to_stat = Location(476, 434)
    accept_exp_to_stat = Location(356, 384)

    the_doi_tu_chat = Location(566, 459)
    accept_doi_tu_chat = Location(421, 431)
    tui_pet = Location(622, 466)
    sieu_than_thuy = Location(817, 619)
    accept_sieu_than_thuy = Location(344, 362)

    tu_chat = Location(577, 451)
    accept_use_tan_cong = Location(414, 359)
    accept_use_toc_do = Location(411, 428)
    accept_use_noi_cong = Location(376, 449)

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
        self.DoDongHien = "./Resource/DoDongHien.png"
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
            x, y, w, h = pyautogui.locateOnScreen(self.Opened, confidence = 0.9, grayscale=True)
        except (pyautogui.ImageNotFoundException, TypeError):
            return False
        return True

    def open_bag(self):
        print("trying open bag")
        if(not self.check_bag_is_opened()):
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
    
    def exchange_exp(self):
        delay = 0.25
        (x, y) = pyautogui.locateCenterOnScreen(self.DoDongHien, confidence=0.9, grayscale=True, region=(0,0,900,700))
        pyautogui.moveTo(x, y, 0.1)
        pyautogui.click(x, y, 1, delay, "left")
        pyautogui.click(Config.exchange_nganluong_exp.x, Config.exchange_nganluong_exp.y, 1, delay, "left")
        pyautogui.click(Config.accept_exchange.x, Config.accept_exchange.y, 1, delay, "left")
    
    def exchange_stat(self):
        delay = 0.25
        (x, y) = pyautogui.locateCenterOnScreen(self.DoDongHien, confidence=0.9, grayscale=True, region=(0,0,900,700))
        pyautogui.moveTo(x, y, 0.1)
        pyautogui.click(x, y, 1, delay, "left")
        pyautogui.click(Config.exp_to_stat.x, Config.exp_to_stat.y, 1, delay, "left")
        pyautogui.click(Config.accept_exp_to_stat.x, Config.accept_exp_to_stat.y, 1, delay, "left")
    
    def open_pet(self):
        pyautogui.click(Config.tui_pet.x, Config.tui_pet.y, 1, 0.2, "right")
    
    def doi_pet(self):
        pyautogui.click(Config.the_doi_tu_chat.x, Config.the_doi_tu_chat.y, 1, 0.2, "right")
        pyautogui.click(Config.accept_doi_tu_chat.x, Config.accept_doi_tu_chat.y, 1, 0.2, "left")
    
    def sieu_than_thuy(self):
        pyautogui.click(Config.sieu_than_thuy.x, Config.sieu_than_thuy.y, 1, 0.2, "right")
        pyautogui.click(Config.accept_sieu_than_thuy.x, Config.accept_sieu_than_thuy.y, 1, 0.2, "left")
    
    def tu_chat_tan_cong(self):
        pyautogui.click(Config.tu_chat.x, Config.tu_chat.y, 1, 0.2, "right")
        pyautogui.click(Config.accept_use_tan_cong.x, Config.accept_use_tan_cong.y, 1, 0.2, "left")
    def tu_chat_toc_do(self):
        pyautogui.click(Config.tu_chat.x, Config.tu_chat.y, 1, 0.2, "right")
        pyautogui.click(Config.accept_use_toc_do.x, Config.accept_use_toc_do.y, 1, 0.2, "left")
    
    def detect(self):
        print('Press Ctrl-C to quit.')
        try:
            while True:
                x, y = pyautogui.position()
                positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
                print(positionStr)
                print ('\b' * (len(positionStr) + 2))
        except KeyboardInterrupt:
            print('\n')

def main():
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.25
    Client = GuLong()
    # Client.clean_bag(require_full=False)
    # Client.use_all_item("TuiHoangKim")
    # for i in range(0, 30):
    #     try:
    #         Client.exchange_exp()
    #         Client.exchange_exp()
    #         Client.exchange_stat()
    #     except:
    #         pass

    for i in range(0, 32):
        if(i % 5 == 0):
            Client.open_bag()
            pyautogui.click(599,318,1,0.1) #Tro thu
        try:
            Client.open_pet()
            Client.doi_pet()
        except:
            pass
        if(i % 15 == 14):
            Client.open_pet()
            Client.sieu_than_thuy()

    # for i in range(0, 30):
    #     Client.tu_chat_tan_cong()
    # Client.detect()
    

if __name__ == '__main__':
    main()