# HTML-Text-Extractor

# Installation
Download all modules
```bash
# If you're using yarn
yarn add "module name"

# If you're using npm
npm install "module name"
```
# Usage
### Instructions: Single File
To create "simply.html" run mParse-html.js

Using the "simple.html" file generated from mParse-html.js run extractData-html.py
```bash
python3 extractData-html.py simple.html
```
Make sure "extractData-html.py" is calling process_file() in order to produce output on a single file

### Instructions: Directory

* Place HTML privacy policies in ./test/data

* Make sure "extractData-html.py" is calling process_directory() in order to produce output on a single file

* Run the command
```bash
python3 extractData-html.py simple.html
```

* The output will be in ./test/data under clean.html and plaintext.txt

