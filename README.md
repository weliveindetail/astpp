# astpp

A Clang AST dump post-processor that aims to improve results in structural diffs. Please find more details in my blog post: https://weliveindetail.github.io/blog/post/2021/09/03/clang-ast-dump-diffable.html

# Usage

```bash
➜ astpp --help
usage: astpp [-h] [-i] [-o OUTPUT] [-f]
             [--process {node-ids,source-locs,whitespace} [{node-ids,source-locs,whitespace} ...]]
             input

positional arguments:
  input                 Input file to process

optional arguments:
  -h, --help            show this help message and exit
  -i, --inplace         Overwrite input file
  -o OUTPUT             Output file for results
  -f                    Force overwrite for output file

select passes explicitly:
  --process {node-ids,source-locs,whitespace} [{node-ids,source-locs,whitespace} ...]
                        If omitted they all run
```

# Example

```bash
➜ git clone https://github.com/weliveindetail/astpp
➜ cd astpp/examples/lambda && ./test.sh
Lines before:      129
Lines after:       66
Works
```

Diff after processing is:
```diff
--- plain.out.ast	2021-09-02 22:59:35.000000000 +0200
+++ generic.out.ast	2021-09-02 22:59:35.000000000 +0200
@@ -10,36 +10,48 @@
     |       `-MaterializeTemporaryExpr '(lambda at  )' xvalue
     |         `-LambdaExpr '(lambda at  )'
     |           |-CXXRecordDecl implicit class definition
-    |           | |-DefinitionData lambda pass_in_registers empty standard_layout trivially_copyable can_const_default_init
+    |           | |-DefinitionData generic lambda pass_in_registers empty standard_layout trivially_copyable can_const_default_init
     |           | | |-DefaultConstructor defaulted_is_constexpr
     |           | | |-CopyConstructor simple trivial has_const_param implicit_has_const_param
     |           | | |-MoveConstructor exists simple trivial
     |           | | |-CopyAssignment trivial has_const_param needs_implicit implicit_has_const_param
     |           | | |-MoveAssignment
     |           | | `-Destructor simple irrelevant trivial
-    |           | |-CXXMethodDecl ID0003 used operator() 'int (int) const' inline
-    |           | | |-ParmVarDecl ID0004 used argc 'int'
-    |           | | `-CompoundStmt ID0005
-    |           | |   `-ReturnStmt ID0006
-    |           | |     `-ImplicitCastExpr ID0007 'int' <LValueToRValue>
-    |           | |       `-DeclRefExpr ID0008 'int' lvalue ParmVar ID0004 'argc' 'int'
-    |           | |-CXXConversionDecl implicit operator int (*)(int) 'int (*() const noexcept)(int)' inline
-    |           | |-CXXMethodDecl implicit __invoke 'int (int)' static inline
-    |           | | `-ParmVarDecl argc 'int'
+    |           | |-FunctionTemplateDecl operator()
+    |           | | |-TemplateTypeParmDecl ID0003 implicit class depth 0 index 0 argc:auto
+    |           | | |-CXXMethodDecl operator() 'auto (auto) const' inline
+    |           | | | |-ParmVarDecl ID0004 referenced argc 'auto'
+    |           | | | `-CompoundStmt ID0005
+    |           | | |   `-ReturnStmt ID0006
+    |           | | |     `-DeclRefExpr ID0007 'auto' lvalue ParmVar ID0004 'argc' 'auto'
+    |           | | `-CXXMethodDecl ID0008 used operator() 'int (int) const' inline
+    |           | |   |-TemplateArgument type 'int'
+    |           | |   | `-BuiltinType  'int'
+    |           | |   |-ParmVarDecl ID0009 used argc 'int':'int'
+    |           | |   `-CompoundStmt
+    |           | |     `-ReturnStmt
+    |           | |       `-ImplicitCastExpr 'int':'int' <LValueToRValue>
+    |           | |         `-DeclRefExpr 'int':'int' lvalue ParmVar ID0009 'argc' 'int':'int'
+    |           | |-FunctionTemplateDecl implicit operator auto (*)(type-parameter-0-0)
+    |           | | |-TemplateTypeParmDecl ID0003 implicit class depth 0 index 0 argc:auto
+    |           | | `-CXXConversionDecl implicit operator auto (*)(type-parameter-0-0) 'auto (*() const noexcept)(auto)' inline
+    |           | |-FunctionTemplateDecl implicit __invoke
+    |           | | |-TemplateTypeParmDecl ID0003 implicit class depth 0 index 0 argc:auto
+    |           | | `-CXXMethodDecl implicit __invoke 'auto (auto)' static inline
+    |           | |   `-ParmVarDecl argc 'auto'
     |           | |-CXXDestructorDecl implicit referenced ~ 'void () noexcept' inline default trivial
-    |           | |-CXXConstructorDecl ID0009 implicit constexpr  'void (const (lambda at  ) &)' inline default trivial noexcept-unevaluated ID0009
+    |           | |-CXXConstructorDecl ID0010 implicit constexpr  'void (const (lambda at  ) &)' inline default trivial noexcept-unevaluated ID0010
     |           | | `-ParmVarDecl 'const (lambda at  ) &'
     |           | `-CXXConstructorDecl implicit used constexpr  'void ((lambda at  ) &&) noexcept' inline default trivial
     |           |   |-ParmVarDecl '(lambda at  ) &&'
     |           |   `-CompoundStmt
     |           `-CompoundStmt ID0005
     |             `-ReturnStmt ID0006
-    |               `-ImplicitCastExpr ID0007 'int' <LValueToRValue>
-    |                 `-DeclRefExpr ID0008 'int' lvalue ParmVar ID0004 'argc' 'int'
+    |               `-DeclRefExpr ID0007 'auto' lvalue ParmVar ID0004 'argc' 'auto'
     `-ReturnStmt
       `-CXXOperatorCallExpr 'int':'int' '()'
         |-ImplicitCastExpr 'int (*)(int) const' <FunctionToPointerDecay>
-        | `-DeclRefExpr 'int (int) const' lvalue CXXMethod ID0003 'operator()' 'int (int) const'
+        | `-DeclRefExpr 'int (int) const' lvalue CXXMethod ID0008 'operator()' 'int (int) const'
         |-ImplicitCastExpr 'const (lambda at  )' lvalue <NoOp>
         | `-DeclRefExpr '(lambda at  )':'(lambda at  )' lvalue Var ID0002 'lambda' '(lambda at  )':'(lambda at  )'
         `-ImplicitCastExpr 'int' <LValueToRValue>
```
