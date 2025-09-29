import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import webbrowser

# Define Color Palete 
DARK_BLUE = "#031926"
TEAL = "#468189"
LIGHT_TEAL = "#77ACA2"
PALE_GREEN = "#A3C9A8"
LIGHT_SANDY_BROWN = "#F4E9CD"
MUTED_BLUE = "#5B6A82"
WHITE = "#FFFFFF"
OFF_WHITE = "#F8F9FA"
ACCENT_ORANGE = "#FF6B35"

# Login Window
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        #Configure layout
        self.title("Login")
        self.geometry("400x300")
        self.config(bg=LIGHT_SANDY_BROWN)
        self.center_window()

        # Track login attempts
        self.max_attempts = 3
        self.attempts_left = self.max_attempts

        #After 3 attempts, window closes automatically 
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        #Esc key can be used to close window 
        self.bind("<Escape>", self.on_close)
        self.create_widgets()

    #Centers windows when loaded using device sizing
    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"+{x}+{y}")

    #Create login widget for username/password
    def create_widgets(self):
        # Username  
        self.username_label = tk.Label(self, text="Username:", font=("Helvetica", 14, "bold"), bg=LIGHT_SANDY_BROWN, fg=DARK_BLUE)
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self, font=("Helvetica", 14), bg=WHITE, fg=DARK_BLUE, relief="flat")
        self.username_entry.pack(pady=10, ipady=5)

        # Password 
        self.password_label = tk.Label(self, text="Password:", font=("Helvetica", 14, "bold"), bg=LIGHT_SANDY_BROWN, fg=DARK_BLUE)
        self.password_label.pack(pady=10)

        # Hides password when it is typed using '*' 
        self.password_entry = tk.Entry(self, font=("Helvetica", 14), show="*", bg=WHITE, fg=DARK_BLUE, relief="flat")
        self.password_entry.pack(pady=10, ipady=5)

        # Login button
        self.login_button = tk.Button(self, text="Login", font=("Helvetica", 14, "bold"), bg=TEAL, fg=WHITE, activebackground=LIGHT_TEAL, command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        # Get user input for username and password
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check credentials 
        # If correct, proceed - else, remove one user attempt from the count. 
        if username == "admin" and password == "password":
            self.destroy()
            MainApp().mainloop()
        else:
            self.attempts_left -= 1

            if self.attempts_left > 0:
                messagebox.showerror(
                    "Login Failed",
                    f"You have entered your username or password incorrectly.\n"
                    f"You have {self.attempts_left} more {'attempt' if self.attempts_left == 1 else 'attempts'}. After 3 attempts, the program will close."
                )
        # Upon close, inform user 
            else:
                messagebox.showerror(
                    "Login Failed",
                    f"You have entered your credentials incorrectly too many times.\n"
                    f"The application will now close."
                )
                self.destroy()

    def on_close(self, event=None):  
        self.destroy()

# Main application; shown after a sucessful login 
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Configure Layout 
        self.title("Main Application")
        self.geometry("800x700")
        self.config(bg=DARK_BLUE)
        self.center_window()

        # Configure custom theme - easier styling 
        self.style = ttk.Style(self)
        self.style.theme_create("custom", parent="alt", settings={
            "TNotebook": {
                "configure": {
                    "background": DARK_BLUE,
                    "padding": [5, 5]
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [25, 10],
                    "background": MUTED_BLUE,
                    "foreground": WHITE,
                    "font": ("Arial", 12, "bold"),
                    "width": 15
                },
                "map": {
                    "background": [("selected", TEAL)],
                    "expand": [("selected", [1, 1, 1, 0])]
                }
            },
            "TFrame": {"configure": {"background": LIGHT_SANDY_BROWN}}
        })

        # Use established theme 
        self.style.theme_use("custom")
        # Keybind 
        self.bind("<Escape>", self.on_close)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        # Flags for lazy loading
        self.correlation_loaded = False
        self.map_loaded = False
        self.scatterplot_loaded = False

        self.create_widgets()
    # Centers windows when loaded using device sizing
    def center_window(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"+{x}+{y}")

    # Styling for standard buttons (More info & More)
    def create_standard_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, font=("Arial", 12, "bold"),
                      bg=TEAL, fg=WHITE, activebackground=LIGHT_TEAL,
                      relief="flat", padx=15, pady=5,
                      command=command)
        return btn
    # Before closing, prompts for confirmation from user 
    def on_close(self, event=None):
        if messagebox.askokcancel("Quit", "Do you want to exit the application?"):
            self.destroy()

    # Creates tabs - Map, Clusters, Matrix, Frames 
    def create_widgets(self):
        # Tab control
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")

        # Tabs - defines 4, array formatting 
        self.tab0 = ttk.Frame(self.tab_control)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab0, text="Main")
        self.tab_control.add(self.tab1, text="Correlation Matrix")
        self.tab_control.add(self.tab2, text="Geocoded Map")
        self.tab_control.add(self.tab3, text="Scatterplot")

        # Initializes main tab
        self.create_main_tab(self.tab0)

        # Tab change listener for lazy loading - only loads when tab is open
        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_change)

    # Defines tab change events - when a tab is changed, new content is displayed 
    def on_tab_change(self, event):
        selected_tab = event.widget.select()
        tab_index = event.widget.index(selected_tab)

        # Correlation Matric Tab
        if tab_index == 1 and not self.correlation_loaded:
            self.create_correlation_tab(self.tab1)
            self.correlation_loaded = True
        # Geocoded Map Tab 
        elif tab_index == 2 and not self.map_loaded:
            self.create_map_tab(self.tab2)
            self.map_loaded = True
        # Scatterplot Diagram Tab
        elif tab_index == 3 and not self.scatterplot_loaded:
            self.create_scatterplot_tab(self.tab3)
            self.scatterplot_loaded = True

    def create_main_tab(self, tab):
        # Main content frame
        content_frame = ttk.Frame(tab)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        info_text = (
            "Welcome!\n\n"
            "Using data from the NamUs database, this project combines machine learning and visual analytics to uncover patterns and relationships between features of missing individuals, helping to provide deeper insight into these cases.\n\n"
            "Click on a tab to begin exploring."
        )

        self.info_label = tk.Label(
            content_frame,
            text=info_text,
            justify="left",
            anchor="nw",
            fg=DARK_BLUE,
            bg=LIGHT_SANDY_BROWN,
            font=("Arial", 14),
            wraplength=700
        )
        self.info_label.pack(fill="both", expand=True)

        # Bottom frame for buttons
        bottom_frame = ttk.Frame(tab)
        bottom_frame.pack(side="bottom", fill="x", pady=10)

        # About button
        about_button = self.create_standard_button(bottom_frame, "About", self.show_about)
        about_button.pack(side="right", padx=10)

        # Copyright label
        copyright_label = tk.Label(tab, text="Copyright @2025 Paige Shaffer", 
                                 font=("Arial", 10), bg=LIGHT_SANDY_BROWN)
        copyright_label.pack(side="bottom", pady=5)

    def create_correlation_tab(self, tab):
        # Content frame with scrollbar
        content_frame = ttk.Frame(tab)
        content_frame.pack(fill="both", expand=True)

        # Load correlation matrix image
        try:
            image_path = "In-Progress/SeniorProjects/Visuals/correlation_matrix.png"
            image = Image.open(image_path)
            
            # Resize image to fit window while maintaining aspect ratio
            window_width = self.winfo_width() - 40  # Account for padding
            window_height = self.winfo_height() - 100  # Account for buttons and padding
            image.thumbnail((window_width, window_height), Image.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            
            image_label = tk.Label(content_frame, image=photo, bg=LIGHT_SANDY_BROWN)
            image_label.image = photo  # Keep a reference
            image_label.pack(fill="both", expand=True, padx=10, pady=10)
        except Exception as e:
            error_label = tk.Label(content_frame, text=f"Failed to load correlation matrix: {str(e)}", 
                                 bg=LIGHT_SANDY_BROWN, fg="red")
            error_label.pack(fill="both", expand=True)

        # Bottom button frame
        button_frame = ttk.Frame(tab)
        button_frame.pack(side="bottom", fill="x", pady=10)

        back_button = self.create_standard_button(button_frame, "Back", self.go_to_main_tab)
        back_button.pack(side="left", padx=10)

        info_button = self.create_standard_button(button_frame, "More Info", self.describe_correlation)
        info_button.pack(side="right", padx=10)

    def create_map_tab(self, tab):
        # Top button frame
        top_frame = ttk.Frame(tab)
        top_frame.pack(side="top", fill="x", pady=10)

        full_map_path = "In-Progress\SeniorProjects\Visuals\geocoded_map.html" 
        open_button = self.create_standard_button(top_frame, "Open Full Map in Browser", 
                                                lambda: webbrowser.open(full_map_path))
        open_button.pack(pady=5)

        # Content frame for map preview
        content_frame = ttk.Frame(tab)
        content_frame.pack(fill="both", expand=True)

        # Load map preview image
        try:
            image_path = "In-Progress/SeniorProjects/Visuals/geocoded_map_preview.png" 
            image = Image.open(image_path)
            
            # Resize image to fit window while maintaining aspect ratio
            window_width = self.winfo_width() - 40
            window_height = self.winfo_height() - 100
            image.thumbnail((window_width, window_height), Image.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            
            image_label = tk.Label(content_frame, image=photo, bg=LIGHT_SANDY_BROWN)
            image_label.image = photo  # Keep a reference
            image_label.pack(fill="both", expand=True, padx=10, pady=10)
        except Exception as e:
            error_label = tk.Label(content_frame, text=f"Failed to load map preview: {str(e)}", 
                                 bg=LIGHT_SANDY_BROWN, fg="red")
            error_label.pack(fill="both", expand=True)

        # Bottom button frame
        button_frame = ttk.Frame(tab)
        button_frame.pack(side="bottom", fill="x", pady=10)

        back_button = self.create_standard_button(button_frame, "Back", self.go_to_main_tab)
        back_button.pack(side="left", padx=10)

        info_button = self.create_standard_button(button_frame, "More Info", self.describe_map)
        info_button.pack(side="right", padx=10)

    def create_scatterplot_tab(self, tab):
        # Content frame
        content_frame = ttk.Frame(tab)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Load scatterplot image
        try:
            image_path = "In-Progress/SeniorProjects/Visuals/Clusters.png"  
            image = Image.open(image_path)
            
            # Resize image to fit window while maintaining aspect ratio
            window_width = self.winfo_width() - 45
            window_height = self.winfo_height() - 100
            image.thumbnail((window_width, window_height), Image.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            
            image_label = tk.Label(content_frame, image=photo, bg=LIGHT_SANDY_BROWN)
            image_label.image = photo  # Keep a reference
            image_label.pack(fill="both", expand=True, padx=10, pady=10)
        except Exception as e:
            error_label = tk.Label(content_frame, text=f"Failed to load scatterplot: {str(e)}", 
                                 bg=LIGHT_SANDY_BROWN, fg="red")
            error_label.pack(fill="both", expand=True)

        # Bottom button frame
        button_frame = ttk.Frame(tab)
        button_frame.pack(side="bottom", fill="x", pady=10)

        back_button = self.create_standard_button(button_frame, "Back", self.go_to_main_tab)
        back_button.pack(side="left", padx=10)

        info_button = self.create_standard_button(button_frame, "More Info", self.describe_scatterplot)
        info_button.pack(side="right", padx=10)

    def describe_map(self):
        description = (
            "This map represents geocoded data based on age groups. The static preview is shown here. "
            "For full interaction, click 'Open Full Map in Browser'. \n \n"
            "This interactive map visualizes missing persons cases from the NamUS database, showing each case's location  with color-coded markers representing different demographic attributes. \n \n "

            "When within the full map interface, you have three diffent viewing modes: \n \n"

            "Age - Colors indicate the person's age group \n \n"
            "Ethnicity - Colors represent racial/ethnic background \n \n"
            "Sex - Colors distinguish between Male and Female cases \n \n"

            "When you hover over a point, it will display a popup with information on the persons age, missing location, ethnicity/race and sex. \n \n"
            
        )
        self.show_description(description)

    def describe_correlation(self):
        description = (
            "This correlation matrix shows the relationship between different variables in the dataset, "
            "by calculating Pearson correlation coefficients, which measure how strongly pairs of variables relate linearly (from -1 to 1). "
            "It generates a heatmap, where negative correlations are represented in dark teal and positive correlations are indicated by the cream-color. It is used to determine which features (age, race location) influence each the most. \n \n"

            "Based on the correlation graph, we can conclude: \n \n"
            "Our strongest relationships are age/clustering, race/location, state/city. Age groups tend to cluster together, race demographics tend to be grouped together in certain geographic locations, and individuals go missing in many cities within a state. \n \n" 

            "Our medium-impact relationships are age/sex and race/clustering. Some racial groups dominate specfic clusters, and certain gender groups contain more of the same age group. \n \n"

            "Our low impact groups are county/age, and sex/state. Age distribution is relatively even across counties, and gender ratios remain consistent geographically."
        )
        self.show_description(description)

    def describe_scatterplot(self):
        description = (
            "The scatterplot visualizes connections between features of missing individuals "
            "using kmeans clustering and unsupervised learning. "
            "While using PCA (Principal Component Analysis) for dimensionality reduction, " 
            "each new point represents an individual case, following the key provided. "
            "Tighter groupings are indictative of similar demographic and geographic features in the data. \n \n"

            "What Each Cluster Represents \n \n"

            "Cluster 0 - 859 cases \n"
            "Average Age: 48.4 years \n"
            "Most Common Gender: Male \n"
            "Dominant Race/Ethnicity: White / Caucasian \n"
            "Most Frequent Locations: City of York, State of New York \n \n"

            "Cluster 1 - 321 cases \n"
            "Average Age: 30.2 years \n"
            "Most Common Gender: Male \n"
            "Dominant Race/Ethnicity: White / Caucasian \n"
            "Most Frequent Locations: City of Washington, State of Virginia \n \n" 
                                                                                                     
            "Cluster 2 - 1337 cases \n"
            "Average Age: 23.5 years \n"
            "Most Common Gender: Male \n"
            "Dominant Race/Ethnicity: Hispanic / Latino \n"
            "Most Frequent Locations: The City of York, State of Arizona \n \n"

            "Cluster 3 - 535 cases \n"
            "Average Age: 28.3 years \n"  
            "Most Common Gender: Female \n"
            "Dominant Race/Ethnicity: Black / African American \n"
            "Most Frequent Locations: City of York, State of New York \n \n"

            "Cluster 4 - 431 cases \n "
            "Average Age: 27.4 years \n"
            "Most Common Gender: Male \n"
            "Dominant Race/Ethnicity: White / Caucasian \n"
            "Most Frequent Locations: City of Staten Island,  State of California \n \n"

            "Cluster 5 - 88 cases \n"
            "Average Age: 29.5 years \n"
            "Most Common Gender: Male \n"
            "Dominant Race/Ethnicity: Hispanic / Latino, Uncertain \n"
            "Most Frequent Locations: City of Los Angeles, State of California \n \n"
        )
        self.show_description(description)

    def show_about(self):
        description = (
            "Missing Persons Analysis Tool\n"
            "Version 1.0\n\n"
            "This application provides visual analytics for missing persons data."
        )
        self.show_description(description)

    def show_description(self, description):
        messagebox.showinfo("More Info", description)

    def go_to_main_tab(self):
        self.tab_control.select(self.tab0)

# Run 
if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()