import tkinter as tk
from tkinter import filedialog
import os

# Debug mode settings
debug_mode = False  
debug_lines = 5   

def read_transcript(file_path):
    transcript = []
    error_count = 0  # Track invalid timestamp errors

    with open(file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
        
        i = 0
        while i < len(lines):
            time = lines[i]

            # Validate timestamp format
            if ":" in time and time.replace(":", "").isdigit():
                text = lines[i+1] if i+1 < len(lines) else ""
                i += 2
                
                # Check if the next line is another line of text (not a timestamp)
                while i < len(lines) and (":" not in lines[i] or not lines[i].replace(":", "").isdigit()):
                    text += " " + lines[i]  # Append extra lines to the same subtitle
                    i += 1
                
                transcript.append((time, text))
            else:
                error_count += 1  # Count errors
                i += 1  # Move to the next line

    # Debug mode: Print sample lines
    if debug_mode:
        print("\n--- Debug Mode Enabled ---")
        print(f"Showing first {debug_lines} lines:")
        for entry in transcript[:debug_lines]:
            print(entry)

    # Display total error count
    print(f"\nTotal invalid timestamp errors: {error_count}")

    return transcript

def convert_to_srt(transcript):
    srt_output = []
    for index, (time, text) in enumerate(transcript, start=1):
        minutes, seconds = map(int, time.split(":"))
        start_time = f"00:{minutes:02}:{seconds:02},000"

        if index < len(transcript):  # If there's a next subtitle
            next_time = transcript[index][0]  # Next line's timestamp
            next_minutes, next_seconds = map(int, next_time.split(":"))
            end_time = f"00:{next_minutes:02}:{next_seconds-1:02},500"  # Adjusting by -500ms
        else:
            end_time = f"00:{minutes:02}:{seconds+2:02},500"  # Default 2-second duration for last line
        
        srt_entry = f"{index}\n{start_time} --> {end_time}\n{text}\n"
        srt_output.append(srt_entry)
    
    return "\n".join(srt_output)

# Initialize GUI for file selection
root = tk.Tk()
root.withdraw()  
file_path = filedialog.askopenfilename(title="Select Transcript File", filetypes=[("Text Files", "*.txt")])

if file_path:
    transcript = read_transcript(file_path)
    srt_format = convert_to_srt(transcript)

    output_file = os.path.join(os.path.dirname(file_path), os.path.basename(file_path).replace(".txt", "_converted.srt"))
    
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(srt_format)
    
    print(f"SRT subtitle file saved as: {output_file}")
else:
    print("No file selected.")