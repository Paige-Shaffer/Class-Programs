#include <iostream>
#include <string>
#include <fstream>
#include <unordered_set>
using namespace std; 
// fstream - file upload, iostream is standard library 

string color; // Define Color
string colorInput; //define color reference recieved by user 
bool collectColor = false; //boolean to recall function 
unordered_set<string> validColors = {"W", "w", "B", "b", "G", "g"}; 
// Define unordered set of validcolors to run function
unordered_set<string> validQuit = {"Q", "q"}; 

//Get color
string getColor(string colorInput) {
    // White
    if (colorInput == "W" || colorInput == "w") {
        return "White"; 
    }
    // Grey
    if (colorInput == "G" || colorInput == "g") {
        return "Grey"; 
    }
    // Black
    if (colorInput == "B" || colorInput == "b") {
        return "Black";
    }
return colorInput; 
}
    
int main () { 
    // While collectColor has not been recieved, run following loop: 
    while (!collectColor) {
        // Ask user to enter B, W, G as a color or Q to quit 
        cout << "" << endl;
        cout << "What color would you like your car to be? " << endl; 
        cout << "Please choose Black (B), White (W) or Gray (G)" << endl;
        cout << "If you would prefer to quit, please enter Q." << endl;
        cin >> colorInput; 

        // Grab color input from function
        if (validColors.count(colorInput) > 0) {
            color = getColor(colorInput); collectColor = true; 
            cout << "You have chosen the color " << color << ". " << endl;
            cout << "Please continue...";
            }
        // Quit Program
        if  (validQuit.count(colorInput) > 0){
            cout << "You have chosen to quit the program. " << endl; 
            cout << "Please have a good day." << endl;
            cout << "..." << endl;
            return 0; 
        }
        // Other --- Error code and retrial 
        if (validColors.count(colorInput) < 0 && validQuit.count(colorInput) < 0) {
            collectColor = false; 
            cout << "" << endl;
            cout << "Please enter a valid color input and try again." << endl; 
            cout << "" << endl; 
        }
    }
return 0; 
} 