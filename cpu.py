#!/usr/bin/env python3

# Created by Ryan C.
# Created in May 2022
# Code runner for 8-bit code

import sys
import time


class CPU:
    """_CPU class handling all the CPU operations_

    Raises:
        ValueError: _Error checking if there is any issues with the user-inputted lines of code_
    """

    def __init__(self):
        # RAM
        self.number_of_bytes = 16
        self.memory = ["00000000"] * self.number_of_bytes

        # Program Counter
        self.program_counter = 0b0000

        # General register
        self.register_a = "0b0000"

        # Flags
        self.flag_cf = False
        self.flag_zf = False
        self.flag_halt = False
        self.flag_debug = False

    def load_program(self):
        """_Opens the file and parses it into an array_"""
        try:
            with open(sys.argv[1], "rb") as file_content:
                instruction_array = file_content.readlines()
                file_content.close()
                print("Starting computer...")

            for line in range(self.number_of_bytes):
                try:
                    self.memory[line] = instruction_array[line][:8]
                except IndexError:
                    self.memory[line] = None
            self.execute_program()
        except (IndexError, OSError):
            print("Error: Unable to open file.")
            sys.exit()

    def execute_program(self):
        """_Executes the program written in the opened file, line by line_

        Raises:
            ValueError: _description_
        """
        # Hard-coded instruction set, formatted to 6 characters, accounting
        # for the python prefix of "0b", resulting in a 4 bit binary number
        instruction_set = {
            "NOP": format(int("0000", 2), "#06b"),
            "LDA": format(int("0001", 2), "#06b"),
            "ADD": format(int("0010", 2), "#06b"),
            "SUB": format(int("0011", 2), "#06b"),
            "STA": format(int("0100", 2), "#06b"),
            "LDI": format(int("0101", 2), "#06b"),
            "JMP": format(int("0110", 2), "#06b"),
            "JC": format(int("0111", 2), "#06b"),
            "JZ": format(int("1000", 2), "#06b"),
            "DEBUG": format(int("1001", 2), "#06b"),
            "OUT": format(int("1110", 2), "#06b"),
            "HLT": format(int("1111", 2), "#06b"),
        }

        # Iterating line by line of the given main.bin file.
        while self.flag_halt is not True:
            if self.memory[self.program_counter] is not None:
                try:
                    operator = format(int(self.memory[self.program_counter][:4], 2), "#06b")
                    operand = format(int(self.memory[self.program_counter][4:9], 2), "#06b")
                    if operator == instruction_set["NOP"]:
                        pass
                    elif operator == instruction_set["LDA"]:
                        self.register_a = self.memory[int(operator, 2)][:4]
                    elif operator == instruction_set["ADD"]:
                        self.register_a = format(
                            int(self.register_a, 2) + int(operand, 2), "#06b"
                        )
                        self.flag_zf = int(self.register_a, 2) == 0
                        self.flag_cf = int(self.register_a, 2) > 15
                        if self.flag_cf:
                            self.register_a = self.register_a[:2] + self.register_a[3:]
                        if self.flag_debug:
                            print(f'"A" register value + {operand} = {self.register_a}')
                    elif operator == instruction_set["SUB"]:
                        self.register_a = format(
                            int(self.register_a, 2) - int(operand, 2), "#06b"
                        )
                        if self.flag_debug:
                            print(f'"A" register value - {operand} = {self.register_a}')
                        self.flag_cf = int(self.register_a, 2) < 0
                        self.flag_zf = int(self.register_a, 2) == 0
                    elif operator == instruction_set["STA"]:
                        self.memory[int(operand, 2)] = f"0000{self.register_a[2:]}"
                    elif operator == instruction_set["JMP"]:
                        self.program_counter = int(operand, 2)
                    elif operator == instruction_set["JC"]:
                        if self.flag_cf:
                            self.program_counter = int(operand, 2)
                    elif operator == instruction_set["JZ"]:
                        if self.flag_zf:
                            self.program_counter = int(operand, 2)
                    elif operator == instruction_set["LDI"]:
                        # Set the register A to the operand
                        self.register_a = operand
                        if self.flag_debug:
                            print(f'Updated "A" register to {operand}.')
                    elif operator == instruction_set["DEBUG"]:
                        # Toggle debug mode
                        self.flag_debug = not self.flag_debug
                        print(f"Debug is on: {self.flag_debug}")
                    elif operator == instruction_set["OUT"]:
                        # Output register A to console
                        if self.flag_cf:
                            print(f"Output: {self.register_a}")
                        else:
                            print(f"Output: {self.register_a}")
                    elif operator == instruction_set["HLT"]:
                        # Halt the program
                        self.flag_halt = True
                    else:
                        print(f"Invalid opcode {operator}.")
                        raise ValueError
                except ValueError:
                    print(f"Error in line {self.program_counter}!")
                    self.flag_halt = True
            else:
                self.flag_debug = True

            if self.flag_debug:
                time.sleep(3)
            # If debug mode is on, and any of the flags are enabled, print a warning.
            if self.flag_cf and self.flag_debug:
                print(f"Warning: Carry out detected in line {self.program_counter}.")
                self.flag_cf = False
            elif self.flag_zf and self.flag_debug:
                print(f"Warning: Zero value detected in line {self.program_counter}.")
                self.flag_zf = False
            if self.flag_halt:
                print("Done. Halting Computer...")
                sys.exit()
            self.program_counter += 0b0001


if __name__ == "__main__":
    CPU().load_program()
