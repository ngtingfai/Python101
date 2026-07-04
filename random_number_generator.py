#!/usr/bin/env python3
"""Simple random number generator CLI.

Usage examples:
  python random_number_generator.py --min 1 --max 10 --count 3
  python random_number_generator.py --min 0 --max 1 --float --count 5
"""
import argparse
import random
import sys


def generate_random(min_val, max_val, count=1, as_float=False, seed=None, unique=False):
    if seed is not None:
        random.seed(seed)

    if as_float:
        return [random.uniform(min_val, max_val) for _ in range(count)]

    # integer mode
    min_i = int(min_val)
    max_i = int(max_val)
    if unique:
        pool_size = max_i - min_i + 1
        if count > pool_size:
            raise ValueError('count is larger than the range when unique is requested')
        return random.sample(range(min_i, max_i + 1), count)

    return [random.randint(min_i, max_i) for _ in range(count)]


def parse_args(argv=None):
    p = argparse.ArgumentParser(description='Random number generator')
    p.add_argument('--min', dest='min_val', type=float, default=0, help='Minimum value (inclusive)')
    p.add_argument('--max', dest='max_val', type=float, default=100, help='Maximum value (inclusive for ints)')
    p.add_argument('--count', type=int, default=1, help='How many numbers to generate')
    p.add_argument('--float', action='store_true', dest='as_float', help='Generate floats instead of integers')
    p.add_argument('--seed', type=int, default=None, help='Optional random seed for reproducibility')
    p.add_argument('--unique', action='store_true', help='Require unique integers (only in integer mode)')
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        numbers = generate_random(args.min_val, args.max_val, count=args.count,
                                  as_float=args.as_float, seed=args.seed, unique=args.unique)
    except Exception as e:
        print('Error:', e, file=sys.stderr)
        return 2

    for n in numbers:
        print(n)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
