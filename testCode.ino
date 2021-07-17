#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define SAMPLE_SIZE_PULSE 8
#define SAMPLE_SIZE_INTERRUPT 4
#define SAMPLE_SIZE_VOLTAGE 12
#define MAX_VOLTAGE 50

#define LED_PIN 13
#define FLOWMETER_INPUT_PIN 2
#define VOLTAGE_READ_PIN A0
// #define BUTTON_INTERRUPT_PIN 3

LiquidCrystal_I2C lcd(0x27, 30, 4);

float readavgPulse[SAMPLE_SIZE_PULSE] = {0.0f};
float readavgInterrupt[SAMPLE_SIZE_INTERRUPT] = {0.0f};
float readavgVoltage[SAMPLE_SIZE_VOLTAGE] = {0.0f};
int indexForreadavgPulse = 0;
int indexForreadavgInterrupt = 0;
int voltageIndex = 0;
int counterPulses = 0;
int onePulesDuration = 0;
float flowrateInterrupt = 0.0f;
float tempFlowrateInterrupt = 0.0f;

float flowratePulse = 0.0f;
float avgFlowrateInterrupt = 0.0f;
float avgFlowratePulse = 0.0f;

int integerPartFlowrateInterup = 0;
int fractionalPartFlowrateInterupt = 0;
int integerPartFlowratePulse = 0;
int fractionalPartFlowRatePulse = 0;

int avgintegerPartFlowrateInterup = 0;
int avgfractionalPartFlowrateInterupt = 0;
int avgintegerPartFlowratePulse = 0;
int avgfractionalPartFlowRatePulse = 0;
// Taking Integer and fraction part of a number to display.
// Eg. 123.456 --> Integer = 123, Fraction = 456

float Voltage = 0.0f;
float avgVoltage = 0.0f;
float Current = 0.0f;

int flagLcdInterupt = 0;
// int button=0;

void setup()
{
  Serial.begin(9600);
  Serial.println("Init");
  pinMode(A0, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(FLOWMETER_INPUT_PIN, INPUT_PULLUP);

  lcd.init(); // initialize the lcd
  lcd.backlight();
  lcdSetup(); // Displaying all the static parts [FlowRate(P)][FlowRate(I)]
  InitialiseTimer1();
  // initialize timer1
  // noInterrupts(); // disable all interrupts
  // TCCR1A = 0;
  // TCCR1B = 0;
  // TCNT1 = 0;
  // OCR1A = 31250;                                                                     // 31250 = 500 Mili Seconds, 1 Sec,
  // TCCR1B |= (1 << WGM12);                                                            // CTC mode
  // TCCR1B |= (1 << CS12);                                                             // 256 prescaler
  // TIMSK1 |= (1 << OCIE1A);                                                           // enable timer compare interrupt
  // interrupts();                                                                      // enable all interrupts
  // attachInterrupt(digitalPinToInterrupt(FLOWMETER_INPUT_PIN), flowrateISR, FALLING); // Pulse on p
}

float round2(float var) 
{ 
    // 37.66666 * 100 =3766.66 
    // 3766.66 + .5 =3767.16    for rounding off value 
    // then type cast to int so value is 3767 
    // then divided by 100 so the value converted into 37.67 
    float value = (int)(var * 100 + .5); 
    return (float)value / 100; 
}

ISR(TIMER1_COMPA_vect) // timer compare interrupt service routine
{                      // 500 miliseconds
  // interruptCalculations();
  // flowrateInterrupt = (((counterPulses * 0.5) / 71.8)*15.8501) / 4;
  tempFlowrateInterrupt = ((((float)counterPulses * 0.5) / 70.3)) / 4;
  flowrateInterrupt = round2(tempFlowrateInterrupt);
  Serial.println(flowrateInterrupt);
  // Serial.print("Value=");
  // Serial.println(counterPulses);
  // flowrateInterrupt = readValues(flowrateInterrupt, readavgInterrupt, indexForreadavgInterrupt);
  integerPartFlowrateInterup = flowrateInterrupt;
  fractionalPartFlowrateInterupt = (flowrateInterrupt * 1000) - (integerPartFlowrateInterup * 1000);
  // Serial.print("Value=");
  // Serial.println(flowrateInterrupt);

  // if (counterPulses != 0)
  // {
  //   onePulesDuration = pulseIn(FLOWMETER_INPUT_PIN, HIGH);
  // }
  counterPulses = 0;
  // pulseInCalculations();
  float timePerLiter = (onePulesDuration * 76.73) / (1000000);
  flowratePulse = 1 / timePerLiter;
  // Serial.print("Value= ");
  // Serial.println(flowratePulse);
  // flowratePulse = readValues(flowratePulse, readavgPulse, indexForreadavgPulse);
  integerPartFlowratePulse = flowratePulse;
  fractionalPartFlowRatePulse = (flowratePulse * 100) - (integerPartFlowratePulse * 100);

  // digitalWrite(LED_PIN, digitalRead(LED_PIN) ^ 1); // toggle LED pin

  flagLcdInterupt = 1;
  // flagLcdInterupt = 0;
}
void interruptCalculations()
{
  flowrateInterrupt = (counterPulses) / 76.76;
  integerPartFlowrateInterup = flowrateInterrupt;
  fractionalPartFlowrateInterupt = (flowrateInterrupt * 1000) - (integerPartFlowrateInterup * 1000);
}
void pulseInCalculations()
{
  float timePerLiter = (onePulesDuration * 76.73) / (1000000);
  flowratePulse = 1 / timePerLiter;
  integerPartFlowratePulse = flowratePulse;
  fractionalPartFlowRatePulse = (flowratePulse * 100) - (integerPartFlowratePulse * 100);
}

void flowrateISR()
{ // Falling Edge External Interupt

  counterPulses = counterPulses + 1;
  //  Serial.print(" Value of counterPulses = ");
  //  Serial.println(counterPulses);
}
void PulseInISR()
{
  onePulesDuration = pulseIn(FLOWMETER_INPUT_PIN, LOW, 100);
  // pulseInCalculations();
  float timePerLiter = (onePulesDuration * 76.73) / (1000000);
  flowratePulse = 1 / timePerLiter;
  // Serial.print("Value= ");
  // Serial.println(flowratePulse);
  // flowratePulse = readValues(flowratePulse, readavgPulse, indexForreadavgPulse);
  integerPartFlowratePulse = flowratePulse;
  fractionalPartFlowRatePulse = (flowratePulse * 100) - (integerPartFlowratePulse * 100);
}

void interruptFlowrate()
{ // Zombie code - DO not delete dont know impact.

  flowrateInterrupt = (2 * counterPulses) / 76.76;

  //  lcd.print((2*counterPulses)/76.76);
  //  lcd.print("lit./sec");
}

void lcdSetup()
// prints the static values to the LCD once in the setup
{
  lcd.init(); // initialize the lcd
  lcd.backlight();
  lcd.setCursor(0, 0); // move cursor to   (0, 0)
  lcd.print("Flowrate in Lit./sec.");
  lcd.setCursor(0, 1);
  lcd.print("V=");
  lcd.setCursor(2, 1);
  lcd.print("000.00V");
  lcd.setCursor(0, 2);
  lcd.print("N0000");
  lcd.setCursor(5, 2);
  lcd.print(".");
  lcd.setCursor(6, 2);
  lcd.print("000I");
  // lcd.setCursor(11, 2);
  // lcd.print("0000");
  // lcd.setCursor(15, 2);
  // lcd.print(".");
  // lcd.setCursor(16, 2);
  // lcd.print("000P");
  lcd.setCursor(0, 3);
  lcd.print("A0000");
  lcd.setCursor(5, 3);
  lcd.print(".");
  lcd.setCursor(6, 3);
  lcd.print("000I");
  // lcd.setCursor(11, 3);
  // lcd.print("0000");
  // lcd.setCursor(15, 3);
  // lcd.print(".");
  // lcd.setCursor(16, 3);
  // lcd.print("000P");
}

void LcdPrintNewValues()
// Prints the reading achieved from different ways onto the LCD
{

  lcd.setCursor(1, 2);

  if (integerPartFlowrateInterup > 999)
  {
    // lcd.setCursor(2, 2);
  }
  else if (integerPartFlowrateInterup < 100 && (integerPartFlowrateInterup >= 10))
  {
    // lcd.setCursor(2, 2);
    lcd.print("00");
  }
  else if (integerPartFlowrateInterup < 10)
  {
    // lcd.setCursor(2, 2);
    lcd.print("000");
  }
  else if ((integerPartFlowrateInterup > 99) && (integerPartFlowrateInterup < 1000))
  {
    // lcd.setCursor(3, 2);
    lcd.print("0");
  }

  lcd.print(integerPartFlowrateInterup);
  lcd.setCursor(6, 2);


  if (fractionalPartFlowrateInterupt < 10)
  {
    lcd.print("00");
  }
  else if (fractionalPartFlowrateInterupt < 100)
  {
    lcd.print("0");
  }
  lcd.print(fractionalPartFlowrateInterupt);

  // lcd.setCursor(11, 2);

  // if (integerPartFlowratePulse > 999)
  // {
  //   //4 digit print
  // }
  // else if ((integerPartFlowratePulse < 100) && (integerPartFlowratePulse >= 10))
  // {
  //   // 2 digit print
  //   // lcd.setCursor(13, 2);
  //   lcd.print("00");
  // }
  // else if (integerPartFlowratePulse < 10)
  // {
  //   // 1 dgit print
  //   // lcd.setCursor(14, 2);
  //   lcd.print("000");
  // }
  // else if (integerPartFlowratePulse > 99 && integerPartFlowratePulse < 1000)
  // {
  //   // 2 digit print
  //   lcd.print("0");
  //   // lcd.setCursor(12, 2);
  // }

  // lcd.print(integerPartFlowratePulse);
  // lcd.setCursor(16, 2);
  // lcd.print(fractionalPartFlowRatePulse);
  // if (fractionalPartFlowRatePulse < 10)
  // {
  //   lcd.print("00");
  // }
  // else if (fractionalPartFlowRatePulse < 100)
  // {
  //   lcd.print("0");
  // }

  //voltage and current readings

  lcd.setCursor(2, 1);
  lcd.print(avgVoltage);
  // lcd.setCursor(10, 1);
  // lcd.print("I=");
  // lcd.setCursor(13, 1);
  // lcd.print(Current);
}

void printAvgValues()
{
  // avgFlowrateInterrupt = readValues(flowrateInterrupt, readavgInterrupt, indexForreadavgInterrupt, SAMPLE_SIZE_INTERRUPT);
  // avgFlowratePulse = readValues(flowratePulse, readavgPulse, indexForreadavgPulse, SAMPLE_SIZE_PULSE);

  avgFlowrateInterrupt = averageInterruptReading(flowrateInterrupt);
  avgFlowratePulse = averagePulseReading(flowratePulse);

  avgintegerPartFlowrateInterup = avgFlowrateInterrupt;
  avgfractionalPartFlowrateInterupt = (avgFlowrateInterrupt * 1000) - (avgintegerPartFlowrateInterup * 1000);
  avgintegerPartFlowratePulse = avgFlowratePulse;
  avgfractionalPartFlowRatePulse = (avgFlowratePulse * 100) - (avgintegerPartFlowratePulse * 100);

  lcd.setCursor(1, 3);
  if (avgintegerPartFlowrateInterup > 999)
  {
    // lcd.setCursor(2, 3);
  }
  else if ((avgintegerPartFlowrateInterup < 100) && (avgintegerPartFlowrateInterup >= 10))
  {
    // lcd.setCursor(4, 3);
    lcd.print("00");
  }
  else if (avgintegerPartFlowrateInterup < 10)
  {
    // lcd.setCursor(5, 3);
    lcd.print("000");
  }
  else if (avgintegerPartFlowrateInterup > 99 && avgintegerPartFlowrateInterup < 1000)
  {
    lcd.print("0");
  }
  lcd.print(avgintegerPartFlowrateInterup);
  lcd.setCursor(6, 3);

  if (avgfractionalPartFlowrateInterupt < 10)
  {
    lcd.print("00");
  }
  else if (avgfractionalPartFlowrateInterupt < 100)
  {
    lcd.print("0");
  }
  lcd.print(avgfractionalPartFlowrateInterupt);

  // lcd.setCursor(11, 3);
  // if (avgintegerPartFlowratePulse > 999)
  // {
  //   // lcd.setCursor(11, 3);
  // }
  // else if ((avgintegerPartFlowratePulse < 100) && (avgintegerPartFlowratePulse >= 10))
  // {
  //   // lcd.setCursor(13, 3);
  //   lcd.print("00");
  // }
  // else if (avgintegerPartFlowratePulse < 10)
  // {
  //   // lcd.setCursor(14, 3);
  //   lcd.print("000");
  // }
  // else if (avgintegerPartFlowratePulse < 1000 && avgintegerPartFlowratePulse > 99)
  // {
  //   // lcd.setCursor(12, 3);
  //   lcd.print("0");
  // }

  // lcd.print(avgintegerPartFlowratePulse);
  // lcd.setCursor(16, 3);
  // lcd.print(avgfractionalPartFlowRatePulse);

  // if (avgfractionalPartFlowRatePulse < 10)
  // {
  //   lcd.print("00");
  // }
  // else if (avgfractionalPartFlowRatePulse < 100)
  // {
  //   lcd.print("0");
  // }
}

void InitialiseTimer1()
{
  // noInterrupts(); // disable all interrupts
  // TCCR1A = 0;
  // TCCR1B = 0;
  // TCNT1 = 0;
  // OCR1A = 15624;           // 31250 = 500 Mili Seconds, 15624 - 1 Sec,
  // TCCR1B |= (1 << WGM12);  // CTC mode
  // TCCR1B |= (1 << CS12);   // 256 prescaler
  // TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt
  // interrupts();            // enable all interrupts

  cli(); //stop interrupts

  //set timer1 interrupt at 1Hz
  TCCR1A = 0; // set entire TCCR1A register to 0
  TCCR1B = 0; // same for TCCR1B
  TCNT1 = 0;  //initialize counter value to 0
  // set compare match register for 1hz increments
  OCR1A = 62499; //31250; //7812; //62499;//15624;// = (16*10^6) / (1*1024) - 1 (must be <65536)
  //1 Second value= 15624
  // 0.5 second Value = 7812
  // 2 seconds value = 31250
  // 4 Second Value = 62499
  //  formula= [(crystal frequency)/ (desiredFrequency * Presclar)]-1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS12 and CS10 bits for 1024 prescaler
  TCCR1B |= (1 << CS12) | (1 << CS10);
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);

  sei(); //allow interrupts

  attachInterrupt(digitalPinToInterrupt(FLOWMETER_INPUT_PIN), flowrateISR, CHANGE);
  // attachInterrupt(digitalPinToInterrupt(FLOWMETER_INPUT_PIN), flowrateISR, RISING);
  // attachInterrupt(digitalPinToInterrupt(BUTTON_INTERRUPT_PIN), PulseInISR, FALLING);
}

void loop()
{
  if (flagLcdInterupt == 1)
  {
    digitalWrite(LED_PIN, digitalRead(LED_PIN) ^ 1);
    // Serial.println("12A");

    // Voltage=100;
    LcdPrintNewValues();
   printAvgValues();
    flagLcdInterupt = 0;
  }
  voltageRead();

  // onePulesDuration = pulseIn(FLOWMETER_INPUT_PIN, HIGH,250);
  // // pulseInCalculations();
  // float timePerLiter = (onePulesDuration * 76.73) / (1000000);
  // flowratePulse = 1 / timePerLiter;
  // // Serial.print("Value= ");
  // // Serial.println(flowratePulse);
  // // flowratePulse = readValues(flowratePulse, readavgPulse, indexForreadavgPulse);
  // integerPartFlowratePulse = flowratePulse;
  // fractionalPartFlowRatePulse = (flowratePulse * 100) - (integerPartFlowratePulse * 100);

  // voltageRead();
  // int a = analogRead(A0);
  // Voltage = map(a, 0, 0, 1023, MAX_VOLTAGE);
  // Serial.print(" Voltage = ");
  // Serial.println(Voltage);
}

void voltageRead()
{
  int temp = analogRead(VOLTAGE_READ_PIN);
  float a = temp;
  // Voltage = ((a * 5) / 1024) / 0.09599;
  Voltage = ((a * 5) / 1024) / 0.0955;
  //  Voltage = map(a, 0, 1023,0, MAX_VOLTAGE);
  // Serial.print("Voltage = ");
  // Serial.println(Voltage);
  avgVoltage = averageVoltReading(Voltage);
  // delay(10);
}

float averageReading(float readingavg[], int sampleSize)
// This calculates the average of the array of readings everytime a new reading is added to the array.
{
  int i = 0;
  float avg = 0.0f;
  float tempavg = 0.0f;
  for (i = 0; i < sampleSize; i++)
  {
    tempavg = tempavg + readingavg[i];
    // Serial.print("Value of index ");
    // Serial.print(i);
    // Serial.print(" = ");
    // Serial.println(readingavg[i]);
  }
  avg = tempavg / sampleSize;
  // avg = tempavg;
  Serial.println(avg);
  return avg;
}

float readValues(float reading, float readavgs[], int index, int sampleSize)
// This adds a reading to the array everytime a new reading is made.
{
  // if(index>=sampleSize)
  // {
  //   index=0;
  // }
  readavgs[index] = reading;
  index = index + 1;
  // Serial.print("Index = ");
  // Serial.println(index);
  return averageReading(readavgs, sampleSize);
}
void PrintValuesISR()
{
  // Serial.print();
  // Serial.print(", ");
  // Serial.print();
  // Serial.print(", ");
}

float averageVoltReading(float Voltage)
// This calculates the average of the array of readings everytime a new reading is added to the array.
{
  int i = 0;
  if (voltageIndex >= SAMPLE_SIZE_VOLTAGE)
  {
    voltageIndex = 0;
  }
  readavgVoltage[voltageIndex] = Voltage;
  voltageIndex = voltageIndex + 1;
  // Serial.print("Index = ");
  // Serial.println(voltageIndex);
  float avg = 0.0f;
  float tempavg = 0.0f;
  for (i = 0; i < SAMPLE_SIZE_VOLTAGE; i++)
  {
    tempavg = tempavg + readavgVoltage[i];
    // Serial.print("Value of index ");
    // Serial.print(i);
    // Serial.print(" = ");
    // Serial.println(readavgVoltage[i]);
  }
  avg = tempavg / SAMPLE_SIZE_VOLTAGE;
  // avg = tempavg;
  // Serial.println(avg);
  return avg;
}

float averageInterruptReading(float avgFlowrateInterrupt)
// This calculates the average of the array of readings everytime a new reading is added to the array.
{
  int i = 0;
  if (indexForreadavgInterrupt >= SAMPLE_SIZE_INTERRUPT)
  {
    indexForreadavgInterrupt = 0;
  }
  readavgInterrupt[indexForreadavgInterrupt] = avgFlowrateInterrupt;
  indexForreadavgInterrupt = indexForreadavgInterrupt + 1;
  // Serial.print("Index = ");
  // Serial.println(indexForreadavgInterrupt);
  float avg = 0.0f;
  float tempavg = 0.0f;
  for (i = 0; i < SAMPLE_SIZE_INTERRUPT; i++)
  {
    tempavg = tempavg + readavgInterrupt[i];
    // Serial.print("Value of index ");
    // Serial.print(i);
    // Serial.print(" = ");
    // Serial.println(readavgInterrupt[i]);
  }
  avg = tempavg / SAMPLE_SIZE_INTERRUPT;
  // avg = tempavg;
  // Serial.println(avg);
  return avg;
}

float averagePulseReading(float avgFlowratePulse)
// This calculates the average of the array of readings everytime a new reading is added to the array.
{
  int i = 0;
  if (indexForreadavgPulse >= SAMPLE_SIZE_PULSE)
  {
    indexForreadavgPulse = 0;
  }
  readavgPulse[indexForreadavgPulse] = avgFlowratePulse;
  indexForreadavgPulse = indexForreadavgPulse + 1;
  // Serial.print("Index = ");
  // Serial.println(indexForreadavgPulse);
  float avg = 0.0f;
  float tempavg = 0.0f;
  for (i = 0; i < SAMPLE_SIZE_PULSE; i++)
  {
    tempavg = tempavg + readavgPulse[i];
    // Serial.print("Value of index ");
    // Serial.print(i);
    // Serial.print(" = ");
    // Serial.println(readavgPulse[i]);
  }
  avg = tempavg / SAMPLE_SIZE_PULSE;
  // avg = tempavg;
  // Serial.println(avg);
  return avg;
}
