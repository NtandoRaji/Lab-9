import sys
from subprocess import run


def parse_output(text: str) -> str:
    tokens = text.split(" ")
    return tokens[-1][:-2]


def main() -> None:
    python_exec = "python3" if sys.platform == "linux" else "python"
    brute_force_file = open("brute_force_cpa.csv", "w")
    optimized_file = open("optimized_cpa.csv", "w")

    brute_force_file.write("input,time\n")
    optimized_file.write("input,time\n")

    input_sizes = [i for i in range(4, 12)]
    for input_size in input_sizes:
        run([python_exec, "generate_points.py", f"{input_size}", "output.csv"])
        run([python_exec, ".\\visualiser.py", ".\\output.csv"])
        
        process_3 = run([python_exec, "closest_pair_algorithm.py", "output.csv"], capture_output=True, text=True)
        output = process_3.stdout.rstrip().split("\n")

        brute_force_file.write(f"{2 ** input_size},{parse_output(output[0])}\n")
        optimized_file.write(f"{2 ** input_size},{parse_output(output[1])}\n")

    brute_force_file.close()
    optimized_file.close()

    run([python_exec, "AAAgraphGenerator.py", "2", "brute_force_cpa.csv", "optimized_cpa.csv", "Lab9Experiment1"])


if __name__ == '__main__':
    main()
