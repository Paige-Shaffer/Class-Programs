#include <iostream>
#include <string>
#include <fstream>
using namespace std; 
// fstream - file upload, iostream is standard library 

string dealerName;
string memoRef;
//undefined strings

string getMemo(string memoRef) {
    cout << "Please enter the Memo Reference: " << endl; //user enters memo reference
    cin >> memoRef; 
    return memoRef; 

}
string getDealer(string dealerName) {
    cout << "Please enter dealer name: " << endl;  //user enters dealer name
    cin >> dealerName; 
    return dealerName; 
}

int main() {
    dealerName = getDealer(dealerName);
    memoRef = getMemo(memoRef);
    cout << dealerName << " " << memoRef << endl; 
    
return 0; 
}
