**GameBot AI Project**
This repository contains the code and assets for the GameBot AI project (Spring 2025). The GameBot uses a trained Random Forest model to play Street Fighter II (SNES) via the BizHawk (EmuHawk) emulator. Below you will find instructions for setting up your environment, reproducing the training experiments, running the GameBot, and evaluating its performance.

**Table of Contents**
1.	Prerequisites
2.	Environment Setup
3.	Training the Model
4.	Running the GameBot
5.	Evaluating Model Performance

**Prerequisites**
•	Operating System: Windows 10 or later (64 bit)
•	Python: 3.9 or above
•	BizHawk / EmuHawk: Emulator for SNES games
•	Street Fighter II Turbo (U).smc: ROM file placed in the single-player and two-players folders

**Environment Setup**
1.	Install Python 3.9+
o	Download and install from python.org.
o	Make sure to add Python to your PATH.
2.	Clone this repository
3.	git clone <your-repo-url>
4.	cd gamebot-competition-master/PythonAPI
5.	Create and activate a virtual environment (optional but recommended)
6.	python -m venv venv
7.	venv\Scripts\activate     # on Windows
8.	source venv/bin/activate   # on Linux/macOS
9.	Install Python dependencies
10.	pip install --upgrade pip

**Training the Model**
Location: PythonAPI/train_model.py
1.	Ensure training_data.csv is in the PythonAPI folder.
2.	Open a terminal in the PythonAPI directory.
3.	Run the training script:
4.	python train_model.py
5.	The script will:
o	Read training_data.csv
o	Encode fight_result into integers
o	Split data into train/validation sets
o	Scale features with StandardScaler
o	Train a smaller, shallower RandomForestClassifier wrapped by MultiOutputClassifier
o	Print validation accuracy
o	Save scaler.pkl and bot_model.pkl

**Running the GameBot**
Location: PythonAPI/controller.py
1.	Launch the BizHawk (EmuHawk) emulator.
2.	Single-player mode (Bot vs CPU):
o	Open the single-player folder in the emulator (File → Open ROM).
o	Select Street Fighter II Turbo (U).smc.
o	In a terminal, run:
o	cd PythonAPI
o	python controller.py 1
3.	Two-player mode (Bot vs Bot):
o	Open the two-players folder in the emulator.
o	Launch VS Battle and pick two characters.
o	In one terminal:
o	cd PythonAPI
o	python controller.py 1
o	In another terminal:
o	cd PythonAPI
o	python controller.py 2
4.	Human vs Bot
o	Map your keyboard or gamepad to Player 2 in the emulator’s Controllers options.
o	Run only:
o	python controller.py 1
Your bot will connect (“Connected to game!”) and begin playing.

**Evaluating Model Performance**
Location: PythonAPI/evaluate_model.py
1.	Make sure scaler.pkl, bot_model.pkl, and training_data.csv are present.
2.	Run the evaluation script:
3.	python evaluate_model.py
4.	The script reports:
o	Exact‐match accuracy (all 12 buttons correct)
o	Hamming loss (per‐button error)
o	Per‐button accuracy breakdown
Use these metrics to verify your model before deploying.
