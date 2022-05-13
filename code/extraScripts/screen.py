fpywXfrom subprocess import call

import mss
with mss.mss() as scr:
    scr.shot()
call(["move", "monitor-1.png", f"C:/Users/Public"], shell=True)