# subtitles_extract
Tool for extraction hardcoded chinese subtitles from video files with 720p resolution (1280 × 720) based on [EasyOCR](https://github.com/JaidedAI/EasyOCR) tool by [JaidedAI](https://github.com/JaidedAI)

Inspride by [Entrepreneurial Age/创业时代 (2018)](https://www.imdb.com/title/tt9085276/)
 
# Download:
	git clone https://github.com/krviolent/subtitles_extract.git
 	or tap Code -> Download ZIP and extract
# Install requirements:
OS: Windows 10/WSL
Instructions: [Enable and install WSL](https://www.windowscentral.com/install-windows-subsystem-linux-windows-10)

	Install python3, ffmpeg, easyocr (https://github.com/JaidedAI/EasyOCR):
	sudo apt install python3
	sudo apt install ffmpeg
	git clone https://github.com/JaidedAI/EasyOCR.git
	cd EasyOCR
	sudo python3 setup.py install

# Use:
	Tested on WSL Ubuntu 20.04. Meet some difficulties running CUDA on Windows to use GPU for OCR.
	
		bash scripts/run_extract_subs.sh [video.mp4] [episode_number] [duration_of_video_in_seconds] [frame_rate]
		[duration_of_video_in_seconds] - optional argument
		[frame_rate] = 1
	Example:
		bash scripts/run_extract_subs.sh video_ep34.mp4 34 2600
	Divide subs_file_[EP].txt into the timestamps.txt and textonly.txt:
		bash scripts/divide_timestamp_and_text.py [episode_number]

# Steps to extract subtitles into the text file:
	1. crop.sh -> frame_xx/*.jpg
	2. 2580 - 43 minites, 2600 - ok
		python3 easyocr_test.py [episode_number] [duration_in_seconds]
		Output files will saved in files:
			subs/subs_file_[episode_number].txt
			subs/EP.A.[episode_number]/subs_[episode_number].srt
	3. Auto-translate obtained subs using https://translatesubtitles.co/
	 
# Optional (replace names, for example):
	bash scripts/replace.sh
	
	command to replace A -> B:
	sed -i -e 's/[A]/[B]/g' subs_file.srt
	This might not work quite right.
# Info
	Duplicated subs not removed during extraction, because same phrases might be repeated during video.
	Also sometimes recognition accuracy is not sophisticated.
