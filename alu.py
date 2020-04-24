class ALU:
    def __init__(self, running, ram, register, flags):
        self.running = running
        self.ram = ram
        self.reg = register
        self. fl_reg = flags

        self.less_than = 5
        self.greater_than = 6
        self.equal_to = 7
    #!ALU operations.

    def add(self, reg_a, reg_b):  # !ADD
        self.reg[reg_a] += self.reg[reg_b]

    def div(self, reg_a, reg_b):  # !DIV
        if self.reg[reg_b] == 0:
            self.running = False
            raise ValueError("cannot divide by 0")
        else:
            self.reg[reg_a] = self.reg[reg_a] / self.reg[reg_b]

    def dec(self, reg_a, reg_b):  # !INC  (increment by 1)
        self.reg[reg_a] -= 1

    def inc(self, reg_a, reg_b):  # !INC  (increment by 1)
        self.reg[reg_a] += 1

    def mod(self, reg_a, reg_b):  # !MOD
        if self.reg[reg_b] == 0:
            self.running = False
            raise ValueError("cannot divide by 0")
        else:
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]

    def mul(self, reg_a, reg_b):  # !MUL (multiply)
        self.reg[reg_a] *= self.reg[reg_b]

    def or_bitwise(self, reg_a, reg_b):  # ! OR - bitwise
        self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]

    def xor(self, reg_a, reg_b):  # ! XOR
        self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]

    def shl(self, reg_a, reg_b):  # ! SHL  bitwise shift left
        self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]

    def shr(self, reg_a, reg_b):  # ! SHR  bitwise shift right
        self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]

    def sub(self, reg_a, reg_b):  # ! SUB
        self.reg[reg_a] -= self.reg[reg_b]

    def _cmp(self, reg_a, reg_b):
        value_1 = self.reg[reg_a]
        value_2 = self.reg[reg_b]
        if value_1 == value_2:
            self.fl_reg[self.equal_to] = 1
            self.fl_reg[self.less_than] = 0
            self.fl_reg[self.greater_than] = 0
        elif value_1 < value_2:
            self.fl_reg[self.equal_to] = 0
            self.fl_reg[self.less_than] = 1
            self.fl_reg[self.greater_than] = 0
        elif value_1 > value_2:
            self.fl_reg[self.equal_to] = 0
            self.fl_reg[self.less_than] = 0
            self.fl_reg[self.greater_than] = 1
