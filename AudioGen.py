import wave
import numpy as np
import struct

class AudioGenerator:
    def __init__(self):
        pass
    
    # Cleans hertz data from having consecutive duplicates
    @classmethod
    def CleanBeforSine(cls, hertzData:list, durationData:list):
        cleanTone = []
        cleanDuration = []
        
        for i in range(len(hertzData)-1):
            if hertzData[i] != hertzData[i+1]:
                cleanTone.append(hertzData[i])
                cleanDuration.append(durationData[i])
            else:
                currentDur = cleanDuration[len(cleanDuration)-1]
                currentDur += durationData[i]
                cleanDuration[len(cleanDuration)-1] = currentDur

        return cleanTone, cleanDuration

    @classmethod
    def SineWave( cls, freq=440, durationMS = 500, phase = 0, sample_rate = 22050.0):
        num_samples = int(durationMS * (sample_rate / 1000))
        audio = []

        for i in range(num_samples):
            audio.insert(i, np.sin(2 * np.pi * freq * (i / sample_rate) + phase))

        phase = (phase + 2 * np.pi * freq * (num_samples / sample_rate)) % (2 * np.pi)
        return audio, phase

    @classmethod
    def SaveAudio(cls, file_name, audio:list, sample_rate = 22050.0, volume = 1):
        wav_file = wave.open(file_name,'w')
        wav_file.setnchannels(1)
        wav_file.setframerate(sample_rate)
        wav_file.setsampwidth(2)
        wav_file.setcomptype("NONE","not compressed")
        volume = 32767.0 * volume
        for i in audio:
            value = float(i) * float(volume)
            wav_file.writeframes(struct.pack('h', int(value)))
        wav_file.close()
        return

    @classmethod
    def Create_Audio(cls, file_name:str, hertz:list, duration:list, sample_rate = 44100.0,):
        hertzData, durationData = cls.CleanBeforSine(hertz,duration)
        audio = []
        sineData = []
        phase = 0
        for i in range(len(hertzData)):
            sineData,phase = cls.SineWave(hertzData[i],durationData[i],phase,sample_rate)
            for i in sineData:
                audio.append(i)
        
        cls.SaveAudio(file_name,audio, sample_rate)