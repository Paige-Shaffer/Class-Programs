#include <iostream>
#include <string>
#include <fstream>
#include <unordered_set>
using namespace std;
// fstream - file upload, iostream is standard library

unordered_set<string> validQuit = {"Q", "q"};
unordered_set<string> validTypeIC = {"IC", "Ic", "ic"};
unordered_set<string> validTypeEV = {"EV", "ev", "Ev"};
//String sets - used to simplify validation of correct input 


string EvIc;
string Cargo;
string Wheelbase; 
// Strings used in Functions

// EVIC Function
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
    EvIc = getEcIv(EvIc); 
    if (EvIc == "IC") {
        Wheelbase = getWheelbase(Wheelbase);
        cout << "Press Enter to continue" << endl; 
        Cargo = getCargo(Cargo);
        cout << "You have chosen an IV vehicle with a " << Wheelbase << " wheelbase and a " << Cargo << " cargo measurement." << endl; 
    }
    else if (EvIc == "EV") {
        cout << "You have chosen a EV vehicle, which has a medium cargo length and roofline." << endl;
    }
    else {
        cout << "An error has occured. Please attempt to run the program again." << endl; 
    }  
return 0; 
}