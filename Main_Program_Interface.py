import sys

if sys.argv.__len__() == 1:
    print(sys.argv[0], "   has to be run with: -c / --close (for close objects) ")
    print("or -f / --far (for far objects) ")

else:
    inp1 = sys.argv[1]

    if inp1 == "-c" or inp1 == "--close":
        print("close objects tracking...")

    elif inp1 == "-f" or inp1 == "--far":
        print("far objects tracking...")

    else:
        print("unknown param input:   (", inp1, ")")
