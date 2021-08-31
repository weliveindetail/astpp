# addr2id

Clang AST nodes are identified by allocation address at parse-time. Most of them are unique, but a few ones (especially those of interest) are cross-referenced in other nodes. The `addr2id` script removes all unique addresses and replaces the remaining ones with ascending IDs. It greatly improves diffability.
