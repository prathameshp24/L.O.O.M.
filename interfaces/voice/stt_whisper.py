import logging
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

print("Loading local whisper AI model into memory... (Takes a few seconds)")

model = WhisperModel("base.en", device="cpu", compute_type="int8")
print("Whisper model loaded")

def listenAndTranscribe(duration: int = 5) -> str:
    """Captures audio using sounddevice and transcribes it using faster whisper"""
    sampleRate = 16000
    print(f"Listening.... (Speak clearly for {duration} seconds)")

    try:
        audio = sd.rec(
            int(duration * sampleRate),
            samplerate=sampleRate,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        print("Transcribing speech locally...")

        audio = np.squeeze(audio)

        segments, info = model.transcribe(audio, beam_size=5)

        fullText = "".join([segment.text for segment in segments]).strip()

        if fullText:
            logging.info(f"Transcribed : {fullText}")
            return fullText
        
        else:
            logging.warning("No speech detected")
            return ""
        
    except Exception as e:
        logging.error(f"Mic or transcription error : {e}")
        return ""
    

if __name__ == "__main__":
    print("testing stt local .....")
    while True:
        try:
            result = listenAndTranscribe(duration=5)
            if result:
                print(f"\nYou said : {result}")
            
            else:
                print("Try again")

        except KeyboardInterrupt:
            print("Exiting voice test....")
            break
        