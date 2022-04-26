# import library
import argparse
from pathlib import Path



# # TODO : make neater, possibly allow for user input functionality
# creating parser
parser = argparse.ArgumentParser(description='Adding Emails')

# parse the argument
args = parser.parse_args()

# creating parser
parser = argparse.ArgumentParser(description='Adding Emails')

# add the argument
parser.add_argument('--email_from', type= str)
parser.add_argument('--rt_number', type= str)
parser.add_argument('--email_send',type= str)


# parse the argument
args = parser.parse_args()

# print [requirement] + user input argument
print('Email from: ' + args.email_from)
print('RT number: ' + args.rt_number)
print('Sending to: ' + args.email_send)
# print('Located in directory,' + )

def obtain_dir(directory):
    for d in directory:
        dir_name = Path.dirname(d)
    return dir_name

    # simp_path = input('test/path.py')
    # abs_path = os.path.abspath(simp_path)
    # return (abs_path)



def obtain_info(email_from, rt_num, email_to):
    parser = argparse.ArgumentParser(description='Adding Emails')
    for p in parser:
        args = parser.parse_args()
        parser.add_argument(email_from, type=str)
        parser.add_argument(rt_num, type=str)
        parser.add_argument(email_to ,type=str)
    return p
