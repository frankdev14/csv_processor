from app.processors.csv_processor import CSVProcessor
import argparse


def main():
    """Method for run the csv processor with args
    """
    parser = argparse.ArgumentParser(description="CSV Processor to aggregate \
        play counts")
    parser.add_argument('--input', help="Input CSV File")
    parser.add_argument('--output', help="Output CSV File")
    parser.add_argument('--chunk_size', type=int, default=1000, help="Chunk \
        size for processing, by default: 1000")

    args = parser.parse_args()

    processor = CSVProcessor(args.input, args.output, args.chunk_size)
    processor.process()

if __name__ == "__main__":
    main()