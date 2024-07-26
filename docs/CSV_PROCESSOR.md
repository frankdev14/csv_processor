# CSV Processor Code Review

This CSV processing project bears similarities to another project I was involved in,
where we processed databases on Athena which generated millions of small files that
slowed down the searches, and we needed to create larger files to accelerate the
queries.

A simple and effective solution has been implemented,
which also allows for scalability. The project is structured to be able to run from
anywhere and could even be installed on a system.

## Features

* The process is completely modular and reusable.
* The system is designed to handle large files by allowing users to dynamically adjust the splitting strategy based on the input file size or characteristics. This flexibility enables
efficient processing of files of varying sizes and formats.
* A command-line executable has been generated outside of the app directory, allowing users to run the process using a variety of commands and options. This design enables seamless
integration with existing workflows and scripts.
* A post-execution cleanup process has been integrated to automatically remove temporary files and folders from the tmp directory, ensuring a clean and organized state after processing
is completed.

## Tech

The implementation leverages built-in Python libraries, rather than relying on advanced or esoteric techniques, to provide a concise and readable solution.

The development environment consisted of Ubuntu 24.04 and Python 3.12 with a virtualenv. As such, the solution is expected to be backwards compatible with earlier versions of Python, including those from Python 2.x to Python 3.x.

## Code

In this README, a general analysis will be made of how each file works and their
corresponding functions. However, for more detailed information about each method, it is
recommended to review the code itself and consult the docstrings associated with each
function.


### **Code Analysis for CSVProcessor**

The code is located in `app/processors/csv_processor.py`, is found as the class
that initializes our processor.

**Attributes**

The class consists of the following attributes:

* **`input_filename`**: input file
* **`output_filename`**: output file
* **`chunk_size`**: chunk size, defaults to 1000
* **`chunk_files`**: global list of the class that is initialized empty and where the
names of the chunks to be processed will go
* **`tmp_dir`**: temporary directory where the chunks will go

### **Private methods**

**`_cleanTemp`**: Clean temporary directory method.

**`_mergeChunks`**: Merge Chunks into a single file.

1. **Opens the chunked files**: opens each of the files that have been created in the
temporary directory (`tmp_dir`) and loads them into memory.
2. **Merges the counts**: combines the columns containing the total number of
reproductions made on the same day and with the same name.
3. **Sorts the data**: sorts the data in ascending order (ASC) first by date, then
alphabetically by name.
4. **Saves to output file**: finally, saves all the processed data to the output file
(`output_filename`) that has been specified.

**`_readChunks`**: Read the input file and split for processing

1. **Reads the input file**: reads the entire input file (`input_filename`) and load row by row.
2. **Generates chunks**: depending on the chunk size that has been set (e.g. 1000),
generates smaller chunks from the input data and saves them to a temporary directory
(`tmp_dir`). This chunk names previously generated random names for multiprocessing.
3. **Adds chunk names to list**: adds the name of each chunk to an empty list called
`chunk_files`, which will be used later to keep track of all the chunks that have been
generated.

**`_writeChunks`**: Write the chunk that **`_readChunks`** provide

1. **Writes chunk to file**: writes the specified chunk (e.g. a slice of data) to a new
file in the temporary directory (`tmp_dir`).
2. **Returns file name**: returns the name of the file that was created, which can be
used later to identify the chunk.

### **Public methods**

**`process`**: Public method for processing data

This method is the main entry point for processing data, and it orchestrates the execution of the internal modules in a specific order.

## Explanation of Computational Complexity (Big O)

#### `__init__`

* __Complexity__: \( O(1) \)
* Variable initialization is constant.

#### `_cleanTemp`

* __Complexity__: \( O(n) \), where \( n \) is the number of temporary files.

#### `_mergeChunks`

* __Complexity__: \( O(n \log n + m \log m) \), where \( n \) is the number of songs and \( m \) is the total number of unique dates for all songs.
* Writing the data to the output file is linear with respect to the total number of rows.

#### `_readChunks`

* __Complexity__: \( O(N + k \log k) \), where \( N \) is the total number of rows in the input file and \( k \) is the number of chunks.
* Writing each chunk is linear with respect to the size of the chunk.

#### `_writeChunks`

* __Complexity__: \( O(c) \), where \( c \) is the size of the chunk.
* Writing the chunk data to a temporary file is linear with respect to the size of the chunk.

#### `process`

* __Complexity__: \( O(N + k \log k + n \log n + m \log m) \)
* The total complexity is derived from the complexities of `_readChunks`, `_mergeChunks`, and `_cleanTemp`.
* Most of the processing time is spent reading the input file and merging the temporary files.

### Summary

The code is designed to handle large CSV files by splitting them into chunks, processing them, and then merging them. The main complexity of the processing comes from reading the data and merging the results. The structure of the class and methods ensures that the processing is efficient and scalable.

</br>

# [`Go Back`](../README.md)
