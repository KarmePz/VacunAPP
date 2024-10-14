import csv

##LEER NO ES CLASE YA QUE NO VI NECESARIO INSTANCIARLO PARA PODER LEER UN ARCHIVO CSV, SIN EMBARGO VERIFICADOR SI, YA QUE NO ES 
##ESTRICTAMENTE NECESARIO VERIFICAR UN NUEVO ARCHIVO(en otro programa) QUE YA CUENTA CON TODOS SUS REGISTROS CORRECTAMENTE VERIFICADOS. 


    ##-------------------------------------------------
    #             VARIABLES PARA EL CONTROL
    ##-------------------------------------------------

    
vacuna_list = ['Sinopharm', 'Pfizer Bivariante BA 4 5', 'Sputnik Light', 'Moderna 010 mg mL', 
                'Moderna ARNm 020 mg mL', 'Moderna Bivariante BA 4 5', 'AstraZeneca', 'Pfizer', 
                'Pfizer Pediátrica', 'Sputnik', 'Cansino']
jurisdiccion_list=[
        'Córdoba', 'CABA', 'Catamarca', 'Chaco', 'Santiago del Estero', 'San Juan', 'San Luis', 'Entre Ríos', 
        'Jujuy', 'Río Negro', 'Santa Fe', 'La Rioja', 'Neuquén', 'Tucumán', 'Mendoza', 'Misiones', 'La Pampa', 
        'Salta', 'Formosa', 'Buenos Aires','Chubut','Santa Cruz','Tierra del Fuego']

grupo_etario_list=['18-29', '<12', '50-59', '90-99', '30-39', '60-69', '12-17', '70-79', '80-89', '40-49']
grupo_etario_mayores_list = ['60-69', '70-79', '80-89','90-99']



##LECTURA DE ARCHIVOS CSV
def LeerCSV(PathCSV):
    with open(PathCSV , "r", encoding="utf-8") as pacientes:
        reader = csv.DictReader(pacientes)
        datos_pacientes = [fila for fila in reader]
    return datos_pacientes

def CantidadPacientes(datos_pacientes): 
    print(f"DATOS DE PACIENTES\n Cantidad de pacientes:{len(datos_pacientes)}\n\n")


def Analizar(PathCSV,opcion):
    datos_pacientes = LeerCSV(PathCSV)
    
    ##Análisis por genero
    
    if opcion == 'genero' or opcion == 'sexo':
        cont_M=0
        cont_F = 0
        contador_otros = 0
        for paciente in datos_pacientes:
            if paciente['sexo'] == 'M':
                cont_M +=1 
            elif paciente['sexo'] == 'F':
                cont_F +=1
            else:
                contador_otros += 1
        print(f"Masculinos: {cont_M}\nFemeninos: {cont_F}\nOtros no especificados: {contador_otros}")


    ##Análisis por vacuna

    elif opcion == 'vacuna':
        contador_otros = 0
        for vacuna in vacuna_list:
            contador = 0
            
            for paciente in datos_pacientes:
                if paciente['vacuna'] == vacuna:
                    contador += 1
            print(f"{vacuna} : \t%{round(((contador*100)/len(datos_pacientes)),3)}", end="\n")
            
            if contador == 0:
                contador_otros += 1
            
            
        print(f"otros no registrados: \t%{round(((contador_otros*100)/len(datos_pacientes)),2)}", end="\n")
    
    
    ##Análisis por Residencia
    
    elif opcion == 'residencia':
        contador_otros = 0
        for residencia in jurisdiccion_list:
            contador = 0
            
            for paciente in datos_pacientes:
                if paciente['jurisdiccion_residencia'] == residencia:
                    contador += 1
            print(f"{residencia} : \t{contador}  dosis", end="\n")
            
            if contador == 0:
                contador_otros += 1
            
        print(f"otros no registrados: %{contador_otros}", end="\n")
    
    
    ##Análisis por segundas dosis por Residencia
    
    
    
    elif opcion == 'segundaDosis' or opcion == 'segunda_dosis':
        
        for residencia in jurisdiccion_list:
            contador = 0
            for paciente in datos_pacientes:
                if paciente['nombre_dosis_generica'] == '2da' and paciente['jurisdiccion_residencia'] == residencia:
                    contador += 1
            print(f"{residencia} : \t{contador}  segundas dosis", end="\n")
    
    
    ##Análisis por mayores con dosis de refuerzo
    
    elif opcion == 'mayoresRefuerzo' or opcion == 'mayores_refuerzo':
        contador = 0
        for paciente in datos_pacientes:
            if paciente['grupo_etario'] in grupo_etario_mayores_list and paciente['nombre_dosis_generica'] == 'Refuerzo':
                contador += 1
        print(f"cantidad de adultos mayores que recibieron dosis de refuerzo : {contador}")




##PRUEBA DE LECTURA CON LA LIBRERÍA PANDAS

# import pandas as pd

# df = pd.read_csv("./ArchivosPrueba/datos_prueba_parte1_PRUEBA.csv")

# distribucion_genero = df["sexo"].value_counts()
# print(distribucion_genero)
