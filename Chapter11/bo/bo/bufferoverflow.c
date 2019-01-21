#include <stdio.h>
#include <unistd.h>

int vuln() {
    // Define variables
    char arr[400];
    int return_status;
    // Grab user input
    printf("What's your name?\n");
    return_status = read(0, arr, 800);
    // Print user input
    printf("Hey %s", arr);
    // Return success
    return 0;
}

int main(int argc, char *argv[]) {
    // Call vulnerable function
    vuln();
    // Return success
    return 0;
}
