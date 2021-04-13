#include <stdio.h>
#include <stdlib.h>

#define NAN 8080

typedef struct {
    int value;
    struct Node *prev;
} Node;

void push(Node **top, int value);
int pop(Node **top);
int peek(Node **top);
void clear(Node **top);
int empty(Node **top);
