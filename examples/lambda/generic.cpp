int main(int argc, char *argv[]) {
  auto lambda = [](auto argc) { return argc; };
  return lambda(argc);
}
