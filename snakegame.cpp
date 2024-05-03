#include <iostream>
#include <conio.h>
#include <cstdlib>
#include <ctime>
using namespace std;

const int width = 20;
const int height = 20;
int snakeX, snakeY, fruitX, fruitY, score;
int tailX[100], tailY[100];
int nTail;
enum eDirection { STOP = 0, LEFT, RIGHT, UP, DOWN };
eDirection dir;

void Setup() {
    srand(time(0));
    dir = STOP;
    snakeX = width / 2;
    snakeY = height / 2;
    fruitX = rand() % width;
    fruitY = rand() % height;
    score = 0;
    nTail = 0;
}

void Draw() {
    system("cls"); // Clear the console
    for (int i = 0; i < width+2; i++)
        cout << "#";
    cout << endl;

    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            if (j == 0)
                cout << "#";
            if (i == snakeY && j == snakeX)
                cout << "O"; // Snake's head
            else if (i == fruitY && j == fruitX)
                cout << "F"; // Fruit
            else {
                bool print = false;
                for (int k = 0; k < nTail; k++) {
                    if (tailX[k] == j && tailY[k] == i) {
                        cout << "o"; // Snake's tail
                        print = true;
                    }
                }
                if (!print)
                    cout << " ";
            }
            if (j == width - 1)
                cout << "#";
        }
        cout << endl;
    }

    for (int i = 0; i < width+2; i++)
        cout << "#";
    cout << endl;
    cout << "Score:" << score << endl;
}

void Input() {
    if (_kbhit()) {
        switch (_getch()) {
        case 'a':
            dir = LEFT;
            break;
        case 'd':
            dir = RIGHT;
            break;
        case 'w':
            dir = UP;
            break;
        case 's':
            dir = DOWN;
            break;
        case 'x':
            dir = STOP;
            break;
        }
    }
}

void Logic() {
    int prevX = tailX[0];
    int prevY = tailY[0];
    int prev2X, prev2Y;
    tailX[0] = snakeX;
    tailY[0] = snakeY;
    for (int i = 1; i < nTail; i++) {
        prev2X = tailX[i];
        prev2Y = tailY[i];
        tailX[i] = prevX;
        tailY[i] = prevY;
        prevX = prev2X;
        prevY = prev2Y;
    }
    switch (dir) {
    case LEFT:
        snakeX--;
        break;
    case RIGHT:
        snakeX++;
        break;
    case UP:
        snakeY--;
        break;
    case DOWN:
        snakeY++;
        break;
    default:
        break;
    }
    if (snakeX >= width) snakeX = 0; else if (snakeX < 0) snakeX = width - 1;
    if (snakeY >= height) snakeY = 0; else if (snakeY < 0) snakeY = height - 1;

    for (int i = 0; i < nTail; i++)
        if (tailX[i] == snakeX && tailY[i] == snakeY)
            score = 0;

    if (snakeX == fruitX && snakeY == fruitY) {
        score += 10;
        fruitX = rand() % width;
        fruitY = rand() % height;
        nTail++;
    }
}

int main() {
    char userInput;
    do {
        Setup();
        while (score > -1) {
            Draw();
            Input();
            Logic();
            // Adjust speed by adding delay
            // For faster gameplay, decrease the value of sleep duration
            // For slower gameplay, increase the value of sleep duration
            // Experiment with different values to find what suits best
            // This delay is in milliseconds
            // You may need to include <windows.h> on Windows systems for this sleep function
            // usleep(100000) for Unix-like systems like Linux or macOS
            // Change the sleep function as per your system
            // Replace sleep function with Sleep() on Windows
            // Replace sleep function with usleep() on Unix-like systems
            // You may also use cross-platform libraries like SDL or SFML for more control over the game loop
            sleep(200);
        }
        cout << "game over. press R to restart or any other key to exit." << endl;
        userInput = _getch();
    } while (userInput == 'R' || userInput == 'r');
    cout << "exiting snake." << endl;
    return 0;
}
