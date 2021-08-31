int main(int argc, char *argv[]) {
  auto lambda = [](int argc) { return argc; };
  return lambda(argc);
}
