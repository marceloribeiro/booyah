#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libgen.h>  // For dirname()
#include <limits.h>  // For PATH_MAX
#include <unistd.h>  // For realpath()

int main(int argc, char *argv[]) {
    if (argc != 1) {
        return 1;
    }

    char command[1024];
    char binary_path[PATH_MAX];
    
    if (realpath(argv[0], binary_path) == NULL) {
        perror("Error resolving binary path");
        return 1;
    }
    
    char *dir_path = dirname(binary_path);
    
    snprintf(command, sizeof(command), "PYTHONSTARTUP=%s/console_preload.py python", dir_path);
    system(command);

    return 0;
}
