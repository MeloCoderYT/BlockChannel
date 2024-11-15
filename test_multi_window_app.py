import tkinter as tk
import pytest

def test_multi_window_app():
    # Create the main window
    main_window = tk.Tk()
    assert main_window is not None, "Main window should be created"

    # Create the second window
    second_window = tk.Toplevel(main_window)
    assert second_window is not None, "Second window should be created"

    # Clean up
    main_window.destroy()
    second_window.destroy()

if __name__ == "__main__":
    pytest.main()
