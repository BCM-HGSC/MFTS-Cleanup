# import library
import argparse
import os
# from pathlib import Path

# creating parser
parser = argparse.ArgumentParser(description='Adding Emails')

# add the argument
parser.add_argument('--email_from', type=str)
parser.add_argument('--rt_number', type=str)
parser.add_argument('--email_send',type=str)
# parser.add_argument('--dir_path', type= PosixPath)



# parse the argument
args = parser.parse_args()

# user input for directory path
# import os

# path = input("Enter filepath: ")

# for f in os.listdir(os.path.expanduser(path)):
#     print(f)





# print [requirement] + user input argument
print('Email from: ' + args.email_from)
print('For RT#: ' + args.rt_number)
print('Sending to: ' + args.email_send)
# print('Located in directory,' + args.dir_path)






# parser.add_argument("From", type= str, help = "Receive")

# args = parser.parse_args("Adding Emails")

# print(args.To)
# print(args.From)

# TODO  missing arguments for "To:" and "From"

