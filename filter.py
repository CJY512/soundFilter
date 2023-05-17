from scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import os
import librosa

#그래프를 그려줄 함수
def show_plot(files):
    #3행 2열로 구간 나눔
    fig, axes = plt.subplots(3,2)
    #현재 경로
    path = os.getcwd()
    
    for idx, file in enumerate(files) :
        full_path = path + '\\data\\' + file
        wav = full_path # Original file
        
        sample_rate, data = wavfile.read(wav) # sample_rate : sampling rate, data : wave data array
        #위 wavfile.read() 대신 아래의 librosa.load()를 사용하면 정상적인 그래프 출력
        #data, sample_rate = librosa.load(wav, sr=None)
        
        #시간축
        time = np.linspace(0, len(data)/sample_rate, len(data))
        
        #시간, 진폭 그래프
        axes[idx][0].plot(time, data)
        axes[idx][0].set_ylabel("Amplitude")
        axes[idx][0].set_xlabel("Time[s]")
        axes[idx][0].set_title(file)
        
        #고속 푸리에 변환
        fft = np.fft.fft(data)
        #변환 배열 절댓값
        magnitude = np.abs(fft) 

        f = np.linspace(0, sample_rate, len(magnitude))
        #진폭
        left_spectrum = magnitude[:int(len(magnitude)/2)]
        #주파수
        left_f = f[:int(len(magnitude)/2)]

        axes[idx][1].plot(left_f, left_spectrum)
        axes[idx][1].set_xlabel("Frequency")
        axes[idx][1].set_ylabel("Magnitude")
        axes[idx][1].set_title(file)
    
    plt.tight_layout()
    plt.show()

#high pass filter func
def highpass_filter(data, high, fs, order):
    b = signal.firwin(order, cutoff=high, fs=fs , pass_zero='highpass')
    y = signal.lfilter(b, [1.0], data)
    return y

#low pass filter func
def lowpass_filter(data, low, fs, order):
    b = signal.firwin(order, cutoff=low, fs=fs , pass_zero='lowpass')
    y = signal.lfilter(b, [1.0], data)
    return y

#humtest.wav파일에 적용
def hum():
    full_path = r'.\data\humtest.wav'
    wav = full_path # Original file
    sample_rate, data = wavfile.read(wav) #sample_rate : sampling rate, data : wave data array
    
    # humtest.wav 800Hz highpass filter를 적용
    hum_filtered_data = highpass_filter(data, 800 , sample_rate, 101)
    #저장할 파일 이름
    hum_filtered_file = r'.\result\humtest_clean.wav'
    #파일 저장
    wavfile.write(hum_filtered_file, sample_rate, hum_filtered_data.astype(np.int16))
    
#electest.wav파일에 적용
def elec():
    full_path = r'.\data\electest.wav'
    wav = full_path # Original file
    sample_rate, data = wavfile.read(wav) # sample_rate : sampling rate, data : wave data array
    
    # electest.wav에 3000 lowpass filter를 적용
    elec_filtered_data = lowpass_filter(data, 3000 , sample_rate, 101)
    #저장할 파일 이름
    elec_filtered_file = r'.\result\electest_clean.wav'
    #소리가 너무 작아서 amplitude 10000배
    elec_filtered_data *= 10000
    #파일 저장
    wavfile.write(elec_filtered_file, sample_rate, elec_filtered_data.astype(np.int16))

# MSE 계산 함수
def calc_mse(file):
    original_data, sample_rate_original = librosa.load('data\\test.wav', sr=None)
    modified_data, sample_rate_hum = librosa.load(file, sr=None)

    mse = np.mean((original_data - modified_data) ** 2)
 
    return mse

# Original files
files = ['test.wav', 'humtest.wav', 'electest.wav']
show_plot(files)

hum()
elec()

print("Mean Square Error between humtest_clean and test: ", calc_mse('result\humfilter.wav'))
print("Mean Square Error between electest_clean and test: ", calc_mse('result\elecfilter2.wav'))