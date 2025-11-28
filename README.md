## Installation

#check that you have ollama client downloaded and opened, and that the chatmodel specified in code is downloaded and available on pc.

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`

## Usage

1. Place your CV file yaml file in the `input_files` folder, named `CV_data.yaml`, keys describe what data goes where. (job experience text and skills text)
2. Add the job description to `job_application_text.txt` in the input_files folder.
3. Run the program: `python cv_tailorer.py`

The program will generate a tailored CV based on the job description, to the location of `output_files` inside a the folder that is named after the company name taken from job application text.

CAUTION! If the filepath already exist, it will overwrite!
