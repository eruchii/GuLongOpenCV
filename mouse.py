import pyautogui, sys
try:
	while True:
		x, y = pyautogui.position()
		pst = "X : " + str(x).rjust(4) + " Y : " + str(y).rjust(4)
		print(pst, end = '')
		print("\b" * len(pst), end = '', flush = True)
except KeyboardInterrupt:
	print("\n")