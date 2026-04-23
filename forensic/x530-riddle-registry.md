#
- `strings`: print the sequences of printable characters in files
- `exiftool`: Read and write meta information in files

#
`exiftool confidential.pdf | grep "Author" | awk -F': ' '{print $2}' | base64 -d`

#
`strings confidential.pdf | grep "/Author" | awk -F'(' '{print $2}' | sed 's/\\075/=/' | tr -d ')' | base64 -d`
