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

Install emp:
```shell
wget https://raw.githubusercontent.com/emp-toolkit/emp-readme/master/scripts/install.py
python install.py --deps --tool --ot --sh2pc
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
src/ppsat 1 12345  $nvar $nstep $phi # run this in one terminal
src/ppsat 2 12345  $nvar $nstep $phi # run this in another terminal
$nvar: the number of variables of the formulae
$nstep: the maximum number of giant steps that the solver will run. 
$phi: the string of the input formula. The syntax of the formula is the (\(-? [0-9]+\))+
```
