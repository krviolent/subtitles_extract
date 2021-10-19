frame_rate=1
echo "bash cut_to_frame.sh video-crop.mp4 frame_rate folder_frame"
mkdir $3
if [ -z "$2" ]; then 
	echo "var is blank"; 
else 
	echo "var is set to '$1'";
	frame_rate = $2
fi
ffmpeg -i $1 -start_number 1 -vf fps=$frame_rate $3/video-%04d.jpg
rm $1
