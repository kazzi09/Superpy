## Three Technical Elements

## 1
Delegate the stock and sales tracking to seperate classes. By doing so from the start it was much
easier to keep oversight of what does what. And I think the end result is much cleaner code. So
called seperation of concerns.

## 2
Structuring SuperPy in such a way that all neccecary data is stored in external files. This makes
initializing and reinitializing SuperPy a breeze. Generate the two classes, clear the files and 
set up the CLI, and done!

## 3
Exporting both sales and stock data as either a graph or JSON file without affecting the CSV files
in use. It was fun to implement (and I learned a lot from it) and I think this is one of the core
strengths of Python.