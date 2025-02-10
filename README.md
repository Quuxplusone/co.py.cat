co.py.cat
=========

An implementation of [Douglas Hofstadter](http://prelectur.stanford.edu/lecturers/hofstadter/)'s Copycat algorithm.
The Copycat algorithm is explained [on Wikipedia](https://en.wikipedia.org/wiki/Copycat_%28software%29), and that page has many links for deeper reading.

This implementation is a copycat of Scott Boland's [Java implementation](https://archive.org/details/JavaCopycat).
The original Java-to-Python translation work was done by J Alan Brogan (@jalanb on GitHub).
The Java version has a GUI similar to the original Lisp; this Python version has no GUI code built in but can be incorporated into a larger GUI program.

J Alan Brogan writes:
> In cases where I could not grok the Java implementation easily, I took ideas from the
> [LISP implementation](http://web.cecs.pdx.edu/~mm/how-to-get-copycat.html), or directly
> from [Melanie Mitchell](https://en.wikipedia.org/wiki/Melanie_Mitchell)'s book
> "[Analogy-Making as Perception](http://www.amazon.com/Analogy-Making-Perception-Computer-Melanie-Mitchell/dp/0262132893/ref=tmm_hrd_title_0?ie=UTF8&qid=1351269085&sr=1-3)".

For a very large selection of Copycat problems, see Melanie Mitchell's list
[here](https://melaniemitchell.me/ExplorationsContent/analogy-problems.html).
The same list is mirrored as EXAMPLES.txt in this repository.


Running the command-line program
--------------------------------

To clone the repo locally, run these commands:

```
$ git clone https://github.com/Quuxplusone/co.py.cat.git
$ cd co.py.cat/copycat
$ python main.py --iterations 10 abc abd ppqqrr
```

The script takes three non-named arguments.
The first two are a pair of strings with some change, for example "abc" and "abd".
The third is a string which the script should try to change analogously.

This might produce output such as

```
ppqqss: 6 (avg time 869.0, avg temp 23.4)
ppqqrs: 4 (avg time 439.0, avg temp 37.3)
```

The first number indicates how many times Copycat chose that string as its answer; higher means "more obvious".
The last number indicates the average final temperature of the workspace; lower means "more elegant".


Running the `curses` interface
------------------------------

Follow the instructions to clone the repo as above, but then run `curses_main` instead of `main`:

```
$ git clone https://github.com/Quuxplusone/co.py.cat.git
$ cd co.py.cat/copycat
$ python curses_main.py abc abd ppqqrr
```

This script takes only three arguments.
The first two are a pair of strings with some change, for example "abc" and "abd".
The third is a string which the script should try to change analogously.
The number of iterations is always implicitly "infinite".
To kill the program, hit Ctrl+C.


Installing the module
---------------------

To install the Python module and get started with it, run these commands:

```
$ pip install -e git+https://github.com/Quuxplusone/co.py.cat.git/#egg=copycat
$ python
>>> from copycat import Copycat
>>> Copycat().run('abc', 'abd', 'ppqqrr', 10)
{'ppqqrs': {'count': 4, 'avgtime': 439, 'avgtemp': 37.3}, 'ppqqss': {'count': 6, 'avgtime': 869, 'avgtemp': 23.4}}
```

The result of `run` is a dict containing the same information as was printed by `main.py` above.
