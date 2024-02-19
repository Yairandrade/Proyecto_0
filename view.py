from robot_parser import parse_program
import pynput as pynput

def read_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text


file_path = "code.txt"  
input_text = read_file(file_path)
program_results = parse_program(input_text)
print(program_results)

