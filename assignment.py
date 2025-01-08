import pandas as pd
import json

def apply_instruction(df, instruction):
    """Apply the parsed instruction to the DataFrame."""
    if "find duplicates" in instruction.lower():
        if "in column" in instruction.lower():
            column = instruction.split("in column")[-1].strip()
            if column in df.columns:
                df = df.drop_duplicates(subset=[column])
            else:
                raise ValueError(f"Column '{column}' not found in the DataFrame.")
        else:
            default_column = df.columns[0]
            df = df.drop_duplicates(subset=[default_column])
    elif "display numbers" in instruction.lower():
        rule = instruction.split(":")[-1].strip()
        column = df.columns[0] 
        df["Modified Column"] = df[column].apply(lambda x: eval(rule))
    elif "add row" in instruction.lower():
        row = instruction.split(":")[-1].strip().split(",")
        if len(row) != len(df.columns):
            raise ValueError(
                f"Cannot add row. Provided {len(row)} values, but DataFrame has {len(df.columns)} columns."
            )
        df.loc[len(df)] = row
    elif "delete row" in instruction.lower():
        row_index = int(instruction.split(":")[-1].strip())
        if row_index not in df.index:
            raise KeyError(f"Row index {row_index} not found in the DataFrame.")
        df = df.drop(row_index)
    return df

def log_progress(logs, step, instruction, before, after):
    """Log the modification progress."""
    logs.append({
        "step": step,
        "instruction": instruction,
        "before": before.to_dict(),
        "after": after.to_dict()
    })

def modify_excel_data(input_file, output_file):
    logs = []
    df = pd.read_csv(input_file)
    print("Detected Columns:", df.columns.tolist())
    
    step = 1
    while True:
        instruction = input("Enter an instruction (or type 'exit' to finish): ").strip()
        if instruction.lower() == "exit":
            break
        
        before_df = df.copy()
        try:
            df = apply_instruction(df, instruction)
        except (ValueError, KeyError) as e:
            print(f"Error: {e}")
            continue
        
        log_progress(logs, step, instruction, before_df, df)
        step += 1
    
    df.to_csv(output_file, index=False)
    
    with open("progress_log.json", "w") as log_file:
        json.dump(logs, log_file, indent=4)
    
    print(f"Modified file saved at: {output_file}")
    print("Modification progress has been logged in 'progress_log.json'.")

input_file = "input.csv"   
output_file = "output.csv" 
modify_excel_data(input_file, output_file)
