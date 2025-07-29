#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// Função para converter int para string
char* to_str_int(long long value) {
    // Alocar espaço suficiente para o número + null terminator
    char* buffer = malloc(32);
    if (buffer == NULL) {
        return NULL;
    }
    sprintf(buffer, "%lld", value);
    return buffer;
}

// Função para converter float para string
char* to_str_float(double value) {
    // Alocar espaço suficiente para o float + null terminator
    char* buffer = malloc(64);
    if (buffer == NULL) {
        return NULL;
    }
    sprintf(buffer, "%.6f", value);
    return buffer;
}

// Função para converter array de int para string
char* array_to_str_int(long long* arr, int size) {
    if (arr == NULL || size <= 0) {
        char* buffer = malloc(3);
        if (buffer == NULL) {
            return NULL;
        }
        strcpy(buffer, "[]");
        return buffer;
    }
    
    // Calcular tamanho necessário para a string
    int total_size = 3; // "[]" + null terminator
    for (int i = 0; i < size; i++) {
        char temp[32];
        sprintf(temp, "%lld", arr[i]);
        total_size += strlen(temp);
        if (i < size - 1) {
            total_size += 2; // ", " para separar elementos
        }
    }
    
    // Alocar memória
    char* buffer = malloc(total_size);
    if (buffer == NULL) {
        return NULL;
    }
    
    // Construir a string
    strcpy(buffer, "[");
    for (int i = 0; i < size; i++) {
        char temp[32];
        sprintf(temp, "%lld", arr[i]);
        strcat(buffer, temp);
        if (i < size - 1) {
            strcat(buffer, ", ");
        }
    }
    strcat(buffer, "]");
    
    return buffer;
}

// Função para converter array de float para string
char* array_to_str_float(double* arr, int size) {
    if (arr == NULL || size <= 0) {
        char* buffer = malloc(3);
        if (buffer == NULL) {
            return NULL;
        }
        strcpy(buffer, "[]");
        return buffer;
    }
    
    // Calcular tamanho necessário para a string
    int total_size = 3; // "[]" + null terminator
    for (int i = 0; i < size; i++) {
        char temp[64];
        sprintf(temp, "%.6f", arr[i]);
        total_size += strlen(temp);
        if (i < size - 1) {
            total_size += 2; // ", " para separar elementos
        }
    }
    
    // Alocar memória
    char* buffer = malloc(total_size);
    if (buffer == NULL) {
        return NULL;
    }
    
    // Construir a string
    strcpy(buffer, "[");
    for (int i = 0; i < size; i++) {
        char temp[64];
        sprintf(temp, "%.6f", arr[i]);
        strcat(buffer, temp);
        if (i < size - 1) {
            strcat(buffer, ", ");
        }
    }
    strcat(buffer, "]");
    
    return buffer;
}

// Função para converter float para int (trunca)
long long to_int(double value) {
    return (long long)value;
}

// Função para converter int para float
double to_float(long long value) {
    return (double)value;
} 