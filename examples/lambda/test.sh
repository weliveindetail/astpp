#!/bin/bash
#set -x

rm -r generic.*.ast plain.*.ast

# Generate ASTs
clang++ -std=c++14 -fsyntax-only -fno-color-diagnostics -Xclang -ast-dump generic.cpp > generic.in.ast
clang++ -std=c++14 -fsyntax-only -fno-color-diagnostics -Xclang -ast-dump plain.cpp > plain.in.ast

lines_before=$(diff -u generic.in.ast plain.in.ast | wc -l)
echo "Lines before: ${lines_before}"

# Run addr2id
python3 ../../addr2id.py -o generic.out.ast generic.in.ast
python3 ../../addr2id.py -o plain.out.ast plain.in.ast

lines_after=$(diff -u generic.out.ast plain.out.ast | wc -l)
echo "Lines after: ${lines_after}"

if [ "${lines_before}" -gt "${lines_after}" ]; then
  echo "Works"
else
  echo "Fails"
fi
