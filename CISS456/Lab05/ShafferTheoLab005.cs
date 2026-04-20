using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;  
using System.Text;

namespace Lab05
{
    public class ArticleMeta
    {
        public string Title { get; set; } = string.Empty;
        public DateTime DatePublished { get; set; }
        public string Tags { get; set; } = string.Empty;
    }

    public class ArticleInfo
    {
        public string Title { get; set; } = string.Empty;
        public DateTime DatePublished { get; set; }
        public string RelativePath { get; set; } = string.Empty;
    }

    internal class CSVExportTool
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Article CSV Export ===");
            Console.WriteLine();

            // Get current directory
            string rootDirectory = Directory.GetCurrentDirectory();

            // 1. Author folder input
            Console.Write("Enter author name with no spaces. (e.g., MichealChen): ");
            string? authorNameInput = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(authorNameInput))
            {
                Console.WriteLine("Author name cannot be empty.");
                return;
            }

            // Recursively search for the folder that matches the author name
            string? authorDirectory = FindAuthorFolderRecursive(rootDirectory, authorNameInput);

            if (authorDirectory == null)
            {
                Console.WriteLine("Could not locate an author folder matching that name.");
                return;
            }

            Console.WriteLine($"Author folder found: {authorDirectory}");
            Console.WriteLine();

            string authorFolderName = Path.GetFileName(authorDirectory);

            // 2. Date range input
            DateTime startDate = ReadDate("Enter start date (yyyy-MM-dd): ");
            DateTime endDate = ReadDate("Enter end date (yyyy-MM-dd): ");

            if (endDate < startDate)
            {
                Console.WriteLine("End date cannot be earlier than start date.");
                return;
            }

            // 3. Process files
            if (!Directory.Exists(authorDirectory))
            {
                Console.WriteLine($"Directory '{authorDirectory}' not found.");
                return;
            }

            // 4. Collect matching articles
            List<ArticleInfo> results = new List<ArticleInfo>();

            // Get all .meta files in the author's directory
            string[] metaFiles = Directory.GetFiles(authorDirectory, "*.csv");

            foreach (string metaFile in metaFiles)
            {
                try
                {   // Read and parse metadata (CSV format)
                    ArticleMeta? meta = ReadMetaFromCsv(metaFile);

                    if (meta == null)
                        continue;

                    if (meta.DatePublished < startDate || meta.DatePublished > endDate)
                        continue;

                    // Construct relative HTML path
                    string baseName = Path.GetFileNameWithoutExtension(metaFile);
                    string htmlFile = baseName + ".html";

                    string fullHtmlPath = Path.Combine(authorDirectory, htmlFile);
                    string relativePath = Path.GetRelativePath(rootDirectory, fullHtmlPath)
                                              .Replace(Path.DirectorySeparatorChar, '/');

                    // Add to results
                    results.Add(new ArticleInfo
                    {
                        Title = meta.Title,
                        DatePublished = meta.DatePublished,
                        RelativePath = relativePath
                    });
                }
                // Handle potential errors
                catch (Exception ex)
                {
                    Console.WriteLine($"Error reading {metaFile}: {ex.Message}");
                }
            }

            // 5. Output results
            if (results.Count == 0)
            {
                Console.WriteLine("No matching articles found.");
                return;
            }

            // Create CSV file
            string datePart = $"{startDate:yyyyMMdd}_{endDate:yyyyMMdd}";
            string csvName = "Articles.csv";
            string lab05Directory = Directory.GetParent(authorDirectory)!.FullName;
            string csvPath = Path.Combine(lab05Directory, csvName);

            WriteCsv(results, csvPath);

            Console.WriteLine($"\nCSV created: {csvPath}");
        }

        // Read and validate date input
        static DateTime ReadDate(string prompt)
        {
            while (true)
            {
                Console.Write(prompt);
                string? input = Console.ReadLine();

                if (DateTime.TryParseExact(
                    input,
                    "yyyy-MM-dd",
                    CultureInfo.InvariantCulture,
                    DateTimeStyles.None,
                    out DateTime date))
                {
                    return date;
                }
                // Invalid input
                Console.WriteLine("Invalid date. Format must be yyyy-MM-dd.");
            }
        }

        // Escape CSV special characters
        static string CsvEscape(string value)
        {
            if (value.Contains(",") || value.Contains("\"") || value.Contains("\n"))
            {
                value = value.Replace("\"", "\"\"");
                return $"\"{value}\"";
            }
            // No escaping needed
            return value;
        }

        // Build CSV content and write to file
        static void WriteCsv(List<ArticleInfo> list, string path)
        {
            // Build CSV content
            StringBuilder sb = new StringBuilder();
            sb.AppendLine("Title,DatePublished,RelativePath");

            foreach (var item in list)
            {
                string title = CsvEscape(item.Title);
                string date = item.DatePublished.ToString("yyyy-MM-dd");
                string rel = CsvEscape(item.RelativePath);

                sb.AppendLine($"{title},{date},{rel}");
            }
            // Write to file
            File.WriteAllText(path, sb.ToString(), Encoding.UTF8);
        }

        // Recursive folder search
        static string? FindAuthorFolderRecursive(string startDir, string authorNameInput)
        {
            // Normalizes input: removes spaces, punctuation, and makes lowercase.
            string Normalize(string s)
            {
                return new string(
                    s.Where(char.IsLetterOrDigit)
                     .Select(char.ToLowerInvariant)
                     .ToArray()
                );
            }

            string target = Normalize(authorNameInput);

            foreach (string dir in Directory.GetDirectories(startDir, "*", SearchOption.AllDirectories))
            {
                string folderName = Path.GetFileName(dir);
                string normalizedFolder = Normalize(folderName);

                if (normalizedFolder == target)
                {
                    return dir;  // Full path to matching folder
                }
            }

            return null;
        }

        
        static ArticleMeta? ReadMetaFromCsv(string metaFilePath)
        {
            string[] lines = File.ReadAllLines(metaFilePath);

            if (lines.Length < 2)
                return null; 

            string dataLine = lines[1];
            string[] parts = SplitCsvLine(dataLine);

            if (parts.Length < 2)
                return null;

            string title = parts[0].Trim().Trim('"');
            string dateStr = parts[1].Trim().Trim('"');
            string tags = parts.Length >= 3 ? parts[2].Trim().Trim('"') : "";

            if (!DateTime.TryParseExact(
                    dateStr,
                    "yyyy-MM-dd",
                    CultureInfo.InvariantCulture,
                    DateTimeStyles.None,
                    out DateTime date))
            {
                return null;
            }

            return new ArticleMeta
            {
                Title = title,
                DatePublished = date,
                Tags = tags
            };
        }

        // Simple CSV line splitter handling quoted fields
        static string[] SplitCsvLine(string line)
        {
            List<string> result = new List<string>();
            bool inQuotes = false;
            StringBuilder current = new StringBuilder();

            foreach (char c in line)
            {
                if (c == '\"')
                {
                    inQuotes = !inQuotes;
                    continue;
                }

                if (c == ',' && !inQuotes)
                {
                    result.Add(current.ToString());
                    current.Clear();
                }
                else
                {
                    current.Append(c);
                }
            }

            result.Add(current.ToString());
            return result.ToArray();
        }
    }
}
