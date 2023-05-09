from scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import os

#그래프를 그려줄 함수
def show_plot(files):
    #3행 2열로 구간 나눔
    fig, axes = plt.subplots(3,2)
    #현재 경로
    path = os.getcwd()
    
    for idx, file in enumerate(files) :
        full_path = path + '\\data\\' + file
        wav = full_path # Original file
        # (file_dir, file_id) = os.path.split(wav)

        # print("Path : ", file_dir)
        # print("Name : ", file_id)

        sample_rate, data = wavfile.read(wav) # sr : sampling rate, x : wave data array

        # print("Sample rate:{0}, data size:{1}, duration:{2} seconds".format(sample_rate,data.shape,len(data)/sample_rate))

        time = np.linspace(0, len(data)/sample_rate, len(data))
        
        # axes[idx].figure(figsize=(20,10))
        axes[idx][0].plot(time, data)
        axes[idx][0].set_ylabel("Amplitude")
        axes[idx][0].set_xlabel("Time[s]")
        axes[idx][0].set_title(file)
        
        fft = np.fft.fft(data)

        magnitude = np.abs(fft) 

        f = np.linspace(0, sample_rate, len(magnitude))
        left_spectrum = magnitude[:int(len(magnitude)/2)]
        left_f = f[:int(len(magnitude)/2)]

        axes[idx][1].plot(left_f, left_spectrum)
        axes[idx][1].set_xlabel("Frequency")
        axes[idx][1].set_ylabel("Magnitude")
        axes[idx][1].set_title(file)
    
    plt.tight_layout()
    plt.show()

files = ['test.wav', 'humtest.wav', 'electest.wav']
show_plot(files)

def highpass_filter(data, high, fs, order):
    b = signal.firwin(order, cutoff=high, fs=fs , pass_zero='highpass')
    y = signal.lfilter(b, [1.0], data)
    return y

def lowpass_filter(data, low, fs, order):
    b = signal.firwin(order, cutoff=low, fs=fs , pass_zero='lowpass')
    y = signal.lfilter(b, [1.0], data)
    return y

def hum():
    full_path = r'.\data\humtest.wav'
    wav = full_path # Original file
    sample_rate, data = wavfile.read(wav) # sr : sampling rate, x : wave data array
    
    hum_filtered_data = highpass_filter(data, 800 , sample_rate, 101)
    hum_filtered_data2 = lowpass_filter(data, 0.000001 , sample_rate, 101)
    hum_filtered_file = r'.\result\humfilter.wav'
    hum_filtered_file2 = r'.\result\humfilter2.wav'
    wavfile.write(hum_filtered_file, sample_rate, hum_filtered_data.astype(np.int16))
    wavfile.write(hum_filtered_file2, sample_rate, hum_filtered_data2.astype(np.int16))
    
hum()

# highpass filter를 사용하면 removing hum이 어느 정도 가능하다.
# 참고 https://github.com/hyorea1/wavFile_preprocessing/blob/main/waveFilter.ipynb
#       https://eclipse360.tistory.com/114
#       https://coding-yoon.tistory.com/23

# electest는 어떻게 없애야 하나

def elec():
    full_path = r'.\data\electest.wav'
    wav = full_path # Original file
    sample_rate, data = wavfile.read(wav) # sr : sampling rate, x : wave data array
    
    elec_filtered_data = highpass_filter(data, 7000 , sample_rate, 101)
    elec_filtered_data2 = lowpass_filter(data, 3000 , sample_rate, 101)
    elec_filtered_file = r'.\result\elecfilter.wav'
    elec_filtered_file2 = r'.\result\elecfilter2.wav'
    elec_filtered_data *= 10000
    elec_filtered_data2 *= 10000
    wavfile.write(elec_filtered_file, sample_rate, elec_filtered_data.astype(np.int16))
    wavfile.write(elec_filtered_file2, sample_rate, elec_filtered_data2.astype(np.int16))
    #소리가 너무 작아서 amplitude 10000배
    data *= 10000
    wavfile.write(r'.\eleczz.wav',sample_rate,data.astype(np.int16))
    
elec()