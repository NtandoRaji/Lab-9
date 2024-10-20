import sys
from typing import List
from subprocess import run

# Parse the output of the closest_pair_algorithm.py script
def parse_output(text: str) -> str:
    tokens = text.split(" ")
    return tokens[-1][:-2]


def main() -> None:
    argv, argc = sys.argv, len(sys.argv)
    if (argc != 2):
        usage(argv)
    
    input_file = argv[1]
    # Set the Python executable based on the platform (python3 for Linux, python for others)
    python_exec = "python3" if sys.platform == "linux" else "python"

    # Open two output files, one for brute force algorithm results and one for optimized algorithm results
    brute_force_file = open("brute_force_cpa.csv", "w")
    optimized_file = open("optimized_cpa.csv", "w")

    # Write headers to both files
    brute_force_file.write("input,time\n")
    optimized_file.write("input,time\n")

    # Define a range of input sizes from 4 to 15 (inclusive)
    input_sizes = [4, 5, 6, 7, 8, 9, 10, 11, 12]

    for input_size in input_sizes:
        # Generate points for each input size by running the generate_points.py script
        run([python_exec, "generate_points.py", f"{input_size}", input_file])

        # Run the visualizer script to display the points generated
        # run([python_exec, "visualiser.py", input_file])
        
        # Run the closest pair algorithm script and capture its output
        process_3 = run([python_exec, "closest_pair_algorithm.py", input_file], capture_output=True, text=True)
        output = process_3.stdout.rstrip().split("\n")

        # Write the parsed output times to the corresponding CSV files
        brute_force_file.write(f"{2 ** input_size},{parse_output(output[0])}\n")
        optimized_file.write(f"{2 ** input_size},{parse_output(output[1])}\n")

    # Close the output files after the loop is complete
    brute_force_file.close()
    optimized_file.close()

    # Generate graphs based on the experiment results stored in the CSV files
    run([python_exec, "AAAgraphGenerator.py", "2", "brute_force_cpa.csv", "optimized_cpa.csv", "Lab9Experiment1"])


# Usage error function
def usage(argv: List[str]) -> None:
    print(f"[!] Usage: {argv[0]} <input file>")
    print(f"[!] Example Usage: {argv[0]} input.csv")
    sys.exit()


if __name__ == '__main__':
    main()
