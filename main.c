#include "Multiples_fuentes.h"

int main(){
    char nombreaux[64], docenteaux[64];
    Materia Materias[100], aux;
    int cursadaaux, i, opcion, bucle = 1;
    float notaaux;
    for(i = 0; i < 100; i++) strcpy(&Materias[i].Nombre[0], "");
    //printf("%d\n\n", strcmp(&Materias[1].Nombre[0], "")); 0 si esta vacio
    printf("Bienvenido al sistema de materias de la universidad nacional de lomas de zamora.\n");
    while(bucle){
        printf("1-Ingresar los datos de una materia.\n2-Mostrar materias.\n3-Buscar materias.\n4-Ordenar materias.\n5-Calcular promedio.\n6-Modificar estado de una materia.\n7-Borrar materia.\n8-Salir del programa.\n");
        scanf("%d", &opcion);
        switch(opcion){
            case 1:
                for ( ; ; ) {
                    fflush(stdin);
                    printf("Ingrese el nombre de la materia:\n");
                    fgets(&nombreaux[0], 64, stdin);
                    fflush(stdin);
                    printf("Ingrese el nombre del docente:\n");
                    fgets(&docenteaux[0], 64, stdin);
                    printf("Ingrese el a\xA4o de la cursada:\n");
                    fflush(stdin);
                    scanf("%d", &cursadaaux);
                    printf("Ingrese la nota final de la cursada:\n");
                    fflush(stdin);
                    scanf("%f", &notaaux);
                    for(i = 0; i < 100; i++){
                       if (!strcmp(&Materias[i].Nombre[0], "")){
                            Materias[i] = datos(&nombreaux[0], &docenteaux[0], cursadaaux, notaaux);
                            break;
                        }
                    }
                    printf("Los datos ingresados son correctos?\n1) Si\n2) No\n\n");
                    fflush(stdin);
                    scanf("%d", &opcion);
                   if (opcion == 1) break;
                     strcpy(&Materias[i].Nombre[0], "");
                     }
                break;
            case 2:
                mostrar(&Materias[0]);
                break;
            case 3:
                fflush(stdin);
                printf("Ingrese el nombre de la materia a buscar:\n");
                fgets(&nombreaux[0], 64, stdin);
                if (buscar(&nombreaux[0], &Materias[0], &aux)) printf("Nombre de la Materia: %sNombre del Docente: %s%d, %f\n%s\n\n", aux.Nombre, aux.Docente, aux.Cursada, aux.Nota, aux.Estado);
                else printf("No se encontro la materia %s\n", nombreaux);
                break;
            case 4:
                ordenar(&Materias[0]);
                mostrar(&Materias[0]);
                break;
            case 5:
                notaaux = promedio(&Materias[0]);
                if (notaaux == 0) printf("Para usar esta opcion deben haber al menos dos materias ingresadas.\n\n");
                else printf("El promedio de notas de las diferentes materias es %f.\n\n", notaaux);
                break;
            case 6:
                fflush(stdin);
                printf("Ingrese el nombre de la materia a modificar:\n");
                fgets(&nombreaux[0], 64, stdin);
                printf("Ingrese la nota final de la cursada:\n");
                fflush(stdin);
                scanf("%f", &notaaux);
                if (modificar(&Materias[0], &nombreaux[0], notaaux)) printf("Se ha ingresado correctamente la nota final.\n\n");
                else printf("No se ha encontrado la materia o ya se ha rendido examen final.\n\n");
                break;
            case 7:
                fflush(stdin);
                printf("Ingrese el nombre de la materia a eliminar:\n");
                fgets(&nombreaux[0], 64, stdin);
                printf("Ingrese la cursada:\n");
                fflush(stdin);
                scanf("%d", &cursadaaux);
                if (eliminar(&Materias[0], &nombreaux[0], cursadaaux)) {
                    ordenarAlfabeticamente(&Materias[0]);
                    printf("La materia se ha eliminado correctamente.\nLas Materias que quedan son:\n\n");
                    mostrar(&Materias[0]);
                }
                else printf("La materia no se ha encontrado.\n\n");
                break;
            case 8:
                printf("Saliendo del Sistema...\n\n\n\n");
                bucle = 0;
                break;
            default:
                printf("Opcion no valida.\n");
                break;
        }
    }
    return 0;
}
