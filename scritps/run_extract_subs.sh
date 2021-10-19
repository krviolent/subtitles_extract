# $1 - file.mp4
echo "$pwd"
if [[ $# -lt 2 ]]; then
	echo "wrong number of arguments!"
	exit 1
fi
bash scripts/crop.sh $1
# $2 - series number
bash scripts/cut_to_frame.sh $1_video-cropped.mp4 1 frame_$2
rm $1_video-cropped.mp4
python3 scripts/easyocr_test.py $2 $3
echo -e "Extracted subtitles saved in $pwd/frame_$2/subs/EP.A.$2"
