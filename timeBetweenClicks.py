import tkinter as tk
import time

# Define a class for measuring click intervals
class ClickIntervalTester:

    def __init__(self):
        self.root = tk.Tk()  # Create the main Tkinter window
        self.root.title("Click Interval Tester")

        # Store the last click time for measuring intervals
        self.last_click_time = None

        # Create a button for measuring clicks
        self.click_button = tk.Button(
            self.root, text="Click Me", width=20, height=5, bg="lightblue"
        )
        self.click_button.pack(pady=20)  # Add some padding for spacing

        # Bind the button to capture click events
        self.click_button.bind("<Button-1>", self.on_click)  # Button-1 is the left mouse button

    def on_click(self, event):
        # Get the current time
        current_time = time.time()

        if self.last_click_time is not None:
            # Calculate the interval since the last click
            interval = current_time - self.last_click_time
            print(f"Time between clicks: {interval:.4f} seconds")
            self.intervalDur.append(interval)

        # Update the last click time to the current time
        self.last_click_time = current_time

    def run(self):
        # Start the Tkinter event loop
        self.intervalDur = []
        self.root.mainloop()
        return self.intervalDur


# Create an instance of the Click Interval Tester and run it

tester = ClickIntervalTester()
result = tester.run()
import matplotlib.pyplot as plt
plt.hist(result, bins=20)
plt.show()

