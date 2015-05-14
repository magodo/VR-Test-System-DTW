#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Wed 22 Apr 2015 03:41:17 PM CST
# File Name: main.py
# Description:
#########################################################################

import os
import waveio
from mfcc import mfcc
from dtw import dtw
from time import time

voice_dir = "voiceMaterial"
templates = ["strawberry", "apple", "beef", "egg", "lemon", "mushroom", "noodle", "orange", "spaghetti", "spam", "watermelon"]
test = "mushroom"

# Get MFCC for each template, using the 1st sample of them
print "Get MFCC for each template, begin..."
template_feature = {}
for template in templates:
    template_feature[template] = mfcc(signal = waveio.wave_from_file(os.path.join(voice_dir, template+"1.wav"))[0], fs = waveio.wave_from_file(os.path.join(voice_dir, template+"1.wav"))[1])
print "Get MFCC for each template, finish."

overhead = {}
score = {}

def compare(arg, dirname, fnames):
    for fname in fnames:
        if test in fname:
            # Get MFCC for each test sample
            test_features = mfcc(signal = waveio.wave_from_file(os.path.join(dirname, fname))[0], fs = waveio.wave_from_file(os.path.join(dirname, fname))[1])
            # Record overhead and score for each test sample versus each template.(Each sample is of a dict corresponding to each template)
            overhead[fname]= {}
            score[fname] = {}
            for template in template_feature.keys():
                time_start = time()
                score[fname][template] = dtw(template_feature[template], test_features)
                overhead[fname][template] = time() - time_start

os.path.walk(voice_dir, compare, None)

for test in score:
    print "----------------------------------------"
    print u"测试模板: %s"%test
    print "----------------------------------------"
    for template in score[test]:
        print u"模板: %10s  匹配度: %15.2f  耗时: %8.2f (秒)"%(template, score[test][template], overhead[test][template])
    print u"匹配结果: %10s"%(min(score[test], key = lambda x: score[test][x]))


