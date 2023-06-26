#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define MULTIPLES_FUENTES_H_INCLUDED

typedef struct Materia Materia;
struct Materia{
    char Nombre[64], Docente[64], Estado[20];
    int  Cursada;
    float Nota;
};
Materia datos(char* nombre, char* docente, int cursada, float nota) {
    Materia resultado;
    strcpy(resultado.Nombre, nombre);
    strcpy(resultado.Docente, docente);
    resultado.Cursada = cursada;
    resultado.Nota = nota;
    if (nota >= 7) strcpy(resultado.Estado, "PROMOCIONADA");
    else strcpy(resultado.Estado, "DEBE DAR FINAL");
    return resultado;
}
int mostrar(Materia* lista) {
    int i;
    for(i = 0; i < 100; i++) if (strcmp(&lista[i].Nombre[0], ""))
        printf("Nombre de la Materia: %sNombre del Docente: %s%d, %f\n%s\n\n", lista[i].Nombre, lista[i].Docente, lista[i].Cursada, lista[i].Nota, lista[i].Estado);
    return 1;
}
int buscar(char* nombre, Materia* lista, Materia* retorno) {
    int i;
    for (i = 0; i < 100; i++) {
        if (!strcmp(&lista[i].Nombre[0], nombre)) {
            *retorno = lista[i];
            if (retorno != NULL) return 1;
        }
    }
    return 0;
}
int ordenar(Materia* lista) {
    int i, j, k, l;
    long double suma1, suma2;
    for (i = 0, j = 0; i < 100; i++) if (strcmp(&lista[i].Nombre[0], "")) j++;
    if (j < 2) return 0;
    Materia aux;
    //ordeno primero por cursada
    for (i = 0; i < 100; i++) {
        for (j = 0; j < 100 - i - 1; j++) {
            if (strcmp(&lista[j].Nombre[0], "") && strcmp(&lista[j + 1].Nombre[0], "")) {
                if (lista[j].Cursada > lista[j + 1].Cursada) {
                    aux = lista[j];
                    lista[j] = lista[j + 1];
                    lista[j + 1] = aux;
                }
            }
        }
    }
    //luego ordeno por nombre de docente de manera ascendente respetando el orden de cursada
    for (i = 0; i < 100; i++) {
        for (j = 0; j < 100 - i - 1; j++) {
            //para poder comparar cual nombre es mayor que otro, transformo la frase en un numero utilizando codigo ascii
            for (k = 0; k < 64 || lista[j].Docente[k] == '\0' || lista[j].Docente[k] == '\n'; k++);
            for (l = 0; l < 64 || lista[j + 1].Docente[l] == '\0' || lista[j + 1].Docente[l] == '\n'; l++);
            if (k > l) l = k - l;
            else if (l > k) l = l - k;
            for (k = 0, suma1 = 0, suma2 = 0; k < l; k++){ //recorro todo el string hasta encontrar el fin del mismo
                suma1 *= 256; //muevo la letra dos espacios a la izquierda
                suma1 += (long double) lista[j].Docente[k]; //sumo la nueva letra
                suma2 *= 256;
                suma2 += (long double) lista[j + 1].Docente[l];
            }
            if (suma1 > suma2 && lista[j].Cursada == lista[j + 1].Cursada) {
                aux = lista[j];
                lista[j] = lista[j + 1];
                lista[j + 1] = aux;
            }
        }
    }
    return 1;
}
int ordenarAlfabeticamente(Materia* lista) {
    int i, j, k, l;
    long double suma1, suma2;
    for (i = 0, j = 0; i < 100; i++) if (strcmp(&lista[i].Nombre[0], "")) j++;
    if (j < 2) return 0;
    Materia aux;
    for (i = 0; i < 100; i++) {
        for (j = 0; j < 100 - i - 1; j++) {
            //para poder comparar cual nombre es mayor que otro, transformo la frase en un numero utilizando codigo ascii
            for (k = 0; k < 64 || lista[j].Nombre[k] == '\0' || lista[j].Nombre[k] == '\n'; k++);
            for (l = 0; l < 64 || lista[j + 1].Nombre[l] == '\0' || lista[j + 1].Nombre[l] == '\n'; l++);
            if (k > l) l = k - l;
            else if (l > k) l = l - k;
            for (k = 0, suma1 = 0, suma2 = 0; k < l; k++){ //recorro todo el string hasta encontrar el fin del mismo
                suma1 *= 256; //muevo la letra dos espacios a la izquierda
                suma1 += (long double) lista[j].Nombre[k]; //sumo la nueva letra
                suma2 *= 256;
                suma2 += (long double) lista[j + 1].Nombre[l];
            }
            if (suma1 > suma2) {
                aux = lista[j];
                lista[j] = lista[j + 1];
                lista[j + 1] = aux;
            }
        }
    }
    return 1;
}
float promedio(Materia* lista) {
    int i, materias;
    float promedio = 0;
    for (i = 0, materias = 0; i < 100; i++) if (strcmp(&lista[i].Nombre[0], "")) {
        materias++;
        promedio += lista[i].Nota;
    }
    if (materias < 3) return 0;
    return (float) promedio / materias;
}
int modificar(Materia* lista, char* nombre, float nota) {
    int i;
    for (i = 0; i < 100; i++) if (!strcmp(&lista[i].Nombre[0], &nombre[0]) && strcmp(&lista[i].Estado[0], "FINAL RENDIDO")) {
        lista[i].Nota = nota;
        strcpy(lista[i].Estado, "FINAL RENDIDO");
        return 1;
    }
    return 0;
}
int eliminar(Materia* lista, char* nombre, int cursada) {
    int i;
    for (i = 0; i < 100; i++) {
        if (!strcmp(&lista[i].Nombre[0], &nombre[0]) && lista[i].Cursada == cursada) {
            strcpy(lista[i].Nombre, "");
            strcpy(lista[i].Docente, "");
            strcpy(lista[i].Estado, "");
            lista[i].Cursada = 0;
            lista[i].Nota = 0;
            return 1;
        }
    }
    return 0;
}