import os
from typing import List, Optional


# ============================================================
# Lab 5 – Pseudo Random Generators
# ============================================================
#
# Task 1:
#   Generate random bytes using external entropy and write them
#   to a file as hexadecimal values.
#
# Task 2:
#   Implement a Linear Congruential Generator:
#
#       x_next = (a * x + b) mod n
#
# Task 3:
#   Implement Wichmann-Hill generator, based on three LCGs.
# ============================================================


# ============================================================
# Task 1 – External entropy generator
# ============================================================

def get_random_bytes(number_of_bytes: int) -> bytes:
    """
    Reads random bytes from an entropy source.

    On Linux, the lab mentions /dev/random.
    On Windows, /dev/random does not exist, so we use os.urandom(),
    which is the portable Python interface for secure system randomness.
    """

    if number_of_bytes <= 0:
        raise ValueError("number_of_bytes must be greater than 0")

    # Linux / Unix case
    if os.path.exists("/dev/random"):
        with open("/dev/random", "rb") as random_file:
            return random_file.read(number_of_bytes)

    # Windows / portable case
    return os.urandom(number_of_bytes)


def write_entropy_to_hex_file(
    filename: str = "Lab_5/keyFile.txt",
    number_of_bytes: int = 32,
    repetitions: int = 5
) -> None:
    """
    Reads random bytes several times and writes them as hexadecimal strings.

    Example:
        32 bytes = 64 hexadecimal characters
    """

    if repetitions <= 0:
        raise ValueError("repetitions must be greater than 0")

    folder = os.path.dirname(filename)

    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(filename, "w", encoding="utf-8") as key_file:
        for _ in range(repetitions):
            random_data = get_random_bytes(number_of_bytes)
            hex_data = random_data.hex()
            key_file.write(hex_data + "\n")


# ============================================================
# Task 2 – Linear Congruential Generator
# ============================================================

class LCGRandom:
    """
    Linear Congruential Generator.

    Formula:
        x_next = (a * x + b) mod n

    Where:
        seed = initial value
        a    = multiplier
        b    = increment
        n    = modulus
    """

    def __init__(self, seed: int, a: int, b: int, n: int):
        if n <= 0:
            raise ValueError("n must be greater than 0")

        self._seed = seed % n
        self._a = a
        self._b = b
        self._n = n

    def rseed(self, seed: int) -> None:
        """
        Resets the seed.
        """

        self._seed = seed % self._n

    def random(self) -> int:
        """
        Generates the next pseudo-random value.
        """

        self._seed = (self._a * self._seed + self._b) % self._n
        return self._seed

    def generate(self, count: int) -> List[int]:
        """
        Generates a list with count pseudo-random values.
        """

        if count <= 0:
            raise ValueError("count must be greater than 0")

        values = []

        for _ in range(count):
            values.append(self.random())

        return values

    @property
    def state(self) -> int:
        """
        Returns the current internal state.
        """

        return self._seed

    @property
    def parameters(self):
        """
        Returns the parameters of the generator.
        """

        return self._a, self._b, self._n


def check_lcg_period(seed: int, a: int, b: int, n: int, max_steps: Optional[int] = None) -> Optional[int]:
    """
    Checks the period of an LCG.

    The period is the number of generated values after which
    the internal state repeats.

    If max_steps is None, we check at most n + 1 states.
    """

    if max_steps is None:
        max_steps = n + 1

    generator = LCGRandom(seed, a, b, n)

    seen_states = {
        generator.state: 0
    }

    for step in range(1, max_steps + 1):
        generator.random()

        if generator.state in seen_states:
            return step - seen_states[generator.state]

        seen_states[generator.state] = step

    return None


# ============================================================
# Task 3 – Wichmann-Hill Generator
# ============================================================

class WHRandom:
    """
    Wichmann-Hill pseudo-random generator.

    It combines three LCG generators and returns a float in [0, 1).

    Standard formulas:

        x = 171 * x mod 30269
        y = 172 * y mod 30307
        z = 170 * z mod 30323

        result = (x / 30269 + y / 30307 + z / 30323) mod 1
    """

    def __init__(self, seed1: int, seed2: int, seed3: int):
        self._m1 = 30269
        self._m2 = 30307
        self._m3 = 30323

        self._s1 = self._normalize_seed(seed1, self._m1)
        self._s2 = self._normalize_seed(seed2, self._m2)
        self._s3 = self._normalize_seed(seed3, self._m3)

    def _normalize_seed(self, seed: int, modulus: int) -> int:
        """
        Seeds must be between 1 and modulus - 1.
        Zero is avoided because it would keep that LCG stuck at zero.
        """

        seed = seed % modulus

        if seed == 0:
            seed = 1

        return seed

    def random(self) -> float:
        """
        Generates the next pseudo-random number in [0, 1).
        """

        self._s1 = (171 * self._s1) % self._m1
        self._s2 = (172 * self._s2) % self._m2
        self._s3 = (170 * self._s3) % self._m3

        result = (
            self._s1 / self._m1 +
            self._s2 / self._m2 +
            self._s3 / self._m3
        ) % 1.0

        return result

    def generate(self, count: int) -> List[float]:
        """
        Generates a list with count pseudo-random float values.
        """

        if count <= 0:
            raise ValueError("count must be greater than 0")

        values = []

        for _ in range(count):
            values.append(self.random())

        return values


# ============================================================
# Demo / Testing
# ============================================================

def demo_external_entropy() -> None:
    print("=== Task 1: External entropy ===")

    filename = "Lab_5/keyFile.txt"

    write_entropy_to_hex_file(
        filename=filename,
        number_of_bytes=16,
        repetitions=5
    )

    print(f"Random hexadecimal values were written to: {filename}")
    print()


def demo_lcg() -> None:
    print("=== Task 2: Linear Congruential Generator ===")

    seed = 1
    a = 5
    b = 1
    n = 16

    lcg = LCGRandom(seed=seed, a=a, b=b, n=n)

    values = lcg.generate(20)
    period = check_lcg_period(seed=seed, a=a, b=b, n=n)

    print(f"Parameters: seed={seed}, a={a}, b={b}, n={n}")
    print(f"Generated values: {values}")
    print(f"Period: {period}")
    print()

    print("Another example: Lehmer-style generator, where b = 0")

    seed = 1
    a = 3
    b = 0
    n = 31

    lcg = LCGRandom(seed=seed, a=a, b=b, n=n)

    values = lcg.generate(20)
    period = check_lcg_period(seed=seed, a=a, b=b, n=n)

    print(f"Parameters: seed={seed}, a={a}, b={b}, n={n}")
    print(f"Generated values: {values}")
    print(f"Period: {period}")
    print()


def demo_wichmann_hill() -> None:
    print("=== Task 3: Wichmann-Hill Generator ===")

    wh = WHRandom(seed1=1, seed2=2, seed3=3)

    values = wh.generate(10)

    print("Generated values in [0, 1):")

    for value in values:
        print(value)

    print()


def main() -> None:
    demo_external_entropy()
    demo_lcg()
    demo_wichmann_hill()


if __name__ == "__main__":
    main()



## Lab 5 studies pseudo-random generators. 
## First, we generate random bytes from an external entropy source and save them as hexadecimal values.
## Then, we implement a Linear Congruential Generator using the formula x_next = (a * x + b) mod n and test its period.
## Finally, we implement the Wichmann-Hill generator, which combines three LCG generators and produces pseudo-random numbers in the interval [0, 1).