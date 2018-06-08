# -*- coding: utf-8 -*-
"""
Created on Thu May 31 07:48:58 2018


ALEJANDRA PÉREZ GARCÍA - 1040755282
   MAURICIO TORO VASCO - 1152224455

"""
#Se importan las librerias necesarias para lnzar la aplicacion
import sys 
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtGui
import smtplib #libreria par la conexion del correo
from email.mime.text import MIMEText #enviar el cuerpo de un correo
from email.mime.multipart import MIMEMultipart #Crear el mensaje
from email.mime.base import MIMEBase #Adjuntr un archivo en el correo
from email import encoders
#Se crea la primer clase, esta es la ventana principal con toda la informacion del paciente
class Sistema(QDialog):
    def __init__(self):
        super(Sistema, self).__init__()
        loadUi('sangre.ui', self)
        #Validaciones para ingresar solo numeros en los line edit
        self.cedula.setValidator(QtGui.QDoubleValidator())
        self.edad.setValidator(QtGui.QDoubleValidator())
        self.peso.setValidator(QtGui.QDoubleValidator())
        #llamo la siguiente clase que me abrira la nueva ventana
        self.info_paciente=Opciones()
        self.guardaryc.clicked.connect(self.on_clicked)#Coecto el boton con mi funcion que me dice que hacer
        
    def sNombre(self): #funcion para recibir y guardar el nombre del paciente
        if self.nombre.text()=='':
            return 'Ninguno'
        else:
            return 'NOMBRE: '+ self.nombre.text() + '\n'
    def sCedula(self): # funcion para recibir y guardar la cedula del paciente
        if self.cedula.text()=='':
            return 'Ninguno'
        else:
            return 'CEDULA: '+ self.cedula.text() + '\n'
    def sEdad(self): # funcion para recibir y guardar la edad del paciente
        if self.edad.text()=='':
            return 'Ninguno'
        else:
            return 'EDAD: '+ self.edad.text() + '\n'
    def sPeso(self): # funcion para recibir y guardar el peso del paciente
        if self.peso.text()=='':
            return 'Ninguno'
        else:
            return 'PESO: ' + self.peso.text() + '\n'
    def sGenero(self): # funcion para recibir y guardar el genero del paciente
        if self.bmasculino.isChecked():
            genero = 'Masculino'
        elif self.bfemenino.isChecked():
            genero = 'Femenino'
        else:
            genero = 'Ninguno'
        return 'GENERO: ' + genero + '\n'
    def sEps(self): # funcion para recibir y guardar la EPS del paciente
        centro=self.eps.currentText()
        return 'EPS: '+ centro + '\n'
    #Creo la funcion que esta conectada con el boton
    def on_clicked(self):
        #Llamo todas as funciones anteriores y las guardo en variables para crear un mensaje
        nombre=self.sNombre()
        cedula=self.sCedula()
        edad=self.sEdad()
        peso=self.sPeso()
        sexo=self.sGenero()
        eps=self.sEps()
        correo=self.correo.text()
        #Se crea el mensaje y se guarda en una variable
        datos_pa= 'Los datos del paciente ingresado son: \n' + nombre + cedula + edad + peso + sexo + eps + '\nSu diagnostico sera enviado en instantes. Gracias por usar nuestro servicio.'
        #Validacion. Todos los dtos deben estar llenos para continuar
        if nombre=='Ninguno' or cedula=='Ninguno' or edad=='Ninguno' or peso=='Ninguno' or sexo=='Ninguno' or correo=='':
            self.error.setText('Error. Faltan datos por llenar')
        else: #Si todo esta lleno envia el primer correo y abre la nueva ventana
            self.error.setText('Paciente ingresado correctamente.')
            self.info_paciente.show()
            #Se crea toda la iformacion del correo 
            remitente = 'alejandra.perezg@udea.edu.co'
            destinatarios = correo
            asunto = 'Análisis de resultados'
            cuerpo = datos_pa
            ruta_adjunto = 'imaglab.png'
            nombre_adjunto = 'imaglab.png'
            #Se crea mensaje
            mensaje = MIMEMultipart()
            #los atributos del mensaje
            mensaje['From'] = remitente
            mensaje['To'] = ", ".join(destinatarios)
            mensaje['Subject'] = asunto
            # Agregamos el cuerpo del mensaje como un texto plano
            mensaje.attach(MIMEText(cuerpo, 'plain'))
            # Abrimos la imagen a adjuntar
            archivo_adjunto = open(ruta_adjunto, 'rb')
            adjunto_MIME = MIMEBase('application', 'octet-stream')
            adjunto_MIME.set_payload((archivo_adjunto).read())
            encoders.encode_base64(adjunto_MIME)
            adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
            #agregamos al mensaje
            mensaje.attach(adjunto_MIME)
            sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
            sesion_smtp.starttls()
            sesion_smtp.login('alejandra.perezg@udea.edu.co','xekone84')
            texto = mensaje.as_string()
            # Enviamos el mensaje
            sesion_smtp.sendmail(remitente, destinatarios, texto)
            sesion_smtp.quit()
            
#Se crea la clase que abre la siguiente ventana con las opcines a realizar
class Opciones(QDialog):
    def __init__(self):
        super(Opciones, self).__init__()
        loadUi('opciones.ui', self)
        #ventana opcion 1
        self.a_hemograma=opHemograma()
        self.bhemog.clicked.connect(self.ventana2)
        #ventana ocion 2
        self.a_bioquimico=opBioquimica()
        self.bbioqui.clicked.connect(self.ventana3)
       
    def ventana2(self):
        self.a_hemograma.show()#abir ventana opcion 1
    def ventana3(self):
        self.a_bioquimico.show()#abrir entana opcion 2
        
#S crea la clase que es la primera opcio. Ventana de hemograma        
class opHemograma(QDialog):
    def __init__(self):
        super(opHemograma, self).__init__()
        loadUi('hemograma.ui', self)
        #validacion. Solo numeros en todos
        self.hematies.setValidator(QtGui.QDoubleValidator())
        self.hemoglobina.setValidator(QtGui.QDoubleValidator())
        self.hematocrito.setValidator(QtGui.QDoubleValidator())
        self.leucocito.setValidator(QtGui.QDoubleValidator())
        self.linfocito.setValidator(QtGui.QDoubleValidator())
        self.neutrofilo.setValidator(QtGui.QDoubleValidator())
        self.eusinofilo.setValidator(QtGui.QDoubleValidator())
        self.plaqueta.setValidator(QtGui.QDoubleValidator())
        #conecto el boton con todas las acciones 
        self.banalizar.clicked.connect(self.on_clicked)
        
    #aqui se crean todas las funcines de los datos que recibe el hemograma
    #cada dato se debe analizar si esta o no dentro del rango
    #se retorna el resultado y el diagnostico
    #los datos deben ser flotantes
    def hHema(self):
        if self.hematies.text()=='':
            dato='Ninguno'
        a=float(self.hematies.text())
        if a>=4.5 and a<=5.5:
            dato='Hematies: ' + str(a) + ' Esta en el rango indicado [4.5-5.5]millones/mm3\n'
        elif a<4.5:
            dato='Hematies: ' + str(a) + ' Esta por debajo del rango indicado [4.5-5.5]millones/mm3. Puede padecer anemia \n' 
        elif a>5.5:
            dato='Hematies: ' + str(a) + ' Esta por encima del rango indicado [4.5-5.5]millones/mm3. Puede padecer poliglobulina (sangre espesa) \n'
        return dato
        
    def hHemo(self):
        if self.hemoglobina.text()=='':
            dato='Ninguno'
            return dato
        b=float(self.hemoglobina.text())
        if b>=12.5 and b<=16.5:
            dato='Hemoglobina: ' + str(b) + ' Esta en el rango indicado [12.5-16.5]g/dl \n'
        elif b<12.5:
            dato='Hemoglobina: ' + str(b) + ' Esta por debajo del rango indicado [12.5-16.5]g/dl. Puede padecer anemia y falta de hierro\n'
        elif b>16.5:
            dato='Hemoglobina: ' + str(b) + ' Esta por encima del rango indicado [12.5-16.5]g/dl. Puede padecer poliglobulina (sangre espesa)\n'
        return dato
        
    def hHemato(self):
        if self.hematocrito.text()=='':
            dato='Ninguno'
            return dato
        c=float(self.hematocrito.text())
        if c>=38.5 and c<=49.5:
            dato='Hematocrito: ' + str(c) + ' Esta en el rango indicado [38.5-49.5]%\n'
        elif c<38.5:
            dato='Hematocrito: ' + str(c) + ' Esta por debajo del rango indicado [38.5-49.5]%. Puede padecer anemia y/o hipertiroidismo.\n'
        elif c>49.5:
            dato='Hematocrito: ' + str(c) + ' Esta por encima del rango indicado [38.5-49.5]%. Puede padecer problemas cardiacos y/o falta de hidratacion.\n'
        return dato

    def hLinfo(self):
        if self.linfocito.text()=='':
            dato='Ninguno'
            return dato
        d=float(self.linfocito.text())
        if d>=1300 and d<=4000:
            dato='Linfocitos: ' + str(d) + ' Esta en el rango indicado [1300-4000]mL\n'
        elif d<1300:
            dato='Linfocitos: ' + str(d) + ' Esta por debajo del rango indicado [1300-4000]mL. Su sistema inmune es defectuoso.\n'
        elif d>4000:
            dato='Linfocitos: ' + str(d) + ' Esta por encima del rango indicado [1300-4000]mL. Puede padecer linfocitosis y/o alergias farmacologicas\n'
        return dato
        
    def hLeu(self):
        if self.leucocito.text()=='':
            dato='Ninguno'
            return dato
        e=float(self.leucocito.text())
        if e>=4500 and e<=11500:
            dato='Leucocitos: ' + str(e) + ' Esta en el rango indicado [4500-11500]mL\n'
        elif e<4500:
            dato='Leucocitos: ' + str(e) + ' Esta por debajo del rango indicado [4500-11500]mL.\n'
        elif e>11500:
            dato='Leucocitos: ' + str(e) + ' Esta por encima del rango indicado [4500-11500]mL.\n'
        return dato
        
    def hNeu(self):
        if self.neutrofilo.text()=='':
            dato='Ninguno'
            return dato
        f=float(self.neutrofilo.text())
        if f>=2000 and f<=7500:
            dato='Neutrofilos: ' + str(f) + ' Esta en el rango indicado [2000-7500]mL\n'
        elif f<2000:
            dato='Neutrofilos: ' + str(f) + ' Esta por debajo del rango indicado [2000-7500]mL. Puede padecer neutropenia.\n'
        elif f>7500:
            dato='Neutrofilos: ' + str(f) + ' Esta por encima del rango indicado [2000-7500]mL. Puede padecer neutrofilia. \n'
        return dato
    
    def hEosi(self):
        if self.eusinofilo.text()=='':
            dato='Ninguno'
            return
        g=float(self.eusinofilo.text())
        if g>=50 and g<=500:
            dato='Eosinofilos: ' + str(g) + ' Esta en el rango indicado [50-500]mL \n'
        elif g<50:
            dato='Eosinofilos: ' + str(g) + ' Esta por debajo del rango indicado [50-500]mL.\n'
        elif g>500:
            dato='Eosinofilos: ' + str(g) + ' Esta por encima del rango indicado [50-500]mL. Puede padecer alergias, asma, parásitos e/o infecciones. \n'
        return dato
        
    def hPla(self):
        if self.plaqueta.text()=='':
            dato='Ninguno'
            return dato
        h=float(self.plaqueta.text())
        if h>=150000 and h<=400000:
            dato='Plaquetas: ' + str(h) + ' Esta en el rango indicado [150000-400000]mm3 \n'
        elif h<150000:
            dato='Plaquetas: ' + str(h) + ' Esta por debajo del rango indicado [150000-400000]mm3. Puede padecer una mala coagulacion.\n'
        elif h>400000:
            dato='Plaquetas: ' + str(h) + ' Esta por encima del rango indicado [150000-400000]mm3. Puede padecer trombocitosis.\n'
        return dato
    #se crea l funcion que me conecta el boton   
    def on_clicked(self):
        #se llaman todas las funcines y se guardan en una variable
        hematies=self.hHema()
        hemoglobina=self.hHemo()
        hematocrito=self.hHemato()
        linfocitos=self.hLinfo()
        leucocitos=self.hLeu()
        neutrofilos=self.hNeu()
        eosinofilos=self.hEosi()
        plaquetas=self.hPla()
        #se crea el mensaje y se guarda en una variable
        correo_h=self.correo1.text()
        resultados= 'Segun los datos ingresados, los resultados son: \n\n' + hematies + '\n' + hemoglobina + '\n' + hematocrito + '\n' + linfocitos + '\n' + leucocitos + '\n' + neutrofilos + '\n' + eosinofilos + '\n' + plaquetas + '\nNOTA: si al menos un resultado esta alterado, debe ir al medico.\nGracias por usar nuestros servicios.'
        #validacion de los datos. Todos deben estar llenos para continuar
        if hematies=='Ninguno' or hemoglobina=='Ninguno' or hematocrito=='Ninguno' or linfocitos=='Ninguno' or leucocitos=='Ninguno' or neutrofilos=='Ninguno'or eosinofilos=='Ninguno' or plaquetas=='Ninguno':
            self.error.setText('Error. Faltan datos por llenar.')
        else:# si estan llenos se abre una ventana emergente con todos los resultados y el diagnostico
            self.error.setText('Datos ingresados correctamente.')
            QMessageBox.about(self,'Hemograma', resultados)
            
            #Se crea toda la iformacion del correo 
            remitente = 'alejandra.perezg@udea.edu.co'
            destinatarios = correo_h
            asunto = 'Análisis de resultados - Hemograma'
            cuerpo = resultados
            ruta_adjunto = 'download.png'
            nombre_adjunto = 'download.png'
            # Creamos el objeto mensaje
            mensaje = MIMEMultipart()
            #atributos del mensaje
            mensaje['From'] = remitente
            mensaje['To'] = ", ".join(destinatarios)
            mensaje['Subject'] = asunto
            mensaje.attach(MIMEText(cuerpo, 'plain'))
            archivo_adjunto = open(ruta_adjunto, 'rb')
            adjunto_MIME = MIMEBase('application', 'octet-stream')
            adjunto_MIME.set_payload((archivo_adjunto).read())
            encoders.encode_base64(adjunto_MIME)
            adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
            mensaje.attach(adjunto_MIME)
            sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
            sesion_smtp.starttls()
            sesion_smtp.login('alejandra.perezg@udea.edu.co','xekone84')
            texto = mensaje.as_string()
            sesion_smtp.sendmail(remitente, destinatarios, texto) 
            sesion_smtp.quit()
            
# se crea la clase que abre la ventana de la segunda opcon. Analisis bioquimico
class opBioquimica(QDialog):
    def __init__(self):
        super(opBioquimica, self).__init__()
        loadUi('bioquimica.ui', self)
        #validacion de todos los campos, deben ser solo numeros
        self.glucosa.setValidator(QtGui.QDoubleValidator())
        self.creatinina.setValidator(QtGui.QDoubleValidator())
        self.colesterol.setValidator(QtGui.QDoubleValidator())
        self.hdl.setValidator(QtGui.QDoubleValidator())
        self.ldl.setValidator(QtGui.QDoubleValidator())
        self.triglicerido.setValidator(QtGui.QDoubleValidator())
        self.calcio.setValidator(QtGui.QDoubleValidator())
        self.hierro.setValidator(QtGui.QDoubleValidator())
        self.bilirrubina.setValidator(QtGui.QDoubleValidator())
        #conecto el boton con las acciones que me realiza
        self.banalizar.clicked.connect(self.on_clicked)
    #aqui se crean todas las funcines de los datos que recibe el analsis bioquimico
    #cada dato se debe analizar si esta o no dentro del rango
    #se retorna el resultado y el diagnostico
    #los datos deben ser flotantes    
    def bGlu(self):
        if self.glucosa.text()=='':
            cosa='Ninguno'
            return cosa
        a=float(self.glucosa.text())
        if a>=70 and a<=110:
            cosa='Glucosa: ' + str(a) + ' Esta en el rango indicado [70-110]mg/dl\n'
        elif a<70:
            cosa='Glucosa: ' + str(a) + ' Esta por debajo del rango indicado [70-110]mg/dl. Puede padecer hipoglucemia\n'
        elif a>110:
            cosa='Glucosa: ' + str(a) + ' Esta por encima del rango indicado [70-110]mg/dl. Puede padecer hiperglucemia \n'
        return cosa
    
    def bCre(self):
        if self.creatinina.text()=='':
            cosa='Ninguno'
            return cosa
        b=float(self.creatinina.text())
        if b>=70 and b<=110:
            cosa='Creatinina: ' + str(b) + ' Esta en el rango indicado [70-110]mL/min \n'
        elif b<70:
            cosa='Creatinina: ' + str(b) + ' Esta por debajo del rango indicado [70-110]mL/min. Usted tiene poca masa muscular\n'
        elif b>110:
            cosa='Creatinina: ' + str(b) + ' Esta por encima del rango indicado [70-110]mL/min. Puede padecer deshidratacion o fallo renal \n'
        return cosa
            
    def bCol(self):
        if self.colesterol.text()=='':
            cosa='Ninguno'
            return cosa
        c=float(self.colesterol.text())
        if c>=120 and c<=200:
            cosa='Colesterol: ' + str(c) + ' Esta en el rango indicado [120-200]mg/dl \n'  
        elif c<120:
            cosa='Colesterol: ' + str(c) + ' Esta por debajo del rango indicado [120-200]mg/dl. \n'
        elif c>200:
            cosa='Colesterol: ' + str(c) + ' Esta por encima del rango indicado [120-200]mg/dl. Puede padecer nodulos rojos ya amarillos en la piel\n'
        return cosa
        
    def bH(self):
        if self.hdl.text()=='':
            cosa='Ninguno'
            return cosa
        d=float(self.hdl.text())
        if d>=42 and d<=90:
            cosa='HDL: ' + str(d) + ' Esta en el rango indicado [42-90]mg/dl\n'
        elif d<42:
            cosa='HDL: ' + str(d) + ' Esta por debajo del rango indicado [42-90]mg/dl. Puede sufrir episodios de isquemia cardiaca \n'
        elif d>90:
            cosa='HDL: ' + str(d) + ' Esta por encima del rango indicado [42-90]mg/dl.\n'
        return cosa
        
    def bL(self):
        if self.ldl.text()=='':
            cosa='Ninguno'
            return cosa
        e=float(self.ldl.text())
        if e>=0 and e<=160:
            cosa='LDL: ' + str(e) + ' Esta en el rango indicado [0-160]mg/dl\n'
        elif e>160:
            cosa='LDL: ' + str(e) + ' Esta por encima del rango indicado [0-160]mg/dl. Puede padecer enfermedades cardiacas\n'
        return cosa
        
    def bTri(self):
        if self.triglicerido.text()=='':
            cosa='Ninguno'
            return cosa
        f=float(self.triglicerido.text())
        if f>=30 and f<=250:
            cosa='Trigliceridos: ' + str(f) + ' Esta en el rango indicado [30-250]mg/dl\n'
        elif f<30:
            cosa='Trigliceridos: ' + str(f) + ' Esta por debajo del rango indicado [30-250]mg/dl. \n'
        elif f>250:
            cosa='Trigliceridos: ' + str(f) + ' Esta por encima del rango indicado [30-250]mg/dl. Puede padecer un factor de riesgo cardiovascular por arteriosclerosis.\n'
        return cosa
        
    def bCal(self):
        if self.calcio.text()=='':
            cosa='Ninguno'
            return cosa
        g=float(self.calcio.text())
        if g>=8.5 and g<=10.5:
            cosa='Calcio: ' + str(g) + ' Esta en el rango indicado [8.5-10.5]mg/dl\n'
        elif g<8.5:
            cosa='Calcio: ' + str(g) + ' Esta por debajo del rango indicado [8.5-10.5]mg/dl. Puede padecer hipocalcemia \n'
        elif g>10.5:
            cosa='Calcio: ' + str(g) + ' Esta por encima del rango indicado [8.5-10.5]mg/dl. Puede padecer hipercalcemia\n'
        return cosa
        
    def bHi(self):
        if self.hierro.text()=='':
            cosa='Ninguno'
            return cosa
        h=float(self.hierro.text())
        if h>=50 and h<=150:
            cosa='Hierro: ' + str(h) + ' Esta en el rango indicado [50-150]mg/dl \n'
        elif h<50:
            cosa='Hierro: ' + str(h) + ' Esta por debajo del rango indicado [50-150]mg/dl. Puede padecer anemia ferropenica\n'
        elif h>150:
            cosa='Hierro: ' + str(h) + ' Esta por encima del rango indicado [50-150]mg/dl. Puede padecer hemocromatosis\n'
        return cosa
        
    def bBi(self):
        if self.bilirrubina.text()=='':
            cosa='Ninguno'
            return cosa
        i=float(self.bilirrubina.text())
        if i>=0.2 and i<=1:
            cosa='Bilirrubina: ' + str(i) + ' Esta en el rango indicado [0.2-1]mg/dl\n'
        elif i<0.2:
            cosa='Bilirrubina: ' + str(i) + ' Esta por debajo del rango indicado [0.2-1]mg/dl.\n'
        elif i>1:
            cosa='Bilirrubina: ' + str(i) + ' Esta por encima del rango indicado [0.2-1]mg/dl. Puede padecer una enfermedad hepatica\n'
        return cosa
    #funcion que esta conetada cn el boton que realiza las acciones        
    def on_clicked(self):
        #llamo todas las funciones anteriores y las gardo en una variable
        glucosa=self.bGlu()
        creati=self.bCre()
        colest=self.bCol()
        hdl=self.bH()
        ldl=self.bL()
        trigliceridos=self.bTri()
        calcio=self.bCal()
        fe=self.bHi()
        bilirrubina=self.bBi()
        correo=self.correo2.text()
        #creo el mensaje con esas variables para ser mostrado en pantalla y mandado al correo
        resultados= 'Segun los datos ingresados, los resultados son: \n\n' + glucosa + '\n' + creati + '\n' + colest + '\n' + hdl + '\n' + ldl + '\n' + trigliceridos + '\n' + calcio + '\n' + fe + '\n' + bilirrubina + '\nNOTA: si al menos un resultado esta alterado, debe ir al medico.\nGracias por usar nuestros servicios.'
        #validacion de campos. Todos deben estar llenos para poder continuar
        if glucosa=='Ninguno' or creati=='Ninguno' or colest=='Ninguno' or hdl=='Ninguno' or ldl=='Ninguno' or trigliceridos=='Ninguno'or calcio=='Ninguno' or fe=='Ninguno' or bilirrubina=='':
            self.error.setText('Error. Faltan datos por llenar.')
        else: # si todos estan llenos se puede continuar. Muestra ventana emergente y envia el correo
            self.error.setText('Datos ingresados correctamente.')
            QMessageBox.about(self,'Analisis Bioquimico', resultados)
            #Se crea toda la iformacion del correo 
            remitente = 'alejandra.perezg@udea.edu.co'
            destinatarios = correo
            asunto = 'Análisis de resultados - Bioquimica'
            cuerpo = resultados
            ruta_adjunto = 'download.png'
            nombre_adjunto = 'download.png'
            mensaje = MIMEMultipart()
            #atributos del mensaje
            mensaje['From'] = remitente
            mensaje['To'] = ", ".join(destinatarios)
            mensaje['Subject'] = asunto
            mensaje.attach(MIMEText(cuerpo, 'plain'))
            # Abrimos el archivo que vamos a adjuntar
            archivo_adjunto = open(ruta_adjunto, 'rb')
            adjunto_MIME = MIMEBase('application', 'octet-stream')
            adjunto_MIME.set_payload((archivo_adjunto).read())
            encoders.encode_base64(adjunto_MIME)
            adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
            mensaje.attach(adjunto_MIME)
            sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
            sesion_smtp.starttls()
            sesion_smtp.login('alejandra.perezg@udea.edu.co','xekone84')
            texto = mensaje.as_string()
            sesion_smtp.sendmail(remitente, destinatarios, texto)
            sesion_smtp.quit()
#lineas de codigo obligatorias para lnzar la aplicacion         
if __name__ == "__main__":
    app=QApplication(sys.argv)
    widget=Sistema()#ventana principal
    widget.show()#lanzar ventana
    app.exec_()
    