'''
Driver code for the D.A.R.T.S Rover System

Algorithm:
- Start robot, initialize the HTTP server code and constants.

- While 1
    - Move robot arm to correct position. (15 positions defined from -15degree to 195degree, 15 degree interval)
    - Collect distance from LiDAR.
    - Compute point value.
    - Store in array of points.
    - Check if robot is at position 15 or position 1
        - If data exists send to main server.
        - Move robot 1 unit forward.
        - Change direction of arm. (NOT position)
    - else
        - Move the arm depending on the direction.
    - Delay by interval
'''

#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <HTTPClient.h>
#include <math.h>


const char *ssid = "YourNetworkName";
const char *password = "YourNetworkPassword";
const char *serverUrl = "http://example.com/api/send";

AsyncWebServer server(80);


// Each point is stored in this.
struct Point3D {
  float x;
  float y;
  float z;
};


// Position of LiDAR arm. Send data when at 15 or 1. 
// 15 total positions possible from -15 degree till 195 degree with 15 degree increment.
int position = 1;
// The direction to move the LiDAR arm. 1-> Clockwise, 0-> Anticlockwise.
int direction = 1;
// IMPORTANT: Length of arm in units. (Set this value properly, check the units)
int armLength = 10;
// The distance the robot moves.
int zDistance = 0;
// Store the point data captured.
Point3D points[15];
// Variable to store if this is the first iteration.
int firstIteration = 1


// Function to generate a random alphanumeric session ID
String generateSessionID()
{
    const char *charset = "0123456789ABCDEFGHIJ1LMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    const int idLength = 5;
    String sessionId = "";
    for (int i = 0; i < idLength; i++)
    {
        sessionId += charset[random(strlen(charset))];
    }
    return sessionId;
}

// Generate URL with session ID.
String sessionID = generateSessionID();
String urlWithSessionID = serverAddress + sessionID;


void handleStop(AsyncWebServerRequest *request)
{
    // Stop motors code here
    request->send(200, "text/plain", "LED blinked!");
}


void setup()
{
    Serial.begin(115200);

    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    // Set up routes
    server.on("/api/stop", HTTP_GET, handleStop);

    server.begin();
    Serial.println("HTTP server started");
}


void loop()
{
    server.handleClient();

    float angle = -15 + (position*15);

    // IMPORTANT: Get distance from LiDAR sensor here.
    // IMPORTANT: Move the arm to the angle defined above.

    float distance = 10.1;
    
    // Check this. Not sure about if pi value is defined in math.h
    float radianAngle = angle * ( M_PI / 180.0 );

    // Each point is of the form: (d*cos(theta), d*sin(theta), z)
    points[position - 1].x = armLength*cos(radianAngle);
    points[position - 1].y = armLength*sin(radianAngle);
    points[position - 1].x = zDistance;

    // Send data only when position=15 or position=1. Increment or decrement depending on direction.
    // When the data is being transmitted do not move the arm. Only change the direction it moves in.
    // This is because for the next iteration, it can capture information from the same position. 
    if ((position == 15 || position == 1) && firstIteration==1)
    {
        HTTPClient http;
        http.begin(urlWithSessionID);
        http.addHeader("Content-Type", "application/json");

        int httpCode = http.POST("{\"key\":\"value\"}");
        if (httpCode > 0)
        {
            Serial.printf("HTTP POST request to %s returned code: %d\n", serverUrl, httpCode);
        }
        else
        {
            Serial.printf("HTTP POST request to %s failed\n", serverUrl);
        }
        http.end();

        // IMPORTANT: Move the robot by 1 unit.
        zDistance++;

        // Change the direction the arm moves in.
        direction = !direction;
    }
    else {
        
        if(direction == 1)
            position++;
        else
            position--;
    }

    firstIteration = 0;
    delay(1000); 
}
