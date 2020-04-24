"""CPU functionality."""

import sys
from alu import ALU
program_filename = sys.argv[1]


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # memory or RAM, 256 bytes (1 byte = 8 bits)
        self.running = True
        self.ram = [0] * 256
        self.reg = [0] * 8  # register
        self.sp = 7
        self.reg[self.sp] = 0xf4
        self.pc = 0   # program counter (pc)
        self.alu = ALU(self.running, self.ram, self.reg)
        self.function_table = {}  # * AKA jump table or branch table
        self.function_table[0b01000111] = self.prn
        self.function_table[0b00000001] = self.hlt
        self.function_table[0b01000101] = self.push
        self.function_table[0b01000110] = self.pop
        # * Register functions
        self.function_table[0b10000010] = self.ldi
        self.function_table[0b01010100] = self.jmp
        self.function_table[0b01010000] = self.call
        self.function_table[0b00010001] = self.ret

        self.function_table[0b10100000] = self.alu.add
        self.function_table[0b10100011] = self.alu.div
        self.function_table[0b01100110] = self.alu.dec
        self.function_table[0b01100101] = self.alu.inc
        self.function_table[0b10100100] = self.alu.mod
        self.function_table[0b10100010] = self.alu.mul
        self.function_table[0b10101010] = self.alu.or_bitwise
        self.function_table[0b10101011] = self.alu.xor
        self.function_table[0b10101100] = self.alu.shl
        self.function_table[0b10101101] = self.alu.shr
        self.function_table[0b10100001] = self.alu.sub

    def ram_read(self, address):
        """
        Returns the value (MDR) stored at a memory address (MAR)
        """
        if self.ram[address] is not None:
            return self.ram[address]
        else:
            print(
                f"error, address:{address} either out of bounds or not a valid index")

    def ram_write(self, address, value):
        """Writes a value (MDR =memory data register ) to a memory address register (MAR)."""
        self.ram[address] = value

    def ldi(self, op_a, op_b):  # LDI: load immediate
        self.reg[op_a] = op_b

    def jmp(self, op_a, op_b):
        self.pc = self.reg[op_a]

    def call(self, op_a, op_b):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.pc + 2
        self.jmp(op_a, op_b)

    def ret(self, op_a, op_b):
        value = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1
        self.pc = value

    def prn(self, op_a, op_b):  # Print register[x]
        print(self.reg[op_a])

    def hlt(self, op_a, op_b):  # HALT/STOP
        self.running = False

    def push(self, op_a, op_b):
        self.reg[self.sp] -= 1
        value = self.reg[op_a]
        self.ram[self.reg[self.sp]] = value

    def pop(self, op_a, op_b):
        value = self.ram[self.reg[self.sp]]
        self.reg[op_a] = value
        self.reg[self.sp] += 1

    def load(self,):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8  --> load integer directly into the register
        #     0b00000000,  # op_a  --> address pointer index
        #     0b00001000,  # op_b --> value: 8
        #     0b01000111,  # PRN R0 --> print the value
        #     0b00000000,  # empty
        #     0b00000001,  # HLT  --> halt/stop
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        global program_filename
        with open(program_filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()

                if line == '':
                    continue

                self.ram[address] = int(line)
                address += 1

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        # print(f"TRACE: %02X | %02X %02X %02X |" % (
        print(f"TRACE: %s | %s %s %s |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            # Read the instruction stored in memory
            # *ir == instruction reader
            ir = self.ram_read(self.pc)
            ir_int = int(str(ir), 2)
            if ir_int == 0b01010100 or ir_int == 0b01010000 or ir_int == 0b00010001:
                # these functions intentionally set pc so no need to increment
                increment_by = 0
            else:
                # increment by opcode AND num of variables needed by opcode
                increment_by = 1
                increment_by += (int(str(ir), 2) & 0b11000000) >> 6

            if int(str(ir), 2) in self.function_table:
                ram_a = self.ram_read(self.pc + 1)
                ram_b = self.ram_read(self.pc + 2)
                op_a = int(str(ram_a), 2)
                op_b = int(str(ram_b), 2)
                self.function_table[int(str(ir), 2)](op_a, op_b)

            else:  # Catch invalid / other instruction
                print(
                    f"Unrecognized instruction please review instruction:{ir}(binary) {int(str(ir),2)} decimal")
                self.running = False

            self.pc += increment_by

            # self.trace()
