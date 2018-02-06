//
// Created by Veniversum on 06/02/2018.
//

#include <fcntl.h>
#include <unistd.h>
#include <sys/sendfile.h>

int main() {
    int r = 1;
    int splice_ = 0;
    if (lseek(STDOUT_FILENO, 0, SEEK_CUR) < 0) splice_ = 1;
    if (splice_) {
        while (r > 0) {
            r = splice(STDIN_FILENO, NULL, STDOUT_FILENO, NULL, 10000, 0);
        }
    } else {
        while (r > 0) {
            r = sendfile(STDOUT_FILENO, STDIN_FILENO, NULL, 1000);
        }
    }

    return 0;
}