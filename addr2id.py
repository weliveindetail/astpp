#!/usr/bin/env python3

import argparse
import os
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, help='Input file to process')
parser.add_argument("-i", "--inplace", action='store_true',
                          help="Overwrite input file")
parser.add_argument("-o", dest="output", type=str, default=None,
                          help="Output file for results")
args = parser.parse_args()

if args.inplace and args.output:
  parser.print_help(sys.stderr)
  sys.exit("\nInvalid arguments provided: please choose either -i or -o")

if not os.path.isfile(args.input):
  sys.exit("Invalid arguments provided: cannot find input file '%s'" % args.input)

if args.output:
  if os.path.exists(args.output):
    sys.exit("Invalid arguments provided: cannot overwrite output file '%s'" % args.output)

addr_pattern = re.compile(r'0x[0-9a-f]+')
id_pattern = 'ID%04i'
id_count = 0
search_pos = 0

with open(args.input, 'r') as f:
  content = f.read()
  match = addr_pattern.search(content, search_pos)
  while match is not None:
    str = match.group(0)
    search_pos = match.start(0)
    occurrences = len(re.findall(str, content))
    if occurrences == 1:
      content = re.sub(str, '', content)
    else:
      id_count += 1
      content = re.sub(str, id_pattern % id_count, content)
      search_pos += len(id_pattern % id_count)
    match = addr_pattern.search(content, search_pos)

if args.output:
  with open(args.output, 'w') as f:
    f.write(content)
elif args.inplace:
  with open(args.input, 'w') as f:
    f.write(content)
else:
  print(content)
