# Student AI Usage Dashboard
### A global survey analysis on how higher education students perceive and use generative AI

## Project Description
This project was created as part of the Data Visualization course. [cite_start]It is an interactive dashboard developed with Streamlit that explores data from the "Global ChatGPT Student Survey" conducted by the Faculty of Public Administration, University of Ljubljana, alongside international partners[cite: 55, 56].

* **Topic:** The dashboard visualizes how higher education students globally perceive and use generative AI tools like ChatGPT. It explores usage patterns, capabilities, and ethical concerns.
* **Social Impact:** The exponential growth of AI tools makes it crucial to understand their impact on higher education. This project sheds light on how diverse student populations view AI, addressing important questions about its role in learning outcomes, potential ethical issues (like cheating or plagiarism), and its broader societal implications regarding the labor market and skills mismatch.
* **Target Audience:** University students.

## Project Structure
The repository contains the following files necessary for the tool to run properly:
* `app.py`: The main file for the Streamlit application (home page).
* `pages/`: Directory containing the sub-pages of the application (User Profile, Usage Cases, Ethics).
* `data/`: Directory containing the datasets used for the visualizations (source files).
* `requirements.txt`: List of Python libraries required to run the application.

## How to Run the Application Locally

Here are the instructions to run the source code on your machine:

**1. Prerequisites**
Make sure you have Python installed on your computer.

**2. Navigate to the Project**
Navigate to the main project directory (the one containing the `app.py` file) using your terminal.

**3. Install Dependencies**
It is recommended to install the required libraries using pip:
```bash
pip install -r requirements.txt
```

**4. Start Streamlit**
Launch the web application by typing the following command in your terminal:
```bash
streamlit run app.py
```

Additional Notes
Data: The data used in this project originates from the "Global ChatGPT Student Survey". The original survey stated that collected data would only be disseminated in aggregate form for research purposes. Please ensure that any data shared in this repository complies with the original researchers' terms of use.