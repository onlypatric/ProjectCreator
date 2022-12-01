import socket
import sys
from colorama import init, Fore, Back, Style as Style_
from datetime import datetime
import lib.System.out
import lib.Style as Style
import os
import platform
import json
import pyMin.__main__ as minifier


init()

formatOptions = {
    "$T1": f"{Fore.RESET}",
    "$T2": f"{Fore.GREEN}",
    "$T3": f"{Fore.CYAN}",
    "$T4": f"{Fore.BLUE}",
    "$T5": f"{Fore.BLACK}",
    "$T6": f"{Fore.RED}",
    "$T7": f"{Fore.YELLOW}",
    "$T8": f"{Fore.MAGENTA}",
    "$T9": f"{Fore.WHITE}",
    "$R1": f"{Back.RESET}",
    "$R2": f"{Back.GREEN}",
    "$R3": f"{Back.CYAN}",
    "$R4": f"{Back.BLUE}",
    "$R5": f"{Back.BLACK}",
    "$R6": f"{Back.RED}",
    "$R7": f"{Back.YELLOW}",
    "$R8": f"{Back.MAGENTA}",
    "$R9": f"{Back.WHITE}",
    "$U1": f"{Style_.NORMAL}",
    "$U2": f"{Style_.BRIGHT}",
    "$U3": f"{Style_.DIM}",
    "$U4": f"{Style_.RESET_ALL}",
    "$_": "\n",
    "$$": "$",
    "$A": "&",
    "$B": "|",
    "$C": "(",
    "$D": datetime.now().strftime("%D"),
    "$E": "\x1b",
    "$F": ")",
    "$G": ">",
    "$H": "~",
    "$I": os.getlogin(),
    "$J": socket.gethostname(),
    "$L": "<",
    "$N": f"{os.getcwd().split(':')[0]}",
    "$M": f"{os.getcwd()}",
    "$O": "/{0}/".format(os.getcwd().replace("\\", "/").split("/")[-1]),
    "$P": "=",
    "$Q": " ",
    "$S": datetime.now().strftime("%T"),
    "$V": f"{platform.version()}",
}


class Console:
    def __init__(self) -> None:

        self.clear()
        self.variables = {
            "$FORMAT": "$T2$L$T4$I$T2$G$T7$T6$U3$H$U1$T4$J$T9$Q$U3[$T7$O$T9]$U1$T1$Q$$$Q",
            "$SHOWCODE": "True",
            "$SILENT":"False",
        }
        self.variables.update({
            "$VAR":self.variables
        })
        self.last: str = None
        self.lastAsArray: "list[str]" = None
        self.path = os.environ["PATH"].split(";")
        self.path.append(os.getcwd())
        self.main()

    def clear(self):
        os.system("cls")

    def update(self) -> None:
        self.path = os.environ["PATH"].split(";")
        self.path.append(os.getcwd())
        self.variables.update({
                    "$VAR":self.variables
                })
        formatOptions.update({
            "$D": datetime.now().strftime("%D"),
            "$S": datetime.now().strftime("%T"),
            "$N": f"{os.getcwd().split(':')[0]}",
            "$M": f"{os.getcwd()}",
            "$O": "/{0}/".format(os.getcwd().replace("\\", "/").split("/")[-1]), })

    def getFileOrDirInfo(self, point: str) -> str:
        x = ""
        tStamp = "GG/MM/YYYY hh:mm:ss"
        if os.path.isfile(point):
            if os.access(point, os.R_OK):
                x += "R"
            else:
                x += "-"
            if os.access(point, os.W_OK):
                x += "W"
            else:
                x += "-"
            if os.access(point, os.F_OK):
                x += "F"
            else:
                x += "-"
            if os.access(point, os.X_OK):
                x += "X"
            else:
                x += "-"
            m_time = os.path.getmtime(point)
            tStamp = datetime.fromtimestamp(m_time).strftime("%D %T")
            type_ = "<FIL>"
        else:
            x = "RWFX"
            tStamp = ""
            type_ = "<DIR>"
        return "%s|%-20s|%-15s|%s" % (x, tStamp, point, type_)

    def get(self, arr: list, pos: int) -> "object|None":
        try:
            return arr[pos]
        except:
            pass

    def isArgument(self, string: str) -> bool:
        return string.startswith("-")

    def readInput(self):
#---------------------- SET RESULT AS 0
        r=0;
#---------------------- UPDATE
        self.update()
#---------------------- FIRST ARRAY SPLIT
        self.lastAsArray = self.last.split()
#---------------------- WRITE IN VARIABLES
        if self.last.startswith("$") and self.last.__contains__(" = ") and self.last.endswith(";"):
            self.variables.update(
                

                {self.lastAsArray[0]: self.last.split(" = ")[1].split(";")[0].replace("\"","")} if not os.path.exists(self.last.split(" = ")[1].split(";")[0]) else {self.lastAsArray[0]: open(self.last.split(" = ")[1].split(";")[0].replace("\"","")).read()})
            self.update()
            return 
#---------------------- FORMAT VARIABLES TO THEIR VALUE
        for i in self.variables:
            if i in self.last and "vtype" in self.last:
                break
            self.last = self.last.replace(i, str(self.variables.get(i, None)))
#---------------------- SECOND ARRAY SPLIT AFTER VALUE FORMATTING
        self.lastAsArray = self.last.split()
#---------------------- RETURN NOTHING IF COMMAND IS NONE
        if not self.lastAsArray.__len__():
            return self.update()
#---------------------- MOVE ARGUMENTS FURTHER
        for i in self.lastAsArray:
            if self.isArgument(i) and self.lastAsArray.index(i) > 0:
                self.lastAsArray.append(
                    self.lastAsArray.pop(self.lastAsArray.index(i)))
#---------------------- List-Dir command
        if self.lastAsArray[0] == "vtype":
            if self.get(self.lastAsArray,1) is not None:
                e_=str(self.get(self.lastAsArray,1))
                for i in self.variables:
                    e_=e_.replace(i,str(self.variables[i]))
                lib.System.out.println(e_)
            return self.update()
        if self.lastAsArray[0] == "List-Dir" or self.lastAsArray[0]=="ls":
            if "-all" in self.lastAsArray:
                lib.System.out.println(
                    f"\n{Fore.YELLOW}Mode{Fore.RESET}|{Fore.YELLOW}%-20s{Fore.RESET}|{Fore.YELLOW}%-15s{Fore.RESET}|{Fore.YELLOW}%s{Fore.RESET}" % ("Last-Opened", "File-Name", "Type"))
            o = os.listdir(self.get(self.lastAsArray, 1))
            for i, n in zip(os.listdir(self.get(self.lastAsArray, 1)), range(o.__len__())):
                if "-all" in self.lastAsArray:
                    lib.System.out.println(self.getFileOrDirInfo(i))
                else:
                    lib.System.out.print("%s%s%s%s" % (
                        Fore.CYAN if os.path.isdir(i) else Fore.WHITE,
                        i,
                        Fore.RESET,
                        "\n" if n % 5 == 0 and n != 0 else " "
                    ))
            lib.System.out.println("")
            return;
#---------------------- clear command
        elif self.lastAsArray[0] == "clear":
            os.system("cls")
            return;
#---------------------- change directory command
        elif (self.lastAsArray[0]=="Change-Dir" or self.lastAsArray[0]=="cd"):
            if self.get(self.lastAsArray,1) is None:
                self.update()
                lib.System.out.println(os.getcwd())
            else:
                os.chdir(self.get(self.lastAsArray,1))
            self.update()
            return
#---------------------- minify code (python only)
        elif (self.lastAsArray[0]=="minify"):
            if self.get(self.lastAsArray,1) is None:
                self.update()
                return
            if not os.path.exists("minified"):
                os.mkdir("minified")
            minifier.main(["--obfuscate-variables","--destdir","--obfuscate","--obfuscate-import"]+(["--nonlatin",str(self.get(self.lastAsArray,1))]if "--nonlatin" in self.lastAsArray else[str(self.get(self.lastAsArray,1))]))
#---------------------- compile and run for languages: C,C++,Python,Java
        elif (self.lastAsArray[0]=="run"):
            if self.get(self.lastAsArray,1) is None:
                self.update()
                return
            if str(self.get(self.lastAsArray,1)).endswith(".c"):
                if not os.system("gcc {0} -o {1}".format(self.get(self.lastAsArray,1),str(self.get(self.lastAsArray,1)).split(".",1)[0])):
                    if self.variables.get("$SILENT","False")!="True":lib.System.out.println(f"{Fore.GREEN}{Style_.BRIGHT}c file compiled successfully{Fore.RESET}{Style_.NORMAL}")
                    r=os.system("{0}".format(str(self.get(self.lastAsArray,1)).split(".",1)[0]))
                    if self.variables.get("$SILENT","False")=="True":return self.update()
                    if self.variables.get("$SHOWCODE","False")=="False":
                        lib.System.out.print(f"\n{Fore.RED if r!=0 else Fore.GREEN}•{Fore.RESET}")
                    else:
                        lib.System.out.print(f"\nExecuted with status:{Fore.RED if r!=0 else Fore.GREEN}{r}{Fore.RESET}\n")
            elif str(self.get(self.lastAsArray,1)).endswith(".cpp"):
                if not os.system("g++ {0} -o {1}".format(self.get(self.lastAsArray,1),str(self.get(self.lastAsArray,1)).split(".",1)[0])):
                    lib.System.out.println(f"{Fore.GREEN}{Style_.BRIGHT}c++ file compiled successfully{Fore.RESET}{Style_.NORMAL}")
                    r=os.system("{0}".format(str(self.get(self.lastAsArray,1)).split(".",1)[0]))
                    if self.variables.get("$SILENT","False")=="True":return self.update()
                    if self.variables.get("$SHOWCODE","False")=="False":
                        lib.System.out.print(f"\n{Fore.RED if r!=0 else Fore.GREEN}•{Fore.RESET}")
                    else:
                        lib.System.out.print(f"\nExecuted with status:{Fore.RED if r!=0 else Fore.GREEN}{r}{Fore.RESET}\n")
            elif str(self.get(self.lastAsArray,1)).endswith(".java"):
                if not os.system("javac {0}".format(self.get(self.lastAsArray,1),str(self.get(self.lastAsArray,1)).split(".",1)[0])):
                    lib.System.out.println(f"{Fore.GREEN}{Style_.BRIGHT}java class file compiled successfully{Fore.RESET}{Style_.NORMAL}")
                    r=os.system("java {0}".format(str(self.get(self.lastAsArray,1)).split(".",1)[0]))
                    if self.variables.get("$SHOWCODE","False")=="False":
                        lib.System.out.print(f"\n{Fore.RED if r!=0 else Fore.GREEN}•{Fore.RESET}")
                    else:
                        lib.System.out.print(f"\nExecuted with status:{Fore.RED if r!=0 else Fore.GREEN}{r}{Fore.RESET}\n")
            elif str(self.get(self.lastAsArray,1)).endswith(".py"):
                if os.name=="nt":
                    r=os.system("python {0}".format(str(self.get(self.lastAsArray,1))))
                    if self.variables.get("$SILENT","False")=="True":return self.update()
                    if self.variables.get("$SHOWCODE","False")=="False":
                        lib.System.out.print(f"\n{Fore.RED if r!=0 else Fore.GREEN}•{Fore.RESET}")
                    else:
                        lib.System.out.print(f"\nExecuted with status:{Fore.RED if r!=0 else Fore.GREEN}{r}{Fore.RESET}\n")
                else:
                    r=os.system("python3 {0}".format(str(self.get(self.lastAsArray,1))))
                    if self.variables.get("$SILENT","False")=="True":return self.update()
                    if self.variables.get("$SHOWCODE","False")=="False":
                        lib.System.out.print(f"\n{Fore.RED if r!=0 else Fore.GREEN}•{Fore.RESET}")
                    else:
                        lib.System.out.print(f"\nExecuted with status:{Fore.RED if r!=0 else Fore.GREEN}{r}{Fore.RESET}\n")
            elif str(self.get(self.lastAsArray,1)).endswith(".pyw"):
                if os.name=="nt":
                    r=os.system("pythonw {0}".format(str(self.get(self.lastAsArray,1))))
                    if self.variables.get("$SILENT","False")=="True":return self.update()
                    if self.variables.get("$SHOWCODE","False")=="False":
                        lib.System.out.print(f"\n{Fore.RED if r!=0 else Fore.GREEN}•{Fore.RESET}")
                    else:
                        lib.System.out.print(f"\nExecuted with status:{Fore.RED if r!=0 else Fore.GREEN}{r}{Fore.RESET}\n")
                else:
                    r=os.system("pythonw3 {0}".format(str(self.get(self.lastAsArray,1))))
                    if self.variables.get("$SILENT","False")=="True":return self.update()
                    if self.variables.get("$SHOWCODE","False")=="False":
                        lib.System.out.print(f"\n{Fore.RED if r!=0 else Fore.GREEN}•{Fore.RESET}")
                    else:
                        lib.System.out.print(f"\nExecuted with status:{Fore.RED if r!=0 else Fore.GREEN}{r}{Fore.RESET}\n")
        elif (self.lastAsArray[0]=="exit"):
            sys.exit(0)
#---------------------- Use os.system for anything else
        else:
            r=os.system(self.last)
            if self.variables.get("$SILENT","False")=="True":return self.update()
            if self.variables.get("$SHOWCODE","False")=="False":
                lib.System.out.print(f"\n{Fore.RED if r!=0 else Fore.GREEN}•{Fore.RESET}")
            else:
                lib.System.out.print(f"\nExecuted with status:{Fore.RED if r!=0 else Fore.GREEN}{r}{Fore.RESET}\n")

    def format(self, template: str):
        o = template
        for i in formatOptions:
            o = o.replace(i, formatOptions[i])
        return o

    def main(self):
        while True:
            try:
                lib.System.out.print(
                    self.format(self.variables.get(
                        "$FORMAT")).replace("$$", "$"),
                    flush=True
                )
                self.last = input(f"{Style_.BRIGHT}")
                lib.System.out.print(Style_.NORMAL,flush=True)
                self.readInput()
            except KeyboardInterrupt or EOFError:
                break


Console()
