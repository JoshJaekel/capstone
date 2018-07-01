#include <VarSpeedServo.h>
#include <Console.h>
#include "Arduino.h"

const float A = 5.75;
const float B = 7.375;
const float rtod = 57.295779;
float X = 4;
float Y = 4;
float Z = 90;
int G = 90;
float WA = 0;
int WR = 90;

//Arm temp pos
float tmpx = 4;
float tmpy = 4;
float tmpz = 90;
int tmpg = 90;
int tmpwr = 90;
float tmpwa = 0;




// Arm Servo pins
#define Base_pin 10
#define Shoulder_pin 9
#define Elbow_pin 11
#define Wrist_pin 13
#define Gripper_pin 12

// Onboard Speaker
#define Speaker_pin 5

// Servo Objects
VarSpeedServo Elb;
VarSpeedServo Shldr;
VarSpeedServo Wrist;
VarSpeedServo Base;
VarSpeedServo Gripper;


struct angles {
   float base;
   float shoulder;
   float elbow;
};

int data[3];
int speed=20;
int base_angle=135;
void setup()
{
  // Setup serial
  Serial.begin(9600);
  Base.attach(Base_pin);
  Shldr.attach(Shoulder_pin);
  Elb.attach(Elbow_pin);
  Wrist.attach(Wrist_pin);
  Gripper.attach(Gripper_pin);

  
  pinMode(Speaker_pin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  // Tone & wait
  tone(Speaker_pin, 440, 500);
  delay(1500);

  // Tone and move to 1500
  tone(Speaker_pin, 220, 1000);

}
//
//int Arm(float xt, float yt, float zt) //Here's all the Inverse Kinematics to control the arm
//{
//    angles
//    float x = sqrt((yt*yt)+(xt*xt));
//    float y= zt-6.193;
//    float l1=14.605;
//    float l2=18.733;
//    float k1, k2, theta_2;
//    theta2=atan2(-sqrt(1-((x*x+y*y-l1*l1-l2*l2)/(2*l1*l2))*((x*x+y*y-l1*l1-l2*l2)/(2*l1*l2))),((x*x+y*y-l1*l1-l2*l2)/(2*l1*l2)));
//    k1=l1+l2*cos(theta2);
//    k2=l2*sin(theta2);
//    theta1=atan2(y,x)-atan2(k2,k1);
//    rtd=180.0/PI;
//    return
//
//  #endif
//    Y = tmpy;
//    X = tmpx;
//    Z = tmpz;
//    WA = tmpwa;
//  #ifndef FSRG
//    G = tmpg;
//  #endif
//    return 0; 
//
//Serial.println(Shoulder);
//Serial.println(Elbow);
//Serial.println(Base);

//Gripper.write(0,20);
//Gripper.wait();
//
////Move to eraser
//Base.write(90,20);
//Shldr.write(20,20);
//Elb.write(45,20);
//Wrist.write(0,20);
//Base.wait();
//Elb.wait();
//Shldr.wait();
//Wrist.wait();
//
//delay(10000);
//


  //}
void loop()
{
Serial.println("move_ready");


int xt_int, yt_int, zt_int;

xt_int=Serial.parseInt();
//Serial.println("done");
yt_int=Serial.parseInt();
//Serial.println("done");
zt_int=Serial.parseInt();
//Serial.println("done");

Serial.println(xt_int);
Serial.println(yt_int);
Serial.println(zt_int);




if ((xt_int==0)&&(yt_int==0)&&(zt_int==0)){
  }
  
else{
  float yt=float(yt_int)/10;
  float xt=float(xt_int)/10;
  float zt=float(zt_int)/10;
  float x = sqrt((yt*yt)+(xt*xt));
  float y= zt-6.193;
  float l1=14.605;
  float l2=18.733;
  float k1, k2, theta2,theta1,theta0,rtd;
  theta2=atan2(-sqrt(1-((x*x+y*y-l1*l1-l2*l2)/(2*l1*l2))*((x*x+y*y-l1*l1-l2*l2)/(2*l1*l2))),((x*x+y*y-l1*l1-l2*l2)/(2*l1*l2)));
  k1=l1+l2*cos(theta2);
  k2=l2*sin(theta2);
  theta1=atan2(y,x)-atan2(k2,k1);
  theta0=atan2(yt,xt);
  rtd=180.0/PI;
  
  float base_val=map(theta0*rtd,0,90,33,118);
  float shoulder_val=map(theta1*rtd,0,90,5,85);
  float elbow_val=map(theta2*-rtd,0,135,40,160);

  Base.write(base_val,speed);
  
  Shldr.write(shoulder_val,speed);
  Elb.write(elbow_val,speed);
  //Wrist.write((theta2*-rtd)-theta1*rtd,speed);
  Base.wait();
  Elb.wait();
  Shldr.wait();
  //Wrist.wait();
}



}
