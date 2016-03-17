int incomingByte = 0;

void setup(){
  pinMode(12, OUTPUT);
  digitalWrite(12, LOW);
  Serial.begin(9600);
}

void loop(){
  //digitalWrite(12, HIGH);
  //digitalWrite(13, LOW);
}

void serialEvent() {
  if(Serial.available() > 0) {
    char data = Serial.read();
    char str[2];
    str[0] = data;
    str[1] = '\0';
    if(str == "1\n"){
      digitalWrite(12,HIGH);
    }
    if(str == "0\n"){
      digitalWrite(12,LOW);
    }
  }
}
