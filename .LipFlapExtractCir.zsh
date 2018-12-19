#!/usr/bin/zsh

# Export a selected portion of a lip flap (with full transparency around the rest of the image)
# using an input argument (prepended by -i) and the selection argument 
#
# Selection Argument Syntax: (xpos, ypos, diameter)
#
# Command Usage: command $xpos $ypos $diameter $file(s)

# !!!! NOTE: The circle is drawn from the Center out to any point on the perimeter.
# XPOS & YPOS specify the top-left corner of the Circle (if you were to draw it using a box-like selection (which is the default in GIMP)).

## Save Selection arguments & shift Positional Parameters each time
XPOS=$1
YPOS=$2
DIAMETER=$3
shift
shift
shift

RADIUS=$(($DIAMETER/2))

for item in $@; do
	## Apply operations here
	#
	# Define Mask/Matte from Selection Parameters
	convert -size 1920x1080 canvas:none -fill white -draw "circle $(($XPOS+$RADIUS)),$(($YPOS+$RADIUS)) $(($XPOS+$DIAMETER)),$(($YPOS+$RADIUS))" TEST_MASK.png
	# Create new image from mask and source image
	composite -compose Dst_In  -gravity center \
            TEST_MASK.png  $item -alpha Set  $item
done

rm TEST_MASK.png
