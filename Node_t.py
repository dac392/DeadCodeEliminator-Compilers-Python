import re
class Node_t:
	"""docstring for Node_t"""
	ARITHMATIC = ["add", "sub", "mult"]
	def __init__(self, inst, id_num):
		self.inst_string = self.normalize(inst)
		self.inst_id = id_num
		temp = self.inst_string.split()
		self.opcode = temp[0]
		self.fields = []
		self.next = None

		if(self.opcode == "outputAI"):
			self.fields.append(temp[1])
		elif(self.opcode == "add" or self.opcode == "sub" or self.opcode == "mult"):
			self.fields.append(temp[1])
			self.fields.append(temp[3])
			self.fields.append(temp[5])
		else:
			self.fields.append(temp[1])
			self.fields.append(temp[3])
		
		print()
		print(self.opcode)
		print(self.fields)

	def getReadable(self):
		if(self.opcode in self.ARITHMATIC):
			return [self.fields[0], self.fields[1]]
		return [self.fields[0]]
	def getWritable(self):
		return self.fields[-1]	# should be the last item, I hope





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