#include <iostream>
#include <string>
#include <fstream>
using namespace std; 
// fstream - file upload, iostream is standard library 

string color; 
string EvIc; 
char cp; 
char cargo;
char wheelbase;
string LRH; 
string SME; 
string dealerName;
string memoRef;
//undefined strings

int quantity;
//undefined integers 

bool carCount = false;
bool colorInput = false;
bool EvIcInput = false; 
//boolean values 

int main() {
    ofstream outputFile("project2.txt");
    cout << "Please enter dealer name: ";  //user enters dealer name
    cin >> dealerName; 
    cout << "Please enter the Memo Reference: ";//user enters memo reference
    cin >> memoRef; 
    cout << "" << endl;
    cout << "please wait... " << endl; //stall code test inline
    cout << "system processing..." << endl; //stall code 2
    cout << "" << endl;
    cout << "" << endl; 
    // While loop requesting car count validation 
    while (!carCount) { 
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
            cout << "You have selected " << quantity << " car(s).";
            cout << "" << endl; carCount = true; }
    }
        
    while (!colorInput) {
    cout << "" << endl;
    cout << "What color would you like your car to be? Please choose Black, White or Gray. (enter 'q' to quit)"; //Color request
    cin >> color; //Color output
    // Request and recieve car color
    if (color == "White" || color == "Gray" || color == "Grey" || color == "Black") {
        cout << "" << endl;
        cout << "You chose the color " << color << ". " << endl; colorInput = true; 
    }
    //Validate Car color
    else {
        if (color == "q" || color == "Q") {
                return 0; }
        else {
        cout << "Please enter a valid color value and try again. " << endl; 
        //Color Error Occurs
        cout << "" << endl;
        cout << "redirecting..." << endl; } 
    } 
    // Error message for incorrect car color; redirect and ask again 
}
    while (!EvIcInput) {
        cout << "" << endl;
        cout << "EV or IC? (or press 'q' to quit)"; 
        cin >> EvIc;
        if (EvIc == "q" || EvIc == "Q") {
                return 0; }
        else {
            cout << "" << endl; 
            if (EvIc == "IC") { 
            cout << "You have chosen IC. Would you like Cargo Roofline (C) or Wheelbase (P)?"; //Request C or P
            cin >> cp; // Define cp
                switch(cp) {
                    case 'C': case 'c': //User input is C 
                        cout << "" << endl;
                        cout << "You have chosen Cargo Roofline. Would you like {L},{R}, or {H}?";
                        cin >> cargo; //Recieve Cargo
                    switch(cargo) {
                        case 'L': case 'l': //User chooses L
                            LRH = 'L';
                            cout << "" << endl;
                            cout << "You have chosen a cargo vehicle (L)." << endl; EvIcInput = true;  
                            cout << "" << endl;   
                            continue; 
                        case 'R': case 'r': //User chooses R
                            LRH = 'R'; 
                            cout << "" << endl;
                            cout << "You have chosen a cargo vehicle (R). " << endl; EvIcInput = true;
                            cout << "" << endl;
                            continue; 
                        case 'H': case 'h': //User chooses H
                            LRH = 'H';
                            cout << "You have chosen a cargo vehicle (H). " << endl; EvIcInput = true;
                            continue; 
                            }
                    break;
                    case 'p': case 'P':
                    cout << "You have chosen Wheelbase. Would you like {S},{M} or {E}?";
                    cin >> wheelbase; //Recieve Wheelbase
                            switch(wheelbase) {
                            case 'S': case 's':
                                SME = 'S';
                                //User choses S
                                cout << "" << endl;
                                cout << "You have chosen a wheelbase vehicle (S)." << endl; EvIcInput = true;  
                                cout << "" << endl;
                                continue; 
                            case 'M': case 'm':
                                SME = 'M'; 
                                //User choses M
                                cout << "" << endl;
                                cout << "You have chosen a wheelbase vehicle (M)."<< endl; EvIcInput = true;
                                cout << "" << endl;
                                continue; 
                            case 'E': case 'e':
                            SME = 'E'; //User choses E
                            cout << "" << endl;
                            cout << "You have chosen a wheelbase vehicle (E)." << endl; EvIcInput = true;
                                continue; 
                            continue;}
            } 
        } 
            else if (EvIc == "EV") { 
                cout << "" << endl;
                cout << "You have chosen EV. EV is Cargo only with Medium length and roofline" << endl; EvIcInput = true;} 
                //User chooses EV

            else {
                cout << "Please enter either EV or IC and try again. " << endl; 
                cout << "" << endl;
                cout << "redirecting..." << endl; }
        } 
    } 
        
    cout << "Thank you for your purchase of " << quantity << " car(s) in the color " << color << " ." << endl;
    outputFile << "Dealer Name: " << dealerName << ", Memo Name: " << memoRef <<  endl;
    outputFile << "Quantity: " << quantity << " Color: " << color << " EV/IC: " << EvIc; 
    outputFile << "C/P: " << cp << " Cargo: " << cargo << " Wheelbase: " << wheelbase << " L/R/H: " << LRH << " SME  :" << SME << endl;
    outputFile.close();
    return 0;
    }