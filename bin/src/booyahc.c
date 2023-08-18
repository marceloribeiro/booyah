#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libgen.h>  // For dirname()
#include <limits.h>  // For PATH_MAX
#include <unistd.h>  // For realpath()

int main(int argc, char *argv[]) {
    // Execute the 'which' command to get the program's absolute path
    char which_command[1024];
    snprintf(which_command, sizeof(which_command), "which %s", argv[0]);

    FILE *fp = popen(which_command, "r");
    if (!fp) {
        perror("Error executing 'which' command");
        return 1;
    }

    char link_path[1024];
    if (fgets(link_path, sizeof(link_path), fp) == NULL) {
        perror("Error reading 'which' command output");
        return 1;
    }

    // Remove trailing newline
    link_path[strcspn(link_path, "\n")] = 0;

    pclose(fp);

    // Extract the directory path from the link path
    char program_dir[1024];
    strncpy(program_dir, link_path, sizeof(program_dir));
    char *last_slash = strrchr(program_dir, '/');
    if (last_slash) {
        *last_slash = '\0'; // Remove the program filename to get the directory
    }

    char command[1024];
    snprintf(command, sizeof(command), "PYTHONSTARTUP=%s/lib/console.py python", program_dir);
    system(command);

    return 0;
}
