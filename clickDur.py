import tkinter as tk
import time
import tkinter as tk
import time

# Create a class for the Click Speed Tester
class ClickSpeedTester:
    def __init__(self):
        self.root = tk.Tk()  # Create the main Tkinter window
        self.root.title("Click Speed Tester")

        # Variables to track click timing
        self.press_time = None  # When the button is pressed
        self.release_time = None  # When the button is released
        self.last_double_click_time = None  # For double-click interval tracking

        # Create a button for measuring single click length (hold duration)
        self.click_length_button = tk.Button(
            self.root, text="Hold Me", width=10, height=2
        )
        self.click_length_button.pack(pady=20)

        # Create a button for measuring double click interval
        self.double_click_button = tk.Button(
            self.root, text="Double Click Me", width=10, height=2
        )
        self.double_click_button.pack(pady=20)

        # Bind press and release events for measuring click length
        self.click_length_button.bind("<ButtonPress-1>", self.on_press)
        self.click_length_button.bind("<ButtonRelease-1>", self.on_release)

        # Bind double-click events for measuring double click interval
        self.double_click_button.bind("<Double-Button-1>", self.on_double_click)

    def on_press(self, event):
        # Record the press time when the button is clicked
        self.press_time = time.time()

    def on_release(self, event):
        # Record the release time and calculate click length
        if self.press_time:
            self.release_time = time.time()
            click_duration = self.release_time - self.press_time
            self.clickDur.append(round(click_duration,3))
            print(f"Click duration: {click_duration:.4f} seconds")

    def on_double_click(self, event):
        # Record the current time and calculate the double click interval
        current_time = time.time()
        if self.last_double_click_time:
            double_click_interval = current_time - self.last_double_click_time
            print(f"Double click interval: {double_click_interval:.4f} seconds")

        # Update the last double click time
        self.last_double_click_time = current_time

    def run(self):
        self.clickDur = []
        self.root.mainloop()  # Start the Tkinter event loop
        return self.clickDur


# Create an instance of the Click Speed Tester and run it
tester = ClickSpeedTester()
result = tester.run()
import matplotlib.pyplot as plt
plt.hist(result, bins=20)
plt.show()
