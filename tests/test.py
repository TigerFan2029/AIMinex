import unittest
import mineralAI
from threading import Thread
import time

class TestMainGUI(unittest.TestCase):
    
    def test_gui_startup(self):
        """Test to check if the GUI starts without errors."""
        def run_gui():
            try:
                mineralAI.main()  # Start the GUI
            except Exception as e:
                self.fail(f"GUI failed to start with error: {e}")
        
        # Start the GUI in a separate thread to avoid blocking
        gui_thread = Thread(target=run_gui)
        gui_thread.start()

        # Allow the GUI to run for a short time and check for errors
        time.sleep(2)  # Let the GUI run for 2 seconds

        # Terminate the test if the GUI thread is alive (this simulates closing the GUI)
        if gui_thread.is_alive():
            print("pass")  # If the GUI is running without issues, print "pass"
        
        gui_thread.join(timeout=1)  # Close the thread

if __name__ == "__main__":
    unittest.main()