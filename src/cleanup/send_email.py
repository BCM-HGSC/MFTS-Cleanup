# import library
import argparse
from pathlib import Path


# creating parser
parser = argparse.ArgumentParser(description='Adding Emails')

# add the argument
parser.add_argument('--email_from', type=str)
parser.add_argument('--rt_number', type=str)
parser.add_argument('--email_send',type=str)
# parser.add_argument('--dir_path', type= path)



# parse the argument
args = parser.parse_args()


# # print [requirement] + user input argument

print('Email from: ' + args.email_from)
print ('For RT#: ' + args.rt_number)
print('Sending to: ' + args.email_send)



# print('Located in directory,' + args.dir_path)

def obtain_dir(directory):
    for d in directory:
        dir_name = Path.dirname(d)
    return dir_name

    # simp_path = input('test/path.py')
    # abs_path = os.path.abspath(simp_path)
    # return (abs_path)

