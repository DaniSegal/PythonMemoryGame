from vosk import Model, KaldiRecognizer
from word2number import w2n
import pyaudio
import json
import os


# Initialize the VOSK model
def init_vosk_model():
    MODEL_PATH = '.\\vosk-model-small-en-us-0.15'
    if not os.path.exists(MODEL_PATH):
        print("VOSK model directory not found.")
        exit(1)
    
    return Model(MODEL_PATH)

# Recognize speech and print numbers
def recognize_numbers_from_mic(model):
    sample_rate = 16000
    channel_count = 1
    format = pyaudio.paInt16
    
    recognizer = KaldiRecognizer(model, sample_rate)
    
    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channel_count, rate=sample_rate, input=True, frames_per_buffer=4096)
    stream.start_stream()
    
    

    print("Listening... Speak numbers into the microphone.")
    
    try:
        
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                results = json.loads(recognizer.Result())
                text = results.get("text")
                print(f"you said :{text}")
                parsed_number = parse_number_from_text(text)
                print(f"parsed number is: {parse_number_from_text(text)}")
                if parsed_number != None: 
                    break
                    
                
    except KeyboardInterrupt:
        print("\nStopped listening.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        return parsed_number
        
def parse_number_from_text(text):
    text = text.lower()
    
    number_map = {
        'one': 1, 'won': 1, 'what': 1,
        'two': 2, 'to': 2, 'too': 2, 'tu': 2,
        'three': 3, 'tree': 3, 'free': 3,
        'four': 4, 'for': 4, 'fore': 4,
        'five': 5, 'hive': 5,
        'six': 6, 'sicks': 6, 'sex': 6,
        'seven': 7, 'heaven': 7,
        'eight': 8, 'ate': 8, 'hate': 8,
        'nine': 9, 'nein': 9, 'mine': 9,
        'ten': 10, 'tin': 10, 'then': 10, 'tan': 10,
        'eleven': 11, 'elven': 11, 'elfin': 11,
        'twelve': 12, 'twelf': 12, 'delve': 12,
        'thirteen': 13, 'thirteenth': 13, 'thirtine': 13,
        'fourteen': 14, 'forteen': 14, 'fortin': 14, 'forty': 14,
        'fifteen': 15, 'fifty': 15, 'fitten': 15,
        'sixteen': 16, 'sixtin': 16, 'sicksteen': 16, 'sixty': 16,
    }
    
    
    for word, number in number_map.items():
        if word in text:
            return number
    
    return None
    
if __name__ == "__main__":    
    model = init_vosk_model()
    recognize_numbers_from_mic(model)
