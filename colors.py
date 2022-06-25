def get(backgroundcolor):
	colors = {}
	WHITE = (255, 255, 255)
	AQUA = (0, 255, 255)
	BLACK = (0, 0, 0)
	BLUE = (0, 0, 255)
	BROWN = (165, 42, 42)
	CYAN = (0, 238, 238)
	GOLD = (255, 215, 0)
	GRAY = (128, 128, 128)
	GREEN = (0, 128, 0)
	INDIGO = (75, 0, 130)
	MAGENTA = (255, 0, 255)
	ORANGE = (255, 128, 0)
	PINK = (255, 192, 203)
	PURPLE = (128, 0, 128)
	RED = (255, 0, 0)
	VIOLET = (238, 130, 238)
	YELLOW = (255, 255, 0)
	#Add colors to colors dictionary
	colors['aqua'] = AQUA
	colors['black'] = BLACK
	colors['blue'] = BLUE
	colors['brown'] = BROWN
	colors['cyan'] = CYAN
	colors['gold'] = GOLD
	colors['gray'] = GRAY
	colors['green'] = GREEN
	colors['indigo'] = INDIGO
	colors['magenta'] = MAGENTA
	colors['orange'] = ORANGE
	colors['pink'] = PINK
	colors['purple'] = PURPLE
	colors['red'] = RED
	colors['violet'] = VIOLET
	colors['white'] = WHITE
	colors['yellow'] = YELLOW
	try:
		return colors[backgroundcolor]
	except:
		return colors["white"]