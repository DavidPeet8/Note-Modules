# Preprocessor

This supports the following directives:
1. [//]:# (include [path array])
2. [//]:# (link path)

## Notes: 
All paths must not contain spaces, or must be wrapped in quotations

# Testing
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
7. `./unitTests`