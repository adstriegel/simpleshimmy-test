#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <time.h>
#include <cjson/cJSON.h>

#define PORT 9999
#define BUFFER_SIZE 1024
#define RESPONSE "ACK"
#define MAX_DURATIONS 10000

double durations[MAX_DURATIONS];
int duration_count = 0;

double now() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}

void append_gap_to_csv(const char *filename, double intended_gap, double average_gap) {
    FILE *f = fopen(filename, "a");
    if (!f) {
        perror("fopen (csv)");
        return;
    }
    fprintf(f, "%f,%.6f\n", intended_gap, average_gap);
    fclose(f);
}
    
void save_durations_to_file(const char *filename) {
    FILE *f = fopen(filename, "w");
    if (!f) {
        perror("fopen");
        return;
    }
    
    for (int i = 0; i < duration_count; i++) {
        fprintf(f, "%.2f\n", durations[i]);
    }
    
    fclose(f);
    printf("[*] Wrote %d durations to %s\n", duration_count, filename);
}

void send_packet_train(int sockfd, struct sockaddr_in *client, socklen_t client_len, cJSON *pattern_json, const char *average_gap_filename, double intended_gap) {
    cJSON *item = NULL;
    cJSON_ArrayForEach(item, pattern_json) {
        const char *train_id = item->string;
        cJSON *train = item;
        
        int num_packets = cJSON_GetObjectItem(train, "num_packets")->valueint;
        int packet_size = cJSON_GetObjectItem(train, "packets_size")->valueint;
        double local_gap = cJSON_GetObjectItem(train, "local_gap")->valuedouble;
        double global_gap = cJSON_GetObjectItem(train, "global_gap")->valuedouble;
        
        printf("[Train %s] %d packets, %d bytes each, %.3f s local gap, %.3f s global gap\n", train_id, num_packets, packet_size, local_gap, global_gap);
        
        for (int i = 0; i < num_packets; i++) {
            double start = now();
            
            char payload[BUFFER_SIZE];
            snprintf(payload, sizeof(payload), "{\"packet_train\": %s, \"packet_id\": %d, \"timestamp\": %.6f}", train_id, i, now());
            
            int payload_len = strlen(payload);
            int final_size = (packet_size > payload_len) ? packet_size : payload_len;
            memset(payload + payload_len, ' ', final_size - payload_len);
            
            // double start = now();
            sendto(sockfd, payload, final_size, 0, (struct sockaddr *)client, client_len);
            // double end = now();
            
            // if (duration_count < MAX_DURATIONS) {
            //    durations[duration_count++] = (end - start) * 1e6;
            // }
            
            // printf("    Sent packet %d, sendto() took %.2f us\n", i + 1, (end - start) * 1e6);
            usleep((int)(local_gap * 1e6));
            
            double end = now();
            double duration = end - start;
            durations[duration_count++] = (duration - local_gap) * 1e6;
        }
        
        usleep((int)(global_gap * 1e6));
    }
    
    // int count = 100;
    // double sum = 0.0;
    // for (int i = 0; i < count; i++) {
    //    sum += durations[i];
    // }
    // double average_gap = sum / count;
    // printf("Filename: %s\n", average_gap_filename);
    FILE *f = fopen(average_gap_filename, "a");
    if (!f) {
        perror("fopen (csv)");
        return;
    }
     
    for (int i = 0; i < duration_count; i++) {
        fprintf(f, "%.1f,%.2f\n", intended_gap * 1e6, durations[i]);
    }
    duration_count = 0;
    
    fclose(f);
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        fprintf(stderr, "Usage: %s <timing_output_file> <average_gap_filename> <intended_gap>\n", argv[0]);
        return 1;
    }
    
    const char *output_filename = argv[1];
    const char *average_gap_filename = argv[2];
    double intended_gap = atof(argv[3]);

    int sockfd;
    char buffer[BUFFER_SIZE];
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = INADDR_ANY;
    
    bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));
    
    printf("UDP server listening on port %d...\n", PORT);
    
    while (1) {
        int len = recvfrom(sockfd, buffer, BUFFER_SIZE - 1, 0, (struct sockaddr*)&client_addr, &client_len);
        buffer[len] = '\0';
        
        printf("[*] Received pattern JSON from client.\n");
        
        cJSON *pattern = cJSON_Parse(buffer);
        if (!pattern) {
            printf("[-] Invalid JSON format\n");
            continue;
        }
        
        send_packet_train(sockfd, &client_addr, client_len, pattern, average_gap_filename, intended_gap);
        // save_durations_to_file(output_filename);
        duration_count = 0;
        
        cJSON_Delete(pattern);
    }
    
    close(sockfd);
    return 0;
}
