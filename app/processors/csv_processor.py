import os
import csv
from collections import defaultdict
import random
import string

class CSVProcessor:
    """
    Processes CSV files by reading it in chunks, aggregate number of plays per
    song and writing the results into ASC sort.
    """
    def __init__(self, input_filename, output_filename, chunk_size=1000):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.chunk_size = chunk_size
        self.chunk_files = []
        self.tmp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),\
            'tmp'))

    def _cleanTemp(self, tmp):
        """
        Removes all temporary chunk files.
        """
        if tmp:
            os.remove(self.input_filename)
        for file in self.chunk_files:
            os.remove(file)

    def _mergeChunks(self):
        """
        Merges all the temporary chunk files into the final output file.
        """
        aggregate_data = defaultdict(lambda: defaultdict(int))
        file_pointers = [open(file, 'r') for file in self.chunk_files]
        readers = [csv.reader(fp) for fp in file_pointers]

        for reader in readers:
            for row in reader:
                song, date, total_plays = row[0], row[1], int(row[2])
                aggregate_data[song][date] += total_plays

        with open(self.output_filename, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['Song', 'Date', 'Total Number of Plays for Date'])

            for song in sorted(aggregate_data):
                for date in sorted(aggregate_data[song]):
                    writer.writerow([song, date, aggregate_data[song][date]])

        for fp in file_pointers:
            fp.close()

    def _readChunks(self):
        """
        Reads the input file and write each chunk into a temp file
        """
        with open(self.input_filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)

            letters = string.ascii_lowercase
            random_chunkName = ''.join(random.choice(letters) for i in range(8))

            chunk_data = defaultdict(lambda: defaultdict(int))

            for i, row in enumerate(reader):
                song, date, num_plays = row[0], row[1], int(row[2])
                chunk_data[song][date] += num_plays

                if (i + 1) % self.chunk_size == 0:
                    self.chunk_files.append(self._writeChunks(random_chunkName,\
                        chunk_data))
                    chunk_data = defaultdict(lambda: defaultdict(int))

            if chunk_data:
                self.chunk_files.append(self._writeChunks(random_chunkName,\
                    chunk_data))

    def _writeChunks(self, chunk_name, chunk_data):
        """
        Writes a chunk data to a temporary file.

        Args:
            chunk_data (defaultdict): The data for the current chunk.

        Returns:
            str: The path to the written chunk file.
        """
        chunk_filename = os.path.join(
            self.tmp_dir,
            f"chunk_{chunk_name}_{len(self.chunk_files)}.csv"
        )
        os.makedirs(self.tmp_dir, exist_ok=True)
        with open(chunk_filename, 'w', newline='') as chunk_file:
            writer = csv.writer(chunk_file)
            for song, dates in chunk_data.items():
                for date, total_plays in dates.items():
                    writer.writerow([song, date, total_plays])
        return chunk_filename

    def process(self, tmp=False):
        """
        Processes the input file using the private methods
        """
        self._readChunks()
        self._mergeChunks()
        self._cleanTemp(tmp)
