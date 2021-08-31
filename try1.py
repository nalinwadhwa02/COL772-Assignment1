import json
import re

if __name__ == "__main__" :
    #main function
    with open('assignment_1_data/input.json','r') as input_file:
        input_data = json.load(input_file)
        input_file.close()
    with open('assignment_1_data/output.json','r') as output_file:
        output_data = json.load(output_file)
        output_file.close()

