#include <VarSpeedServo.h>

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
//  delay(1000);
//Base.write(150,30,true);
//  Shldr.writeMicroseconds(1500);
//  Elb.writeMicroseconds(1500);
//  Wrist.writeMicroseconds(1500);
//  Gripper.writeMicroseconds(1500);

}

int Arm(float x, float y, float z, int g, float wa) //Here's all the Inverse Kinematics to control the arm
{
    float M = sqrt((y*y)+(x*x));
    if(M <= 0)
      return 1;
//    float P=z-2.5;
//    float Elbow=atan2(-sqrt(1-((M*M+P*P-A*A-B*B)/(2*A*B))*((M*M+P*P-A*A-B*B)/(2*A*B))),((M*M+P*P-A*A-B*B)/(2*A*B)));
//    float Shoulder=atan2(P,M)-atan2(B*sin(Elbow),A+B*cos(Elbow));
    float A1 = atan(y/x);
    if(x <= 0)
      return 1;
    float A2 = acos((A*A-B*B+M*M)/((A*2)*M));
    float Elbow = acos((A*A+B*B-M*M)/((A*2)*B));
    float Shoulder = A1 + A2;
    Elbow = Elbow * rtod;
    Shoulder = Shoulder * rtod;
    if((int)Elbow <= 0 || (int)Shoulder <= 0)
      return 1;
    float Wris = abs(wa - Elbow - Shoulder) - 90;

  
  #ifdef DIGITAL_RANGE
    Elb.writeMicroseconds(map(180 - Elbow, 0, 180, 900, 2100  ));
    Shldr.writeMicroseconds(map(Shoulder, 0, 180, 900, 2100));
  #else
    Elb.write(180-Elbow,20);
    Shldr.write(Shoulder,20);
  #endif
    Wrist.write(180 - Wris,20);
    Base.write(z,20);
  
  #ifndef FSRG
    Gripper.write(g,20);




  #endif
    Y = tmpy;
    X = tmpx;
    Z = tmpz;
    WA = tmpwa;
  #ifndef FSRG
    G = tmpg;
  #endif
    return 0; 
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


  }
void loop()
{

int base_val;//=map(45,0,90,33,118);
int shoulder_val;//=map(94.71,0,90,5,85);
int elbow_val;//=map(129.73,0,135,40,160);

base_val=0;
shoulder_val=90;
elbow_val=45;

Base.write(base_val,speed);
Shldr.write(shoulder_val,speed);
Elb.write(elbow_val,speed);
Wrist.write(0,speed);
Base.wait();
Elb.wait();
Shldr.wait();
Wrist.wait();

delay(3000);

base_val=45;
shoulder_val=90;
elbow_val=45;

//base_val=map(69.23,0,90,33,118);
//shoulder_val=map(30.21,0,90,5,85);
//elbow_val=map(41.11,0,135,40,160);
Base.write(base_val,speed);
Shldr.write(shoulder_val,speed);
Elb.write(elbow_val,speed);
Wrist.write(0,speed);
Base.wait();
Elb.wait();
Shldr.wait();
Wrist.wait();

delay(3000);

base_val=90;
shoulder_val=90;
elbow_val=45;

//base_val=map(90,0,90,33,118);
//shoulder_val=map(91.26,0,90,5,85);
//elbow_val=map(126.4,0,135,40,160);
Base.write(base_val,speed);
Shldr.write(shoulder_val,speed);
Elb.write(elbow_val,speed);
Wrist.write(0,speed);
Base.wait();
Elb.wait();
Shldr.wait();
Wrist.wait();

delay(3000);



}
