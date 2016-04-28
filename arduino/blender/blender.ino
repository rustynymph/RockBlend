int blend = 0;
int incomingByte = 0;

void setup(){
  pinMode(12, OUTPUT);
  digitalWrite(12, LOW);
  Serial.begin(9600);
}

void loop(){
  if (blend == 0){
    digitalWrite(12, LOW);
  }
  else{
    digitalWrite(12, HIGH);
  }
}

void serialEvent() {
  if(Serial.available() > 0) {
    char data = Serial.read();
    if(data == '1'){
      blend = 1;
    }
    if(data == '0'){
      blend = 0;
    }
  }
}
