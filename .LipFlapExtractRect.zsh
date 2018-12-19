#!/usr/bin/zsh

# Export a selected portion of a lip flap (with full transparency around the rest of the image)
# using an input argument (prepended by -i) and the selection argument 
#
# Selection Argument Syntax: (xpos, ypos, width, length)
#
# Command Usage: command $xpos $ypos $width $length $file(s)


## Save Selection arguments & shift Positional Parameters each time
XPOS=$1
YPOS=$2
WIDTH=$3
LENGTH=$4
shift
shift
shift
shift

for item in $@; do
	## Apply operations here
	#
	# Define Mask/Matte from Selection Parameters
	convert -size 1920x1080 canvas:none -fill white -draw "rectangle  $XPOS,$YPOS $(($XPOS+$WIDTH)),$(($YPOS+$LENGTH))" TEST_MASK.png
	composite -compose Dst_In  -gravity center \
            TEST_MASK.png  $item -alpha Set  $item
	#
	# Export as .png file
	
done

rm TEST_MASK.png
