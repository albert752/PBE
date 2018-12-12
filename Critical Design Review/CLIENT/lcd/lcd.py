#import lcddriver
import subprocess
from time import *

#lcd = lcddriver.lcd()


def println(text, line):
	#lcd.lcd_display_string(text[:20], line)
	print(text[:20])
	
def print_text(text):
	separated=text.split("\n")
	for i in range(4):
		println(separated[i],i)

def main():
	text=""
	for i in range(4):
		text=text+input()+"\n"
	
	print_text(text)

if __name__ == '__main__':
    main()
