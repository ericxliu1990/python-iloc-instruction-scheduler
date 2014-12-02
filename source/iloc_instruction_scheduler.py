"""
The main file for the instruction scheduler
"""

import argparse, os
import iloc_parser
import dep_graph_gen
import priority_gen
import scheduler
from subprocess import call

DESCRIPTION = """
An instruction scheduler for a single basic block
"""
FILENAME_HELP = """
This argument specifies	 the name of he input file. It is a valid Linux pathname 
elative to the current working directory.
"""
G_HELP = """
creates a '.dot' file for graphviz
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
	argument_parser.add_argument("-g", help = G_HELP, action = "store_true")
	arguments = argument_parser.parse_args()
	return arguments

def gen_graphviz_file(is_gen_graphviz, instrct_list, filename, offset = 0):
	if is_gen_graphviz:
		dot_file_name = filename.name.replace(".i",".before.dot")
		dot_file = open(dot_file_name, "w")
		dot_file.write("digraph DG {\n")
		for idx, instrct in enumerate(instrct_list):
			dot_file.write('  %s [label="%s:  %s, %s"];\n' % (idx + offset, idx + offset, str(instrct), instrct.priority))
		edge_num = 0
		for idx, instrct in enumerate(instrct_list):
			for another_instrct in instrct.dep_set:
				dot_file.write('  %s -> %s [label="%s, %s"];\n' % (idx + offset, instrct_list.index(another_instrct[0]) + offset, another_instrct[1], another_instrct[2]))
				edge_num += 1
		dot_file.write("}")
		dot_file.close()
		print edge_num
		call(["/usr/local/Cellar/graphviz/2.38.0/Graphviz.app/Contents/MacOS/Graphviz", dot_file_name])

def main():
	arguments = arguments_parse()
	parser = iloc_parser.IlocParser(arguments.filename)
	instrct_list = parser.parse()

	dep_graph_gen.is_gen_graphviz = arguments.g
	priority_gen.is_gen_graphviz = arguments.g
	scheduler.is_gen_graphviz = arguments.g
	a_dep_graph_gen = dep_graph_gen.DepGraphGen(instrct_list)
	a_dep_graph_gen.rename()	
	a_dep_graph_gen.build_dep_graph()

	a_priority_gen = priority_gen.PriorityGen(instrct_list)
	a_priority_gen.compute()

	a_scheduler = scheduler.Scheduler(instrct_list)
	a_scheduler.schedule()
	print a_scheduler.get_schedule_str()

	gen_graphviz_file(arguments.g, instrct_list, arguments.filename)
	# print a_dep_graph_gen.get_instrct_list()
	# print "--------------------------------"
	# for _ in a_dep_graph_gen.instrct_list:
	# 	print _, _.dep_set
if __name__ == '__main__':
	main()