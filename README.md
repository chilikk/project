Dependencies:
- Python 2.5 or higher
- PyCrypto
- NumPy [http://numpy.scipy.org/]
- Multiprocessing [http://pypi.python.org/pypi/multiprocessing/] (included in Python core since version 2.7)
- PySNMP [http://pysnmp.sourceforge.net/] (included in the software distribution)
- PyASN1 [http://pyasn1.sourceforge.net/] (included in the software distribution)
Exception will be raised if one or more dependencies are not met.

To run the project:
1. First run 'main.py' to detect the topology and save in to the file (default 'routers.dat')
$ python main.py
2. Any of the 'task1.py', 'task2.py', 'task3.py' can be run when 'main.py' successfully finished its job:
$ python task1.py

Only data which is necessary for building a plot is output to STDOUT. Everything else is output to STDERR. If everything needs to be redirected to STDOUT, should be invoked as follow:
$ python task2.py 2>&1
