WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
import random
"""BLOCK_MAP = [
	'555555555555',
	'444555555444',
	'333333333333',
	'222222222222',
	'111111111111',
	'            ',
	'            ',
	'            ',
	'            ']"""

def generate_BLOCK_MAP(rows, columns):
    BLOCK_MAP = []
    for i in range(rows):
        if i < 2:
            first = ''.join(str(random.randint(5, 6)) for _ in range(6))
            last = first[::-1]
            row = first + last
        elif 2 <= i < 4:
            first = ''.join(str(random.randint(3, 4)) for _ in range(6))
            last = first[::-1]
            row = first + last
        elif i == 4:
            first = ''.join(str(random.randint(1,2)) for _ in range(6))
            last = first[::-1]
            row = first + last
        else:
            row = ' ' * columns
        BLOCK_MAP.append(row)
    return BLOCK_MAP

# Example usage:
BLOCK_MAP = generate_BLOCK_MAP(9, 12)


BLOCK_LEGEND = {
	'1': 'level1_nobg_b.png',
	'2': 'level2.png',
	'3': 'level3_nobg_b.png',
	'4': 'level4.png',
	'5': 'level5.png',
	'6': 'level6.png',
	'7': 'level7.png'
}

GAP_SIZE = 2
BLOCK_HEIGHT = WINDOW_HEIGHT / len(BLOCK_MAP) - GAP_SIZE
BLOCK_WIDTH = WINDOW_WIDTH / len(BLOCK_MAP[0]) - GAP_SIZE

UPGRADES = ['michael_running','holly','kevin_chilly','toby_hand']
#UPGRADES = ['kevin_chilly']