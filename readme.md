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

# whats the point of this?
[this is why i made this](why.md)