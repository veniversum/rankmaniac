#include <stdio.h>
#include <unistd.h>

int main() {
//    int c;
//    while ((c = getchar()) != EOF){
//        putchar(c);
//    }
    char buffer[10];
    size_t len = 0;
    do {
        len = read(STDIN_FILENO, buffer, 10);
        if (len == 0) return 0;
        len = write(STDOUT_FILENO, buffer, len);
    } while (len > 0);
    return 0;
}