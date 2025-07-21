import sys

class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.variables = {}
        self.labels = {}
        self.pc = 0

    def run(self, code):
        if isinstance(code, str) and code.endswith('.vm'):
            with open(code, 'r') as file:
                lines = file.readlines()
        else:
            lines = code.split('\n') if isinstance(code, str) else code
        self.pc = 0
        while self.pc < len(lines):
            instr = lines[self.pc].strip()
            if not instr:
                self.pc += 1
                continue
            parts = instr.split()
            op = parts[0]
            if op == 'PUSH':
                self.stack.append(int(parts[1]))
            elif op == 'STORE':
                self.variables[parts[1]] = self.stack.pop()
            elif op == 'LOAD':
                self.stack.append(self.variables[parts[1]])
            elif op == 'MUL':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a * b)
            elif op == 'STORE_ARRAY':
                dest, count = parts[1], int(parts[2])
                array = [self.stack.pop() for _ in range(int(count))][::-1]
                self.variables[dest] = array
            elif op == 'PARFOR':
                var, array, label = parts[1], parts[2], parts[3].rstrip(':')
                self.labels[label] = self.pc + 1
                array_vals = self.variables[array]
                for val in array_vals:
                    self.variables[var] = val
                    self.pc = self.labels[label]
                    while self.pc < len(lines) and lines[self.pc].strip() != f"ENDPARFOR {label}":
                        self.run([lines[self.pc]])
                    self.pc = self.labels[label] - 1
            elif op == 'ENDPARFOR':
                pass
            elif op == 'PRINT':
                print(self.stack.pop())
            elif op == 'RET':
                break
            else:
                raise ValueError(f"Unknown VM instruction: {instr}")
            self.pc += 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python vm_simulator.py <input_file>")
        sys.exit(1)
    vm = VirtualMachine()
    vm.run(sys.argv[1])