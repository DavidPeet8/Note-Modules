# Preprocessor

Supports the following directives:
```md
1. <!-- [include <list of note names>] --> Inline copy pastes the content of each note name listed in order, equivalent to a C #include preprocessor directive
2. <!-- [link note_name optional_visible_name] --> Creates a link called optional_visible_name if present, other wise called note_name and links to the note called note_name
3. <!-- [image <list of image_name>] --> Inserts image inline, if multiple images are specified, they are placed horizontally adjacent in the note
4. <!-- [nobuild] --> Indicates that the note containing this directive should not be displayed in any filter in the build subtree. The note will still exist under `build/.flat_notes`
```
# Dependencies
This project depends on libc++ (LLVM implementation) due to the use of the filesystem header. To install the required packages run the following command
`sudo apt-get install libc++-10-dev libc++abi-10-dev`
For more information check out:
https://libcxx.llvm.org/docs/UsingLibcxx.html#using-libc-on-linux
https://apt.llvm.org/

<!-- # Testing
To run the suite of tests using google tests, run the following commands:
1. `sudo apt install libgtest-dev`
This will install the google testing libraries under `/usr/src`
2. ```bash
cd /usr/src/googletest/googletest
sudo mkdir build
cd build
sudo mkdir /usr/lib/googletest
```
3. ```bash
sudo cmake ..
sudo make
sudo cp lib/*.a /usr/lib/googletest
```
4. ```bash
sudo mkdir /usr/local/lib/googletest
sudo ln -s /usr/lib/googletest/libgtest.a /usr/local/lib/googletest/libgtest.a
sudo ln -s /usr/lib/googletest/libgtest_main.a /usr/local/lib/googletest/libgtest_main.a
```
5. `cd [back to root of preprocessor directory]`
6. `make test`
7. `./unitTests` -->
