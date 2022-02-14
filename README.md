# Dependency
Install cmake:
```shell
sudo apt install cmake
```

Install gtest:
```shell
sudo apt install libgtest-dev
cd /usr/src/gtest
sudo cmake CMakeLists.txt
sudo make
sudo cp *.a /usr/lib
```

# Compile
```shell
cmake .
make
```

# Run
Run tests:
```shell
./runTests.sh
```

Evaluate solver on one step:
```shell
src/unit 1 12345 # run this in one terminal
src/unit 2 12345 # run this in another terminal
```
