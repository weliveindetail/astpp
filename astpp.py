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
parser.add_argument("-f", dest="overwrite", action='store_true',
                          help="Force overwrite for output file")

passes_group = parser.add_argument_group("select passes explicitly")
passes_group.add_argument("--process",
  nargs="+", action="extend", default=[],
  help="If omitted they all run",
  choices=[
    "node-ids",
    "source-locs",
    "whitespace"
  ],
)

args = parser.parse_args()

if args.inplace and args.output:
  parser.print_help(sys.stderr)
  sys.exit("\nInvalid arguments provided: please choose either -i or -o")

if not os.path.isfile(args.input):
  sys.exit("Invalid arguments provided: cannot find input file '%s'" % args.input)

if args.output:
  if os.path.exists(args.output):
    if args.overwrite:
      os.remove(args.output)
    else:
      sys.exit("Invalid arguments provided: cannot overwrite output "
              "file '%s' (use -f to force overwrite)" % args.output)

# E.g. replace: 0x1234 -> ID0001
def subst_addrs():
  pattern = re.compile(r'0x[0-9a-f]+')
  subst = 'ID%04i'
  count = 0
  def run(txt):
    nonlocal count
    pos = 0
    while match := pattern.search(txt, pos):
      pos += len(match.group(0))
      if len(re.findall(match.group(0), txt)) == 1:
        # Unique occurrence -> drop
        txt = re.sub(match.group(0), '', txt)
      else:
        # Multiple occurrences -> replace with unique ID string
        count += 1
        txt = re.sub(match.group(0), subst % count, txt)
    return txt
  return run

# E.g. replace: <some.cpp:1:3, col:8> -> <, >
def strip_sourcelocs():
  n = r'[0-9]+'
  col = r'col:' + n
  line = r'line:' + n + ':' + n
  invalid = r'<invalid sloc>'
  filenames = list(map(lambda ext: r'[^ \t<>\(\)]+\.{0}:{1}:{1}'.format(ext, n),
                       ['cpp', 'cc', 'c', 'hpp', 'hh', 'h']))
  brackets = re.compile(r'[ \t]*<[ \t,]*>[ \t]*')
  pattern_strings = [col, line, invalid] + filenames + [brackets]
  patterns = list(map(re.compile, pattern_strings))
  def run(txt):
    for p in patterns:
      while matches := p.findall(txt):
        # Process by descending length to avoid leftovers, e.g. col:1 and col:13
        matches = list(set(matches))
        matches.sort(key=len, reverse=True)
        for match in matches:
          txt = re.sub(match, ' ', txt)
    return txt
  return run

# Trim it
def trailing_whitespace():
  pattern = re.compile(r'[ \t]+\n')
  def run(txt):
    matches = pattern.findall(txt)
    for match in matches:
      txt = re.sub(match, r'\n', txt)
    return txt
  return run

# Build sequence of passes
passes = []
all_passes = (args.process == [])
if all_passes or "node-ids" in args.process:
  passes.append(subst_addrs())
if all_passes or "source-locs" in args.process:
  passes.append(strip_sourcelocs())
if all_passes or "whitespace" in args.process:
  passes.append(trailing_whitespace())

# Run all passes on the file contents
with open(args.input, 'r') as f:
  content = f.read()
  for subst in passes:
    content = subst(content)

# Output the result
if args.output:
  with open(args.output, 'w') as f:
    f.write(content)
elif args.inplace:
  with open(args.input, 'w') as f:
    f.write(content)
else:
  print(content)
