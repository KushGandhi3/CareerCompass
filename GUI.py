"""
CSC111 Winter 2024 Course Project 2: CareerCompass

This Python module is the GUI

This file is Copyright (c) 2024 Kush Gandhi
"""

from pathlib import Path
import webbrowser
import tkinter as tk
from job import Job
from structures import load_graph_and_tree
from tkinter import ttk, messagebox
from PIL import ImageTk, Image

# Get File Directory
folder = Path(__file__).absolute().parent


##############################################
# CareerCompass
##############################################


class CareerCompass:
    """
    Class representing the CareerCompass application

    NOTE: Below are only the instance attributes EXCLUDING tkinter widgets.

    Instance Attributes:
    - user_name: the name of the user
    - preferences: a dictionary containing the preferences of the user
    - job_postings: a list containing the job postings

    Representation Invariants:
    - user_name.length() <= 9
    - preferences.length() == 7
    - job_postings.length() <= 5

    """

    user_name: str | None
    preferences: list[str]
    job_postings: list[Job]

    def __init__(self, root):
        """
        Initialize the CareerCompass application
        """

        # Creating container for the pages
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        # Dictionary to store all the pages
        self.pages = {}

        # Load all the images
        self.images = {
            "line": ImageTk.PhotoImage(file=folder / "assets" / "Line.png"),
            "compass_emoji": ImageTk.PhotoImage(
                Image.open(folder / "assets" / "CompassEmoji.png")
            ),
            "hbutton": ImageTk.PhotoImage(
                Image.open(folder / "assets" / "HomeButton.png")
            ),
            "pbutton": ImageTk.PhotoImage(
                Image.open(folder / "assets" / "PreferencesButton.png")
            ),
            "cbutton": ImageTk.PhotoImage(
                Image.open(folder / "assets" / "ContactButton.png")
            ),
            "rs_image": ImageTk.PhotoImage(
                Image.open(folder / "assets" / "Rocket.png")
            ),
            "name_entry_image": ImageTk.PhotoImage(
                Image.open(folder / "assets" / "NameEntryBox.png")
            ),
            "start_button_image": ImageTk.PhotoImage(
                Image.open(folder / "assets" / "StartButton.png")
            ),
            "gradient_background": ImageTk.PhotoImage(
                Image.open(folder / "assets" / "FactBackground.png")
            ),
            "input_box": ImageTk.PhotoImage(
                file=folder / "assets" / "QuestionareEntryBox.png"
            ),
            "find_jobs": ImageTk.PhotoImage(
                Image.open(folder / "assets" / "FindJobsButton.png")
            ),
            "job_posting_img": ImageTk.PhotoImage(
                Image.open(folder / "assets" / "JobPostingBackground.png")
            ),
            "star_img": ImageTk.PhotoImage(Image.open(folder / "assets" / "Star.png")),
            "start_over_button_image": ImageTk.PhotoImage(
                Image.open(folder / "assets" / "StartOverButton.png")
            ),
            "URLButton": ImageTk.PhotoImage(
                Image.open(folder / "assets" / "URLButton.png")
            ),
        }

        # Initializing the instance attributes
        self.user_name = ""
        self.preferences = []
        self.job_postings = []

        # Load Decision Tree and Graph
        self.graph, self.tree = load_graph_and_tree()

        # Getting size of data set
        self.num_jobs = len(self.graph)
        self.avg_salary = str(self.graph.get_average_salary())
        print(len(self.avg_salary))
        if len(self.avg_salary) == 5:
            self.avg_salary = self.avg_salary[:2] + "," + self.avg_salary[2:]
        elif len(self.avg_salary) == 6:
            self.avg_salary = self.avg_salary[:3] + "," + self.avg_salary[3:]
        self.avg_salary = "$" + self.avg_salary

        # Show the HomePage
        self.show_pages("HomePage")

    def show_pages(self, target_page):
        """
        Shows the target page and destroys the current page
        """

        # Destroying Current Page
        if self.pages:
            current_page = next(iter(self.pages.values()))
            current_page.destroy()
            self.pages.clear()

        # Create the new page and store it in the dictionary
        new_page = None
        if target_page == "HomePage":
            new_page = HomePage(self.container, self)
        elif target_page == "PreferencesPage":
            new_page = PreferencesPage(self.container, self)
        elif target_page == "JobsPage":
            new_page = JobsPage(self.container, self)

        self.pages[target_page] = new_page
        new_page.pack(fill="both", expand=True)

    def reset_job_postings(self):
        self.job_postings.clear()

    def start_over(self):
        """
        Resets the application
        """

        # Clear the user name, preferences, and job postings
        self.user_name = None
        self.preferences.clear()
        self.job_postings.clear()


##############################################
# Home Page
##############################################


class HomePage(ttk.Frame):
    """
    Class for the Home Page

    Instance Attributes:
    - app: Instance of CareerCompass class representing the application

    """

    app: CareerCompass

    def __init__(self, container_home, app):
        super().__init__(container_home)

        self.app = app

        # Background
        canvas = tk.Canvas(
            self,
            bg="#0E355D",
            height=750,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.create_rectangle(0, 0, 270.0, 750.0, fill="#0084FF", outline="")
        canvas.create_image(138.0, 154.0, image=self.app.images["line"])

        # Title
        canvas.create_text(
            7.0,
            4.0,
            anchor="nw",
            text="Career",
            fill="#0E355D",
            font=("Karma Bold", 64 * -1),
        )
        canvas.create_image(63.0, 107.0, image=self.app.images["compass_emoji"])
        canvas.create_text(
            7.0,
            58.0,
            anchor="nw",
            text="C  mpass",
            fill="#0E355D",
            font=("Karma Bold", 64 * -1),
        )

        # Home Button
        home_button = tk.Button(
            self,
            image=self.app.images["hbutton"],
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
        )
        home_button.place(x=87.0, y=194.0, width=95.0, height=40.0)

        # Preferences Button
        preferences_button = tk.Button(
            self,
            image=self.app.images["pbutton"],
            borderwidth=0,
            highlightthickness=0,
            command=self.start_button_command,
            relief="flat",
        )
        preferences_button.place(x=46.0, y=268.0, width=180.0, height=40.0)

        # Contact Button
        contact_url = "https://github.com/sherwinokhowat/Internship-Finder"
        contact_button = tk.Button(
            self,
            image=self.app.images["cbutton"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda u=contact_url: webbrowser.open(u),
            relief="flat",
        )
        contact_button.place(x=69.0, y=344.0, width=128.0, height=40.0)

        # Rocket Ship
        canvas.create_image(150.0, 565.0, image=self.app.images["rs_image"])

        # Title
        canvas.create_text(
            625.0,
            75.0,
            anchor="center",
            text="Launch Your Career",
            fill="#D6F4FF",
            font=("Karma Bold", 64 * -1),
        )

        # Input Name
        canvas.create_text(
            383.0,
            155.0,
            anchor="nw",
            text="What's your name?",
            fill="#FFFFFF",
            font=("Karma Medium", 20 * -1),
        )
        canvas.create_image(635.0, 215.0, image=self.app.images["name_entry_image"])
        self.name_entry = tk.Entry(
            self, bg="#0084FF", fg="#FFFFFF", font=("Karma Medium", 16), bd=0
        )
        self.name_entry.place(x=395.0, y=200.0, width=481.0, height=35.0)

        # Filling in the name if it exists
        if self.app.user_name:
            self.name_entry.insert(0, self.app.user_name)

        # Start Button
        start_button = tk.Button(
            self,
            image=self.app.images["start_button_image"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.start_button_command(),
            relief="flat",
        )
        start_button.place(x=562.0, y=254.0, width=147.0, height=42.0)

        # Jobs Available Fact
        canvas.create_image(465.0, 500.0, image=self.app.images["gradient_background"])
        canvas.create_text(
            465.0,
            530.0,
            anchor="center",
            text="Jobs Available!",
            fill="#0E355D",
            font=("Karma Medium", 36 * -1),
        )
        canvas.create_text(
            465.0,
            470.0,
            anchor="center",
            text=self.app.num_jobs,
            fill="#FFFFFF",
            font=("Karma Bold", 64 * -1),
        )

        # Average Pay Fact
        canvas.create_image(800.0, 500.0, image=self.app.images["gradient_background"])
        canvas.create_text(
            800.0,
            530.0,
            anchor="center",
            text="Average Pay",
            fill="#0E355D",
            font=("Karma Medium", 36 * -1),
        )
        canvas.create_text(
            800.0,
            470.0,
            anchor="center",
            text=self.app.avg_salary,
            fill="#FFFFFF",
            font=("Karma Bold", 64 * -1),
        )

        # Packing the canvas
        canvas.pack(fill="both", expand=True)

    def start_button_command(self):
        """
        Receives the name from the entry box and proceeds to the next page upon clicking the start button
        """

        # Update the name
        self.update_name()

        # Proceed to the next page once the name is entered
        if self.app.user_name is not None:
            self.app.show_pages("PreferencesPage")

    def update_name(self):
        """
        Updates the name of the user from the entry box
        """

        # Get the name from the entry box
        username = self.name_entry.get()

        # Check if the name is empty
        if username.strip() == "":
            messagebox.showerror("Error", "Please enter your name.")
            return

        # Update the name
        self.app.user_name = username[:9]


##############################################
# Preferences Page
##############################################
class PreferencesPage(ttk.Frame):
    """
    Class for the Preferences Page

    Instance Attributes:
    - app: Instance of CareerCompass class representing the application
    """

    app: CareerCompass

    def __init__(self, container_preferences, app):
        super().__init__(container_preferences)

        self.app = app

        # Background
        canvas = tk.Canvas(
            self,
            bg="#0E355D",
            height=750,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.create_rectangle(0, 0, 270.0, 750, fill="#0084FF", outline="")
        canvas.create_image(138.0, 154.0, image=self.app.images["line"])

        # Title
        canvas.create_text(
            7.0,
            4.0,
            anchor="nw",
            text="Career",
            fill="#0E355D",
            font=("Karma Bold", 64 * -1),
        )
        canvas.create_image(63.0, 107.0, image=self.app.images["compass_emoji"])
        canvas.create_text(
            7.0,
            58.0,
            anchor="nw",
            text="C  mpass",
            fill="#0E355D",
            font=("Karma Bold", 64 * -1),
        )

        # Home Button
        home_button = tk.Button(
            self,
            image=self.app.images["hbutton"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.app.show_pages("HomePage"),
            relief="flat",
        )
        home_button.place(x=87.0, y=194.0, width=95.0, height=40.0)

        # Preferences Button
        preferences_button = tk.Button(
            self,
            image=self.app.images["pbutton"],
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
        )
        preferences_button.place(x=46.0, y=268.0, width=180.0, height=40.0)

        # Contact Button
        contact_url = "https://github.com/sherwinokhowat/Internship-Finder"
        contact_button = tk.Button(
            self,
            image=self.app.images["cbutton"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda u=contact_url: webbrowser.open(u),
            relief="flat",
        )
        contact_button.place(x=69.0, y=344.0, width=128.0, height=40.0)

        # Rocket Ship
        canvas.create_image(150.0, 565.0, image=self.app.images["rs_image"])

        # Page Title
        canvas.create_text(
            625.0,
            70.0,
            anchor="center",
            text=f"{self.app.user_name}, " f"let's see what you prefer.",
            fill="#D6F4FF",
            font=("Karma Bold", 40 * -1),
        )

        # Input Boxes
        self.input_boxes = []
        self.input_box = self.app.images["input_box"]

        # Inputs
        initial_y = 139.0
        questions = [
            "Jobs in Canada? (Yes/No/Don't Care)",
            "Remote jobs? (Yes/No/Don't Care)",
            "Frontend jobs? (Yes/No/Don't Care)",
            "Do you prefer a rating score above 3? (Yes/No/Don't Care)",
            "Are you skilled at Python? (Yes/No/Don't Care)",
            "Are you skilled at Java? (Yes/No/Don't Care)",
            "Are you skilled at C/C++? (Yes/No/Don't Care)",
        ]
        for i in range(7):
            canvas.create_text(
                385.0,
                initial_y - 34,
                anchor="nw",
                text=questions[i],
                fill="#FFFFFF",
                font=("Karma Medium", 18 * -1),
            )
            canvas.create_image(636.5, initial_y + 15, image=self.input_box)
            input_box = tk.Entry(
                self, bg="#0084FF", fg="#FFFFFF", font=("Karma Medium", 14), bd=0
            )
            input_box.place(x=395.0, y=initial_y, width=481.0, height=35.0)
            self.input_boxes.append(input_box)
            initial_y += 78

        # Filling in the preferences if they exist
        if self.app.preferences:
            for i in range(7):
                self.input_boxes[i].insert(0, self.app.preferences[i])

        # Next Button
        find_jobs_button = tk.Button(
            self,
            image=self.app.images["find_jobs"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.find_jobs_button_command(),
            relief="flat",
        )
        find_jobs_button.place(x=498.0, y=659.0, width=276.0, height=71.0)

        # Packing the canvas
        canvas.pack(fill="both", expand=True)

    def find_jobs_button_command(self):
        """
        Receives the preferences from the entry boxes and converts them to the correct format for tree traversal.
        The function then proceeds to the next page upon clicking the find jobs button with the updated job postings.
        """

        # Update the preferences
        if self.update_preferences():

            # Converting the preferences to the correct format
            new_preferences = []
            for pref in self.app.preferences:
                if pref == "yes":
                    new_preferences.append(0)
                elif pref == "no":
                    new_preferences.append(1)
                else:
                    new_preferences.append(2)

            # Getting Job Postings
            self.app.job_postings = self.app.tree.get_jobs(new_preferences)

            # Creating the job postings
            self.app.show_pages("JobsPage")

    def update_preferences(self) -> bool:
        """
        Updates the preferences of the user from the entry boxes
        """

        # Valid Answers
        valid_answers = ["yes", "no", "don't care", "dont care"]
        temp = []

        # Check if all the input boxes are filled
        for i in range(7):
            preference = self.input_boxes[i].get().lower().strip()

            if preference not in valid_answers:
                messagebox.showerror("Error", "Please enter a valid answer.")
                return False
            else:
                temp.append(preference)

        # Update the preferences
        self.app.preferences = temp

        # Return True if all the input boxes are filled
        return True


##############################################
# Jobs Pages
##############################################


class JobsPage(ttk.Frame):
    """
    Class for the Jobs Page

    Instance Attributes:
    - app: Instance of CareerCompass class representing the application
    """

    app: CareerCompass

    def __init__(self, container_jobs, app):
        super().__init__(container_jobs)

        self.app = app

        # Background
        canvas = tk.Canvas(
            self,
            bg="#0E355D",
            height=750,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        canvas.create_rectangle(0, 0, 270.0, 750, fill="#0084FF", outline="")
        canvas.create_image(133.9, 153.5, image=self.app.images["line"])

        # Title
        canvas.create_text(
            7.0,
            4.0,
            anchor="nw",
            text="Career",
            fill="#0E355D",
            font=("Karma Bold", 64 * -1),
        )
        canvas.create_image(63.0, 107, image=self.app.images["compass_emoji"])
        canvas.create_text(
            7.0,
            58.0,
            anchor="nw",
            text="C  mpass",
            fill="#0E355D",
            font=("Karma Bold", 64 * -1),
        )

        # Home Button
        home_button = tk.Button(
            self,
            image=self.app.images["hbutton"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.app.show_pages("HomePage"),
            relief="flat",
        )
        home_button.place(x=87.0, y=194.0, width=95, height=40.0)

        # Preferences Button
        preferences_button = tk.Button(
            self,
            image=self.app.images["pbutton"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.app.show_pages("PreferencesPage"),
            relief="flat",
        )
        preferences_button.place(x=46.0, y=268.0, width=180, height=40.0)

        # Contact Button
        contact_url = "https://github.com/sherwinokhowat/Internship-Finder"
        contact_button = tk.Button(
            self,
            image=self.app.images["cbutton"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda u=contact_url: webbrowser.open(u),
            relief="flat",
        )
        contact_button.place(x=69.0, y=344.0, width=128.0, height=40.0)

        # Rocket Ship
        canvas.create_image(150.0, 565.0, image=self.app.images["rs_image"])

        # Page Text
        canvas.create_text(
            625.0,
            70.0,
            anchor="center",
            text=f"{self.app.user_name}, find your job!",
            fill="#D6F4FF",
            font=("Karma Bold", 40 * -1),
        )
        canvas.create_text(
            414.0,
            98.0,
            anchor="nw",
            text="Click one of the stars to find similar jobs!",
            fill="#FFFFFF",
            font=("Karma SemiBold", 20 * -1),
        )

        # Load Job Postings
        initial_y = 175
        count = 0
        for job in self.app.job_postings:
            if count == 5:
                break

            count += 1

            # Organizing the title
            job_title = job.job_details["job_title"][:23]
            company = job.job_details["employer_name"][:20]
            if len(job_title) == 23:
                job_title += "..."
            if len(company) == 20:
                company += "..."
            title = job_title + " @ " + company

            # Organizing the description
            desc = self.format_description(job.job_details["fragmented_desc"])

            # Checking if pay period is annual or hourly
            if job.job_details["pay_period"] == "ANNUAL":
                salary = "$" + (str(job.job_details["pay"]) + "/year")
            elif job.job_details["pay_period"] == "MONTHLY":
                salary = "$" + (str(job.job_details["pay"]) + "/month")
            else:
                salary = "$" + (str(job.job_details["pay"]) + "/hour")

            # Checking if city is provided
            if job.job_details["city"] == "":
                location = job.job_details["country"][:50]
            else:
                location = (
                    job.job_details["city"] + ", " + job.job_details["country"]
                )[:50]

            # Organizing Location + Salary
            details = location + " | " + salary

            # Getting Job URL
            job_url = job.job_details["link"]

            # Creating Job Postings
            star = tk.Button(
                self,
                image=self.app.images["star_img"],
                borderwidth=0,
                highlightthickness=0,
                command=lambda temp=job: self.star_button_command(temp),
                relief="flat",
            )
            star.place(x=322.0, y=initial_y, width=44.0, height=44.0)
            url_button = tk.Button(
                self,
                image=self.app.images["URLButton"],
                borderwidth=0,
                highlightthickness=0,
                command=lambda temp=job_url: self.open_url(temp),
                relief="flat",
            )
            url_button.place(x=900.0, y=initial_y - 20, width=15.0, height=83.0)
            canvas.create_image(
                635.0, initial_y + 19, image=self.app.images["job_posting_img"]
            )
            canvas.create_text(
                635.5,
                initial_y - 15,
                anchor="center",
                text=title,
                fill="#FFFFFF",
                font=("Karma Bold", 20 * -1),
            )
            canvas.create_text(
                635.0,
                initial_y + 8,
                anchor="center",
                text=details,
                fill="#0E355D",
                font=("Karma Bold", 18 * -1),
            )
            canvas.create_text(
                635.0,
                initial_y + 40,
                anchor="center",
                text=desc,
                fill="#FFFFFF",
                font=("Karma Light", 15 * -1),
            )

            initial_y += 106

        # Start Over Button
        start_over_button = tk.Button(
            self,
            image=self.app.images["start_over_button_image"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.start_over_button_command(),
            relief="flat",
        )
        start_over_button.place(x=515.0, y=676.0, width=241.0, height=65.0)

        # Packing the canvas
        canvas.pack(fill="both", expand=True)

    def star_button_command(self, job: Job):
        """
        Receives the job from the star button and proceeds to the next page upon clicking the star button
        """

        # Getting similar jobs
        self.app.job_postings = self.app.graph.get_similar_jobs(job)

        # Refreshing Job Page
        self.app.show_pages("JobsPage")

    def open_url(self, url: str):
        """
        Opens the URL in the browser
        """

        webbrowser.open(url)

    def format_description(self, desc: str) -> str:
        """
        Formats the description to fit the job posting
        """

        max_line_length = 77
        words = desc.split()
        lines = []
        current_line = []

        # Split the description into lines
        for word in words:
            if len(" ".join(current_line + [word])) <= max_line_length:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                # Break at 2 lines
                if len(lines) == 2:
                    break

        # Append the last line
        if len(lines) < 2:
            lines.append(" ".join(current_line))

        formatted_description = ""

        # Return the formatted description without the brackets and quotes
        if "..." not in lines[-1]:
            formatted_description = ("\n".join(lines))[2:-2] + "..."
        else:
            formatted_description = ("\n".join(lines))[2:-2]

        return formatted_description

    def start_over_button_command(self):
        """
        Resets the application and proceeds to the home page upon clicking the start over button
        """

        self.app.start_over()
        self.app.show_pages("HomePage")


def main():
    # Create the main window
    root = tk.Tk()
    root.title("CareerCompass")
    root.geometry("1000x750")
    root.resizable(False, False)

    # Create the CareerCompass object
    CareerCompass(root)

    # Run the main loop
    root.mainloop()


# Run the main function
if __name__ == "__main__":
    main()
