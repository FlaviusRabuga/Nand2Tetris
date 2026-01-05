from os import listdir
from os.path import isfile

import constants

ASSEMBLY_FILES_PATH = "./assembly_files/"
ASSEMBLY_FILES_EXTENSION = ".asm"
BINARY_FILES_PATH = "./binary_files/"
BINARY_FILES_EXTENSION = ".hack"
    
def gather_symbols(lines: list, default_symbols: dict) -> tuple:
    """
    Executes the first pass over the input file while building the symbols table and removing comments
    
    :param lines: List containing all raw lines in the .asm input file
    :type lines: list
    :param default_symbols: Dictionary containing the predefined symbols and their values
    :type default_symbols: dict
    :return: A tuple containing a new list of lines (only the mnemonic lines, no comments) and the updated symbol table
    :rtype: tuple
    """
    mnemonics = list()
    symbols_table = default_symbols.copy()
    instruction_counter = 0
    multi_line_comm = False

    for line in lines:
        striped = line.strip(" \r\n\t")

        # skip empty lines or single-line comments
        if len(striped) == 0:
            continue
        elif striped[0] == '/':
            if striped[1] == '/':
                continue
            elif striped[1] == "*":
                multi_line_comm = True
        # skip lines within multi-lines comments
        elif multi_line_comm == True:
            if len(striped) == 2 and striped[0] == "*" and striped[1] == "/":
                multi_line_comm = False
            else:
                continue
        # process a symbol
        elif striped[0] == '(':
            current_symbol = striped.split('(')[1].split(')')[0]
            if current_symbol not in symbols_table:
                symbols_table[current_symbol] = instruction_counter
        # process actual mnemonic line
        else:
            mnemonics.append(striped)
            instruction_counter += 1

    return (mnemonics, symbols_table)

def translate(lines: list,
              symbols_table: dict,
              comp_bits: dict,
              dest_bits: dict,
              jump_bits: dict
              ) -> list:
    """
    Executes the second pass over the input file and translates each line into binary Hack machine code
    
    :param lines: List containing all mnemonic lines in the .asm input file
    :type lines: list
    :param symbols_table: Dictionary that maps a symbol to its value (address)
    :type symbols_table: dict
    :param comp_bits: Dictionary that maps an operation to its binary value
    :type comp_bits: dict
    :param dest_bits: Dictionary that maps a destination to its binary value
    :type dest_bits: dict
    :param jump_bits: Dictionary that maps a jump condition to its binary value
    :type jump_bits: dict
    :return: List of binary instruction for each line of Hack code
    :rtype: list
    """
    binary_mnemonics = []
    new_symbol_address = 16 # Hardcode, language specific

    for line in lines:
        # A-type insctruction
        if line[0] == '@':
            symbol = line.split('@')[1]
            address = 0

            if symbol.isdigit():
                address = int(symbol)
            else:
                if symbol in symbols_table:
                    address = symbols_table[symbol]
                else:
                    address = new_symbol_address
                    symbols_table[symbol] = address
                    new_symbol_address += 1

            bin_mnemonic = '0' + "{:0>15b}".format(address)
            binary_mnemonics.append(bin_mnemonic)

        # C-type instruction
        else:
            dest = ""            
            comp = ""
            jump = ""
            second_op_bit = '0'

            if "=" in line:
                dest = line.split('=')[0]
                comp = line.split('=')[1].split(';')[0]
            else:
                comp = line.split(';')[0]
            if ';' in line:
                jump = line.split(';')[1]
            if 'M' in comp:
                second_op_bit = '1'

            bin_mnemonic = "111" + second_op_bit + comp_bits[comp] + dest_bits[dest] + jump_bits[jump]
            binary_mnemonics.append(bin_mnemonic)

    return binary_mnemonics

if __name__ == '__main__':
    
    assembly_files = listdir(ASSEMBLY_FILES_PATH)
    for file in assembly_files:
        if isfile(ASSEMBLY_FILES_PATH + file) and file.endswith(ASSEMBLY_FILES_EXTENSION):
            symbolic_file = open(ASSEMBLY_FILES_PATH + file)
            lines = symbolic_file.readlines()
            symbols_table = dict()

            (lines, symbols_table) = gather_symbols(lines = lines,
                                                    default_symbols = constants.DEFAULT_SYMBOLS)

            binary_code = translate(lines = lines,
                            symbols_table = symbols_table,
                            comp_bits = constants.COMPARE_BITS,
                            dest_bits = constants.DESTINATION_BITS,
                            jump_bits = constants.JUMP_BITS)
            
            output_file_name = file.split(ASSEMBLY_FILES_EXTENSION)[0] + BINARY_FILES_EXTENSION
            output_file = open(BINARY_FILES_PATH + output_file_name, "w+")
            for i in range(0, len(binary_code)):
                output_file.write(binary_code[i])
                if i < len(binary_code) - 1:
                    output_file.write("\n")

            symbolic_file.close()
            output_file.close()
