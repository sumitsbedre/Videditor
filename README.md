# videditor 🎬🎥

## Overview
Tired of complicated video editing tasks? Want to quickly cut, extract frames, and merge videos effortlessly? No worries, this repo saves time, buddy 😀😀

This repository contains Python scripts to perform various video editing operations. It simplifies tasks such as cutting videos into smaller parts, extracting frames, and merging frames back into a video. This tool leverages `moviepy` and `opencv-python` libraries to handle video processing and frame manipulation.

## Features
`videditor` provides several key functionalities:
- **Cut Video**: Cut a video into smaller parts based on specified start and end times.
- **Cut Video into Sections**: Divide a video into sections of desired length.
- **Extract Frames**: Extract each frame of a video and save them as image files.
- **Merge Frames**: Merge frames from a folder into a video with a specified frame rate.
- **Handle Missing Frames**: Detect and handle missing frames during the merging process.

## Prerequisites
- Python 3.x
- Required Python libraries: `moviepy`, `opencv-python`

## Installation
Install the required Python libraries using `pip`:
```sh
pip install moviepy opencv-python
