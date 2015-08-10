#include <stdio.h>

int main(int argc, char *argv[])
{
  char one_line[512];
  char *result;
  FILE *fp=fopen("/proc/self/maps","r");
  if (fp == NULL) {
    perror("Opening maps failed!");
    return 1;
  }
  do {
    one_line[0] = '\0';
    result = fgets(one_line, sizeof(one_line), fp);
    if (!result) {
      break;
    }
    printf ("%s",one_line);
  } while(1);
  fclose(fp);
  printf("The stack roughly begins at %p\n",&argc);
  return 0;
}

