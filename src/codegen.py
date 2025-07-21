class CodeGenerator:
    def __init__(self, ir):
        self.ir = ir
        self.code = []

    def generate(self):
        for instr in self.ir:
            if instr.startswith("func"):
                self.code.append(f"{instr}")
            elif instr.startswith("endfunc"):
                self.code.append("RET")
            elif instr.startswith("const"):
                _, value, dest = instr.split(", ")
                self.code.append(f"PUSH {value}")
                self.code.append(f"STORE {dest}")
            elif instr.startswith("store"):
                _, src, dest = instr.split(", ")
                self.code.append(f"STORE {dest}")
            elif instr.startswith("array"):
                # Extract elements and destination
                parts = instr.split(", ")
                elements = parts[0].split("[")[1].split("]")[0].split(",")
                dest = parts[1]
                count = parts[2]
                for elem in elements:
                    self.code.append(f"PUSH {elem}")
                self.code.append(f"STORE_ARRAY {dest} {count}")
            elif instr.startswith("op"):
                _, op, left, right, dest = instr.split()
                self.code.append(f"LOAD {left}")
                self.code.append(f"LOAD {right}")
                self.code.append(f"{op.upper()}")
                self.code.append(f"STORE {dest}")
            elif instr.startswith("parfor"):
                _, var, _, array, label = instr.split()
                self.code.append(f"PARFOR {var} {array} {label}")
            elif instr.startswith("endparfor"):
                _, label = instr.split()
                self.code.append(f"ENDPARFOR {label}")
            elif instr.startswith("print"):
                _, expr = instr.split()
                self.code.append(f"LOAD {expr}")
                self.code.append("PRINT")
            elif instr.startswith("return"):
                _, expr = instr.split()
                self.code.append(f"LOAD {expr}")
                self.code.append("RET")
        return self.code