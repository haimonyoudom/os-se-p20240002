/* dir_list_sys.c */
#include <fcntl.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>
#include <string.h>
#include <stdio.h>    // for snprintf

int main() {
    char buffer[512];
    DIR *dir;
    struct dirent *entry;
    struct stat fileStat;

    // 1. Open current directory
    dir = opendir(".");
    if (dir == NULL) {
        write(2, "Error opening directory\n", 24);
        return 1;
    }

    // 2. Print header
    write(1, "Name\t\tSize (bytes)\n", 20);
    write(1, "---------------------------\n", 28);

    // 3. Loop through entries
    while ((entry = readdir(dir)) != NULL) {

        // 4. Get file info using stat()
        if (stat(entry->d_name, &fileStat) == -1) {
            write(2, "Error getting file info\n", 24);
            continue;
        }

        // 5. Format output into buffer
        int len = snprintf(buffer, sizeof(buffer), "%-15s %ld\n",
                           entry->d_name, fileStat.st_size);

        // Write to stdout
        write(1, buffer, len);
    }

    // 6. Close directory
    closedir(dir);

    return 0;
}