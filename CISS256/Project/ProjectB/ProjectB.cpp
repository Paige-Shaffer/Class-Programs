#include <iostream>
#include <string>
#include <fstream>
#include <unordered_set>
using namespace std; 
// fstream - file upload, iostream is standard library 

string dealerName;
string memoRef;
string color; 
string colorInput; 
string EvIc;
string Cargo;
string Wheelbase; 
// Strings used in Functions

int quantity; // Define Quantity 

bool carCount = false; //CarCount boolean
bool collectColor = false; //boolean to recall function 

unordered_set<string> validColors = {"W", "w", "B", "b", "G", "g"}; 
// Define unordered set of validcolors to run function
unordered_set<string> validQuit = {"Q", "q"}; 
// unordered set to exit function 
unordered_set<string> validTypeIC = {"IC", "Ic", "ic"};
unordered_set<string> validTypeEV = {"EV", "ev", "Ev"};
//String sets - used to simplify validation of correct IcEv input 

string car[6]; 
// Car Array used to write file

string getMemo(string memoRef) {
    cout << "Please enter the Memo Reference: "<< endl; //user enters memo reference
    cin >> memoRef;    
    return memoRef; 

}
string getDealer(string dealerName) {
    cout << "Please enter dealer name: " << endl;  //user enters dealer name
    cin >> dealerName; 
    return dealerName; 
}

//Quantity function 
int getQuantity(int quantity) { 
    cout << "How many cars would you like to purchase? (or enter '999' to quit)"; //Quantity input request
        cin >> quantity; //Quantity output
        cout << "" << endl;
        if (quantity > 99 || quantity < 1) { 
            if (quantity == 999) {
                return 0; 
            }
            else {
            cout << "Please enter an integer value between 1 and 99." << endl; 
            cout << "" << endl; 
            cout << "redirecting..." << endl;
            } 
        }
        else { 
            cout << "" << endl; carCount = true; }
return quantity;
}

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
string getEcIv(string EvIc)
{
    bool EvIcInput = false; // Define Boolean for EvIc
    cout << "" << endl;
    while (!EvIcInput){
        cout << "Would you like an EV or IC vehicle? (or press 'q' to quit)";
        cin >> EvIc;
        if (validQuit.count(EvIc) > 0) {
            exit(0); 
        }
        else if (validTypeEV.count(EvIc) > 0) {
            EvIcInput = true;
            EvIc = "EV"; 
            return EvIc;
        }
        else if (validTypeIC.count(EvIc) > 0) {
            EvIcInput = true;
            EvIc = "IC"; 
            return EvIc; 
        }
        else {
            cout << "Please enter either EV or IC and try again. " << endl;
            cout << "" << endl;
            cout << "redirecting..." << endl;
            EvIcInput = false;
            cin >> EvIc;
        }
    }
    return EvIc;
}
//Cargo Function 
string getCargo(string Cargo) {
    bool cargoInput = false; 
    while(!cargoInput) {
        cout << "Please choose the Cargo Roofline length. " << endl;
        cout << "Choose between a L, R, or H roofline or select Q to quit" << endl;
        cin >> Cargo;  // Recieve Roofline length of a Cargo Vehicle
        if (Cargo == "l" || Cargo == "L") {
            Cargo = "L";
            cargoInput = true;
            return Cargo; 
        }
        else if (Cargo == "R" || Cargo == "r") {
            Cargo = "R";
            cargoInput = true; 
            return Cargo;
        }
        else if (Cargo == "H" || Cargo == "h") {
            Cargo = "H"; 
            cargoInput = true;
            return Cargo;
        }
        else if (validQuit.count(Cargo) > 0) {
            exit(0); 
        }
        else {
            cout << "Please enter a valid measurement and try again."  << endl;
            cargoInput = false; 
            return Cargo; 
        } 
    }
return Cargo; 
}

//Wheelbase Function
string getWheelbase(string Wheelbase) {
    bool wheelbaseInput = false; 
    while(!wheelbaseInput) {
        cout << "Please choose a measurement for the wheelbase." << endl;
        cout << "Choose between Small(S), Medium(M), or Extended(E)." << endl; 
        cout << "To quit, please enter q." << endl; 
        cin >> Wheelbase; // Recieve Wheelbase measurement of a Cargo Vehicle
        if (Wheelbase == "S" || Wheelbase == "s") {
            Wheelbase = "S"; 
            wheelbaseInput = true;
            return Wheelbase;
        }
        else if (Wheelbase == "m" || Wheelbase == "M") {
            Wheelbase = "M"; 
            wheelbaseInput = true;
            return Wheelbase;
        }
        else if (Wheelbase == "e" || Wheelbase == "E") {
            Wheelbase = "E"; 
            wheelbaseInput = true; 
            return Wheelbase; 
        }
        if (validQuit.count(Wheelbase) > 0) {
            exit(0); 
        } 
        else {
             cout << "Please enter a valid measurement and try again."  << endl;
             wheelbaseInput = false; 
             return Wheelbase; }
    }
cout << "" << endl;
return Wheelbase; 
} 


int main() {
    ofstream outputFile("Ford.txt");
    dealerName = getDealer(dealerName);
    car[0] = dealerName;
    memoRef = getMemo(memoRef);
    car[1] = memoRef; 
    cout << dealerName << " " << memoRef << endl; 
    quantity = getQuantity(quantity);
    if (quantity != 0) {
    cout << "You have selected a quantity of " << quantity << " cars.";
    car[2] = to_string(quantity); 
    }
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
            car[3] = color; 
            cout << "Please continue...";
            }
        // Quit Program
        if  (validQuit.count(colorInput) > 0) {
            cout << "You have chosen to quit the program. " << endl; 
            cout << "Please have a good day." << endl;
            cout << "..." << endl;
            return 0; 
        }
        // Other --- Error code and retrial 
        if (validColors.count(colorInput) == 0 && validQuit.count(colorInput) == 0) {
            collectColor = false; 
            cout << "" << endl;
            cout << "Please enter a valid color input and try again." << endl; 
            cout << "" << endl; 
        }
    }
    EvIc = getEcIv(EvIc); 
    if (EvIc == "IC") {
        Wheelbase = getWheelbase(Wheelbase);
        cout << "Press Enter to continue" << endl; 
        Cargo = getCargo(Cargo);
        cout << "You have chosen an IV vehicle with a " << Wheelbase << " wheelbase and a " << Cargo << " cargo measurement." << endl; 
        car[4] = "IC";
        car[5] = Wheelbase;
        car[6] = Cargo;
    }
    else if (EvIc == "EV") {
        cout << "You have chosen a EV vehicle, which has a medium cargo length and roofline." << endl;
        car[4] = "EV"; 
        car[5] = "M";
        car[6] = "R";
    }
    else {
        cout << "An error has occured. Please attempt to run the program again." << endl; 
    }  
    for (int i = 0; i < 7; i++) {
    cout << car[i] << " "; 
    outputFile << " " << car[i] << " " ; 
    }
    outputFile.close(); 
    return 0; 
}
