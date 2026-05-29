PRG Assignment – External Entropy Generator
Name: Claudiu Daniel

The aim of this assignment is to implement a pseudo-random generator that uses external entropy collected from user input. The program logs the time intervals between keyboard and mouse events and stores them in a text file. The PRG then reads this file, hashes its content with SHA-256, and expands the result into an output of n bits.

Files included:
1. real_prg_generator.py – Python implementation of the entropy logger, PRG generator, and tests.
2. readme.txt – short report explaining the work.
3. test_results.txt – generated after running the statistical tests.
4. entropy_log.txt – generated after collecting keyboard/mouse events.

How the program works:
First, the user runs the logger. A small Tkinter window is opened. The user moves the mouse and presses keys inside the window. For every event, the program records the event type, the high-resolution timestamp, the time difference from the previous event, the mouse coordinates, and the key name. These values are written to entropy_log.txt. The most important value is the time difference between events, because human input timing is difficult to predict exactly.

The PRG has a parameter n, representing the required output size in bits. The generator reads entropy_log.txt and computes a SHA-256 digest from the file content. This digest becomes the internal seed. Then the generator expands the seed using SHA-256 in counter mode. For every counter value, it computes SHA256(seed || counter), concatenates the output blocks, and crops the result to exactly n bits.

The simulator includes simple statistical tests for uniform distribution:
1. Monobit test – counts the number of 0 bits and 1 bits.
2. Byte frequency test – counts how often each byte value from 0 to 255 appears and computes a chi-square statistic.
3. Runs test – counts runs of consecutive equal bits.

How to run:
1. Collect entropy:
   python real_prg_generator.py log

2. Generate random bits, for example 128 bits:
   python real_prg_generator.py generate -n 128

3. Run the uniformity tests:
   python real_prg_generator.py test -n 100000

The output of the tests is written to test_results.txt.

Important note:
This implementation is appropriate for a university assignment and demonstrates the idea of using external entropy and a deterministic expansion function. For real production cryptography, standard operating system cryptographic random generators or trusted cryptographic libraries should be used.
