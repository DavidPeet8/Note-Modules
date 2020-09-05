from colorama import init, Fore, Back, Style
init()

prompt_color = Fore.CYAN + Style.BRIGHT

def print_dir(name):
	print(Fore.BLUE + Style.BRIGHT + name)
	reset_print_style()

def reset_print_style():
	print(Style.RESET_ALL, end="")

def get_prompt(base, path, terminator):
	return prompt_color + base + path + terminator + Style.RESET_ALL

