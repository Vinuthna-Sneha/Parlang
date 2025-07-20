class Optimizer:
    def __init__(self, ir):
        self.ir = ir

    def optimize(self):
        # Remove redundant stores
        optimized = []
        last_store = None
        for instr in self.ir:
            if instr.startswith("store") and last_store == instr:
                continue
            optimized.append(instr)
            last_store = instr if instr.startswith("store") else None

        # Add parallel annotations
        for i, instr in enumerate(optimized):
            if instr.startswith("parfor"):
                optimized[i] = f"parallel {instr}"
        return optimized