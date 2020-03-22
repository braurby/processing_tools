# Processing tools for Python3

## Requirements
- [Pillow](https://pypi.org/project/Pillow/) `pip3 install pillow`
- [ffmpeg-python](https://pypi.org/project/ffmpeg-python/) `pip3 install ffmpeg-python`
- [ffmpeg](https://formulae.brew.sh/formula/ffmpeg) `brew install ffmpeg`

## Usage
Use from CLI interface.  
Arguments:
- `location` - required argument of files (minimum number 2) or folders with files.
- `-c`, `--caption` - optional argument. Set captions for your input separated by `|`.
- `-o`, `--output` - optional argument. Set the output folder. If empty - parent folder of the first locations argument will be passed.

**Example**  
- Process files from folders:  
`"./test_images/test1 ./test_images/test2 ./test_images/test3" -c "caption_1 | caption_2 | caption_3"`
- Process selected files and set output:  
`"./videos/file_1.mp4 ./videos/file_2.mp4" -o ./some_folder`
