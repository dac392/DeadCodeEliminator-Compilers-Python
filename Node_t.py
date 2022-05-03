import re
class Node_t:
	"""docstring for Node_t"""
	ARITHMATIC = ["add", "sub", "mult"]
	VOIDABLE = ["loadI", "load"]
	CODE = 0
	def __init__(self, inst, id_num):
		self.inst_string = self.normalize(inst)
		self.inst_id = id_num
		self.mark = False
		self.opcode = None
		self.fields = []
		self.prev = None
		self.next = None
		self.set_fields()


	def set_fields(self):
		string = self.inst_string.split()
		self.opcode = string[self.CODE]

		if(self.opcode == "outputAI"):
			self.fields.append(string[1])
		elif(self.opcode in self.ARITHMATIC):
			self.fields.append(string[1])
			self.fields.append(string[3])
			self.fields.append(string[5])
		else:
			self.fields.append(string[1])
			self.fields.append(string[3])

	def get_readable(self):
		if(self.opcode in self.VOIDABLE):
			return None
		if(self.opcode == "outputAI"):
			return self.fields
		return self.fields[0 : len(self.fields)-1]
	def get_writable(self):
		if(self.opcode == "outputAI"):
			return None
		return self.fields[-1]


	## helper functions
	def normalize(self, instruction):
		statement = ""
		arithmatic_regex = r"^\s*([a-zA-Z]*)\s*(r\d+)\s*,\s*(r?\d+)\s*=>\s*(r\d+)\s*"
		memory_regex = r"^\s*([a-zA-Z]*)\s*(r?\d+)\s*=>\s*(r\d+)\s*,\s*(r?-?\d+)\s*"
		load_regex = r"^\s*([a-zA-Z]*)\s*(r?\d+)\s*=>\s*(r\d+)\s*"
		loadmem_regex = r"^\s*([a-zA-Z]*)\s*(r\d+)\s*,\s*(\d+)\s*=>\s*(r\d+)\s*"
		output_regex = r"^\s*([a-zA-Z]*)\s*(r\d+)\s*,\s*(-?\d+)\s*"

		arith = re.search(arithmatic_regex, instruction)
		memory = re.search(memory_regex, instruction)
		load = re.search(load_regex, instruction)
		load2 = re.search(loadmem_regex, instruction)
		output = re.search(output_regex, instruction)

		if arith != None and "load" not in instruction:
			#print(1)
			statement = re.sub(arithmatic_regex, r"\1 \2 , \3 => \4", instruction)
		elif memory != None:
		    #print(2)
		    statement = re.sub(memory_regex, r"\1 \2 => \3,\4", instruction)
		elif load != None:
		    #print(3)
		    statement = re.sub(load_regex, r"\1 \2 => \3", instruction)
		elif load2 != None:
			statement = re.sub(loadmem_regex, r"\1 \2,\3 => \4",instruction)
		elif output != None:
		    #print(4)
		    statement = re.sub(output_regex, r"\1 \2,\3", instruction)
		else:
			print("I couldn't find anything bro")

		return statement