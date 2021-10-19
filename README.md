# subtitles_extract
Tool for extraction hardcoded chinese subtitles from video files with 720p resolution (1280 × 720) based on [EasyOCR](https://github.com/JaidedAI/EasyOCR) tool by [JaidedAI](https://github.com/JaidedAI)
 
# Download:
	git clone https://github.com/krviolent/subtitles_extract.git
 	or Code - Download ZIP and extract
# Install requirements:
	OS: Windows 10/WSL
	[Enable and install WSL](https://www.windowscentral.com/install-windows-subsystem-linux-windows-10)
	Install python3, ffmpeg, easyocr (https://github.com/JaidedAI/EasyOCR):
	sudo apt install python3
	sudo apt install ffmpeg
	python3 -m pip install easyocr

# Use:
	Tested on WSL Ubuntu 20.04. Meet some difficulties running CUDA on Windows to use GPU for OCR.
	
		bash scripts/run_extract_subs.sh [video.mp4] [episode_number] [duration_in_seconds]
	Example:
		bash scripts/run_extract_subs.sh video_ep34.mp4 34 2600

# Steps to extract subtitles into the text file:
	1. crop.sh -> frame_xx/*.jpg
	2. 2580 - 43 minites, 2600 - ok
		python3 easyocr_test.py [episode_number] [duration_in_seconds]
		Output files will saved in files:
			subs/subs_file_[episode_number].txt
			subs/EP.A.[episode_number]/timestamps.txt
			subs/EP.A.[episode_number]/textonly.txt
	3. Subtitle Edit - form srt file, adjust subtitles duration (2000 ms)
	   Auto-translate or use https://translatesubtitles.co/
	 
# Optinal (replace names, for example):
	bash scripts/replace.sh
	
	command to replace A -> B:
	sed -i -e 's/[A]/[B]/g' subs_file.srt
	This might not work quite right.
