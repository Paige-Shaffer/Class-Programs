#include <iostream>
#include <string> 
#include <vector>
#include <fstream>
#include <sstream> 
#include <algorithm>
#include <cctype>

using namespace std; 

struct Book {
    string title;
    string author;
    string isbn; 
    int publicationYear;
};

class Library {
private: 
    vector<Book> books; 

public:
// Boolean - Confirm ISBN is = 13 and contains only numerical values 
    bool isValidISBN(const string& isbn) {
        if (isbn.size() !=13) return false; 
        for (char c : isbn) {
            if (!isdigit(c)) return false; 
        }
        return true;
    }
// Boolean - Confirm year is between 1900 & 2024
    bool isValidYear(int publicationYear) {
        return publicationYear>= 1900 && publicationYear <=2024;
    }

bool addBook(const Book& b) {
    bool valid = true;

// Run isValidISBN; if false, provide user with error message
    if (!isValidISBN(b.isbn)) {
        cout << "Invalid ISBN. Must be 13 digits.\n";
        valid = false;
    }
    // Run isValidYear; if false, provide user with error message
    if (!isValidYear(b.publicationYear)) {
        cout << "Invalid year. Must be between 1900 and 2024.\n";
        valid = false;
    }

    if (valid) {
        books.push_back(b);
    }

    return valid;
}

// Validate that there are books in the library 
    void printAll() {
        if(books.empty()) {
            cout << "There are no books in the library. \n";
            return; 
        }

    for (auto& b : books) {
            cout << b.title << " | " << b.author 
                 << " | " << b.isbn << " | " << b.publicationYear<< "\n";
        }
    }
// Export current books to a file 
    void exportToFile(const string& filename) {
        ofstream out(filename);
        for (auto& b: books) {
             out << b.title << "," << b.author << ","
                << b.isbn << "," << b.publicationYear << "\n";
        }
    }
// Import current books from a file into the system 
void importFromFile(const string& filename) {
    ifstream in(filename);
    if (!in) {
        cout << "Could not open file: " << filename << "\n";
        return;
    }

    string line;
    int lineNum = 0;
    while (getline(in, line)) {
        lineNum++;
        stringstream ss(line);
        string title, author, isbn, yearStr;

        // Get lines and info within the file
        getline(ss, title, ',');
        getline(ss, author, ',');
        getline(ss, isbn, ',');
        getline(ss, yearStr, ',');

        // Skip if the line is empty
        if (title.empty() || author.empty() || isbn.empty() || yearStr.empty()) {
            cout << "Line " << lineNum << " has invalid formatting: " << line << "\n";
            continue;
        }
        // Check for issues with comma formating - Unoptimized, but a short-term validation solution
        if (title.find(',') != string::npos ||
            author.find(',') != string::npos ||
            isbn.find(',') != string::npos) {
            cout << "Line " << lineNum << " contains misplaced commas: " << line << "\n";
            continue;
        }

        try {
            int year = stoi(yearStr);
            Book b{title, author, isbn, year};

            // Use addBook to validate ISBN and Year - print per line errors 
            if (!addBook(b)) {
                cout << "Line " << lineNum << " Cannot be processed.\n";
            }
        } catch (invalid_argument&) {
            cout << "Line " << lineNum << " has invalid year: " << yearStr << "\n";
        }
    }
}

// Sort books by author, year, or isbn
    void sortBooks(int sortChoice) {
        if (books.empty()) {
            cout << "There are no books to sort.\n";
            return;
        }

        switch (sortChoice) {
            case 1:
                sort(books.begin(), books.end(),
                    [](const Book& a, const Book& b) { return a.author < b.author; });
                cout << "Books sorted by author.\n";
                break;
            case 2:
                sort(books.begin(), books.end(),
                    [](const Book& a, const Book& b) { return a.publicationYear < b.publicationYear; });
                cout << "Books sorted by year.\n";
                break;
            case 3:
                sort(books.begin(), books.end(),
                    [](const Book& a, const Book& b) { return a.isbn < b.isbn; });
                cout << "Books sorted by ISBN.\n";
                break;
            default:
                cout << "Invalid sort choice.\n";
        }
    }
};

int main() {
    Library lib;
    int choice;

// Choice menu for Add, Show, Import, Export, Exit
    do {
        cout << "\nLibrary Menu\n";
        cout << "1. Add Book\n";
        cout << "2. Show Books\n";
        cout << "3. Sort Books\n";
        cout << "4. Export to File\n";
        cout << "5. Import from File\n";
        cout << "0. Exit\n";
        cout << "Choice: ";
        cin >> choice;
        cin.ignore(); 

// If/Else - For user input, import, and export files; If choice picked, asked for input. 
        if (choice == 1) {
            Book b;
            cout << "Enter title: ";
            getline(cin, b.title);
            cout << "Enter author: ";
            getline(cin, b.author);
            cout << "Enter ISBN (13 digits): ";
            getline(cin, b.isbn);
            cout << "Enter year: ";
            cin >> b.publicationYear;
            cin.ignore();

            lib.addBook(b);
        } 
        else if (choice == 2) {
            lib.printAll();
        } 
// Give user sort options; then sort by type 
        else if (choice == 3) {
            int sortChoice;
            cout << "Sort by:\n";
            cout << "1. Author\n";
            cout << "2. Year\n";
            cout << "3. ISBN\n";
            cout << "Choice: ";
            cin >> sortChoice;
            cin.ignore();

            lib.sortBooks(sortChoice);
        } 
// Export file to file specifed by user
    else if (choice == 4) {
        string filename;
        cout << "Enter filename to export to: ";
        getline(cin, filename);
        lib.exportToFile(filename);
        cout << "Exported to " << filename << "\n";
    } 
// Import file for file specified by the user
    else if (choice == 5) {
        string filename;
        cout << "Enter filename to import from: ";
        getline(cin, filename);
        lib.importFromFile(filename);
        cout << "Imported from " << filename << "\n";
}

    } while (choice != 0);

    return 0;
}
