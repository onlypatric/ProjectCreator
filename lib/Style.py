from colorama import Fore,Back,Style;

def format(t:str,elm:str) -> str:
    return "%s%s%s"% elm % t % Fore.RESET+Back.RESET+Style.NORMAL
