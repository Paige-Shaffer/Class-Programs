using System;
using System.Collections.Generic;
using Microsoft.Data.Sqlite; 
using System.IO;
using Newtonsoft.Json;

public class User
{
    public int Id { get; set; }
    public string? FirstName { get; set; }
    public string? LastName { get; set; }
    public string? Email { get; set; }
}

public class UserDatabase
{
    private const string ConnectionString = "Data Source=userdb.sqlite;";
    
    public UserDatabase()
    {
        using (var connection = new SqliteConnection(ConnectionString)) 
        {
            connection.Open();
            var command = new SqliteCommand("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT, FirstName TEXT, LastName TEXT, Email TEXT)", connection); 
            command.ExecuteNonQuery();
        }
    }

    public void InsertUser(User user)
    {
        using (var connection = new SqliteConnection(ConnectionString))
        {
            connection.Open();
            var command = new SqliteCommand("INSERT INTO Users (FirstName, LastName, Email) VALUES (@FirstName, @LastName, @Email)", connection); 
            command.Parameters.AddWithValue("@FirstName", user.FirstName ?? "");
            command.Parameters.AddWithValue("@LastName", user.LastName ?? "");
            command.Parameters.AddWithValue("@Email", user.Email ?? "");
            command.ExecuteNonQuery();
        }
    }

    public User? SelectUser(int id)
    {
        using (var connection = new SqliteConnection(ConnectionString))
        {
            connection.Open();
            var command = new SqliteCommand("SELECT * FROM Users WHERE Id = @Id", connection);
            command.Parameters.AddWithValue("@Id", id);
            using (var reader = command.ExecuteReader())
            {
                if (reader.Read())
                {
                    return new User
                    {
                        Id = reader.GetInt32(0),
                        FirstName = reader.IsDBNull(1) ? null : reader.GetString(1),
                        LastName = reader.IsDBNull(2) ? null : reader.GetString(2),
                        Email = reader.IsDBNull(3) ? null : reader.GetString(3)
                    };
                }
            }
        }
        return null;
    }

    public void UpdateUser(User user)
    {
        using (var connection = new SqliteConnection(ConnectionString)) 
        {
            connection.Open();
            var command = new SqliteCommand("UPDATE Users SET FirstName = @FirstName, LastName = @LastName, Email = @Email WHERE Id = @Id", connection);
            command.Parameters.AddWithValue("@Id", user.Id);
            command.Parameters.AddWithValue("@FirstName", user.FirstName ?? "");
            command.Parameters.AddWithValue("@LastName", user.LastName ?? "");
            command.Parameters.AddWithValue("@Email", user.Email ?? "");
            command.ExecuteNonQuery();
        }
    }

    public void DeleteUser(int id)
    {
        using (var connection = new SqliteConnection(ConnectionString)) 
        {
            connection.Open();
            var command = new SqliteCommand("DELETE FROM Users WHERE Id = @Id", connection);
            command.Parameters.AddWithValue("@Id", id);
            command.ExecuteNonQuery();
        }
    }

    public List<User> ListUsers()
    {
        var users = new List<User>();
        using (var connection = new SqliteConnection(ConnectionString)) 
        {
            connection.Open();
            var command = new SqliteCommand("SELECT * FROM Users", connection);
            using (var reader = command.ExecuteReader())
            {
                while (reader.Read())
                {
                    users.Add(new User
                    {
                        Id = reader.GetInt32(0),
                        FirstName = reader.IsDBNull(1) ? null : reader.GetString(1),
                        LastName = reader.IsDBNull(2) ? null : reader.GetString(2),
                        Email = reader.IsDBNull(3) ? null : reader.GetString(3)
                    });
                }
            }
        }
        return users;
    }

    public void InsertUsers(string jsonFilePath)
    {
        var json = File.ReadAllText(jsonFilePath);
        var users = JsonConvert.DeserializeObject<List<User>>(json) ?? new List<User>();
        foreach (var user in users)
        {
            InsertUser(user);
        }
    }

    public void UpdateUsers(string jsonFilePath)
    {
        var json = File.ReadAllText(jsonFilePath);
        var users = JsonConvert.DeserializeObject<List<User>>(json) ?? new List<User>();
        foreach (var user in users)
        {
            UpdateUser(user);
        }
    }
}

public static class Program
{
    public static void Main()
    {
        var db = new UserDatabase();
        while (true)
        {
            Console.WriteLine();
            Console.WriteLine("User Database - Menu");
            Console.WriteLine("1) List all users");
            Console.WriteLine("2) View user by Id");
            Console.WriteLine("3) Delete user by Id");
            Console.WriteLine("4) Import users from JSON file");
            Console.WriteLine("5) Update users from JSON file");
            Console.WriteLine("0) Exit");
            Console.Write("Select an option: ");
            var choice = Console.ReadLine();

            try
            {
                switch (choice)
                {
                    case "1":
                        ListAll(db);
                        break;
                    case "2":
                        ViewById(db);
                        break;
                    case "3":
                        DeleteById(db);
                        break;
                    case "4":
                        ImportFromJson(db);
                        break;
                    case "5":
                        UpdateFromJson(db);
                        break;       
                    case "0":
                        return;
                    default:
                        Console.WriteLine("Unknown option.");
                        break;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error: " + ex.Message);
            }
        }
    }

    private static void ListAll(UserDatabase db)
    {
        var users = db.ListUsers();
        if (users.Count == 0)
        {
            Console.WriteLine("No users found.");
            return;
        }
        foreach (var u in users)
        {
            Console.WriteLine($"{u.Id}: {u.FirstName ?? ""} {u.LastName ?? ""} <{u.Email ?? ""}>");
        }
    }

    private static void ViewById(UserDatabase db)
    {
        var id = PromptForInt("Enter Id: ");
        var user = db.SelectUser(id);
        if (user == null)
            Console.WriteLine("User not found.");
        else
            Console.WriteLine($"{user.Id}: {user.FirstName ?? ""} {user.LastName ?? ""} <{user.Email ?? ""}>");
    }


    private static void DeleteById(UserDatabase db)
    {
        var id = PromptForInt("Enter Id to delete: ");
        var user = db.SelectUser(id);
        if (user == null)
        {
            Console.WriteLine("User not found.");
            return;
        }
        Console.Write($"Confirm delete {user.Id}: {user.FirstName ?? ""} {user.LastName ?? ""}? (y/N): ");
        var conf = Console.ReadLine();
        if (conf?.ToLower() == "y")
        {
            db.DeleteUser(id);
            Console.WriteLine("User deleted.");
        }
        else
        {
            Console.WriteLine("Cancelled.");
        }
    }

    private static void ImportFromJson(UserDatabase db)
    {
        Console.Write("Path to JSON file: ");
        var path = Console.ReadLine();
        if (string.IsNullOrWhiteSpace(path)) path = "Insert_Users.json";
        if (!File.Exists(path))
        {
            Console.WriteLine("File not found.");
            return;
        }
        db.InsertUsers(path);
        Console.WriteLine("Users imported.");
    }

    private static void UpdateFromJson(UserDatabase db)
    {
        Console.Write("Path to JSON file: ");
        var path = Console.ReadLine();
        if (string.IsNullOrWhiteSpace(path)) path = "Update_Users.json";
        if (!File.Exists(path))
        {
            Console.WriteLine("File not found.");
            return;
        }
        db.UpdateUsers(path);
        Console.WriteLine("Users updated from JSON.");
    }

    private static int PromptForInt(string prompt)
    {
        while (true)
        {
            Console.Write(prompt);
            var s = Console.ReadLine();
            if (int.TryParse(s, out var v)) return v;
            Console.WriteLine("Please enter a valid integer.");
        }
    }
}
