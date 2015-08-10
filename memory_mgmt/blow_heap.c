#include <stdio.h>
#include <stdlib.h>

typedef struct list {
  void *next;
}list_t;

list_t head;
FILE *fp;

void print_map()
{
  char one_line[512];
  char *result;
  int ret;
  ret = fseek(fp, 0L, SEEK_SET);
  if (ret == -1) {
    perror("fseek failed");
    exit(1);
  }
  do {
    one_line[0] = '\0';
    result = fgets(one_line, sizeof(one_line), fp);
    if (!result) {
      break;
    }
    printf ("%s",one_line);
  } while(1);
}

void blow_heap(int how_fast)
{
  list_t *prev = &head;
  do {
    list_t *ptr = malloc(how_fast);
    if (!ptr) {
      prev->next = NULL;
      printf ("Heap appears exhausted\n");
      print_map();
      break;;
    }
    prev->next = ptr;
    prev = ptr;
  } while(1);
  prev = head.next;
  while (prev) {
    list_t *ptr = prev;
    prev = prev->next;
    free(ptr);
  }
}

int main(int argc, char *argv[])
{
  int how_fast;

  fp=fopen("/proc/self/maps","r");
  if (fp == NULL) {
    perror("Opening maps failed!");
    exit(1);
  }

  printf ("How aggressive should the heap grow?");
  scanf("%d",&how_fast);

  printf ("Map before any malloc:\n");
  print_map();
  blow_heap(how_fast);
  printf ("Map afer all free:\n");
  print_map();
 
  fclose(fp);
  return 0;
}
