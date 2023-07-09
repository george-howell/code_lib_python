#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 13:47:58 2023

@author: ghowell
"""

import numpy as np
import wave, struct


def createToneSig(amp, f, N, fs):
    """
    creates tone signal
    
    :param amp: amplitude
    :param f: tone frequency
    :param N: number of samples
    :param fs: sample rate
    
    :return x: tone signal
    :return t: time vector
    """  
    
    # create time vector
    t = np.arange(0,N) * (1/fs)

    # create signal
    x = amp * np.sin(2*np.pi*f*t)
    
    return x, t

def scaleFloatToInt(x, bitd, sign):
    """
    scales floating point values to signed / unsigned integer values determined
    by bit depth
    
    :param x: input signal
    :param bitd: bit depth
    :param sign: False=unsigned, True=signed
    
    :return y: scaled integer values
    """
    
    # scale to -1, 1 by max value
    x /= np.max(x)
    
    # scale to int
    y = np.floor(x * intmax(bitd, sign))
    
    return y

def scaleIntToFloat(x, bitd, sign):
    """
    Scales integer data to floating points values between -1 and 1. Normalises
    data depending on the bit depth
    
    :param x: input data
    :param bitd: bit depth
    :param sign: False=unsigned, True=signed
    
    :return y: scaled data
    """
    
    return x/intmax(bitd, sign)

def intmax(bitd, sign):
    """
    Find the maximum of an integer
    
    :param bitd: bit depth
    :param sign: False=unsigned, True=signed
    
    :return val: integer maximum value
    """
    
    if (sign):
        val = (2**(bitd-1))-1
    else:
        val = (2**bitd)-1
        
    return val

def writeWavFile(x, filename, nch, bitd, fs):
    """
    creates a .wav file and writes the input data
    
    :param x: input signal as a numpy array
    :param filename: name of file
    :param nch: number of channels
    :param bitd: bit depth (8,16,24,32)
    :param fs: sample rate
    
    :return : n/a
    """    
    
    # open .wav file
    wf = wave.open(filename,'w')
    
    # apply settins
    wf.setnchannels(nch)
    if (bitd % 8):
        raise Exception('bit depth not a multiple of 8')
    sw = int(bitd/8)
    wf.setsampwidth(sw)
    wf.setframerate(fs)
    
    # scale data to integer values
    xint = scaleFloatToInt(x, bitd, True)

    # create .wav file
    for i in range(len(x)):
        xTmp = struct.pack('<h', int(xint[i]))
        wf.writeframesraw(xTmp)
        
    wf.close()

def readWavFiles(filename):
    """
    reads a wav file and scales data to float value between -1 and 1
    
    :param filename: name of file
    
    :return : n/a
    """  
    
    # open .wav file
    wf = wave.open(filename,'r')

    # read data
    N = wf.getnframes()
    x = np.empty(N)
    for i in range(N):
        xTmp = wf.readframes(1)
        x[i] = np.array([struct.unpack('<h', xTmp)])
        
    wf.close()
    
    # scale data to float
    bitd = wf.getsampwidth() * 8;
    y = scaleIntToFloat(x, bitd, True)
    
    return y
        
    