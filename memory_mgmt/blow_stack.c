#include <stdio.h>

#define STACK_TIP_FILE_NAME "./stack_tip"

void suicide(int how_fast)
{
  FILE *fp;
  char a[how_fast];
  fp = fopen(STACK_TIP_FILE_NAME,"a");
  fprintf(fp, "%p\n", &a[how_fast-1]);
  fclose(fp);
  suicide(how_fast);
}

int main(int argc, char *argv[])
{
  int how_fast;

  /* okay to fail */
  unlink(STACK_TIP_FILE_NAME); 

  printf ("Stack begins at roughly:%p\n",&how_fast);
  printf ("How fast do u want to die?");
  scanf("%d",&how_fast);
  suicide(how_fast);
  return 0;
}
