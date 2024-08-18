# TextPreprocessing

This script preprocesses text data by removing punctuation and special characters based on language-specific Unicode ranges. It supports multiple languages and can be customized using a YAML configuration file.

## Usage

### 1. Install Dependencies

Ensure you have Python installed on your system. Install the required Python packages listed in `requirements.txt` using pip:

```bash
conda create --name <env_name> python=3.7
```
```bash
pip install -r requirements.txt
```
(or)

```bash
pip install numpy pandas
pip install num2words
pip install PyYAML
pip install google-transliteration-api
```
### 2. Prepare Input Data
  Prepare your input text data in a text file. Each line in the file represents a piece of text to be processed. If you have tab-separated files with text data and IDs, ensure that the text is in the second column.
### 3. Update YAML Configuration
   Update the YAML configuration file (config.yaml) to specify Unicode ranges and punctuation rules for each supported language. See the provided config.yaml for an example.
   ```bash
        unicode_ranges:
          ar: 
            - '\u0621-\u0629\u062A-\u062D\u062E\u062F\u0630-\u0638\u063A\u0641-\u064A\u064B-\u0652\u0660-\u0669'
          ur: 
            - '\u0621-\u0642\u0644-\u0648\u066B\u066C\u0679\u067E\u0686\u0688\u0691\u0698\u06A9\u06AF\u06BE\u06C1\u06CC\u06D2'
          fa: 
            - '\u0621-\u0629\u062A-\u062D\u062E-\u062F\u0630-\u0652\u0654\u067E\u0686\u0698\u06A9\u06AF\u06CC'
          {lang}: 
            - unicoderange for particular language
            
   ```
### 4. Run the Script
  Execute the script from the command line, providing the input file, output file, and YAML configuration file paths as arguments. Optionally, you can specify a log file path to save log messages.
   ```bash 
        python Text_preprocess.py <input_file.txt> <output_file.txt> <path_to_config> <lang>
  ```
    input_file.txt: Path to the input text file.
    output_file.txt: Path to the output file where preprocessed text will be saved.
    config.yaml: Path to the YAML configuration file.
    lang: Language code of the text
   
## Configuration
  The YAML configuration file (config.yaml) contains Unicode ranges and punctuation rules for each supported language. You can customize these ranges and rules according to your requirements.

## Logging
The script logs information, warnings, and errors during execution. If a log file path is provided, log messages will be saved to that file. Otherwise, logs will be printed to the console.

```bash
  python Text_preprocess.py <input_file.txt> <output_file.txt> <path_to_config> <lang> > log_file.txt
```
