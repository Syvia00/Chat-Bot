# Useful links that were used to make this example
https://docs.python-guide.org/writing/structure/  
https://gideonbrimleaf.github.io/2021/01/26/relative-imports-python.html  

https://docs.python.org/3/library/unittest.html  
https://docs.python.org/3/library/unittest.mock.html  


I believe we should also keep all of the empty __init__.py files around in case their systems are using an older version of python3 (perhaps older than 3.3).  


Also make sure when running test code, you use the command line format in the Makefile:  
- python3 -m test.test_work  
Note: the -m and the . instead of / and the lack of .py
