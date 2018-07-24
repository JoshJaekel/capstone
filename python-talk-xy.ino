/*************************************************** 
  This is an example for our Adafruit 16-channel PWM & Servo driver
  Servo test - this will drive 8 servos, one after the other on the
  first 8 pins of the PCA9685

  Pick one up today in the adafruit shop!
  ------> http://www.adafruit.com/products/815
  
  These drivers use I2C to communicate, 2 pins are required to  
  interface.

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);
// you can also call it with a different address and I2C interface
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(&Wire, 0x40);

// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define SERVOMIN  50 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  1000 // this is the 'maximum' pulse length count (out of 4096)

// our servo # counter
uint8_t servonum = 0;

void setup() {
  Serial.begin(9600);
  //Serial.println("8 channel Servo test!");
  
  pwm.begin();
  
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
  
  delay(10);
  pwm.setPWM(0, 0, 390);
  pwm.setPWM(1, 0, 575);
  pwm.setPWM(2, 0, 250);

  pinMode(7, OUTPUT);
  digitalWrite(7,LOW);      
  delay(3000);
}

// you can use this function if you'd like to set the pulse length in seconds
// e.g. setServoPulse(0, 0.001) is a ~1 millisecond pulse width. its not precise!
void setServoPulse(uint8_t n, double pulse) {
  double pulselength;
  
  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= 60;   // 60 Hz
  Serial.print(pulselength); Serial.println(" us per period"); 
  pulselength /= 4096;  // 12 bits of resolution
  Serial.print(pulselength); Serial.println(" us per bit"); 
  pulse *= 1000000;  // convert to us
  pulse /= pulselength;
  Serial.println(pulse);
  pwm.setPWM(n, 0, pulse);
}
int yt_int1,xt_int1,yt_int2,xt_int2,yt_int3,xt_int3,xt_int4,yt_int4, type; 
int pickup = 362, top=250;
long to_move,to_move2, to_move3, from_move,from_temp;
void loop() {
  digitalWrite(7,LOW);  
  Serial.println("move_ready");
  // Drive each servo one at a time
  while (Serial.available()==0);
  from_move=Serial.parseInt();
  Serial.println("ready");
  while (Serial.available()==0);
  to_move=Serial.parseInt();

  type=from_move/1000000;
  from_temp=from_move%1000000;
  xt_int1=from_temp%1000;
  yt_int1=from_temp/1000;

  xt_int2=to_move%1000;
  yt_int2=to_move/1000;
//  Serial.println(in_move);
//  Serial.println(xt_int);
//  Serial.println(yt_int);
  if (type==0){
    pwm.setPWM(0, 0, xt_int1);
    pwm.setPWM(1, 0, yt_int1);
    delay(4000);
    pwm.setPWM(2,0,pickup);
    delay(3000);
    digitalWrite(7, HIGH);
    delay(500);
    pwm.setPWM(2,0,top);
    delay(3000);
    pwm.setPWM(0, 0, xt_int2);
    pwm.setPWM(1, 0, yt_int2);
    delay(3000);
    pwm.setPWM(2,0,pickup);
    delay(3000);
    digitalWrite(7, LOW);
    delay(500);
    pwm.setPWM(2,0,top);
    delay(3000);
    pwm.setPWM(1, 0, 575);
    pwm.setPWM(0,0,390);
  }

    if (type==1 or type==3){
      Serial.println("ready");
      while (Serial.available()==0);
      to_move2=Serial.parseInt();
      xt_int3=to_move2%1000;
      yt_int3=to_move2/1000;
      pwm.setPWM(0, 0, xt_int2);
      pwm.setPWM(1, 0, yt_int2);
      delay(4000);
      pwm.setPWM(2,0,pickup);
      delay(3000);
      digitalWrite(7, HIGH);
      delay(500);
      pwm.setPWM(2,0,top);
      delay(3000);
      pwm.setPWM(1, 0, 575);
      pwm.setPWM(0,0,390);
      delay(5000);
      digitalWrite(7, LOW);
      delay(500);
      
      pwm.setPWM(0, 0, xt_int1);
      pwm.setPWM(1, 0, yt_int1);
      delay(4000);
      pwm.setPWM(2,0,pickup);
      delay(3000);
      digitalWrite(7, HIGH);
      delay(500);
      pwm.setPWM(2,0,top);
      delay(2000);
      pwm.setPWM(0, 0, xt_int3);
      pwm.setPWM(1, 0, yt_int3);
      delay(3000);
      pwm.setPWM(2,0,pickup);
      delay(3000);
      digitalWrite(7, LOW);
      delay(500);
      pwm.setPWM(2,0,top);
      delay(3000);
      pwm.setPWM(1, 0, 575);
      pwm.setPWM(0,0,390);
  }

    if (type==2){
      Serial.println("ready");
      while (Serial.available()==0);
      to_move2=Serial.parseInt();
      Serial.println("ready");
      while (Serial.available()==0);
      to_move3=Serial.parseInt();
      xt_int3=to_move2%1000;
      yt_int3=to_move2/1000;
      
      xt_int4=to_move3%1000;
      yt_int4=to_move3/1000;

//      Serial.println(xt_int1);
//      Serial.println(yt_int1);
//      Serial.println(xt_int2);
//      Serial.println(yt_int2);
      
      
      //Starts moving
      pwm.setPWM(0, 0, xt_int1);
      pwm.setPWM(1, 0, yt_int1);
      delay(3000);
      pwm.setPWM(2,0,pickup);
      delay(3000);
      digitalWrite(7, HIGH);
      delay(500);
      pwm.setPWM(2,0,300);
      delay(2000);
      pwm.setPWM(0, 0, xt_int2);
      pwm.setPWM(1,0,yt_int2);
      delay(2000);
      pwm.setPWM(2,0,pickup);
      delay(1500);
      digitalWrite(7, LOW);
      pwm.setPWM(2,0,300);
      delay(3000);
      
      pwm.setPWM(0, 0, xt_int3);
      pwm.setPWM(1, 0, yt_int3);
      delay(3000);
      pwm.setPWM(2,0,pickup);
      delay(3000);
      digitalWrite(7, HIGH);
      delay(500);
      pwm.setPWM(2,0,top);
      delay(2000);
      pwm.setPWM(0, 0, xt_int4);
      pwm.setPWM(1, 0, yt_int4);
      delay(3000);
      pwm.setPWM(2,0,pickup);
      delay(3000);
      digitalWrite(7, LOW);
      delay(500);
      pwm.setPWM(2,0,top);
      delay(3000);
      pwm.setPWM(1, 0, 575);
      pwm.setPWM(0,0,390);
  }

  Serial.println("done");
//  Serial.println("Enter y-position: ");
//  while (Serial.available()==0);
//
//  yt_int=Serial.parseInt();
//  Serial.println(yt_int);

//
//
//  Serial.println("Enter z-position: ");
//  while (Serial.available()==0);
//
//  zt_int=Serial.parseInt();
//  Serial.println(zt_int);
//  pwm.setPWM(2, 0, zt_int);
//  delay(5000);


}
