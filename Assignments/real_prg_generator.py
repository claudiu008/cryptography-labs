import argparse
import hashlib
import math
import os
import statistics
import struct
import time
import tkinter as tk
from pathlib import Path


# ============================================================
# Assignment – External-Entropy PRG
# ============================================================
#
# Requirements covered:
#   0) the PRG has parameter n = output size in bits
#   1) logs times between keystrokes or mouse movement
#   2) PRG reads entropy data from the file and generates random numbers
#   3) functions test the uniform distribution of the simulator
#
# The entropy is collected with a small Tkinter window.
# The PRG uses SHA-256 in counter mode:
#
#   block_i = SHA256(seed || counter_i)
#
# where seed = SHA256(entropy_file_content).
#
# This is suitable for a university assignment/demo.
# For production cryptography, use standard OS/library CSPRNGs.
# ============================================================


DEFAULT_ENTROPY_FILE = "entropy_log.txt"


# ============================================================
# Part 1 – External entropy logger
# ============================================================

class EntropyLogger:
    """
    Logs timing information from keyboard presses and mouse movement.

    Every event writes one line to entropy_log.txt:
        event_type,timestamp_ns,delta_ns,x,y,key

    The useful entropy comes mainly from delta_ns, because human input timing
    is difficult to predict exactly.
    """

    def __init__(self, output_file: str = DEFAULT_ENTROPY_FILE):
        self.output_file = output_file
        self.last_time_ns = None
        self.event_count = 0

        self.root = tk.Tk()
        self.root.title("Entropy Logger – PRG Assignment")
        self.root.geometry("700x300")

        self.label = tk.Label(
            self.root,
            text=(
                "Move the mouse inside this window and press keys.\n"
                "The program logs timing intervals into entropy_log.txt.\n\n"
                "Press ESC to stop."
            ),
            font=("Arial", 14),
            justify="center"
        )
        self.label.pack(expand=True)

        self.counter_label = tk.Label(self.root, text="Events logged: 0", font=("Arial", 12))
        self.counter_label.pack(pady=10)

        self.root.bind("<Key>", self._on_key)
        self.root.bind("<Motion>", self._on_mouse_move)

        Path(self.output_file).write_text("", encoding="utf-8")

    def _log_event(self, event_type: str, x: int = 0, y: int = 0, key: str = "") -> None:
        now_ns = time.perf_counter_ns()

        if self.last_time_ns is None:
            delta_ns = 0
        else:
            delta_ns = now_ns - self.last_time_ns

        self.last_time_ns = now_ns
        self.event_count += 1

        line = f"{event_type},{now_ns},{delta_ns},{x},{y},{repr(key)}\n"

        with open(self.output_file, "a", encoding="utf-8") as file:
            file.write(line)

        self.counter_label.config(text=f"Events logged: {self.event_count}")

    def _on_key(self, event) -> None:
        if event.keysym == "Escape":
            self.root.destroy()
            return

        self._log_event(
            event_type="KEY",
            x=getattr(event, "x", 0),
            y=getattr(event, "y", 0),
            key=event.keysym
        )

    def _on_mouse_move(self, event) -> None:
        self._log_event(
            event_type="MOUSE",
            x=event.x,
            y=event.y,
            key=""
        )

    def run(self) -> None:
        print(f"[+] Logging entropy to: {self.output_file}")
        print("[+] Move the mouse / press keys in the opened window.")
        print("[+] Press ESC in the window to stop.")
        self.root.mainloop()
        print(f"[+] Finished. Total events logged: {self.event_count}")


# ============================================================
# Part 2 – PRG based on external entropy file
# ============================================================

class ExternalEntropyPRG:
    """
    PRG that reads entropy from a file and expands it into n bits.

    Steps:
        1. Read raw entropy file bytes.
        2. Hash them with SHA-256 to create an internal seed.
        3. Generate blocks with SHA256(seed || counter).
        4. Concatenate blocks until n bits are available.
    """

    def __init__(self, entropy_file: str = DEFAULT_ENTROPY_FILE):
        self.entropy_file = entropy_file
        self.seed = self._load_seed_from_file(entropy_file)

    def _load_seed_from_file(self, entropy_file: str) -> bytes:
        path = Path(entropy_file)

        if not path.exists():
            raise FileNotFoundError(
                f"Entropy file not found: {entropy_file}. "
                "Run the logger first with: python assignment_prg.py log"
            )

        data = path.read_bytes()

        if len(data) == 0:
            raise ValueError("Entropy file is empty. Collect input events first.")

        return hashlib.sha256(data).digest()

    def generate_bits(self, n: int) -> str:
        """
        Generates n pseudo-random bits.
        """

        if n <= 0:
            raise ValueError("n must be greater than 0.")

        output = bytearray()
        counter = 0

        required_bytes = math.ceil(n / 8)

        while len(output) < required_bytes:
            counter_bytes = struct.pack(">Q", counter)
            block = hashlib.sha256(self.seed + counter_bytes).digest()
            output.extend(block)
            counter += 1

        bits = "".join(format(byte, "08b") for byte in output)

        return bits[:n]

    def generate_bytes(self, n: int) -> bytes:
        """
        Generates enough bytes to contain n bits.
        If n is not divisible by 8, the last byte contains extra unused bits.
        """

        bits = self.generate_bits(n)
        padding = (8 - len(bits) % 8) % 8
        bits = bits + ("0" * padding)

        result = bytearray()

        for i in range(0, len(bits), 8):
            result.append(int(bits[i:i + 8], 2))

        return bytes(result)

    def random_int(self, n: int) -> int:
        """
        Generates an integer from n pseudo-random bits.
        """

        bits = self.generate_bits(n)
        return int(bits, 2)


# ============================================================
# Part 3 – Uniform distribution tests
# ============================================================

def monobit_test(bits: str) -> dict:
    """
    Tests whether 0 and 1 appear with approximately equal frequency.
    """

    zeros = bits.count("0")
    ones = bits.count("1")
    total = len(bits)

    return {
        "total_bits": total,
        "zeros": zeros,
        "ones": ones,
        "zero_ratio": zeros / total,
        "one_ratio": ones / total,
        "absolute_difference": abs(zeros - ones)
    }


def byte_frequency_test(random_bytes: bytes) -> dict:
    """
    Counts byte values 0..255 and computes chi-square statistic.

    For a uniform byte distribution, each byte value should appear
    approximately len(random_bytes) / 256 times.
    """

    if len(random_bytes) == 0:
        raise ValueError("No bytes provided.")

    counts = [0] * 256

    for byte in random_bytes:
        counts[byte] += 1

    expected = len(random_bytes) / 256
    chi_square = sum(((observed - expected) ** 2) / expected for observed in counts)

    return {
        "total_bytes": len(random_bytes),
        "expected_per_value": expected,
        "min_frequency": min(counts),
        "max_frequency": max(counts),
        "mean_frequency": statistics.mean(counts),
        "chi_square": chi_square,
        "counts": counts
    }


def runs_test(bits: str) -> dict:
    """
    Counts runs of consecutive equal bits.
    This is a simple additional check for visible clustering.
    """

    if not bits:
        raise ValueError("No bits provided.")

    runs = 1

    for i in range(1, len(bits)):
        if bits[i] != bits[i - 1]:
            runs += 1

    expected_approx = (len(bits) + 1) / 2

    return {
        "total_bits": len(bits),
        "runs": runs,
        "expected_runs_approx": expected_approx,
        "difference": abs(runs - expected_approx)
    }


def run_uniformity_tests(entropy_file: str, n: int, output_report: str = "test_results.txt") -> None:
    """
    Generates n bits and writes test results to test_results.txt.
    """

    prg = ExternalEntropyPRG(entropy_file)
    bits = prg.generate_bits(n)
    random_bytes = prg.generate_bytes(n)

    mono = monobit_test(bits)
    byte_test = byte_frequency_test(random_bytes)
    runs = runs_test(bits)

    with open(output_report, "w", encoding="utf-8") as file:
        file.write("Uniform Distribution Test Results\n")
        file.write("=================================\n\n")

        file.write("1. Monobit test\n")
        file.write(f"Total bits: {mono['total_bits']}\n")
        file.write(f"Zeros: {mono['zeros']}\n")
        file.write(f"Ones: {mono['ones']}\n")
        file.write(f"Zero ratio: {mono['zero_ratio']:.6f}\n")
        file.write(f"One ratio: {mono['one_ratio']:.6f}\n")
        file.write(f"Absolute difference: {mono['absolute_difference']}\n\n")

        file.write("2. Byte frequency chi-square test\n")
        file.write(f"Total bytes: {byte_test['total_bytes']}\n")
        file.write(f"Expected frequency per byte value: {byte_test['expected_per_value']:.4f}\n")
        file.write(f"Minimum frequency: {byte_test['min_frequency']}\n")
        file.write(f"Maximum frequency: {byte_test['max_frequency']}\n")
        file.write(f"Mean frequency: {byte_test['mean_frequency']:.4f}\n")
        file.write(f"Chi-square statistic: {byte_test['chi_square']:.4f}\n")
        file.write("For 255 degrees of freedom, a value close to 255 is usually reasonable.\n\n")

        file.write("3. Runs test\n")
        file.write(f"Total bits: {runs['total_bits']}\n")
        file.write(f"Number of runs: {runs['runs']}\n")
        file.write(f"Expected approximately: {runs['expected_runs_approx']:.2f}\n")
        file.write(f"Difference: {runs['difference']:.2f}\n\n")

        file.write("First 256 generated bits\n")
        file.write(bits[:256] + "\n")

    print(f"[+] Tests written to: {output_report}")


# ============================================================
# Command-line interface
# ============================================================

def command_log(args) -> None:
    logger = EntropyLogger(args.file)
    logger.run()


def command_generate(args) -> None:
    prg = ExternalEntropyPRG(args.file)
    bits = prg.generate_bits(args.n)
    number = int(bits, 2)

    print(f"Generated {args.n} bits:")
    print(bits)
    print()
    print("As integer:")
    print(number)


def command_test(args) -> None:
    run_uniformity_tests(
        entropy_file=args.file,
        n=args.n,
        output_report=args.output
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="External entropy PRG assignment"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    log_parser = subparsers.add_parser("log", help="Log keyboard/mouse timing entropy")
    log_parser.add_argument("--file", default=DEFAULT_ENTROPY_FILE)
    log_parser.set_defaults(func=command_log)

    generate_parser = subparsers.add_parser("generate", help="Generate n pseudo-random bits")
    generate_parser.add_argument("-n", type=int, required=True, help="Output size in bits")
    generate_parser.add_argument("--file", default=DEFAULT_ENTROPY_FILE)
    generate_parser.set_defaults(func=command_generate)

    test_parser = subparsers.add_parser("test", help="Test uniform distribution")
    test_parser.add_argument("-n", type=int, default=100000, help="Number of bits to test")
    test_parser.add_argument("--file", default=DEFAULT_ENTROPY_FILE)
    test_parser.add_argument("--output", default="test_results.txt")
    test_parser.set_defaults(func=command_test)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
