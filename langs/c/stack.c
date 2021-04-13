#include "stack.h"

/**
 * Push an element to the top of the stack.
 */
void push(Node **top, int value) {
    Node *newNode = malloc(sizeof(Node));
    newNode->value = value;
    if (*top == NULL) {
        newNode->prev = NULL;
        *top = newNode;
    } else {
        Node *oldTop = *top;
        *top = newNode;
        newNode->prev = oldTop;
    }
}

/**
 * Peek the top element of the stack without removing it.
 */
int peek(Node **top) {
    return *top == NULL? NAN : (*top)->value;
}

/**
 * Pop from the top of the stack and returned the removed element.
 */
int pop(Node **top){
    Node *oldTop = *top;
    if (oldTop == NULL) {
        return NAN;
    } else {
        Node *prev = oldTop->prev;
        int value = oldTop->value;
        *top = prev;
        free(oldTop);
        return value;
    }
}

/**
 * Clear the stack by removing all the elements.
 */
void clear(Node **top) {
    while (!empty(top)) {
        pop(top);
    }
}

/**
 * Return 1 if the stack is empty, 0 otherwise.
 */
int empty(Node **top) {
    return *top == NULL? 1 : 0;
}

int main(int argc, char *argv[]) {
    Node *top = NULL;
    push(&top, 1);
    push(&top, 2);
    push(&top, 3);
    printf("Peek top: %d\n", peek(&top));

    clear(&top);
    printf("Empty after clear (1: empty, 0: non empty): %d\n", empty(&top));

    push(&top, 1);
    push(&top, 2);
    push(&top, 3);
    while (!empty(&top)) {
        printf("Popping: %d\n", pop(&top));
    }

    printf("Peek an empty stack (8080: NAN): %d\n", peek(&top));
    printf("Pop an empty stack (8080: NAN): %d\n", pop(&top));
    return 0;
}
