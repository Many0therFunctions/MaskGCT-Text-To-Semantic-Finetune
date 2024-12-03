import os
import random
#using second gpu. if you only have one set it to 0
from transformers import pipeline, WhisperProcessor, WhisperForConditionalGeneration, Wav2Vec2FeatureExtractor, HubertModel

import argparse

parser = argparse.ArgumentParser(description="Transcribe audio files to train.txt")
parser.add_argument('--WavFolder', type=str, required=True, help='Name of the speaker')

args = parser.parse_args()


whisperPath = "./whisper-large-v3-turbo"
#whisperPath = "./whisper-large-v3"
whispermodel = WhisperForConditionalGeneration.from_pretrained(whisperPath)
whisperProcessor = WhisperProcessor.from_pretrained(whisperPath)
pipe = pipeline(
    "automatic-speech-recognition",
    model=whispermodel,
    config=whispermodel.config,
    #processor=whisperProcessor,
    tokenizer=whisperProcessor.tokenizer,
    feature_extractor=whisperProcessor.feature_extractor,
    chunk_length_s=30,
    device="cuda",
)


def add_to_textfile(file_path, text):
    with open(file_path, "a") as text_file:
        text_file.write(text)

wavDir = args.WavFolder
print("goddamn wav dir ", wavDir)

open(f"{wavDir}/train.txt", "w").close()

transcribed_lines = []
wavDirectory = wavDir

# Loop through all files in the directory
for file in os.listdir(wavDirectory):
    try:
        filepath = wavDirectory + "/" + file
        #print(filepath)
        
        output = pipe(
            str(filepath),
            chunk_length_s=30,
            batch_size=128,
            generate_kwargs={"task": "transcribe"},
            return_timestamps=True,
        )
        
        text = output["text"].strip()
        duration = output['chunks'][-1]['timestamp'][1]

        # commented out because we were being stupid and fell victim to the 
        # "when all you have is a hammer, everything looks like a nail" effect. Yeah. Happens to the best of us.
        # The above way of doing things ended up being unecessarily complicated, but is it really worth the time
        # To go changing the code to give the appearance of being competent and on top of things in your life?
        # Nah. This is not an essential part to optimize performance. Let it stand as a legacy and reminder
        # Of that most fatal force of nature: human error.
        #transcribed_lines.append(f"{wavDirectory}/{file}|{text}|{duration}\n")
        transcribed_lines.append(f"{wavDirectory}/{file}|{text}\n")
    except:
        print(f"fucked up on file {file}")

#random.shuffle(transcribed_lines)

# Calculate the number of lines for valid.txt (10%)
#num_valid_lines = int(len(transcribed_lines) * 0.1)

# Split the transcribed lines into valid and train
#valid_lines = transcribed_lines[:num_valid_lines]
#train_lines = transcribed_lines[num_valid_lines:]


# Write the lines to the respective files
for line in transcribed_lines:
    add_to_textfile(f"{wavDir}/train.txt", line)

#for line in train_lines:
#    add_to_textfile("./datasets/OzenProcessed/train.txt", line)

