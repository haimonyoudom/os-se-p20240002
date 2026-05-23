/* file_reader_sys.c */
#include <fcntl.h>
#include <unistd.h>

int main() {
    char buffer[256];
    int fd;
    ssize_t bytesRead;

    // 1. Open "output.txt" for reading
    fd = open("output.txt", O_RDONLY);

    if (fd < 0) {
        write(2, "Error opening file\n", 20);
        return 1;
    }

    // 2. Read content into buffer in a loop
    while ((bytesRead = read(fd, buffer, sizeof(buffer))) > 0) {
        // 3. Write content to terminal (stdout = fd 1)
        write(1, buffer, bytesRead);
    }

    if (bytesRead < 0) {
        write(2, "Error reading file\n", 19);
    }

    // 4. Close the file
    close(fd);

    return 0;
}