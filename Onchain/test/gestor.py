# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 21:06:30 2022

@author: UnseR
"""

from PyQt5.QtWidgets import *
import sqlite3
from sqlite3 import Error

class Widgets(QWidget):
    #iniciar caracteristicas de los widgets
    def __init__(self,**kwargs):
        super(Widgets,self).__init__()
        self.vlayout=QVBoxLayout()
        
        self.hlayout_1=QHBoxLayout()
        
        self.l1=QLabel()
        self.l1.setText("Insertar matricula del personal")
        self.hlayout_1.addWidget(self.l1)
        
        self.t1=QLineEdit()
        self.hlayout_1.addWidget(self.t1)
        
        self.vlayout.addLayout(self.hlayout_1)
        
        self.hlayout_2=QHBoxLayout()
        
        self.l2=QLabel()
        self.l2.setText("Insertar nombre del personal")
        self.hlayout_2.addWidget(self.l2)
        
        self.t2=QLineEdit()
        self.hlayout_2.addWidget(self.t2)
        
        self.vlayout.addLayout(self.hlayout_2)
        
        self.hlayout_3=QHBoxLayout()
        
        self.l3=QLabel()
        self.l3.setText("inserte Categoria:")
        self.hlayout_3.addWidget(self.l3)
        
        self.t3=QLineEdit()
        self.hlayout_3.addWidget(self.t3)
        
        self.vlayout.addLayout(self.hlayout_3)
        
        self.btnn=QPushButton("Incluir personal")
        self.btnn.clicked.connect(self.incluir)
        self.vlayout.addWidget(self.btnn)
        
        self.btnn=QPushButton("Imprimir personal")
        self.btnn.clicked.connect(self.imprimir)
        self.vlayout.addWidget(self.btnn)
        
        self.setLayout(self.vlayout)
    #Crear coneccion con la base de datos
    def create_connection(self,path):
    	connection=None
    	try:
    		connection =sqlite3.connect(path)
    		print("Conexion exitosa")
    	except Error as e:
    		print(f"Error: {e}")
    	return connection

    #ejecutar una consulta, añadir en este caso
    def execute_query(self,connec, query):
    	cursor=connec.cursor()
    	try:
    		cursor.execute(query)
    		connec.commit()
    		print("Consulta ejecutada")
    	except Error as e:
    		print(f"Error '{e}' ocurrio")
    #Imprimir en pantalla luego de haber selccionado todos los atributos de la tabla
    def execute_read_query(self,connec,query):
    	cursor=connec.cursor()
    	result=None
    	try:
    		cursor.execute(query)
    		column_names=[description[0] for description in cursor.description]
    		print(column_names)
    		result=cursor.fetchall()
    		return result
    	except Error as e:
    		print(f"Error {e}")
    #Funcion para incluir personal
    def incluir(self):
        con=self.create_connection("Base.db")
        query=f'insert into personal (Matricula,Nombre,Categoria) values ({self.t1.text()},"{self.t2.text()}",{self.t3.text()});'
        self.execute_query(con,query)
    #funcion para imprimir en pantalla
    def imprimir(self):
        con=self.create_connection("Base.db")
        query = "SELECT * from personal"
        personal = self.execute_read_query(con, query)
        if personal:
            for per in personal:
                print(per)
                
#funcion principal
def window():
    app=QApplication([])
    wig=Widgets()

    wig.show()
    app.exec()
if __name__=="__main__":
    window()
