
import os
from datetime import datetime
import pandas as pd


def create_output_dir():
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def save_to_csv(data):
    create_output_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', f"data_{timestamp}.csv")

    if isinstance(data, dict):
        df = pd.DataFrame(list(data.items()), columns=["Field", "Value"])
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Data saved to {filename}")
    else:
        print("No valid data to save.")

def save_to_txt(extracted_text):
    create_output_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', f"data_{timestamp}.txt")

    if extracted_text:
        try:
            with open(filename, mode="w", encoding="utf-8") as file:
                file.write(extracted_text.strip().encode("utf-8").decode("utf-8"))
            print(f"Data successfully saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")
    else:
        print("No valid data to save.")

