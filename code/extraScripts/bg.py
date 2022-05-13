fpywXfrom os import popen, chdir
from time import sleep
import pathlib
path = (pathlib.Path(__file__).parent.absolute())
chdir(path)
print(popen('reg add "HKEY_CURRENT_USER\\\\Control Panel\\\\Desktop" /v Wallpaper /t REG_SZ /d C:\\\\Users\\\\failo\\\\AppData\\\\Local\\\\Temp\\\\a905.PNG /f'))
sleep(1)
print(popen('RUNDLL32.EXE user32.dll, UpdatePerUserSystemParameters'))
