#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define CHUNK_SIZE 4096


int main(){
      
    unsigned char  buf_in[CHUNK_SIZE];
    FILE          *fp_t, *fp_s;
    size_t         read_len;
    int            eof;
    int file_size;
    int file_offset = 0;

    char *mem_file;

    fp_s = fopen("script", "rb");
    fseek(fp_s, 0L, SEEK_END);
    file_size = ftell(fp_s);
    mem_file = malloc(file_size);
    fp_s = fopen("script", "rb");
    
    
    do {
        read_len = fread(buf_in, 1, sizeof buf_in, fp_s);
        
        memcpy(&mem_file[file_offset], &buf_in, read_len);
        file_offset += read_len;
        eof = feof(fp_s);

    } while (! eof);

    fclose(fp_s);

    printf("%s", mem_file);
    
}


