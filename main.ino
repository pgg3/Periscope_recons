/*
  SD card datalogger

  This example shows how to log data from three analog sensors
  to an SD card using the SD library.

  The circuit:
   analog sensors on analog ins 0, 1, and 2
   SD card attached to SPI bus as follows:
 ** MOSI - pin 11
 ** MISO - pin 12
 ** CLK - pin 13
 ** CS - pin 4 (for MKRZero SD: SDCARD_SS_PIN)

  created  24 Nov 2010
  modified 9 Apr 2012
  by Tom Igoe

  This example code is in the public domain.

*/

#include <SPI.h>
#include <SD.h>

const int chipSelect = 10;
const int analogPin = A2;
String dataLog = "1234.txt";
int DataLength = 0;

void setup()
{
    // Open serial communications and wait for port to open:
    Serial.begin(9600);
    while (!Serial)
    {
        ; // wait for serial port to connect. Needed for native USB port only
    }

    Serial.print("Initializing SD card...");

    // see if the card is present and can be initialized:
    if (!SD.begin(chipSelect))
    {
        Serial.println("Card failed, or not present");
        // don't do anything more:
        while (1)
            ;
    }
    Serial.println("card initialized.");

    // remove the log file if it exists:
    if (SD.exists(dataLog))
    {
        Serial.println("log file exists, deleting...");
        SD.remove(dataLog);
        Serial.println("log file deleted.");
    }
    else
    {
        Serial.println("log file does not exist");
    }
}

void loop()
{
    // make a string for assembling the data to log:
    String dataString;
    unsigned long time;

    // read the pin
    dataString = analogRead(analogPin);
    time = millis();

    // open the file. note that only one file can be open at a time,
    // so you have to close this one before opening another.
    File dataFile = SD.open(dataLog, FILE_WRITE);

    // if the file is available, write to it:
    if (dataFile)
    {
        dataFile.print(time);
        dataFile.print(",");
        dataFile.println(dataString);
        dataFile.close();
        // print to the serial port too:
        // Serial.println(dataString);
    }
    // if the file isn't open, pop up an error:
    else
    {
        Serial.println("error opening datalog.txt");
    }

    DataLength += 1;

    if (DataLength > 400)
    {
        Serial.println("DataLength > 400");
        while (1)
            ;
    }
    delay(50);
}
