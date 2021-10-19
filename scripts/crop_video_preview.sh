#!/bin/sh
# 
# crop_video_preview
# is free software created by Fredrik Ax
# The script depends on ffmpeg
# Feel free to use as you wish!
# 
test -x "`which ffprobe`" && test -x "`which ffplay`" && test -x "`which ffmpeg`" || {
        echo "\n### Error\n#\n# This program relies on ffprobe, ffplay & ffmpeg\n# which could not be found in the path:\n# ($PATH)\n#\n# Please install ffmpeg.\n"
        exit 1
    }

test -e "$1" || {
    echo "\nUSAGE: $0 <infile>\n"
    exit 2
}

eval `ffprobe -loglevel quiet -show_entries format:stream=width,height "$1" | egrep -e '^(width|height)='`
test `expr match "$width" '^[0-9]*$'` -eq 0 -o `expr match "$height" '^[0-9]*$'` -eq 0 && {
    echo "\n### Error\n#\n# Could not get video resoloution of \"$1\"\n# Make sure the infile is a media file with a video stream.\n"
    exit 3
}

dw=$width
dh=$height
dx=0
dy=0

loop=y
while test "$loop" = "y"; do
    echo "\n\ninput file: \"$1\""
    echo "video size: ${width}x${height}\n\nSpecify"

    while test "$loop" = "y"; do
        loop=n
        echo -n "\ncropped Width (2 - $width) [$dw]: "
        read w
        test "$w" = "" && w=$dw
        w=`echo $w | sed -e 's/^00*/0/'`
        test "$w" = "0" || w=`echo $w | sed -e 's/^0*//'`
        test `expr match "$w" '^[0-9]*$'` -eq 0 && w=-1
        test $((w)) -gt 1 && test $((w)) -le $width || { echo "### Bad Width ($w)"; loop=y; } 
    done
    dw=$w
    
    loop=y
    while test "$loop" = "y"; do
        loop=n
        echo -n "\ncropped Height (2 - $height) [$dh]: "
        read h
        test "$h" = "" && h=$dh
        h=`echo $h | sed -e 's/^00*/0/'`
        test "$h" = "0" || h=`echo $h | sed -e 's/^0*//'`
        test `expr match "$h" '^[0-9]*$'` -eq 0 && h=-1
        test "$h" = "0" || w=`echo $w | sed -e 's/^0*//'`
        test $((h)) -gt 1 && test $((h)) -le $height || { echo "### Bad Height ($h)"; loop=y; } 
    done
    dh=$h
    
    loop=y
    while test "$loop" = "y"; do
        loop=n
        echo -n "\ncropped X (0 - $((width-$w))) [$dx]: "
        read x
        test "$x" = "" && x=$dx
        x=`echo $x | sed -e 's/^00*/0/'`
        test "$x" = "0" || x=`echo $x | sed -e 's/^0*//'`
        test `expr match "$x" '^[0-9]*$'` -eq 0 && x=-1
        test $((x)) -ge 0 && test $((x+w)) -le $width || {
                echo "### Bad X ($x)"
                test $((x+w)) -le $width || echo "(<x> + <cropped_width> can't be larger than <original_width>)";
                loop=y
            }
    done
    dx=$x
    
    loop=y
    while test "$loop" = "y"; do
        loop=n
        echo -n "\ncropped Y (0 - $((height-h))) [$dy]: "
        read y
        test "$y" = "" && y=$dy
        y=`echo $y | sed -e 's/^00*/0/'`
        test "$y" = "0" || y=`echo $y | sed -e 's/^0*//'`
        test `expr match "$y" '^[0-9]*$'` -eq 0 && y=-1
        test $((y)) -ge 0 && test $((y+h)) -le $height || {
                echo "### Bad Y ($y)"
                test $((y+h)) -le $height || echo "(<y> + <cropped_height> can't be larger than <original_height>)";
                loop=y
            }
    done
    dy=$y

    echo "\n+---\n| Previewing video cropped to ${w}x$h positioned at ${x}x$y.\n|\n| During the preview, press 'q' to end it.\n|\n| Press [RETURN] to start the preview or [Crtl]-'c' to abort.\n+---"
    read c

    ffmpeg -loglevel quiet -i "$1" -filter:v "crop=$w:$h:$x:$y" -f matroska - 2>/dev/null | ffplay -loglevel quiet -

    echo -n "Do you need to tweak the parameters? ([y]/n) "
    read loop
    loop=`echo $loop | sed -e 's/^[nN].*/n/'`
    test "$loop" = "n" || loop=y

done

 echo "\n--- Done. Use the following command to crop the video:\n\nffmpeg -i \"$1\" -filter:v \"crop=$w:$h:$x:$y\" <outputfile>\n"
