import sys
from Graph_t import Graph_t

def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def piping():
	contents = []
	while True:
		try:
			line = input()
		except EOFError:
			break
		if len(line.strip()) and "//" not in line:
			contents.append(line)
	return contents


def main(args):
	if(len(args)!=1):
		print_error("Use command python3 deadcode.py < ilocfile\n")
		sys.exit()

	raw_instructions = piping()
	instruction_tree = Graph_t(raw_instructions)
	instruction_tree.serialize()
	instruction_tree.print_graph()









if __name__ == '__main__':
	main(sys.argv)