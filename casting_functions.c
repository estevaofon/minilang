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

// Função para converter float para int (trunca)
long long to_int(double value) {
    return (long long)value;
}

// Função para converter int para float
double to_float(long long value) {
    return (double)value;
} 