import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
print(f"WIDTH: {screensize[0]}")
print(f"WIDTH: {screensize[1]}")