/* file_creator_sys.c */
#include <fcntl.h>    // open(), O_WRONLY, O_CREAT, O_TRUNC
#include <unistd.h>   // write(), close()
#include <string.h>   // strlen()

int main() {
    // 1. Open/create "output.txt"
    int fd = open("output.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);

    // Check if file opened successfully
    if (fd < 0) {
        write(2, "Error creating file\n", 20); // 2 = stderr
        return 1;
    }

    // 2. Write to file
    char *message = "Hello from Operating Systems class!\n";
    write(fd, message, strlen(message));

    // 3. Close the file
    close(fd);

    // 4. Print success message to terminal (stdout = 1)
    char *success = "File created successfully!\n";
    write(1, success, strlen(success));

    return 0;
}