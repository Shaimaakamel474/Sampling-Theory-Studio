# Sampling-Theory Studio

## Overview
The Sampling-Theory Studio is a desktop application designed to illustrate the concepts of signal sampling and recovery, emphasizing the importance of the Nyquist–Shannon sampling theorem. It allows users to explore how different sampling frequencies affect the ability to reconstruct signals accurately.

## Features
- *Sample & Recover:*
  - Load a mid-length signal (~1000 points) and visualize it.
  - Sample the signal at different frequencies.
  - Recover the original signal using Whittaker–Shannon interpolation.
  - Display sampling frequency in both actual and normalized forms.
- *Graphical Visualization:*
  - Original signal with sampled points.
  - Reconstructed signal.
  - Difference between the original and reconstructed signal.
  - Frequency domain representation to inspect aliasing.
- *Load & Compose:*
  - Load a signal from a file or create a custom mixed signal using multiple sinusoidal components.
  - Add and remove components with control over frequency and magnitude.
- *Additive Noise:*
  - Add controllable noise with adjustable SNR to observe frequency impact.
- *Real-Time Processing:*
  - Sampling and recovery updates occur in real-time with user adjustments.
- *Multiple Reconstruction Methods:*
  - Explore different reconstruction methods via a combobox selection.
- *Resizable UI:*
  - The application layout adjusts dynamically with window resizing.

## Test Scenarios
- *Scenario 1:* Mix of 2Hz and 6Hz sinusoidal signals, sampled at 12Hz and 4Hz to demonstrate proper reconstruction and aliasing.
- *Scenario 2:* Custom signal showing a case where higher sampling rates fail due to complex noise.
- *Scenario 3:* Mix of varying frequencies illustrating reconstruction limits.

## Code Design Principles
- *Object-Oriented Programming (OOP):*
  - Encapsulation and minimal code in the main function.
  - Separate classes for signal handling, visualization, and interaction.
- *Logging:*
  - Use of Python's logging library to track key interactions and debug issues.

## Requirements
- Python 3.x
- Required libraries: matplotlib, numpy, logging

## Getting Started
1. Clone the repository:
   bash
   git clone <repository_url>
   
2. Navigate to the project directory:
   bash
   cd sampling-theory-studio
   
3. Install dependencies:
   bash
   pip install -r requirements.txt
   
4. Run the application:
   bash
   python main.py
   

## Usage
- Load or compose a signal.
- Adjust sampling rates and observe results.
- Experiment with different reconstruction methods.
- Test predefined scenarios.

## File Structure
- main.py: Entry point for the application.
- signal_handler.py: Manages signal operations.
- visualizer.py: Handles graphical output.
- scenarios.py: Contains predefined test cases.
- ui_layout.ui: UI definition file.
- logs/: Stores log files for debugging.

## Contributors        

 [Mohamed Salah](https://github.com/MuhamedSalah10),
 [Mohamed Abdelhamid](https://github.com/mohamed5841), 
 [Shaimaa Kamel](https://github.com/Shaimaakamel474),
 [Bassant Rabie](https://github.com/bassantrabie),
 [Malak Emad](https://github.com/malak-emad) 


## Acknowledgments
Inspired by foundational concepts in digital signal processing and the Nyquist–Shannon sampling theorem.
