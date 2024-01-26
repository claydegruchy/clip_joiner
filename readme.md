# clip joiner
## whats it do
this takes two inputs, a `main` file and an `insert` file, then it
1. cuts the `main` file in two at a random point
2. extracts a random 3-5 second clip from the `insert` file
3. puts the extracted clip in between the two `main` file parts with a fade transition

# installation
`pip install -r requirement.txt`

# usage
`python merge.py -h`

eg: 
- whole folder: `python3 merge.py -m main_clips/ -i insert_clips/`
- single files: `python3 merge.py -m myfile.webm -i myinsert.mp4`

# whats the point of this?
[this is why i made this](why.md)