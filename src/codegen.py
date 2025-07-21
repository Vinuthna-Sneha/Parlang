class CodeGenerator:
    def __init__(self, ir):
        self.ir = ir
        self.code = []

    def generate(self):
        for instr in self.ir:
            print(f"Processing IR: {instr}")  # Debug print
            parts = instr.split(", ")
            op = parts[0].split()[0]  # Extract operation (e.g., "parfor" from "parfor n in numbers t5")
            if op == "func":
                self.code.append(f"{instr}:")
            elif op == "endfunc":
                self.code.append("RET")
            elif op == "const":
                if len(parts) != 2:
                    raise ValueError(f"Invalid const instruction: {instr}")
                value = parts[0].split()[1]
                dest = parts[1]
                self.code.append(f"PUSH {value}")
                self.code.append(f"STORE {dest}")
            elif op == "store":
                src = parts[0].split()[1]
                dest = parts[1]
                self.code.append(f"STORE {dest}")
            elif op == "array":
                elements = parts[0].split()[1].split(",")
                dest = parts[1]
                count = parts[2]
                for elem in elements:
                    self.code.append(f"PUSH {elem}")
                self.code.append(f"STORE_ARRAY {dest} {count}")
            elif op == "op":
                op_name, left, right, dest = parts[0].split()[1], parts[1], parts[2], parts[3]
                self.code.append(f"LOAD {left}")
                self.code.append(f"LOAD {right}")
                self.code.append(op_name.upper())
                self.code.append(f"STORE {dest}")
            elif op == "parfor":
                parfor_parts = parts[0].split()
                if len(parfor_parts) != 5 or parfor_parts[2] != "in":
                    raise ValueError(f"Invalid parfor instruction: {instr}")
                var, array, label = parfor_parts[1], parfor_parts[3], parfor_parts[4]
                self.code.append(f"PARFOR {var} {array} {label}:")
            elif op == "endparfor":
                label = parts[0].split()[1]
                self.code.append(f"ENDPARFOR {label}")
            elif op == "print":
                expr = parts[0].split()[1]
                self.code.append(f"LOAD {expr}")
                self.code.append("PRINT")
            elif op == "return":
                expr = parts[0].split()[1]
                self.code.append(f"LOAD {expr}")
                self.code.append("RET")
        return self.code