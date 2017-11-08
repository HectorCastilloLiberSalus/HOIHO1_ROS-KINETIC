#!/usr/bin/env python
#-*- coding: utf-8 -*-
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
import rospy
from std_msgs.msg import Float32
import numpy
import time
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist
import sys, curses
from std_msgs.msg import String
from std_msgs.msg import Empty
#from face_recognition.msg import FaceRecognitionActionFeedback
from std_msgs.msg import Int16
from opencv_apps.msg import FaceArrayStamped

global voz, mover,vel_msg, soundhandle, X, Y, Z, THETA,G, R1, R2, pub,Xd, Yd, Zd, THETAd, Gd, pubD, TACO, rate,  nombre, nombre_identificado, it, nombre_encontrado,pubcara, idioma, chiste 
chiste = 0
vel_msg = Twist()
it = 0
X = 90
Y = 180
Z = 150
THETA = 90
G = 0
R1 = 90
R2 = 50
voz = 0
vel_msg.linear.y = 0
vel_msg.linear.z = 0
vel_msg.angular.x = 0
vel_msg.angular.y = 0
TACO = 0
nombre = ' '
nombre_identificado = 0
nombre_encontrado= ''
idioma = 2
#rate = rospy.Rate(10)
def nombre(data):
    global it, nombre_identificado, nombre, nombre_encontrado
   
    if (data.faces[0].label):
	    if (nombre_identificado == 0 or it == 10):
	    	nombre = str(data.faces[0].label)
		nombre_identificado = nombre_identificado + 1
	        it  = 0
	    if (nombre_identificado>0):
		if (nombre == str(data.faces[0].label)):
			nombre_identificado = nombre_identificado + 1 
	        if (nombre_identificado == 15):
	   		nombre_encontrado = str(data.faces[0].label)
			print(nombre_encontrado)
			nombre_identificado = 0
    it = it + 1
def callback_create(data):
    global voz, vel_msg, soundhandle
    #rospy.loginfo(rospy.get_caller_id() + 'Parar %s', data)
    vel_msg.linear.x = abs(0)
    vel_msg.angular.z = abs(0)
    mover.publish(vel_msg)


def callback(data):
    recognized = 0

    global voz, vel_msg, soundhandle, X, Y, Z, THETA, G, R1, R2,pub, pubD, TACO,Xd, Yd, Zd, THETAd, Gd, rate, nombre_encontrado, pubcara, idioma, chiste,  pubVOZ, pubidioma, pubidiomarec
    #rospy.loginfo(rospy.get_caller_id() + 'Dijiste:  %s', data.data)
    rate = rospy.Rate(10) # 10hz
    
    if (data.data == 'Spanish' or data.data == 'Espanol'):
	    s = "idioma español"
	    pubidiomarec.publish('spanish')
            pubidioma.publish('es-la')
   	    pubVOZ.publish(s)
    	    rospy.sleep(1)
	    recognized = 1

    
    if (data.data == 'inglés' or data.data == 'english' ):
	    s = "english spoken"
	    pubidiomarec.publish('english')
            pubidioma.publish('en')
   	    pubVOZ.publish(s)
    	    rospy.sleep(1)
	    recognized = 1
    if ('Hola' in data.data):
            pubcara.publish(abs(1))
	    s = "Hola"
            pubidioma.publish('es-la')
   	    pubVOZ.publish(s)
    	    rospy.sleep(1)
	    recognized = 1

    if ('hello' in data.data):
            pubcara.publish(abs(1))
	    s = "hello"
            pubidioma.publish('en')
   	    pubVOZ.publish(s)
    	    rospy.sleep(1)
	    recognized = 1



    if ('who are you' in data.data and recognized == 0):
        pubcara.publish(abs(1))
	s = "Hello, i am hoiho"
        pubidioma.publish('en')
   	pubVOZ.publish(s)
    	rospy.sleep(1)
	recognized = 1

    if ('quién eres' in data.data and recognized == 0):
	s = "Hola, soy joijo"
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
    	rospy.sleep(1)
	recognized = 1

    volume = 1
    if ('front' in data.data and recognized == 0):
	pubcara.publish(abs(3))	
	vel_msg.linear.x = abs(0.05)
	vel_msg.angular.z = abs(0)
	ss = "ok going front,  ,   ,   ,   ,  ,  ,  ,"
	s = ss + nombre_encontrado    	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	for ww in range (0, 30):
		mover.publish(vel_msg)
		time.sleep(0.1)
	recognized = 1

    if ('adelante' in data.data and recognized == 0):
	ss = "OK        yendo al frente                      "
	s = ss + nombre_encontrado    	
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
	pubcara.publish(abs(3))	
	vel_msg.linear.x = abs(0.05)
	vel_msg.angular.z = abs(0)	
	
	for ww in range (0, 30):
		mover.publish(vel_msg)
		time.sleep(0.1)
	recognized = 1

    if ('back' in data.data and recognized == 0):
	vel_msg.linear.x = -abs(0.05)
	vel_msg.angular.z = abs(0)
	pubcara.publish(abs(3))	
	ss = "ok going back,  ,   ,   ,   ,  ,  ,  ,"
	s = ss + nombre_encontrado    	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	for ww in range (0, 30):
		mover.publish(vel_msg)
		time.sleep(0.1)
	recognized = 1

    if ('atrás' in data.data and recognized == 0):
	vel_msg.linear.x = -abs(0.05)
	vel_msg.angular.z = abs(0)
	pubcara.publish(abs(3))	
	ss = "OK, yendo atras "
	s = ss + nombre_encontrado    	
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
	for ww in range (0, 30):
		mover.publish(vel_msg)
		time.sleep(0.1)
	recognized = 1

    if ('sing a song' in data.data and recognized == 0):
	pubcara.publish(abs(5))	
	ss = "Ok, but you must clap"
	s = ss + nombre_encontrado    	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	pubcara.publish(abs(1))	
	cantar = rospy.Publisher('cantar', Int16, queue_size=10)
	cantar.publish(abs(1))
	recognized = 1

    if ('canta una canción' in data.data and recognized == 0):
	pubcara.publish(abs(5))	
	ss = "OK   pero debes aplaudir                  "
	s = ss + nombre_encontrado    	
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
	pubcara.publish(abs(1))	
	cantar = rospy.Publisher('cantar', Int16, queue_size=10)
	cantar.publish(abs(1))
	recognized = 1

    if ('rigth' in data.data and recognized == 0):
	vel_msg.angular.z = -abs(0.55)
	vel_msg.linear.x = abs(0)
	mover.publish(vel_msg)
	pubcara.publish(abs(3))	
	ss =  "ok turning right"
	s = ss + nombre_encontrado    	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	recognized = 1


    if ('derecha' in data.data and recognized == 0):
	vel_msg.angular.z = -abs(0.55)
	vel_msg.linear.x = abs(0)
	mover.publish(vel_msg)
	pubcara.publish(abs(3))	
	ss = "OK, girando a la derecha                     "
	s = ss + nombre_encontrado    	
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
	recognized = 1

    if ('left' in data.data and recognized == 0):
	vel_msg.angular.z = abs(0.5)
	vel_msg.linear.x = abs(0)
	mover.publish(vel_msg)
	pubcara.publish(abs(3))	
	ss =  "ok, turning left"
        pubidioma.publish('en')
   	pubVOZ.publish(s)
    	soundhandle.say(s, voice, volume) 
 	recognized = 1

    if ('izquierda' in data.data and recognized == 0):
	vel_msg.angular.z = abs(0.5)
	vel_msg.linear.x = abs(0)
	mover.publish(vel_msg)
	pubcara.publish(abs(3))	
	ss = "OK, girando a la izquierda                 "
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
    	soundhandle.say(s, voice, volume) 
 	recognized = 1

    if ('how' in data.data and 'are' in data.data and recognized == 0):
	pubcara.publish(abs(2))	
	ss = "I am fine, , , , and you?,,,,,,,,,,,,"
	s = ss + nombre_encontrado    	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1

    if ('Cómo' in data.data and 'estás' in data.data and recognized == 0):
	pubcara.publish(abs(2))	
	ss = "Estoy bien y tu                              "
	s = ss + nombre_encontrado    	
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1


    if ('nice' in data.data and 'meet' in data.data and recognized == 0):
	pubcara.publish(abs(1))	
	ss = "nice to meet you too"
	s = ss + nombre_encontrado    	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1

    if ('not recognized' in data.data and 'meet' in data.data and recognized == 0):
	pubcara.publish(abs(1))	
	rospy.sleep(1)
	recognized = 1


    if ('gusto' in data.data and 'conocerte' in data.data and recognized == 0):
	pubcara.publish(abs(1))	
	ss = "Encantado de conocerte  también             "
	s = ss + nombre_encontrado    	
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1


    if ('go home' in data.data and recognized == 0):
	pubcara.publish(abs(1))	
	ss = "Ok, going home"
	s = ss + nombre_encontrado    	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1

    if ('ve a casa' in data.data and recognized == 0):
	pubcara.publish(abs(1))	
	ss = "Okey llendo a casa              "
	s = ss + nombre_encontrado    	
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1

    if ('fine' in data.data and recognized == 0):
	pubcara.publish(abs(1))	
	ss = "great"
	s = ss + nombre_encontrado    	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1


    if ('estoy bien' in data.data and recognized == 0):
	pubcara.publish(abs(1))	
	ss = "Fantastico                     "
	s = ss + nombre_encontrado    	
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1

    if ('stop' in data.data and recognized == 0):
	pubcara.publish(abs(1))	
	ss ="ok, , , stopping"
   	s = ss + nombre_encontrado    	
        voice = 'voice_cmu_us_slt_arctic_hts'
    	vel_msg.linear.x = abs(0)
    	vel_msg.angular.z = abs(0)
    	mover.publish(vel_msg)

    if ('para' in data.data and recognized == 0):
	pubcara.publish(abs(1))	
	ss = "Okey                  parando         "
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
    	vel_msg.linear.x = abs(0)
    	vel_msg.angular.z = abs(0)
    	mover.publish(vel_msg)


    if ('kind of animal' in data.data and recognized == 0):
	pubcara.publish(abs(1))	
	ss ="Im a penguin"
	s = ss + nombre_encontrado    	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	rospy.sleep(3)
	recognized = 1
	soundhandle.playWave('/home/rissa/Documentos/pinguino.wav',0.3)

    if ('animal eres' in data.data and recognized == 0):
	pubcara.publish(abs(1))	
	ss = "Soy un pinguino                "
	s = ss + nombre_encontrado    	
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
	rospy.sleep(3)
	recognized = 1
	soundhandle.playWave('/home/rissa/Documentos/pinguino.wav',0.3)

    if ('come' in data.data and 'here' in data.data and recognized == 0):
	vel_msg.linear.x = abs(0.05)
	vel_msg.angular.z = abs(0)
	pubcara.publish(abs(1))	
	ss = "ok,  ,   ,   ,   ,  ,  ,  ,"
	s = ss + nombre_encontrado    	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	for ww in range (0, 30):
		mover.publish(vel_msg)
		time.sleep(0.1)
	recognized = 1

    if ('ven aqui' in data.data and recognized == 0):
	vel_msg.linear.x = abs(0.05)
	vel_msg.angular.z = abs(0)
	pubcara.publish(abs(1))	
	ss = "Okey                        "
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
    	soundhandle.say(s, voice, volume)
	for ww in range (0, 30):
		mover.publish(vel_msg)
		time.sleep(0.1)
	recognized = 1


    if ('favorite' in data.data and 'robot' in data.data and recognized == 0):
	pubcara.publish(abs(5))	
	ss = "hoiho robotics is my favorite"
	s = ss + nombre_encontrado    	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1

    if ('favoritos' in data.data and 'robots' in data.data and recognized == 0):
	pubcara.publish(abs(5))	
	ss = "los robots joijo son mis favoritos        "
	s = ss + nombre_encontrado    	
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1


    if ('follow' in data.data and 'me' in data.data and recognized == 0):
	ss = "ok following you"
	s = ss + nombre_encontrado    	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1


    if ('sigueme' in data.data and recognized == 0):
	ss = "Ok              te sigo             "
	s = ss + nombre_encontrado    	
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1
 
    if ('take' in data.data and recognized == 0):
	s = "ok, , ,"
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1
	G = 1
	a = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
	pub.publish(a)

    if ('toma' in data.data and recognized == 0):
	s = "okey"
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1
	G = 1
	a = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
	pub.publish(a)
  
    if ('ugly' in data.data  and recognized == 0):
	pubcara.publish(abs(6))	
	ss = "At least i am not a human being     "
	s = ss + nombre_encontrado    	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1

    if ('feo' in data.data  and recognized == 0):
	pubcara.publish(abs(6))	
	ss = "al menos no soy un humano                "
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
	soundhandle.say(s, voice, volume)
	rospy.sleep(1)
	recognized = 1
 
    if ('can' in data.data  and 'do' in data.data  and recognized == 0):
	pubcara.publish(abs(1))	
	s = "i prepare tacos, clean houses, chew gum and i have hard punch    "
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1

    if ('puedes' in data.data  and 'hacer' in data.data  and recognized == 0):
	pubcara.publish(abs(1))	
        s = "hago tacos, limpio pisos, masco chicle y pego duro                "
        pubidioma.publish('es-la')
   	pubVOZ.publish(s)
	rospy.sleep(1)
	recognized = 1

        voice = 'voice_el_diphone'




######################## Make a taco ########################
    if ('me' in data.data or 'make' in data.data and recognized == 0 ):
	pubcara.publish(abs(1))
	ss1 = "ok , , "
	ss = ss1 + nombre_encontrado
	s = ss + ", , , , can you help me, , ,  ?"   	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	nombre_encontrado= ''
	TACO = 1
	recognized = 1
	rate.sleep()
	time.sleep(2)
    if (TACO == 1 and 'okay' in data.data and recognized == 0 ):
	X = 70
	Y = 200
	Z = 90
	THETA = 80
	G = 0		
	i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
	rospy.loginfo(i)
	pub.publish(i)
	rate.sleep()
	Xd = 165
	Yd = 0
	Zd = 10
	THETAd = 100
        Gd = 0
	d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
	rospy.loginfo(d)		
	pubD.publish(d) 
	rate.sleep()
	time.sleep(2)
	ss1 = "entendido, "
	ss = nombre_encontrado
	s = ss + "put a spoon on my right hand"   	
	rospy.sleep(3)
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	nombre_encontrado= ''
	TACO = 2
	recognized = 1
	rate.sleep()

    if (TACO == 2 and 'okay' in data.data and recognized == 0):
	Xd = 165
	Yd = 0
	Zd = 10
	THETAd = 100
        Gd = 1
	d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
	rospy.loginfo(d)		
	pubD.publish(d) 
	recognized = 1
   	ss1 = "thank you"
	ss = ss1 + nombre_encontrado
	s = ss + ", , , now put a dish on my left hand?"   	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	nombre_encontrado= ''
	rospy.sleep(1)
	X = 70
	Y = 200
	Z = 90
	THETA = 80
	G = 0		
	i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
	rospy.loginfo(i)
	pub.publish(i)
	TACO = 3
    if (TACO == 3 and 'okay' in data.data and recognized == 0):
        X = 70
	Y = 200
	Z = 90
	THETA = 80
	G = 1	
	i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
	rospy.loginfo(i)
	pub.publish(i)
	TACO = 3
	ss1 = "thank you"
	s = ss1 + nombre_encontrado
	nombre_encontrado= ''    	
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	TACO = 4
	recognized = 1
        X = 20
	Y = 200
	Z = 150
	THETA = 80
	G = 1	
	i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
	rospy.loginfo(i)
	pub.publish(i)
	rospy.sleep(1)
################ Moverse hasta la mesa ##############################
	vel_msg.linear.x = abs(0.25)
	vel_msg.angular.z = abs(0)
	for ww in range (0, 60):
		mover.publish(vel_msg)
		time.sleep(0.1)
	rate.sleep()   
		#time.sleep(2)    		
#################################################################
	vel_msg.angular.z = -abs(0.5)
	vel_msg.linear.x = abs(0)
	for ww in (0,1):
		mover.publish(vel_msg)
		time.sleep(0.1)
		rate.sleep()
############### Dejar el plato ###############################
	X = 25
	Y = 200
	Z = 150
	THETA = 170
	G = 1	
	X = 28
	Y = 200
	Z = 150
	THETA = 80
	G = 0	
	i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
	rospy.loginfo(i)
	pub.publish(i)
		#rospy.sleep(2)
        X = 25
	Y = 150
	Z = 150
	THETA = 80
	G = 0	
	i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
	rospy.loginfo(i)
	pub.publish(i)
	rospy.sleep(4)
#################################################################
	vel_msg.linear.x = -abs(0.05) 
	vel_msg.angular.z = abs(0)
	for ww in range (0, 10):
		mover.publish(vel_msg)
		time.sleep(0.1)

#################################################################
	vel_msg.angular.z = abs(0.5)
	vel_msg.linear.x = abs(0)
	for rw in range(0,18):
		mover.publish(vel_msg)
		time.sleep(0.1)
	rate.sleep()
        X = 25
	Y = 150
	Z = 150
	THETA = 80
	G = 0	
        X = 25
	Y = 200
	Z = 150
	THETA = 80
	G = 0	
	i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
	rospy.loginfo(i)
	pub.publish(i)
	rospy.sleep(2)
	Xd = 150
	Yd = 30
	Zd = 10
	THETAd =55
        Gd = 1
	d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
	rospy.loginfo(d)		
	pubD.publish(d) 
	recognized = 1
	rospy.sleep(4)


	Xd = 150
	Yd = 0
	Zd = 10
	THETAd = 55
        Gd = 1
	d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
	rospy.loginfo(d)		
	pubD.publish(d) 
	recognized = 1
	rospy.sleep(2)

	Xd = 150
	Yd = 0
	Zd = 10
	THETAd = 90
        Gd = 1
	d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
	rospy.loginfo(d)		
	pubD.publish(d) 
	recognized = 1
	rospy.sleep(2)

	Xd = 158
	Yd = 0
	Zd = 10
	THETAd = 100
        Gd = 1
	d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
	rospy.loginfo(d)		
	pubD.publish(d) 
	recognized = 1
	rospy.sleep(4)
	vel_msg.angular.z = abs(0.2)
	vel_msg.linear.x = abs(0.02)
	for ww in (0,50):
		mover.publish(vel_msg)
		time.sleep(0.1)
	rate.sleep() 
	vel_msg.angular.z = abs(0.2)
	vel_msg.linear.x = abs(0)
	for ww in range(0,10):
		mover.publish(vel_msg)
		time.sleep(0.1)
	rate.sleep()  
	Xd = 158
	Yd = 0
	Zd = 10
	THETAd = 50
        Gd = 1
	d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
	rospy.loginfo(d)		
	pubD.publish(d) 
	recognized = 1
	rospy.sleep(2) 

	Xd = 173
	Yd = 0
	Zd = 10
	THETAd = 100
        Gd = 1
	d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
	rospy.loginfo(d)		
	pubD.publish(d) 
	recognized = 1
	rospy.sleep(5) 
		
		## Regresar a tomar el plato
	vel_msg.angular.z = -abs(0.5)
	vel_msg.linear.x = abs(0)
	for ww in range(0,27):
		mover.publish(vel_msg)
		time.sleep(0.1)
	rate.sleep() 
	vel_msg.angular.z = 0
	vel_msg.linear.x = abs(0.05)
	for ww in range(0,8):
		mover.publish(vel_msg)
		time.sleep(0.1)
	rate.sleep()  
        X = 25
	Y = 200
	Z = 150
	THETA = 80
	G = 1	
	i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
	rospy.loginfo(i)
	pub.publish(i)
	rospy.sleep(2)

		## 
        X = 15
	Y = 200
	Z = 150
	THETA = 80
	G = 1	
	i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
	rospy.loginfo(i)
	pub.publish(i)
	rospy.sleep(2)

	vel_msg.angular.z = -abs(0.5)
	vel_msg.linear.x = abs(0)
	for ww in range(0,67):
		mover.publish(vel_msg)
		time.sleep(0.1)
	rate.sleep() 
	time.sleep(2)
	vel_msg.linear.x = abs(0.25)
	vel_msg.angular.z = abs(0)
	for ww in range (0, 45):
		mover.publish(vel_msg)
		time.sleep(0.1)
	rate.sleep()  
 
    if ('no connection' in data.data and recognized == 0):
	s = "i dont have internet connection"
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	recognized = 1  


    if ('not recognized' in data.data and recognized == 0):
	s = "Can you repeat?"
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	recognized = 1  

    if(recognized == 0):
        pubcara.publish(abs(2))
	print("la cara publica")
	ss1 = "Sorry,  i dont understand"
	s = ss1 + nombre_encontrado
        pubidioma.publish('en')
   	pubVOZ.publish(s)
	s = ""
	rospy.sleep(1)
	rate.sleep() 

    
def talker():
    global voz, mover, vel_msg, soundhandle, X, Y, Z, THETA, G, R1, R2, pub, pubD, pubcara, pubVOZ, pubidioma, pubidiomarec
    pubcara = rospy.Publisher('expresion', Int16, queue_size=10)
    pubD = rospy.Publisher('derecho', Float32MultiArray, queue_size=10)
    pub = rospy.Publisher('izquierdo', Float32MultiArray, queue_size=10)
    pubC1 = rospy.Publisher('cabezarot', Float32MultiArray, queue_size=10)
    pubC2 = rospy.Publisher('cabezarot2', Float32MultiArray, queue_size=10)
    pubVOZ = rospy.Publisher('text', String, queue_size=10)
    pubidioma = rospy.Publisher('idioma', String, queue_size=10)
    pubidiomarec = rospy.Publisher('idioma_reconocer', String, queue_size=10)
    mover = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('mandobrazos', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.addstr(0,0,"Teclea los comandos")
    stdscr.refresh()
    tecla = '' 
    TACO = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0


    #'''
    X = 90
    Y = 180
    Z = 150
    THETA = 40
    G = 0
    Xd = 90
    Yd = 2
    Zd = 20
    THETAd = 0
    Gd = 0
    R1 = 90
    R2 = 50
    rospy.Subscriber('palabras', String, callback)
    rospy.Subscriber('wheeldrop', Empty, callback_create)
    rospy.Subscriber('/face_recognition/output', FaceArrayStamped, nombre)
    soundhandle = SoundClient()
    rospy.sleep(1)

    voice = 'voice_el_diphone'
    volume = 1
    s = "Hola"
    while not rospy.is_shutdown():
	tecla = stdscr.getch()
        #stdscr.refresh()
	if(tecla == ord('8')):
		vel_msg.linear.x = abs(0.25)
		vel_msg.angular.z = abs(0)
		for ww in range (0, 75):
			mover.publish(vel_msg)
			time.sleep(0.1)
		print("adelante")
	if(tecla == ord('5')):
		vel_msg.linear.x = -abs(0.05)
		vel_msg.angular.z = abs(0)
		for ww in range (0, 30):
			mover.publish(vel_msg)
			time.sleep(0.1)
		print("atras")
	if(tecla == ord('4')):
		vel_msg.angular.z = abs(0.5)
		vel_msg.linear.x = abs(0)
		mover.publish(vel_msg)
		print("izquierda")
	if(tecla == ord('6')):
		vel_msg.angular.z = -abs(0.5)
		vel_msg.linear.x = abs(0)
		mover.publish(vel_msg)
		print("Derecha")
	if(tecla == ord('q')):
		# Empezar los comandos
		X = 70
		Y = 200
		Z = 90
		THETA = 170
		G = 0		
		i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
		Xd = 165
		Yd = 0
		Zd = 10
		THETAd = 90
		Gd = 0
		d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
		rospy.loginfo(d)		
		pubD.publish(d) 
		rospy.sleep(3)
		rospy.loginfo(i)
		pub.publish(i)
		rospy.sleep(3)

		Xd = 165
		Yd = 0
		Zd = 10
		THETAd = 90
                Gd = 0
		d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
		rospy.loginfo(d)		
		pubD.publish(d) 
		TACO = 2

	if (TACO == 2):
		Xd = 165
		Yd = 0
		Zd = 10
		THETAd = 90
                Gd = 1
		d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
		rospy.loginfo(d)		
		pubD.publish(d) 
		recognized = 1
		rospy.sleep(4)
	     
		X = 70
		Y = 200
		Z = 90
		THETA = 170
		G = 0		
		i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
		rospy.loginfo(i)
		pub.publish(i)
		rospy.sleep(4)
		TACO = 3
	if (TACO == 3):
                X = 70
		Y = 200
		Z = 90
		THETA = 170
		G = 1	
		i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
		rospy.loginfo(i)
		pub.publish(i)
		rospy.sleep(4) 	

		TACO = 4
		recognized = 1
                X = 20
		Y = 200
		Z = 150
		THETA = 170
		G = 1	
		i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
		rospy.loginfo(i)
		pub.publish(i)
		rospy.sleep(4)
################moverse hasta la mesa ##########################
		vel_msg.linear.x = abs(0.25)
		vel_msg.angular.z = abs(0)
		for ww in range (0, 60):
			mover.publish(vel_msg)
			time.sleep(0.1)
		rate.sleep()   
		time.sleep(5)    		
#################################################################
		vel_msg.angular.z = -abs(0.5)
		vel_msg.linear.x = abs(0)
		for ww in (0,1):
			mover.publish(vel_msg)
			time.sleep(0.1)
		rate.sleep()
############### Dejar el plato ###############################
		X = 30
		Y = 200
		Z = 150
		THETA = 170
		G = 1	
		X = 35
		Y = 200
		Z = 150
		THETA = 170
		G = 0	
		i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
		rospy.loginfo(i)
		pub.publish(i)
		rospy.sleep(4)
                X = 35
		Y = 150
		Z = 150
		THETA = 170
		G = 0	
		i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
		rospy.loginfo(i)
		pub.publish(i)
		rospy.sleep(10)
#################################################################
		vel_msg.linear.x = -abs(0.05) 
		vel_msg.angular.z = abs(0)
		for ww in range (0, 10):
			mover.publish(vel_msg)
			time.sleep(0.1)

#################################################################
		vel_msg.angular.z = abs(0.5)
		vel_msg.linear.x = abs(0)
		for rw in range(0,18):
			mover.publish(vel_msg)
			time.sleep(0.1)
		rate.sleep()
                X = 35
		Y = 150
		Z = 150
		THETA = 170
		G = 0	
                X = 30
		Y = 200
		Z = 150
		THETA = 170
		G = 0	
		i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
		rospy.loginfo(i)
		pub.publish(i)
		rospy.sleep(4)

		Xd = 147
		Yd = 30
		Zd = 10
		THETAd = 35
                Gd = 1
		d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
		rospy.loginfo(d)		
		pubD.publish(d) 
		recognized = 1
		rospy.sleep(4)


		Xd = 147
		Yd = 0
		Zd = 10
		THETAd = 35
                Gd = 1
		d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
		rospy.loginfo(d)		
		pubD.publish(d) 
		recognized = 1
		rospy.sleep(4)

		Xd = 155
		Yd = 0
		Zd = 10
		THETAd = 70
                Gd = 1
		d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
		rospy.loginfo(d)		
		pubD.publish(d) 
		recognized = 1
		rospy.sleep(4)

		Xd = 155
		Yd = 0
		Zd = 10
		THETAd = 70
                Gd = 1
		d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
		rospy.loginfo(d)		
		pubD.publish(d) 
		recognized = 1
		rospy.sleep(4)
		vel_msg.angular.z = abs(0.2)
		vel_msg.linear.x = abs(0.02)
		for ww in (0,50):
			mover.publish(vel_msg)
			time.sleep(0.1)
		rate.sleep() 
		vel_msg.angular.z = abs(0.2)
		vel_msg.linear.x = abs(0)
		for ww in range(0,10):
			mover.publish(vel_msg)
			time.sleep(0.1)
		rate.sleep()  
		Xd = 155
		Yd = 0
		Zd = 10
		THETAd = 20
                Gd = 1
		d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
		rospy.loginfo(d)		
		pubD.publish(d) 
		recognized = 1
		rospy.sleep(4) 

		Xd = 170
		Yd = 0
		Zd = 10
		THETAd = 70
                Gd = 1
		d = numpy.array([Xd,Yd,Zd,THETAd,Gd],dtype=numpy.float32)
		rospy.loginfo(d)		
		pubD.publish(d) 
		recognized = 1
		rospy.sleep(4) 
		
		## Regresar a tomar el plato
		vel_msg.angular.z = -abs(0.5)
		vel_msg.linear.x = abs(0)
		for ww in range(0,27):
			mover.publish(vel_msg)
			time.sleep(0.1)
		rate.sleep() 
		vel_msg.angular.z = 0
		vel_msg.linear.x = abs(0.05)
		for ww in range(0,8):
			mover.publish(vel_msg)
			time.sleep(0.1)
		rate.sleep()  
                X = 30
		Y = 200
		Z = 150
		THETA = 170
		G = 1	
		i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
		rospy.loginfo(i)
		pub.publish(i)
		rospy.sleep(4)

		## 
                X = 15
		Y = 200
		Z = 150
		THETA = 170
		G = 1	
		i = numpy.array([X,Y,Z,THETA,G],dtype=numpy.float32)
		rospy.loginfo(i)
		pub.publish(i)
		rospy.sleep(4)

		vel_msg.angular.z = -abs(0.5)
		vel_msg.linear.x = abs(0)
		for ww in range(0,67):
			mover.publish(vel_msg)
			time.sleep(0.1)
		rate.sleep() 
		time.sleep(4)
		vel_msg.linear.x = abs(0.25)
		vel_msg.angular.z = abs(0)
		for ww in range (0, 60):
			mover.publish(vel_msg)
			time.sleep(0.1)
		rate.sleep()   
  
	#rospy.loginfo(a)
		
	
	#pubD.publish(a)


	#vel_msg.linear.x = 0
	#mover.publish(vel_msg)
	rate.sleep()
	rospy.spin()
    curses.endwin()
if __name__ == '__main__':
    try:
        talker()

    except rospy.ROSInterruptException:
        pass
