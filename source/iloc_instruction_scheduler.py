"""
The main file for the instruction scheduler
"""

import argparse, os
import iloc_parser
import dep_graph_gen

DESCRIPTION = """
An instruction scheduler for a single basic block
"""
FILENAME_HELP = """
This argument specifies	 the name of he input file. It is a valid Linux pathname 
elative to the current working directory.
"""
def arguments_parse():
	def is_valid_file(parser, arg):
		if not os.path.exists(arg):
			parser.error("The file %s does not exist!" % arg)
		else:
			return open(arg,"r")

	argument_parser = argparse.ArgumentParser(prog = "llgen", 
											description = DESCRIPTION)
	argument_parser.add_argument("filename", help = FILENAME_HELP, 
		type = lambda x: is_valid_file(argument_parser, x))
	arguments = argument_parser.parse_args()
	return arguments

def main():
	arguments = arguments_parse()
	parser = iloc_parser.IlocParser(arguments.filename)
	instrct_list = parser.parse()
	a_dep_graph_gen = dep_graph_gen.DepGraphGen(instrct_list)
	a_dep_graph_gen.rename()
	# print a_dep_graph_gen.get_instrct_list()

if __name__ == '__main__':
	main()