// Online C compiler to run C program online
#include <stdio.h>

int angleArray[] = {-15, -15, 0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 195};
int positionIndex = 1;
// The direction to move the LiDAR arm. 1-> Clockwise, 0-> Anticlockwise.
int direction = 1;

// Variable to store if this is the first iteration.
int firstIteration = 1;

int main() {
    for(int i=0; i<60; i++)
    {
        float angle = angleArray[positionIndex];  
        
        if(direction==1)
            positionIndex++;
        else
            positionIndex--;
        
        printf("Angle : %f, Position: %d, Direction: %d \n", angle, positionIndex, direction);
    
        // printf("%f, ", angle);
        if(positionIndex==16) {
            direction = -1;
            positionIndex = 15;
        }
        else if(positionIndex==0) {
            direction = 1;
            positionIndex = 1;
        }
        
        firstIteration = 0;
    }
    return 0;
}