from LectorVacunasCSV import LeerCSV, Analizar,CantidadPacientes
from VerificadorVacunasCSV import VerificadorCSV




    ##---------------------------------------------------------------------------------
    # Se utilizo un archivo de prueba del "datos_nomivac_parte1"el cual cuenta con unos
    # 1500 registros del mismo, se llama "datos_nomivac_parte1_PRUEBA", el mismo se uso
    # para optimizar el análisis del correcto funcionamiento del programa. También se 
    # realizaron pruebas sobre el "datos_nomivac_parte1" y "modelo_muestra"                 
    ##---------------------------------------------------------------------------------


###CAMBIAR 
pathCsv = "./ArchivosPrueba/datos_prueba_parte1_PRUEBA.csv"##Patron que se puede modificar para elegir un modelo 


##VERIFICACIÓN DE DATOS
print("-------------------------------------------------------") 
print("\n\n\tVERIFICACIÓN DE DATOS\n\n")
print("-------------------------------------------------------") 
datos_pacientes = LeerCSV(pathCsv) 
CantidadPacientes(datos_pacientes)


verificador = VerificadorCSV(datos_pacientes)

verificador.VerificarErrores()


##LECTURA DE DATOS
print("-------------------------------------------------------") 
print("\n\n\tLECTURA DE DATOS\n\n")
print("-------------------------------------------------------") 

#Lista de diccionarios
print(datos_pacientes.__class__)

print("\n\nANÁLISIS DE CANTIDAD POR GÉNERO\n\n")
Analizar(pathCsv,'sexo')


print("\n\nANÁLISIS DE PORCENTAJE DE VACUNAS\n\n")
Analizar(pathCsv,'vacuna')


print("\n\nANÁLISIS DE DOSIS POR RESIDENCIA\n\n")
Analizar(pathCsv,'residencia')

print("\n\nANÁLISIS DE SEGUNDA DOSIS POR RESIDENCIA\n\n")
Analizar(pathCsv,'segunda_dosis')

print("\n\nANÁLISIS DE MAYORES CON DOSIS DE REFUERZO")
Analizar(pathCsv,'mayores_refuerzo')
print()


    


