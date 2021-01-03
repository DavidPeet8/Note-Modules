# [Note Modules](https://notes.davidpeet.me)

Note Modules is a note organization and rendering application focused on providing a modular note taking experience. Providing stylish markdown, Note Modules affords both markdown and Latex rendering to provide clean looking notes - especially technical ones.
Designed to avoid data duplication, Note Modules solves issues of taking notes on closely related subjects but only storing data in one location. Note modules accomplishes this by supporting powerful commands enabling

1. Copy paste of one note into another inline
2. Link to another note inline instead of copy pasting
3. Include images

For a complete commands list, view the [preprocessor README](preprocessor/README.md)
Note modules also provides features that improve on the basic markdown syntax including:
1. **Traditional newline semantics** - all newlines in notes are treated as true newlines removing the sloppy antipattern of adding two or more trailing spaces at the end of a line to create a line break
2. A powerful CLI allowing notes to be stored in multiple filters using hard links so that changing any instance of the note will change all instances of the note

## Installation:
After cloning the repo, cd to the root directory of the repo and do the following:
1. Run `./installer.py`
2. Open `~/.bashrc` or another file that gets interpreted on shell creation and append the following:
`PATH=$PATH:~/.notes_cfg/exe:~/.notes_cfg/exe/driver`

Installation is now complete. To run the note cli, run `notes`. Note that you will have to open a new shell or reload the file you appended the previous line to via `source <file name>`


## Dependencies:
To run the installation as mentioned above the following must be installed on the system:
1. Python3 & Pip3
```bash
	sudo apt install python3
	sudo apt install pip3
```
2. Clang C++ Compiler
```bash
	sudo apt install clang
```
3. LLVM C++ Standard Library Implementation Version 10:
```bash
	sudo apt-get install libc++-10-dev libc++abi-10-dev
```
