"""CPU functionality."""
import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
ADD = 0b10100000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # self.registers = [0] * 8
        # self.registers[7] = 0xF4
        # self.pc = 0
        # self.ram = [0] * 256
        # self.halted = False
# _________________________________________________________________
        self.ram = [0] * 256
        # self.reg = [0, 0, 0, 0, 0, 0, 0, 0xF4]
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.IR = 0
        self.MAR = 0
        self.MDR = 0
        self.halted = False
        self.stack_pointer = 7
        self.PRINT_SUB_INSTRUCTION = 11
        self.fl = 0b00000000
        # self.reg[self.stack_pointer] = len(self.ram) - 1
        # LDI = 1
        # HLT = 2
        # PRN = 3

    def load(self, fileName):
        """Load a program into memory."""
        address = 0
        with open(fileName) as my_file:
            # go through each line to parse and get instruction
            for line in my_file:
                # try and get instruction/operand in the line
                comment_split = line.split("#")
                maybe_binary_number = comment_split[0]
                try:
                    x = int(maybe_binary_number, 2)
                    self.ram_write(x, address)
                    address += 1
                except:
                    continue
        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc

        # elif op == "MUL":
        #     self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        #     self.pc += 3

        elif op == "CMP":
            # `00000LGE`
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            else:
                self.fl = 0b00000001
        else:
            raise Exception("Unsupported ALU operation")

            """
            If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
* If registerA is less than registerB, set the Less-than `L` flag to 1,
  otherwise set it to 0.
* If registerA is greater than registerB, set the Greater-than `G` flag
  to 1, otherwise set it to 0.
            """

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()

    # def ram_read(self, address):
    #     return self.ram

    # def ram_write(self, value, address):
    #     self.ram[address] = value

    def run(self):
        while not self.halted:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.execute_instruction(IR, operand_a, operand_b)

    def execute_instruction(self, instruction, operand_a, operand_b):
        # __________________________________________________________________________________________
        """Run the CPU."""
        # running = True
        # while running:
        # IR = self.ram_read(self.pc)
        # operand_a = self.ram_read(self.pc + 1)
        # operand_b = self.ram_read(self.pc + 2)

        if instruction == HLT:
            self.halted = True

        elif instruction == PRN:

            print(self.reg[operand_a])
            self.pc += 2
        elif instruction == LDI:
            self.reg[operand_a] = operand_b
            self.pc += 3
        elif instruction == MUL:
            self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
            self.pc += 3
        elif instruction == PUSH:
            self.reg[self.stack_pointer] -= 1
            self.ram[self.reg[self.stack_pointer]] == self.reg[operand_a]
            self.pc += 2
        elif instruction == POP:
            self.reg[operand_a] = self.ram[self.reg[self.stack_pointer]]
            self.reg[self.stack_pointer] += 1
            self.pc += 2
        elif instruction == CALL:
            self.reg[self.stack_pointer] -= 1
            self.ram[self.reg[self.stack_pointer]] = self.pc + 2
            reg_address = self.ram[self.pc + 1]
            self.pc = self.reg[reg_address]
        elif instruction == RET:
            # doesnt take in any operands
            # sets the program counter to it
            self.pc = self.ram[self.reg[self.stack_pointer]]
            # pc = memory[reg[stack pointer register]]
            # pops the topmost element of the stack
            self.reg[self.stack_pointer] += 1
            # reg[stack pointer register] += 1

        # elif instruction == self.PRINT_SUB_INSTRUCTION:
        #     print(" Hi, im a subroutine. Thanks for calling me")
        #     self.pc += 1
        elif instruction == ADD:
            self.alu("ADD", operand_a, operand_b)
            self.pc += 3

        elif instruction == JEQ:
            if self.fl == 0b1:
                self.pc = self.reg[operand_a]
            else:
                self.pc += 2
        elif instruction == JNE:
            if self.fl != 0b1:
                self.pc = self.reg[operand_a]
            else:
                self.pc += 2
        elif instruction == JMP:
            self.pc = self.reg[operand_a]
        elif instruction == CMP:
            self.alu("CMP", operand_a, operand_b)
            self.pc += 3
        else:
            print("how did we get here")

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR, ):
        self.ram[MAR] = MDR
