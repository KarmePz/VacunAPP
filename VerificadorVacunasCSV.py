import csv
from datetime import datetime
import os


class VerificadorCSV:
    ##atributos que sirven para el control de los registros
    
    ##-------------------------------------------------
    #                      ATRIBUTOS
    ##-------------------------------------------------
    sexo_list = ['M','F']
    
    ids_persona_existentes = []
    
    grupo_etario_list=['18-29', '<12', '50-59', '90-99', '30-39', '60-69', '12-17', '70-79', '80-89', '40-49']
    
    jurisdiccion_list=[
        'Córdoba', 'CABA', 'Catamarca', 'Chaco', 'Corrientes','Santiago del Estero', 'San Juan', 'San Luis', 'Entre Ríos', 
        'Jujuy', 'Río Negro', 'Santa Fe', 'La Rioja', 'Neuquén', 'Tucumán', 'Mendoza', 'Misiones', 'La Pampa', 
        'Salta', 'Formosa', 'Buenos Aires','Chubut','Santa Cruz','Tierra del Fuego']
    jurisdiccion_id_diccionario = {'Misiones': '54', 'Tucumán': '90', 'Santa Fe': '82', 'Buenos Aires': '06', 
                                    'Catamarca': '10', 'San Luis': '74', 'San Juan': '70', 'Río Negro': '62', 
                                    'CABA': '02', 'La Pampa': '42', 'Córdoba': '14', 'Entre Ríos': '30', 'Chaco': '22', 
                                    'Santiago del Estero': '86', 'La Rioja': '46', 'Mendoza': '50', 'Formosa': '34', 
                                    'Salta': '66', 'Neuquén': '58', 'Jujuy': '38','Chubut':'26','Santa Cruz':'78', 'Tierra del Fuego':'94', 'Corrientes':'18'}
    
    # depto_aplicacion
    # depto_aplicacion_id
    
    vacuna_list = ['Sinopharm', 'Pfizer Bivariante BA 4 5', 'Sputnik Light', 'Moderna 010 mg mL', 
                    'Moderna ARNm 020 mg mL', 'Moderna Bivariante BA 4 5', 'AstraZeneca', 'Pfizer', 
                    'Pfizer Pediátrica', 'Sputnik', 'Cansino']
    
    cod_dosis_generica_list={'2da':'3', 'Refuerzo':'14','1ra':'2'}
    orden_dosis_list={'2da':'2', 'Refuerzo':'3','1ra':'1'}
    # condicion_aplicacion
    
    nombre_dosis_list = ['2da', 'Refuerzo','1ra']
    
    

    
    
    ##-------------------------------------------------
    #                      METODOS
    ##-------------------------------------------------
    ##Constructor
    def __init__(self, _datos_pacientes):
        
        self.pacientes = _datos_pacientes
        self.registros_erroneos = []
        
            
    
    def VerificarErrores(self):
        for paciente in self.pacientes:
            paciente_observacion=''
            
            ## análisis del género
            if paciente['sexo'] not in self.sexo_list:
                paciente_observacion = "Sexo no especificado"
            
            ##Análisis del grupo etario 
            if paciente['grupo_etario'] not in self.grupo_etario_list:
                paciente_observacion = "grupo etario invalido" 
            ##Análisis de la residencia 
            if paciente['jurisdiccion_residencia'] not in self.jurisdiccion_list:
                paciente_observacion = "Jurisdiccion de residencia invalido" 
                
            if paciente['jurisdiccion_aplicacion'] not in self.jurisdiccion_list:
                paciente_observacion= "Jurisdiccion de aplicación invalido"
            
            ## Verificación de la clave de la jurisdicción (id)
            if paciente['jurisdiccion_residencia'] in self.jurisdiccion_id_diccionario:
                id_esperado = self.jurisdiccion_id_diccionario[paciente['jurisdiccion_residencia']]
                if paciente['jurisdiccion_residencia_id'] != id_esperado:
                    paciente_observacion = "ID de jurisdicción de residencia no coincide"
                    
            if paciente['jurisdiccion_aplicacion'] in self.jurisdiccion_id_diccionario:
                id_esperado = self.jurisdiccion_id_diccionario[paciente['jurisdiccion_aplicacion']]
                if paciente['jurisdiccion_aplicacion_id'] != id_esperado:
                    paciente_observacion = "ID de jurisdicción de aplicacion no coincide"
            
            ##verificación departamento de residencia y aplicacion id 
            if not paciente['depto_residencia_id'].isdigit() and not paciente['depto_aplicacion_id'].isdigit():
                paciente_observacion = "depto de residencia o aplicacion invalido, debe ser númerico"
            
            ## Verificación de la fecha de aplicación con try catch para capturar excepciones
            fecha = paciente['fecha_aplicacion']
            if not self.verificar_fecha(fecha):  # Llama a la función de verificación
                paciente_observacion = "Fecha de aplicación inválida (Debe ser en formato YYYY-MM-DD y contener solo números)"
                
                
            ##verificación vacuna
            if paciente['vacuna'] not in self.vacuna_list:
                paciente_observacion = "vacuna no registrada"
            
            ##verificación código de dosis generica 
            if paciente['nombre_dosis_generica'] in self.cod_dosis_generica_list:
                id_esperado = self.cod_dosis_generica_list[paciente['nombre_dosis_generica']]
                if paciente['cod_dosis_generica'] != id_esperado:
                    paciente_observacion = "código de dosis generica no coincide"
            else:
                paciente_observacion = "Nombre de dosis generica no registrado"
            
            ##verificación orden dosis
            if paciente['nombre_dosis_generica'] in self.cod_dosis_generica_list:
                id_esperado = self.orden_dosis_list[paciente['nombre_dosis_generica']]
                if paciente['orden_dosis'] != id_esperado:
                    paciente_observacion = "Orden de dosis no coincide"
            else:
                paciente_observacion = "Nombre de dosis generica no registrado"
                
                
            ##verificación persona id
            id_persona_dw = paciente.get('id_persona_dw', None)  # Asegúrate de que el campo existe
        
            if id_persona_dw is not None:
                es_valido, mensaje = self.verificar_id_unico(id_persona_dw, self.ids_persona_existentes)
            if not es_valido:
                paciente_observacion = mensaje
            else:
                # Si es válido, añade el ID a la lista de IDs existentes
                self.ids_persona_existentes.append(float(id_persona_dw))

            
                
            if paciente_observacion:
                paciente['OBSERVACION'] = paciente_observacion
                self.registros_erroneos.append(paciente)
        self.guardarDatos()




    def guardarDatos(self):
        nombre_archivo = "Registros_inconsistentes.csv"
        path_archivo = f"./Resultados/{nombre_archivo}"
        if self.registros_erroneos:
            with open(path_archivo, "w", newline='', encoding="utf-8" ) as archivoCsv:
                campos_registros = list(self.pacientes[0].keys())+['OBSERVACION'] ##Se añade la columna observacion a un nuevo archivo csv
                writer = csv.DictWriter(archivoCsv, fieldnames=campos_registros) ##Se escriben las columnas en el archivo csv en forma de diccionario
                writer.writeheader() ## escribe la cabecera con los fieldnames ya definidos
                writer.writerows(self.registros_erroneos)##escribe las correspondientes filas en el archivo de registros erroneos
            print("Se genero un archivo con registros erroneos en ./Resultados")
        else:
            print("No se encontraron registros erroneos")
            if os.path.exists(path_archivo):
                os.remove(path_archivo)
                print(f"El archivo {nombre_archivo} ha sido eliminado porque no hay registros erróneos.")




    def verificar_fecha(self, fecha):
        
        ##separamos la fecha en 3 partes AÑO-MES-DIA
        fecha_separada = fecha.split('-')
        if len(fecha_separada) != 3:
            return False
        anio, mes, dia = fecha_separada
        
        # verificamos que las partes sean numéricas
        if not (anio.isdigit() and mes.isdigit() and dia.isdigit()):
            return False
        
        # verificamos que la longitud del año sea de 4, el mes 2 y el día 2 
        if len(anio) != 4 or len(mes) != 2 or len(dia) != 2:
            return False
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return True
        except ValueError:
            return False



    def verificar_id_unico(self, id_persona, ids_existentes):
        # Verifica si el id_persona es un número flotante
        try:
            id_float = float(id_persona)  # Intenta convertir a float
        except ValueError:
            return False, "ID de persona debe ser un número flotante"
        
        # Verifica si el id_persona ya está en la lista de ids existentes
        if id_float in ids_existentes:
            return False, "ID de persona ya existe en los registros"

        return True, "" ##si todo sale bien el mensaje que se devuelve esta vacío
    
    
    