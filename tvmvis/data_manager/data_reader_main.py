import argparse

def main():
    # Create parser
    parser = argparse.ArgumentParser(description="Script to read and store benchmark data into database")

    # Add params
    parser.add_argument(
        "--medium",
        action="store_true",
        dest="medium",
        default=False,
        help="Run benchmarks with medium sizes",
    )
    parser.add_argument(
        "--iterations",
        action="store",
        type=int,
        dest="iterations",
        default=-1,
        help="Set the number of iterations",
    )
    parser.add_argument(
        "--jvm",
        "-J",
        dest="jvmFlags",
        required=False,
        default=None,
        help='Pass options to the JVM e.g. -J="-Ds0.t0.device=0:1"',
    )


    args = parser.parse_args()

    # 使用参数
    print(f"Number: {args.num}")
    print(f"Description: {args.description}")

if __name__ == "__main__":
    main()