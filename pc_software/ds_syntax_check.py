import os

autogui_map = {"ESCAPE":"escape",
"ESC":"esc",
"ENTER":"enter",
"UP":"up",
"DOWN":"down",
"LEFT":"left",
"RIGHT":"right",
"UPARROW":"up",
"DOWNARROW":"down",
"LEFTARROW":"left",
"RIGHTARROW":"right",
"F1":"f1",
"F2":"f2",
"F3":"f3",
"F4":"f4",
"F5":"f5",
"F6":"f6",
"F7":"f7",
"F8":"f8",
"F9":"f9",
"F10":"f10",
"F11":"f11",
"F12":"f12",
"F13":"f13",
"F14":"f14",
"F15":"f15",
"F16":"f16",
"F17":"f17",
"F18":"f18",
"F19":"f19",
"F20":"f20",
"F21":"f21",
"F22":"f22",
"F23":"f23",
"F24":"f24",
"BACKSPACE":"backspace",
"TAB":"tab",
"CAPSLOCK":"capslock",
"PRINTSCREEN":"printscreen",
"SCROLLLOCK":"scrolllock",
"PAUSE":"pause",
"BREAK":"pause",
"INSERT":"insert",
"HOME":"home",
"PAGEUP":"pageup",
"PAGEDOWN":"pagedown",
"DELETE":"delete",
"END":"end",
"SPACE":"space",
"SHIFT":"shift",
"ALT":"alt",
"GUI":"win",
"WINDOWS":"win",
"CONTROL":"ctrl",
"CTRL":"ctrl",
"MK_VOLUP":"volumeup",
"MK_VOLDOWN":"volumedown",
"MK_MUTE":"volumemute",
"MK_PREV":"prevtrack",
"MK_NEXT":"nexttrack",
"MK_PP":"playpause",
"MK_STOP":"stop",
"MENU":"apps",
"APP":"apps",
"NUMLOCK":"numlock",
"KP_SLASH":"/",
"KP_ASTERISK":"*",
"KP_MINUS":"-",
"KP_PLUS":"+",
"KP_ENTER":"enter",
"KP_1":"num1",
"KP_2":"num2",
"KP_3":"num3",
"KP_4":"num4",
"KP_5":"num5",
"KP_6":"num6",
"KP_7":"num7",
"KP_8":"num8",
"KP_9":"num9",
"KP_0":"num0",
"KP_DOT":".",
"KP_EQUAL":"=",
"POWER":""
}

valid_chars = ['!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']

cmd_REPEAT = "REPEAT "
cmd_REM = "REM "
cmd_DEFAULTDELAY = "DEFAULTDELAY "
cmd_DEFAULT_DELAY = "DEFAULT_DELAY "
cmd_DEFAULTCHARDELAY = "DEFAULTCHARDELAY "
cmd_DELAY = "DELAY "
cmd_STRING = "STRING "
cmd_UARTPRINT = "UARTPRINT "
cmd_HOLD = "HOLD "
cmd_LOOP = "LOOP"

PARSE_OK = 0
PARSE_ERROR = 1

def parse_combo(combo_line):
	combo_keys = combo_line.split(' ')
	if len(combo_keys) > 6:
		return 1
	for item in [x.lower() for x in combo_keys if x not in autogui_map.keys()]:
		if item not in valid_chars:
			return 1
	autogui_args = []
	for item in combo_keys:
		if item in autogui_map:
			autogui_args.append(autogui_map[item])
		else:
			autogui_args.append(item.lower())
	return 0

def parse_line(ducky_line):
	parse_result = PARSE_OK
	ducky_line = ducky_line.replace('\n', '').replace('\r', '')
	if not (ducky_line.startswith(cmd_STRING) or ducky_line.startswith(cmd_REM)):
		ducky_line = ducky_line.strip()
	if len(ducky_line) <= 0:
		return PARSE_OK
	elif len(ducky_line) >= 254:
		return PARSE_ERROR
	elif ducky_line.startswith(cmd_REM) or ducky_line.startswith(cmd_UARTPRINT):
		return PARSE_OK
	elif ducky_line.startswith(cmd_LOOP) and ducky_line.endswith(':') and len(ducky_line) == 6 and ducky_line[4].isnumeric():
		return PARSE_OK
	elif ducky_line.startswith(cmd_HOLD):
		sssss = ducky_line[len(cmd_HOLD):].strip().split(' ')
		if len(sssss) > 1:
			return PARSE_ERROR
		if sssss[0] in autogui_map.keys():
			return PARSE_OK
		elif len(sssss[0]) == 1:
			return PARSE_OK
		return PARSE_ERROR
	elif ducky_line.startswith(cmd_STRING):
		return PARSE_OK
	elif ducky_line.startswith(cmd_REPEAT):
		try:
			int(ducky_line[len(cmd_REPEAT):].strip())
		except Exception:
			return PARSE_ERROR
		return PARSE_OK
	elif ducky_line.startswith(cmd_DELAY):
		try:
			if int(ducky_line[len(cmd_DELAY):].strip())/1000 <= 0:
				return PARSE_ERROR
			else:
				return PARSE_OK
		except Exception:
			return PARSE_ERROR
	elif ducky_line.startswith(cmd_DEFAULTDELAY):
		try:
			if int(ducky_line[len(cmd_DEFAULTDELAY):].strip()) <= 0:
				return PARSE_ERROR
			else:
				return PARSE_OK
		except Exception:
			return PARSE_ERROR
	elif ducky_line.startswith(cmd_DEFAULT_DELAY):
		try:
			if int(ducky_line[len(cmd_DEFAULT_DELAY):].strip()) <= 0:
				return PARSE_ERROR
			else:
				return PARSE_OK
		except Exception:
			return PARSE_ERROR
	elif ducky_line.startswith(cmd_DEFAULTCHARDELAY):
		try:
			if int(ducky_line[len(cmd_DEFAULTCHARDELAY):].strip()) <= 0:
				return PARSE_ERROR
			else:
				return PARSE_OK
		except Exception:
			return PARSE_ERROR
	elif ducky_line.split(' ')[0] in autogui_map.keys():
		parse_result = parse_combo(ducky_line)
	else:
		parse_result = PARSE_ERROR
	return parse_result

# content = ''
# with open('test_script.txt') as script_file:
# 	content = script_file.readlines()

# for index, line in enumerate(content):
	# if parse_line(line) != PARSE_OK:
	# 	print("error on line", index, ':', line)
	# print(parse_line(line))
