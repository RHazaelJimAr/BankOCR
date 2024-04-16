from os.path import dirname, join

"""
OCRDigit object is used to compare digits. Each 3x3 grid is mapped to a number, if current grid does not
match any of the map, it will be set to ?
"""
class OCRDigit:
    DIGITS = {
        (" _ ", "| |", "|_|"): "0",
        ("   ", "  |", "  |"): "1",
        (" _ ", " _|", "|_ "): "2",
        (" _ ", " _|", " _|"): "3",
        ("   ", "|_|", "  |"): "4",
        (" _ ", "|_ ", " _|"): "5",
        (" _ ", "|_ ", "|_|"): "6",
        (" _ ", "  |", "  |"): "7",
        (" _ ", "|_|", "|_|"): "8",
        (" _ ", "|_|", " _|"): "9",
    }

    def __init__(self, lines):
        self.lines = lines

    def to_digit(self):
        return OCRDigit.DIGITS.get(tuple(self.lines), '?')

#Split line into 3x3 grids
def parse_input(input_lines):
    for i in range(0, len(input_lines), 4):
        yield input_lines[i:i+3]

#Convert each 3x3 grid into a digit by calling to_digit from OCRDigit
def parse_account_number(account_lines):
    return ''.join(OCRDigit(account_lines[j][i:i+3] for j in range(3)).to_digit() for i in range(0, 27, 3))

try:
    #Set input by opening the txt file
    current_dir = dirname(__file__)
    file_path = join(current_dir, "./user_story.txt")
    file = open(file_path, "r")
    input_lines = file.readlines()

    #Validate input lengths in file
    for index, line in enumerate(input_lines):
        if(len(line) != 28 and (index+1) % 4 != 0):
            raise Exception("Invalid file. Check your input.")

    #Store all account numbers from file in digits
    account_numbers = [parse_account_number(account_lines) for account_lines in parse_input(input_lines)]

    #Validate account numbers by calculating checksum
    for number in account_numbers:
        if ('?' in str(number)):
            print(number + " ILL")
        else:
            checksum_number = (str(number)[::-1]) #Reverse account digits
            checksum = 0

            #Checksum formula: (1*d1 + 2*d2 + 3*d3 + ... + 9*d9) mod 11 = 0
            for index, digit in enumerate(map(int, checksum_number)):
                checksum += (digit * (index + 1)) #Iterate reversed account number and use index to multiply

            if (checksum % 11 == 0):
                print(number + " OK")
            else:
                print(number + " ERR")
except Exception as e:
    print(str(e))
