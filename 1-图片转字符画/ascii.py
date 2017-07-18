import argparse
parser=argparse.ArgumentParser(description="calcute X to the power of Y")
group=parser.add_mutually_exclusive_group()
group.add_argument('-v','--verbose',action='store_true')
group.add_argument('-q','--quiet',action='store_true')
parser.add_argument('x',type=int,help='base')
parser.add_argument('y',type=int,help='exponent')

args=parser.parse_args()
answer=args.x**args.y
if args.quiet:
	print(answer)
elif args.verbose:
	print("{}^{}={}".format(args.x,args.y,answer))
else:
	print("{} to the power {} equals {}".format(args.x,args.y,answer))


