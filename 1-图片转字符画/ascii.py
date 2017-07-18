import argparse
parser=argparse.ArgumentParser()
parser.add_argument('square',type=int,help='input number and output square')
args=parser.parse_args()
print(args.square**2)
