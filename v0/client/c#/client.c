#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 9999
#define BUFFER_SIZE 4096

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <server_ip> <server_port> <pattern_json_file>\n", argv[0]);
        return 1;
    }
    
    const char *server_ip = argv[1];
    int server_port = atoi(argv[2]);
    const char *filename = argv[3];
    
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        perror("fopen");
        return 1;
    }
    
    fseek(fp, 0, SEEK_END);
    long fsize = ftell(fp);
    rewind(fp);
    
    char *json_string = malloc(fsize + 1);
    if (!json_string) {
        perror("malloc");
        fclose(fp);
        return 1;
    }
    
    fread(json_string, 1, fsize, fp);
    json_string[fsize] = '\0';
    fclose(fp);
    
    int sockfd;
    struct sockaddr_in server_addr;
    
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("scoket");
        free(json_string);
        return 1;
    }
    
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(server_port);
    if (inet_pton(AF_INET, server_ip, &server_addr.sin_addr) <= 0) {
        fprintf(stderr, "Invalid server IP address.\n");
        free(json_string);
        close(sockfd);
        return 1;
    }
    
    sendto(sockfd, json_string, strlen(json_string), 0, (struct sockaddr *)&server_addr, sizeof(server_addr));
    
    printf("Sent pattern from file '%s'to %s:%d\n", filename, server_ip, server_port);
    
    free(json_string);
    close(sockfd);
    return 0;
}
