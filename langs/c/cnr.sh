# A shortcut to compile and run a c program.
# ./cnr.sh stack

if [ $# -eq 0 ]; then
    echo "Usage: ./cnr.sh program"
    exit 1
fi

PROGRAM_NAME="$1"

gcc $PROGRAM_NAME.c -o $PROGRAM_NAME
./$PROGRAM_NAME
