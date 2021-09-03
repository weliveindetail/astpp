#!/bin/bash
#set -x

rm -r generic.*.ast plain.*.ast

# Generate ASTs
clang++ -std=c++11 -fsyntax-only -fno-color-diagnostics -Xclang -ast-dump plain.cpp > plain.in.ast
clang++ -std=c++14 -fsyntax-only -fno-color-diagnostics -Xclang -ast-dump generic.cpp > generic.in.ast

lines_before=$(diff -u generic.in.ast plain.in.ast | wc -l)
echo "Lines before: ${lines_before}"

# Run the post-processing
python3 ../../astpp -o generic.out.ast generic.in.ast
python3 ../../astpp -o plain.out.ast plain.in.ast

lines_after=$(diff -u generic.out.ast plain.out.ast | wc -l)
echo "Lines after: ${lines_after}"

if [ "${lines_before}" -gt "${lines_after}" ]; then
  echo "Works"
else
  echo "Fails"
fi
