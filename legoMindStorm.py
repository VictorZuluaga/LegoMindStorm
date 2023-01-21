#!/usr/bin/env python3
from ev3dev.ev3 import *
import os
import time
os.system('setfont Lat15-TerminusBold14')

#Variables referentes al motor
mR = LargeMotor('outA');
mR.stop_action = 'hold';
mL = LargeMotor('outB');
mL.stop_action = 'hold';
us = UltrasonicSensor();
us.mode = 'US-DIST-CM';
#variables
contador_depuracion = 1;
contador_sensor = 1;
contador_log = 1;
#constantes
log_depuracion = open("log_depuracion.txt", "w");
log_sensor1 = open("log_sensor1.txt", "w");
log_sensor2 = open("log_sensor2.txt", "w");
log_sensor3 = open("log_sensor3.txt", "w");
angle = 10;
correction_speed = 25;
normal_speed = 100;
rotate_complete = 83;
rotate_half = rotate_complete/2;
rotate_quarter = rotate_complete/4;

#Espacio de funciones
def move_ticks(right_m,left_m,speed,sense): #giro a izquierda sense = 1, giro a derecha sense = -1
        mR.run_to_rel_pos(position_sp=-sense*right_m, speed_sp=speed);
        mL.run_to_rel_pos(position_sp=sense*left_m, speed_sp=speed);

def move_straight(cm,speed,sense): #marcha atras sense = -1, sense=1 hacia adelante
        #1cm equivale a 10 ticks por rueda?
        ticks = 10*2*cm;
        mR.run_to_rel_pos(position_sp=sense*ticks, speed_sp=speed);
        mL.run_to_rel_pos(position_sp=sense*ticks, speed_sp=speed);
        mR.wait_while('running');
        mL.wait_while('running');
        reset_motors();

def wait_for_both():
        mR.wait_while('running', timeout=300);
        mL.wait_while('running', timeout=300);

def rotate(num,sense):
        global angle;
        global normal_speed;
        global contador_depuracion;
        global contador_log;
        for x in range(num):
                if(contador_log == 1):
                        write_log_sensor(log_sensor1);
                if(contador_log == 2):
                        write_log_sensor(log_sensor2);
                if(contador_log == 3):
                        write_log_sensor(log_sensor3);

                move_ticks(angle,angle,normal_speed,sense);
                wait_for_both();
                correction(contador_depuracion,sense);
                write_log_depuracion();
        contador_log = contador_log + 1;
        reset_motors();

def write_log_depuracion():
        global contador_depuracion;
        global angle;
        log_depuracion.write(str(contador_depuracion)+" "+str(contador_depuracion*angle)+ "--> " + "mR: " + str(mR.position) + " mL: " + str(mL.position) + "\n");
        contador_depuracion = contador_depuracion + 1;

def write_log_sensor(log_sensor):
        global contador_sensor;
        global contador_depuracion;
        global rotate_complete;
        aux = contador_depuracion - 1;
        log_sensor.write(str(contador_sensor)+":"+str(measure())+":"+str(aux*(360/rotate_complete))+"\n");
        contador_sensor = contador_sensor + 1;

def measure():
        global us;
        distance = us.value();
        return distance/10;

def correction(iter,sense):
        global correction_speed;
        global angle;
        right_pos = abs(mR.position);
        left_pos = abs(mL.position);
        error_right = iter*angle - right_pos;
        error_left = iter*angle - left_pos;

        while(abs(error_right) > 1 or abs(error_left) > 1):
                print("correcting")
                move_ticks(error_right,error_left,correction_speed,sense);
                wait_for_both();
                right_pos = abs(mR.position);
                left_pos = abs(mL.position);
                error_right = iter*angle - right_pos;
                error_left = iter*angle - left_pos;

def rotate_no_log(typeOfRotation,sense):
        global normal_speed;
        global angle;
        top = int(typeOfRotation);
        ticksResto = int((typeOfRotation - top) * 10)
        for x in range(1,top+1):
                move_ticks(angle,angle,normal_speed,sense);
                wait_for_both();
                correction(x,sense);

        move_ticks(ticksResto,ticksResto,normal_speed-70,sense);
        wait_for_both();
        reset_motors();

def reset_motors():
        global contador_depuracion;
        global contador_sensor;
        mR.reset();
        mL.reset();
        contador_depuracion = 1;
        contador_sensor = 1;
        time.sleep(2);

reset_motors();
rotate(rotate_complete,1);
rotate_no_log(rotate_half,1);
rotate_no_log(rotate_quarter,-1);
'''rotate_no_log(1,rotate_quarter); #cuarto a la izquierda
move_straight(30,100,1); #1 de frente 30cm
rotate_no_log(-1,rotate_quarter); #derecha un cuarto
move_straight(35,100,1);
rotate(69,1);
rotate_no_log(1,rotate_half);
move_straight(35,100,1);
rotate_no_log(1,rotate_quarter);
move_straight(30,100,1);
move_straight(30,100,1);
rotate_no_log(-1,rotate_quarter);
move_straight(35,100,1);
rotate(69,1);
rotate_no_log(1,rotate_half);
move_straight(35,100,1);
rotate_no_log(1,rotate_quarter);
move_straight(30,100,1);
rotate_no_log(-1,rotate_quarter);
'''

log_depuracion.close();
log_sensor1.close();
log_sensor2.close();
log_sensor3.close();