import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataVisualization:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        self.directory = StringVar()

        title_lbl = Label(self.root, text="DATA VISUALIZATION SECTION", font=("times new roman", 35, "bold"),
                          bg="green", fg="white")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        main_frame = Frame(self.root, bd=3, bg="white")
        main_frame.place(x=10, y=50, width=1500, height=730)

        # Left frame for file selection
        Left_frame = LabelFrame(main_frame, bd=3, bg="white", relief=RIDGE, text="File Selection",
                                font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=10, width=350, height=710)

        btn_select_directory = Button(Left_frame, text="Select Directory", command=self.select_directory, width=20,
                                      font=("times new roman", 14, "bold"), bg="green", fg="white")
        btn_select_directory.place(x=75, y=200, width=200, height=40)

        self.directory_label = Label(Left_frame, textvariable=self.directory, font=("times new roman", 14), bg="white",
                                     fg="black", relief=RIDGE)
        self.directory_label.place(x=10, y=260, width=320, height=40)

        btn_combine_visualize = Button(Left_frame, text="Combine and Visualize", command=self.combine_and_visualize,
                                       width=20, font=("times new roman", 14, "bold"), bg="green", fg="white")
        btn_combine_visualize.place(x=75, y=320, width=200, height=40)

        # Right frame for visualizations
        Right_frame = LabelFrame(main_frame, bd=3, bg="white", relief=RIDGE, text="Visualizations",
                                 font=("times new roman", 12, "bold"))
        Right_frame.place(x=370, y=10, width=1120, height=710)

        # Adding a canvas and scrollbar to Right_frame
        self.canvas = Canvas(Right_frame)
        self.scrollbar = Scrollbar(Right_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=LEFT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

    def select_directory(self):
        dir_path = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Directory")
        if dir_path:
            self.directory.set(dir_path)

    def combine_and_visualize(self):
        if not self.directory.get():
            messagebox.showerror("Error", "Please select a directory first")
            return

        try:
            # Combine CSV files
            df_list = []
            for filename in os.listdir(self.directory.get()):
                if filename.endswith('.csv'):
                    file_path = os.path.join(self.directory.get(), filename)
                    df = pd.read_csv(file_path)
                    df.columns = df.columns.str.strip().str.lower()  # Standardize column names to lowercase
                    df['date'] = df['date'].replace('N/A', pd.NaT)  # Replace 'N/A' with NaT (Not a Time)
                    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')  # Parse dates
                    df_list.append(df)
            combined_df = pd.concat(df_list, ignore_index=True)

            # Check for required columns
            required_columns = ['status', 'date', 'department']
            missing_columns = [col for col in required_columns if col not in combined_df.columns]
            if missing_columns:
                messagebox.showerror("Error", f"Missing columns: {', '.join(missing_columns)}")
                return

            # Visualize data
            self.visualize_data(combined_df)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize_data(self, df):
        # Clear previous visualizations
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Check for 'status' column
        if 'status' not in df.columns:
            messagebox.showerror("Error", "'status' column is missing in the data")
            return

        # Plot a histogram of status
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        df['status'].value_counts().plot(kind='bar', ax=ax1)
        ax1.set_title('Status Distribution')
        ax1.set_xlabel('Status')
        ax1.set_ylabel('Count')

        canvas1 = FigureCanvasTkAgg(fig1, self.scrollable_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

        # Plot status over time
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        df.groupby('date')['status'].value_counts().unstack().plot(kind='line', ax=ax2)
        ax2.set_title('Status Over Time')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Count')
        ax2.legend(title='Status')

        canvas2 = FigureCanvasTkAgg(fig2, self.scrollable_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

        # Plot status by department
        fig3, ax3 = plt.subplots(figsize=(8, 6))
        df.groupby('department')['status'].value_counts().unstack().plot(kind='bar', stacked=True, ax=ax3)
        ax3.set_title('Status by Department')
        ax3.set_xlabel('Department')
        ax3.set_ylabel('Count')

        canvas3 = FigureCanvasTkAgg(fig3, self.scrollable_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

        fig4, ax4 = plt.subplots(figsize=(8, 6))
        df['day_of_week'] = df['date'].dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df['day_of_week'] = pd.Categorical(df['day_of_week'], categories=day_order, ordered=True)
        df_day = df.dropna(subset=['day_of_week', 'status'])
        df_day.groupby('day_of_week')['status'].value_counts(normalize=True).unstack().plot(kind='bar', stacked=True,
                                                                                            ax=ax4)
        ax4.set_title('Attendance Status by Day of Week')
        ax4.set_xlabel('Day of Week')
        ax4.set_ylabel('Proportion')
        ax4.legend(title='Status')

        canvas4 = FigureCanvasTkAgg(fig4, self.scrollable_frame)
        canvas4.draw()
        canvas4.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

        # Correlation analysis (apply to numerical data if available)
        # Correlation analysis
        fig4, ax4 = plt.subplots(figsize=(8, 6))

        # Assuming column 1 is ID and column 4 is department
        id_column = df.iloc[:, 0]  # First column (index 0) for ID
        department_column = df.iloc[:, 3]  # Fourth column (index 3) for department

        # Create a new dataframe with ID and department
        correlation_df = pd.DataFrame({'ID': id_column, 'Department': department_column})

        # Convert department to numeric if it's categorical
        if correlation_df['Department'].dtype == 'object':
            correlation_df['Department'] = pd.Categorical(correlation_df['Department']).codes

        # Calculate correlation
        correlation_matrix = correlation_df.corr()

        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax4)
        ax4.set_title('Correlation between ID and Department')

        canvas4 = FigureCanvasTkAgg(fig4, self.scrollable_frame)
        canvas4.draw()
        canvas4.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)


if __name__ == "__main__":
    root = Tk()
    obj = DataVisualization(root)
    root.mainloop()
