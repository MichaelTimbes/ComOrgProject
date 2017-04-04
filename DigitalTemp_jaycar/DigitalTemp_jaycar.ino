#include <math.h>
double Thermistor(int RawADC){
 double Temp;
 Temp = log(((10240000/RawADC) - 10000));
 Temp = 1/(0.001129148+(0.000234125+(0.0000000876741*Temp*Temp ))*Temp);
 Temp = Temp - 273.15;
 return abs(Temp);
}
void setup() {
 Serial.begin(9600);
}
void loop(){
 Serial.print(Thermistor(analogRead(A0)));
 Serial.println("c");
 delay(1000);
}
