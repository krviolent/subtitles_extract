ffmpeg -i $1 -filter:v "crop=800:150:240:530" -c:a copy $1_"video-cropped.mp4"
#ffmpeg -i $1 -filter:v "crop=800:100:240:580" -c:a copy video-cropped.mp4