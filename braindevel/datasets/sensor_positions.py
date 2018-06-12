import numpy as np
import re
import csv
import h5py
    
cap_positions = \
    [['EOG_H',[],'Sync',[],[],[],[],[],'Fp1',[],'FPz',[],'Fp2',[],[],[],[],[],[],[],'EOG_V'],\
    [[],[],[],[],[],[],[],'AFp3h',[],[],[],[],[],'Afp4h',[],[],[],[],[],[],[]],\
    [[],[],'AF7',[],[],[],'AF3',[],[],[],'AFz',[],[],[],'AF4',[],[],[],'AF8',[],[]],\
    [[],[],[],[],[],'AFF5h',[],[],[],'AFF1',[],'AFF2',[],[],[],'AFF6h',[],[],[],[],[]],\
    [[],[],'F7',[],'F5',[],'F3',[],'F1',[],'Fz',[],'F2',[],'F4',[],'F6',[],'F8',[],[]],\
    [[],'FFT9h',[],'FFT7h',[],'FFC5h',[],'FFC3h',[],'FFC1h',[],'FFC2h',[],'FFC4h',[],'FFC6h',[],'FFT8h',[],'FFT10h',[]],\
    ['FT9',[],'FT7',[],'FC5',[],'FC3',[],'FC1',[],'FCz',[],'FC2',[],'FC4',[],'FC6',[],'FT8',[],'FT10'],\
    [[],'FTT9h',[],'FTT7h',[],'FCC5h',[],'FCC3h',[],'FCC1h',[],'FCC2h',[],'FCC4h',[],'FCC6h',[],'FTT8h',[],'FTT10h',[]],\
    ['M1',[],'T7',[],'C5',[],'C3',[],'C1',[],'Cz',[],'C2',[],'C4',[],'C6',[],'T8',[],'M2'],\
    [[],[],[],'TTP7h',[],'CCP5h',[],'CCP3h',[],'CCP1h',[],'CCP2h',[],'CCP4h',[],'CCP6h',[],'TTP8h',[],[],[]],\
    [[],[],'TP7',[],'CP5',[],'CP3',[],'CP1',[],'CPz',[],'CP2',[],'CP4',[],'CP6',[],'TP8',[],[]],\
    [[],'TPP9h',[],'TPP7h',[],'CPP5h',[],'CPP3h',[],'CPP1h',[],'CPP2h',[],'CPP4h',[],'CPP6h',[],'TPP8h',[],'TPP10h',[]],\
    ['P9',[],'P7',[],'P5',[],'P3',[],'P1',[],'Pz',[],'P2',[],'P4',[],'P6',[],'P8',[],'P10'],\
    [[],'PPO9h',[],[],[],'PPO5h',[],[],[],'PPO1',[],'PPO2',[],[],[],'PPO6h',[],[],[],'PPO10h',[]],\
    ['PO9',[],'PO7',[],'PO5',[],'PO3',[],[],[],'POz',[],[],[],'PO4',[],'PO6',[],'PO8',[],'PO10'],\
    [[],'POO9h',[],[],[],[],[],'POO3h',[],[],[],[],[],'POO4h',[],[],[],[],[],'POO10h',[]],\
    [[],[],[],[],[],[],[],[],'O1',[],'Oz',[],'O2',[],[],[],[],[],[],[],[]],\
    [[],[],[],[],[],[],[],[],[],'OI1h',[],'OI2h',[],[],[],[],[],[],[],[],[]],\
    ['EMG_LH',[],'EMG_LF',[],[],[],[],[],'I1',[],'Iz',[],'I2',[],[],[],[],[],'EMG_RF',[],'EMG_RH']]

tight_cap_positions = [
    [[], [], [], [], 'Fp1', 'FPz', 'Fp2', [], [], [], []],
    [[], [], [], 'AFp3h', [], [], [], 'Afp4h', [], [], []],
    [[], 'AF7', [], 'AF3', [], 'AFz', [], 'AF4', [], 'AF8', []],
    [[], [], 'AFF5h', [], 'AFF1', [], 'AFF2', [], 'AFF6h', [], []],
    [[], 'F7', 'F5', 'F3', 'F1', 'Fz', 'F2', 'F4', 'F6', 'F8', []],
    ['FFT9h', 'FFT7h', 'FFC5h', 'FFC3h', 'FFC1h', [], 'FFC2h', 'FFC4h', 'FFC6h', 'FFT8h', 'FFT10h'],
    ['FT9', 'FT7', 'FC5', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'FC6', 'FT8', 'FT10'],
    ['FTT9h', 'FTT7h', 'FCC5h', 'FCC3h', 'FCC1h', [], 'FCC2h', 'FCC4h', 'FCC6h', 'FTT8h', 'FTT10h'],
    ['M1', 'T7', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6', 'T8', 'M2'],
    [[], 'TTP7h', 'CCP5h', 'CCP3h', 'CCP1h', [], 'CCP2h', 'CCP4h', 'CCP6h', 'TTP8h', []],
    [[], 'TP7', 'CP5', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'CP6', 'TP8', []],
    ['TPP9h', 'TPP7h', 'CPP5h', 'CPP3h', 'CPP1h', [], 'CPP2h', 'CPP4h', 'CPP6h', 'TPP8h', 'TPP10h'],
    ['P9', 'P7', 'P5', 'P3', 'P1', 'Pz', 'P2', 'P4', 'P6', 'P8', 'P10'],
    ['PPO9h', [], 'PPO5h', [], 'PPO1', [], 'PPO2', [], 'PPO6h', [], 'PPO10h'],
    ['PO9', 'PO7', 'PO5', 'PO3', [], 'POz', [], 'PO4', 'PO6', 'PO8', 'PO10'],
    ['POO9h', [], [], 'POO3h', [], [], [], 'POO4h', [], [], 'POO10h'],
    [[], [], [], [], 'O1', 'Oz', 'O2', [], [], [], []],
    [[], [], [], [], 'OI1h', [], 'OI2h', [], [], [], []],
    [[], [], [], [], 'I1', 'Iz', 'I2', [], [], [], []]]


tight_C_positions = [
    ['FFC5h','FFC3h','FFC1h',[],'FFC2h','FFC4h','FFC6h'],
    ['FC5','FC3','FC1','FCz','FC2','FC4','FC6'],
    ['FCC5h','FCC3h','FCC1h',[],'FCC2h','FCC4h','FCC6h'],
    ['C5','C3','C1','Cz','C2','C4','C6'],
    ['CCP5h','CCP3h','CCP1h',[],'CCP2h','CCP4h','CCP6h'],
    ['CP5','CP3','CP1','CPz','CP2','CP4','CP6'],
    ['CPP5h','CPP3h','CPP1h',[],'CPP2h','CPP4h','CPP6h']]

tight_dry_positions = [
    [[],[],'Fp1','Fpz','Fp2',[],[]],
    ['AF7','AF3',[],'AFz',[],'AF4','AF8'],
    ['F5','F3','F1','Fz','F2','F4','F6'],
    [[],[],'FC1','FCz','FC2',[],[]],
    [[],'C3','C1','Cz','C2','C4',[]],
    [[],'CP3','CP1','CPz','CP2','CP4',[]],
    [[],[],'P1','Pz','P2',[],[]],
    [[],[],[],'POz',[],[],[]]]

tight_bci_comp_4_2a_positions = [
    [[],[],[],'Fz',[],[],[]],
    [[],'2','3','4','5','6',[]],
    ['7','C3','9','Cz','11','C4','13'],
    [[],'14','15','16','17','18',[]],
    [[],[],'19','Pz','21',[],[]],
    [[],[],[],'22',[],[],[]]]

tight_Kaggle_positions =  [
    [[],[],'Fp1',[],'FP2',[],[]],
    [[],'F7','F3','Fz','F4','F8',[]],
    [[],'FC5', 'FC1',[],'FC2','FC6',[]],\
    [[],'T7','C3','Cz','C4','T8',[]],\
    ['TP9','CP5','CP1',[],'CP2','CP6','TP10'],\
    [[], 'P7', 'P3','Pz','P4','P8', []],\
    [[],'PO9','O1','Oz','O2','PO10',[]]]



# from
# print extract_angle_from_csv('datautils/sensor_positions_for_plot/Waveguard2Dpos._lukas_mail.csv')
WAVEGUARD_2DANGLE = ('angle',('Fp1', (1.435, 3.676)),
('Fpz', (-0.004, 4.000)),
('Fp2', (-1.439, 3.676)),
('F7', (4.085, 2.382)),
('F3', (2.133, 1.738)),
('Fz', (-0.004, 1.578)),
('F4', (-2.187, 1.769)),
('F8', (-4.069, 2.391)),
('FC5', (3.760, 0.716)),
('FC1', (1.227, 0.440)),
('FC2', (-1.259, 0.467)),
('FC6', (-3.781, 0.747)),
('M1', (6.549, -2.249)),
('T7', (5.280, -0.587)),
('C3', (2.555, -0.720)),
('Cz', (-0.004, -0.747)),
('C4', (-2.608, -0.689)),
('T8', (-5.269, -0.529)),
('M2', (-6.555, -2.276)),
('CP5', (3.589, -1.911)),
('CP1', (1.173, -1.747)),
('CP2', (-1.237, -1.729)),
('CP6', (-3.621, -1.840)),
('P7', (3.888, -3.418)),
('P3', (1.989, -2.951)),
('Pz', (-0.005, -2.836)),
('P4', (-2.032, -2.951)),
('P8', (-3.883, -3.409)),
('POz', (-0.004, -3.542)),
('O1', (1.360, -4.649)),
('Oz', (-0.004, -4.711)),
('O2', (-1.355, -4.649)),
('AF7', (2.827, 3.244)),
('AF3', (1.472, 2.831)),
('AF4', (-1.525, 2.813)),
('AF8', (-2.805, 3.249)),
('F5', (3.136, 2.009)),
('F1', (1.061, 1.600)),
('F2', (-1.131, 1.618)),
('F6', (-3.168, 2.022)),
('FC3', (2.496, 0.542)),
('FCz', (-0.004, 0.418)),
('FC4', (-2.533, 0.578)),
('C5', (3.888, -0.671)),
('C1', (1.264, -0.733)),
('C2', (-1.317, -0.724)),
('C6', (-3.893, -0.627)),
('CP3', (2.363, -1.818)),
('CPz', (-0.005, -1.747)),
('CP4', (-2.411, -1.787)),
('P5', (2.955, -3.111)),
('P1', (0.981, -2.911)),
('P2', (-1.035, -2.893)),
('P6', (-2.981, -3.133)),
('PO5', (2.117, -4.182)),
('PO3', (1.387, -3.880)),
('PO4', (-1.391, -3.911)),
('PO6', (-2.069, -4.213)),
('FT7', (5.013, 1.044)),
('FT8', (-4.981, 1.093)),
('TP7', (4.848, -2.036)),
('TP8', (-4.837, -2.022)),
('PO7', (2.683, -3.947)),
('PO8', (-2.688, -3.938)),
('FT9', (6.107, 1.618)),
('FT10', (-6.112, 1.627)),
('TPP9h', (4.987, -3.018)),
('TPP10h', (-4.991, -3.018)),
('PO9', (3.355, -4.622)),
('PO10', (-3.344, -4.613)),
('P9', (4.901, -3.871)),
('P10', (-4.859, -3.884)),
('AFF1', (0.944, 2.147)),
('AFz', (-0.004, 2.693)),
('AFF2', (-0.971, 2.173)),
('FFC5h', (2.923, 1.258)),
('FFC3h', (1.733, 1.107)),
('FFC4h', (-1.808, 1.129)),
('FFC6h', (-2.981, 1.284)),
('FCC5h', (3.227, -0.053)),
('FCC3h', (1.915, -0.138)),
('FCC4h', (-1.957, -0.116)),
('FCC6h', (-3.264, -0.013)),
('CCP5h', (3.131, -1.293)),
('CCP3h', (1.840, -1.276)),
('CCP4h', (-1.899, -1.249)),
('CCP6h', (-3.173, -1.240)),
('CPP5h', (2.741, -2.373)),
('CPP3h', (1.616, -2.284)),
('CPP4h', (-1.669, -2.258)),
('CPP6h', (-2.795, -2.324)),
('PPO1', (0.885, -3.369)),
('PPO2', (-0.939, -3.351)),
('I1', (1.701, -5.480)),
('Iz', (-0.004, -5.773)),
('I2', (-1.680, -5.489)),
('AFp3h', (0.832, 3.249)),
('AFp4h', (-0.859, 3.236)),
('AFF5h', (2.261, 2.409)),
('AFF6h', (-2.288, 2.431)),
('FFT7h', (4.069, 1.551)),
('FFC1h', (0.549, 1.000)),
('FFC2h', (-0.635, 1.013)),
('FFT8h', (-4.069, 1.578)),
('FTT9h', (5.893, 0.498)),
('FTT7h', (4.555, 0.116)),
('FCC1h', (0.635, -0.173)),
('FCC2h', (-0.667, -0.169)),
('FTT8h', (-4.555, 0.160)),
('FTT10h', (-5.893, 0.489)),
('TTP7h', (4.670, -1.267)),
('CCP1h', (0.597, -1.267)),
('CCP2h', (-0.656, -1.262)),
('TTP8h', (-4.675, -1.267)),
('TPP7h', (3.840, -2.560)),
('CPP1h', (0.517, -2.222)),
('CPP2h', (-0.597, -2.209)),
('TPP8h', (-3.861, -2.560)),
('PPO9h', (3.723, -4.191)),
('PPO5h', (2.208, -3.498)),
('PPO6h', (-2.213, -3.498)),
('PPO10h', (-3.691, -4.200)),
('POO9h', (2.288, -4.867)),
('POO3h', (0.795, -4.333)),
('POO4h', (-0.816, -4.316)),
('POO10h', (-2.261, -4.871)),
('OI1h', (0.768, -5.138)),
('OI2h', (-0.752, -5.138)))

# from 
# print extract_xy_from_csv('datautils/sensor_positions_for_plot/Waveguard2Dpos._lukas_mail.csv')
WAVEGUARD_2DXYPOS = ('cartesian',('Fp1', (0.359, 0.919)),
('Fpz', (-0.001, 1.000)),
('Fp2', (-0.360, 0.919)),
('F7', (1.021, 0.596)),
('F3', (0.533, 0.434)),
('Fz', (-0.001, 0.394)),
('F4', (-0.547, 0.442)),
('F8', (-1.017, 0.598)),
('FC5', (0.940, 0.179)),
('FC1', (0.307, 0.110)),
('FC2', (-0.315, 0.117)),
('FC6', (-0.945, 0.187)),
('M1', (1.637, -0.562)),
('T7', (1.320, -0.147)),
('C3', (0.639, -0.180)),
('Cz', (-0.001, -0.187)),
('C4', (-0.652, -0.172)),
('T8', (-1.317, -0.132)),
('M2', (-1.639, -0.569)),
('CP5', (0.897, -0.478)),
('CP1', (0.293, -0.437)),
('CP2', (-0.309, -0.432)),
('CP6', (-0.905, -0.460)),
('P7', (0.972, -0.854)),
('P3', (0.497, -0.738)),
('Pz', (-0.001, -0.709)),
('P4', (-0.508, -0.738)),
('P8', (-0.971, -0.852)),
('POz', (-0.001, -0.886)),
('O1', (0.340, -1.162)),
('Oz', (-0.001, -1.178)),
('O2', (-0.339, -1.162)),
('AF7', (0.707, 0.811)),
('AF3', (0.368, 0.708)),
('AF4', (-0.381, 0.703)),
('AF8', (-0.701, 0.812)),
('F5', (0.784, 0.502)),
('F1', (0.265, 0.400)),
('F2', (-0.283, 0.404)),
('F6', (-0.792, 0.506)),
('FC3', (0.624, 0.136)),
('FCz', (-0.001, 0.104)),
('FC4', (-0.633, 0.144)),
('C5', (0.972, -0.168)),
('C1', (0.316, -0.183)),
('C2', (-0.329, -0.181)),
('C6', (-0.973, -0.157)),
('CP3', (0.591, -0.454)),
('CPz', (-0.001, -0.437)),
('CP4', (-0.603, -0.447)),
('P5', (0.739, -0.778)),
('P1', (0.245, -0.728)),
('P2', (-0.259, -0.723)),
('P6', (-0.745, -0.783)),
('PO5', (0.529, -1.046)),
('PO3', (0.347, -0.970)),
('PO4', (-0.348, -0.978)),
('PO6', (-0.517, -1.053)),
('FT7', (1.253, 0.261)),
('FT8', (-1.245, 0.273)),
('TP7', (1.212, -0.509)),
('TP8', (-1.209, -0.506)),
('PO7', (0.671, -0.987)),
('PO8', (-0.672, -0.984)),
('FT9', (1.527, 0.404)),
('FT10', (-1.528, 0.407)),
('TPP9h', (1.247, -0.754)),
('TPP10h', (-1.248, -0.754)),
('PO9', (0.839, -1.156)),
('PO10', (-0.836, -1.153)),
('P9', (1.225, -0.968)),
('P10', (-1.215, -0.971)),
('AFF1', (0.236, 0.537)),
('AFz', (-0.001, 0.673)),
('AFF2', (-0.243, 0.543)),
('FFC5h', (0.731, 0.314)),
('FFC3h', (0.433, 0.277)),
('FFC4h', (-0.452, 0.282)),
('FFC6h', (-0.745, 0.321)),
('FCC5h', (0.807, -0.013)),
('FCC3h', (0.479, -0.034)),
('FCC4h', (-0.489, -0.029)),
('FCC6h', (-0.816, -0.003)),
('CCP5h', (0.783, -0.323)),
('CCP3h', (0.460, -0.319)),
('CCP4h', (-0.475, -0.312)),
('CCP6h', (-0.793, -0.310)),
('CPP5h', (0.685, -0.593)),
('CPP3h', (0.404, -0.571)),
('CPP4h', (-0.417, -0.564)),
('CPP6h', (-0.699, -0.581)),
('PPO1', (0.221, -0.842)),
('PPO2', (-0.235, -0.838)),
('I1', (0.425, -1.370)),
('Iz', (-0.001, -1.443)),
('I2', (-0.420, -1.372)),
('AFp3h', (0.208, 0.812)),
('AFp4h', (-0.215, 0.809)),
('AFF5h', (0.565, 0.602)),
('AFF6h', (-0.572, 0.608)),
('FFT7h', (1.017, 0.388)),
('FFC1h', (0.137, 0.250)),
('FFC2h', (-0.159, 0.253)),
('FFT8h', (-1.017, 0.394)),
('FTT9h', (1.473, 0.124)),
('FTT7h', (1.139, 0.029)),
('FCC1h', (0.159, -0.043)),
('FCC2h', (-0.167, -0.042)),
('FTT8h', (-1.139, 0.040)),
('FTT10h', (-1.473, 0.122)),
('TTP7h', (1.168, -0.317)),
('CCP1h', (0.149, -0.317)),
('CCP2h', (-0.164, -0.316)),
('TTP8h', (-1.169, -0.317)),
('TPP7h', (0.960, -0.640)),
('CPP1h', (0.129, -0.556)),
('CPP2h', (-0.149, -0.552)),
('TPP8h', (-0.965, -0.640)),
('PPO9h', (0.931, -1.048)),
('PPO5h', (0.552, -0.874)),
('PPO6h', (-0.553, -0.874)),
('PPO10h', (-0.923, -1.050)),
('POO9h', (0.572, -1.217)),
('POO3h', (0.199, -1.083)),
('POO4h', (-0.204, -1.079)),
('POO10h', (-0.565, -1.218)),
('OI1h', (0.192, -1.284)),
('OI2h', (-0.188, -1.284))
)

LAURA_POS = ('cartesian',
            ('Fp1', (-0.220, 0.932)),
('Fpz', (0.000, 1.000)),
('Fp2', (0.219, 0.932)),
('F7', (-0.624, 0.659)),
('F3', (-0.326, 0.523)),
('Fz', (0.000, 0.490)),
('F4', (0.333, 0.530)),
('F8', (0.621, 0.661)),
('FC5', (-0.574, 0.308)),
('FC1', (-0.188, 0.250)),
('FC2', (0.191, 0.256)),
('FC6', (0.577, 0.315)),
('M1', (-0.957, -0.289)),
('T7', (-0.806, 0.034)),
('C3', (-0.390, 0.006)),
('Cz', (0.000, 0.000)),
('C4', (0.397, 0.012)),
('T8', (0.804, 0.046)),
('M2', (0.957, -0.289)),
('CP5', (-0.548, -0.232)),
('CP1', (-0.180, -0.199)),
('CP2', (0.188, -0.195)),
('CP6', (0.552, -0.218)),
('P7', (-0.594, -0.531)),
('P3', (-0.304, -0.439)),
('Pz', (0.000, -0.416)),
('P4', (0.310, -0.439)),
('P8', (0.592, -0.530)),
('POz', (0.000, -0.556)),
('O1', (-0.208, -0.776)),
('Oz', (0.000, -0.789)),
('O2', (0.206, -0.776)),
('AF7', (-0.432, 0.841)),
('AF3', (-0.225, 0.754)),
('AF4', (0.232, 0.750)),
('AF8', (0.428, 0.842)),
('F5', (-0.479, 0.581)),
('F1', (-0.163, 0.494)),
('F2', (0.172, 0.498)),
('F6', (0.483, 0.583)),
('FC3', (-0.382, 0.272)),
('FCz', (0.000, 0.245)),
('FC4', (0.386, 0.279)),
('C5', (-0.594, 0.016)),
('C1', (-0.194, 0.003)),
('C2', (0.200, 0.005)),
('C6', (0.594, 0.025)),
('CP3', (-0.361, -0.213)),
('CPz', (0.000, -0.199)),
('CP4', (0.367, -0.207)),
('P5', (-0.452, -0.470)),
('P1', (-0.150, -0.431)),
('P2', (0.157, -0.427)),
('P6', (0.454, -0.475)),
('PO5', (-0.324, -0.683)),
('PO3', (-0.212, -0.623)),
('PO4', (0.212, -0.630)),
('PO6', (0.315, -0.690)),
('FT7', (-0.766, 0.377)),
('FT8', (0.760, 0.388)),
('TP7', (-0.740, -0.256)),
('TP8', (0.738, -0.254)),
('PO7', (-0.410, -0.637)),
('PO8', (0.410, -0.635)),
('FT9', (-0.887, 0.462)),
('FT10', (0.887, 0.462)),
('TPP9h', (-0.762, -0.452)),
('TPP10h', (0.761, -0.452)),
('PO9', (-0.513, -0.771)),
('PO10', (0.510, -0.769)),
('P9', (-0.749, -0.622)),
('P10', (0.741, -0.624)),
('AFF1', (-0.145, 0.610)),
('AFz', (0.000, 0.725)),
('AFF2', (0.148, 0.615)),
('FFC5h', (-0.447, 0.422)),
('FFC3h', (-0.265, 0.390)),
('FFC4h', (0.275, 0.395)),
('FFC6h', (0.454, 0.428)),
('FCC5h', (-0.493, 0.146)),
('FCC3h', (-0.293, 0.128)),
('FCC4h', (0.298, 0.133)),
('FCC6h', (0.498, 0.154)),
('CCP5h', (-0.478, -0.109)),
('CCP3h', (-0.281, -0.105)),
('CCP4h', (0.289, -0.100)),
('CCP6h', (0.484, -0.098)),
('CPP5h', (-0.419, -0.324)),
('CPP3h', (-0.247, -0.306)),
('CPP4h', (0.254, -0.301)),
('CPP6h', (0.426, -0.314)),
('PPO1', (-0.136, -0.522)),
('PPO2', (0.143, -0.518)),
('I1', (-0.260, -0.942)),
('Iz', (0.000, -1.000)),
('I2', (0.256, -0.943)),
('AFp3h', (-0.128, 0.842)),
('AFp4h', (0.130, 0.839)),
('AFF5h', (-0.346, 0.665)),
('AFF6h', (0.349, 0.669)),
('FFT7h', (-0.622, 0.484)),
('FFC1h', (-0.084, 0.368)),
('FFC2h', (0.096, 0.371)),
('FFT8h', (0.621, 0.490)),
('FTT9h', (-0.900, 0.262)),
('FTT7h', (-0.696, 0.182)),
('FCC1h', (-0.098, 0.121)),
('FCC2h', (0.101, 0.122)),
('FTT8h', (0.695, 0.191)),
('FTT10h', (0.899, 0.260)),
('TTP7h', (-0.713, -0.103)),
('CCP1h', (-0.092, -0.103)),
('CCP2h', (0.099, -0.103)),
('TTP8h', (0.713, -0.103)),
('TPP7h', (-0.587, -0.361)),
('CPP1h', (-0.080, -0.294)),
('CPP2h', (0.091, -0.291)),
('TPP8h', (0.589, -0.361)),
('PPO9h', (-0.569, -0.685)),
('PPO5h', (-0.338, -0.547)),
('PPO6h', (0.337, -0.547)),
('PPO10h', (0.563, -0.687)),
('POO9h', (-0.350, -0.820)),
('POO3h', (-0.122, -0.714)),
('POO4h', (0.124, -0.710)),
('POO10h', (0.345, -0.821)),
('OI1h', (-0.118, -0.874)),
('OI2h', (0.114, -0.874)))
#New version (with asymmetry bug fixed now), extracted by:
# original file: mntutil_posWaveguard128.m
# channels = ['Fp1','AFp3h','Fpz','AFp4h','Fp2', 
#        'AF7','AFF5h','AF3','AFF1','AFz','AFF2','Af4','AFF6h','AF8', 
#        'F7','F5','F3','F1','Fz','F2','F4','F6','F8', 
#        'FFT7h','FFC5h','FFC3h','FFC1h','FFC2h','FFC4h','FFC6h','FFT8h', 
#        'FT9','FT7','FC5','FC3','FC1','FCz','FC2','FC4','FC6','FT8','FT10', 
#        'FTT9h','FTT7h','FCC5h','FCC3h','FCC1h','FCC2h','FCC4h','FCC6h','FTT8h','FTT10h', 
#        'M1','T7','C5','C3','C1','Cz','C2','C4','C6','T8','M2', 
#        'TTP7h','CCP5h','CCP3h','CCP1h','CCP2h','CCP4h','CCP6h','TTP8h', 
#        'TP7','CP5','CP3','CP1','CPz','CP2','CP4','CP6','TP8', 
#        'TPP9h','TPP7h','CPP5h','CPP3h','CPP1h','CPP2h','CPP4h','CPP6h','TPP8h','TPP10h', 
#        'P9','P7','P5','P3','P1','Pz','P2','P4','P6','P8','P10', 
#        'PPO9h','PPO5h','PPO1','PPO2','PPO6h','PPO10h', 
#        'PO9','PO7','PO5','PO3','PO1','POz','PO2','PO4','PO6','PO8','PO10', 
#        'POO9h','POO3h','O1','Oz','O2','POO4h','POO10h', 
#        'I1','OI1h','Iz','OI2h','I2']
# 
# #7th line from below modified from original file, there were too many values!!
# x = """-4 -1.5 0 1.5 4 
#           -4 -3 -2.5 -2 0 2 2.5 3 4 
#           -5 -4 -3 -2 0 2 3 4 5 
#           -3.5 -2.5 -1.5 -0.5 0.5 1.5 2.5 3.5 
#           -5 -4 -3 -2 -1 0 1 2 3 4 5 
#           -4.5 -3.5 -2.5 -1.5 -0.5 0.5 1.5 2.5 3.5 4.5 
#           -5 -4 -3 -2 -1 0 1 2 3 4 5 
#           -3.5 -2.5 -1.5 -0.5 0.5 1.5 2.5 3.5 
#           -5 -4 -3 -2 0 2 3 4 5 
#           -4.5 -3.5 -2.5 -1.5 -0.5 0.5 1.5 2.5 3.5 4.5 
#           -5 -4 -3 -2 -1 0 1 2 3 4 5 
#           -4.5 -3 -0.65 0.65 3 4.5 
#           -5.5 -4 -3 -2 -1 0 1 2 3 4 5.5 
#           -6.5 -4 -1.5 0 1.5 4 6.5 
#           1.5 1 0 -1 -1.5"""
# 
# lines_splitted = [line.split() for line in x.split('\n')]
# 
# names = """
# 'Fp1','AFp3h','Fpz','AFp4h','Fp2', ...
#        'AF7','AFF5h','AF3','AFF1','AFz','AFF2','Af4','AFF6h','AF8', ...
#        'F7','F5','F3','F1','Fz','F2','F4','F6','F8', ...
#        'FFT7h','FFC5h','FFC3h','FFC1h','FFC2h','FFC4h','FFC6h','FFT8h', ...
#        'FT9','FT7','FC5','FC3','FC1','FCz','FC2','FC4','FC6','FT8','FT10', ...
#        'FTT9h','FTT7h','FCC5h','FCC3h','FCC1h','FCC2h','FCC4h','FCC6h','FTT8h','FTT10h', ...
#        'M1','T7','C5','C3','C1','Cz','C2','C4','C6','T8','M2', ...
#        'TTP7h','CCP5h','CCP3h','CCP1h','CCP2h','CCP4h','CCP6h','TTP8h', ...
#        'TP7','CP5','CP3','CP1','CPz','CP2','CP4','CP6','TP8', ...
#        'TPP9h','TPP7h','CPP5h','CPP3h','CPP1h','CPP2h','CPP4h','CPP6h','TPP8h','TPP10h', ...
#        'P9','P7','P5','P3','P1','Pz','P2','P4','P6','P8','P10', ...
#        'PPO9h','PPO5h','PPO1','PPO2','PPO6h','PPO10h', ...
#        'PO9','PO7','PO5','PO3','PO1','POz','PO2','PO4','PO6','PO8','PO10', ...
#        'POO9h','POO3h','O1','Oz','O2','POO4h','POO10h', ...
#        'I1','OI1h','Iz','OI2h','I2'
# """
# 
# nameslines = names.split('\n')
# 
# nameslines = nameslines[1:-1]
# sensor_name_rows = [filter(lambda s: s!= '', 
#                            l.replace('...', '').replace('\'', '').strip().split(',')) for l in nameslines]
# 
# for i in range(len(sensor_name_rows)):
#     assert (len(sensor_name_rows[i])) == (len(lines_splitted[i]))
# 
# x_vals_per_row = [[float(pos_str) for pos_str in line] for line in lines_splitted]
# 
# ys_per_row = [ 3.5, 3, 2, 1.5, 1, 0.5, 0, -0.5, -1, -1.5, -2, -2.5, -3, -3.5, -5]
# 
# assert len(ys_per_row) == len(x_vals_per_row) == len(sensor_name_rows)
# 
# for i_row in xrange(len(sensor_name_rows)):
#     assert len(x_vals_per_row[i_row]) == len(sensor_name_rows[i_row])
#     y_val = ys_per_row[i_row]
#     
#     for i_col in xrange(len(sensor_name_rows[i_row])):
#         x_val = x_vals_per_row[i_row][i_col]
#         sensor = sensor_name_rows[i_row][i_col]
#         print("('{:s}', ({:.3f}, {:.3f})),".format(sensor, x_val, y_val))

# from
# print extract_sensor_angle_string('datautils/sensor_positions_for_plot/mntutil_posWaveguard128_me.m')
CHANNEL_10_20_APPROX = ('angle',
    ('Fpz',(0.000, 4.000)),
('Fp1',(-3.500, 3.500)),
('Fp2',(3.500, 3.500)),
('AFp3h',(-1.000, 3.500)),
('AFp4h',(1.000, 3.500)),
('AF7',(-4.000, 3.000)),
('AF3',(-2.000, 3.000)),
('AFz',(0.000, 3.000)),
('AF4',(2.000, 3.000)),
('AF8',(4.000, 3.000)),
('AFF5h',(-2.500, 2.500)),
('AFF1',(-0.500, 2.500)),
('AFF2',(0.500, 2.500)),
('AFF6h',(2.500, 2.500)),
('F7',(-4.000, 2.000)),
('F5',(-3.000, 2.000)),
('F3',(-2.000, 2.000)),
('F1',(-1.000, 2.000)),
('Fz',(0.000, 2.000)),
('F2',(1.000, 2.000)),
('F4',(2.000, 2.000)),
('F6',(3.000, 2.000)),
('F8',(4.000, 2.000)),
('FFT7h',(-3.500, 1.500)),
('FFC5h',(-2.500, 1.500)),
('FFC3h',(-1.500, 1.500)),
('FFC1h',(-0.500, 1.500)),
('FFC2h',(0.500, 1.500)),
('FFC4h',(1.500, 1.500)),
('FFC6h',(2.500, 1.500)),
('FFT8h',(3.500, 1.500)),
('FT9',(-5.000, 1.000)),
('FT7',(-4.000, 1.000)),
('FC5',(-3.000, 1.000)),
('FC3',(-2.000, 1.000)),
('FC1',(-1.000, 1.000)),
('FCz',(0.000, 1.000)),
('FC2',(1.000, 1.000)),
('FC4',(2.000, 1.000)),
('FC6',(3.000, 1.000)),
('FT8',(4.000, 1.000)),
('FT10',(5.000, 1.000)),
('FTT9h',(-4.500, 0.500)),
('FTT7h',(-3.500, 0.500)),
('FCC5h',(-2.500, 0.500)),
('FCC3h',(-1.500, 0.500)),
('FCC1h',(-0.500, 0.500)),
('FCC2h',(0.500, 0.500)),
('FCC4h',(1.500, 0.500)),
('FCC6h',(2.500, 0.500)),
('FTT8h',(3.500, 0.500)),
('FTT10h',(4.500, 0.500)),
('M1',(-5.000, 0.000)),
('T7',(-4.000, 0.000)),
('C5',(-3.000, 0.000)),
('C3',(-2.000, 0.000)),
('C1',(-1.000, 0.000)),
('Cz',(0.000, 0.000)),
('C2',(1.000, 0.000)),
('C4',(2.000, 0.000)),
('C6',(3.000, 0.000)),
('T8',(4.000, 0.000)),
('M2',(5.000, 0.000)),
('TTP7h',(-3.500, -0.500)),
('CCP5h',(-2.500, -0.500)),
('CCP3h',(-1.500, -0.500)),
('CCP1h',(-0.500, -0.500)),
('CCP2h',(0.500, -0.500)),
('CCP4h',(1.500, -0.500)),
('CCP6h',(2.500, -0.500)),
('TTP8h',(3.500, -0.500)),
('TP7',(-4.000, -1.000)),
('CP5',(-3.000, -1.000)),
('CP3',(-2.000, -1.000)),
('CP1',(-1.000, -1.000)),
('CPz',(0.000, -1.000)),
('CP2',(1.000, -1.000)),
('CP4',(2.000, -1.000)),
('CP6',(3.000, -1.000)),
('TP8',(4.000, -1.000)),
('TPP9h',(-4.500, -1.500)),
('TPP7h',(-3.500, -1.500)),
('CPP5h',(-2.500, -1.500)),
('CPP3h',(-1.500, -1.500)),
('CPP1h',(-0.500, -1.500)),
('CPP2h',(0.500, -1.500)),
('CPP4h',(1.500, -1.500)),
('CPP6h',(2.500, -1.500)),
('TPP8h',(3.500, -1.500)),
('TPP10h',(4.500, -1.500)),
('P9',(-5.000, -2.000)),
('P7',(-4.000, -2.000)),
('P5',(-3.000, -2.000)),
('P3',(-2.000, -2.000)),
('P1',(-1.000, -2.000)),
('Pz',(0.000, -2.000)),
('P2',(1.000, -2.000)),
('P4',(2.000, -2.000)),
('P6',(3.000, -2.000)),
('P8',(4.000, -2.000)),
('P10',(5.000, -2.000)),
('PPO9h',(-4.500, -2.500)),
('PPO5h',(-3.000, -2.500)),
('PPO1',(-0.650, -2.500)),
('PPO2',(0.650, -2.500)),
('PPO6h',(3.000, -2.500)),
('PPO10h',(4.500, -2.500)),
('PO9',(-5.000, -3.000)),
('PO7',(-4.000, -3.000)),
('PO5',(-3.000, -3.000)),
('PO3',(-2.000, -3.000)),
('PO1',(-1.000, -3.000)),
('POz',(0.000, -3.000)),
('PO2',(1.000, -3.000)),
('PO4',(2.000, -3.000)),
('PO6',(3.000, -3.000)),
('PO8',(4.000, -3.000)),
('PO10',(5.000, -3.000)),
('POO9h',(-4.500, -3.250)),
('POO3h',(-2.000, -3.250)),
('POO4h',(2.000, -3.250)),
('POO10h',(4.500, -3.250)),
('O1',(-2.500, -3.750)),
('Oz',(0.000, -3.750)),
('O2',(2.500, -3.750)),
('OI1h',(1.500, -4.250)),
('OI2h',(-1.500, -4.250)),
('I1',(1.000, -4.500)),
('Iz',(0.000, -4.500)),
('I2',(-1.000, -4.500))
)

def extract_sensor_angle_string(filename):
    """Extracting sensor positions and putting into string form matlab code.
    Very hacky regular expressions code :)"""
    file_content = open(filename, 'r').read()
    # find sensor string
    sensor_string = re.search(r'clab=[ ]*{([^}]*)}', file_content).group(1)
    # split into rows
    sensor_rows = re.split(r'[\r]*\n', sensor_string)
    # remove whitespace
    sensor_rows = [s.strip('... ') for s in sensor_rows]
    # split individual sensors by comma
    sensor_matrix = [s.split(',') for s in sensor_rows]
    # remove empty strings and remove single quotes
    sensor_matrix = [[s.strip("' ") for s in row if s != ''] for row in sensor_matrix]
    angle_string_1 = re.search(r'ea=[ ]*a \* \[([^\]]*)\]', file_content).group(1)
    angle_rows_1 = re.split(r'[\r]*\n', angle_string_1)
    angle_rows_1 = [s[:s.find('%')] if '%' in s else s for s in angle_rows_1]
    angle_rows_1 = [s.strip('... ') for s in angle_rows_1]
    angle_matrix_1 = [[float(s) for s in row.split()] for row in angle_rows_1]
    angle_string_2 = re.search(r'eb=[ ]* \[ ([^\]]*)\]', file_content).group(1)
    angle_rows_2 = re.split(r'[\r]*\n', angle_string_2)
    angle_vals_2 = [s.strip('... ').split()[0].replace("*b", "") for s in angle_rows_2]
    angle_vals_2 = [float(val) for val in angle_vals_2]
    
    assert len(angle_matrix_1) == len(angle_vals_2)
    sensor_pos_strings = []
    for i_row in xrange(len(sensor_matrix)):
        assert len(sensor_matrix[i_row]) == len(angle_matrix_1[i_row])
        for i_col in xrange(len(sensor_matrix[i_row])):
            sensor_pos_strings.append("('{:s}',({:.3f}, {:.3f}))".format(
                sensor_matrix[i_row][i_col], angle_matrix_1[i_row][i_col],
                angle_vals_2[i_row]))
    return (',\n').join(sensor_pos_strings)

# the angles here are given in (90 / 4)th degrees - so multiply it with
# (90 / 4) to get the actual angles
def extract_angle_from_csv(filename):
    sensor_strings = []
    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            sensor_name = row[0].split()[0].strip(':')
            val_1 = float(row[1])
            val_2 = float(row[2])
            sensor_strings.append("('{:s}', ({:.3f}, {:.3f}))".format(sensor_name, val_2 / (90/4.0),
                                                                 val_1/(90/4.0), ))
    return ",\n".join(sensor_strings)

# assuming values inside -1,1 are from -90 to 90
def extract_xy_from_csv(filename):
    sensor_strings = []
    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            sensor_name = row[0].split()[0].strip(':')
            val_1 = float(row[1])
            val_2 = float(row[2])
            sensor_strings.append("('{:s}', ({:.3f}, {:.3f}))".format(
                sensor_name, val_2 / (90.0), val_1/(90.0), ))
    return ",\n".join(sensor_strings)

def sort_topologically(sensor_names):
    """ Get sensors in a topologically sensible order.
    
    >>> sort_topologically(['O1', 'FP1'])
    ['FP1', 'O1']
    >>> sort_topologically(['FP2', 'FP1'])
    ['FP1', 'FP2']
    >>> sort_topologically(['O1', 'FP1', 'FP2'])
    ['FP1', 'FP2', 'O1']

    
    Check that sensors are sorted row-wise, i.e. first row, then second row,
    and inside rows sorted by column 
    >>> sort_topologically(['FP1', 'POO9h', 'FP2', 'POO3h'])
    ['FP1', 'FP2', 'POO9h', 'POO3h']
    
    # Check that all sensors exist
    >>> sort_topologically(['O5', 'POO9h', 'FP2', 'POO3h'])
    Traceback (most recent call last):
        ...
    AssertionError: Expect all sensors to exist in topo grid, not existing: set(['O5'])
    """
    flat_topo_all_sensors = np.array(
        [name for row in cap_positions for name in row if name != []])
    sorted_sensor_names = []
    # Go through all sorted sensors and add those that are requested
    for sensor_name in flat_topo_all_sensors:
        for sensor_name_wanted in sensor_names:
            if sensor_name.lower() == sensor_name_wanted.lower():
                sorted_sensor_names.append(sensor_name_wanted)
    assert len(set(sensor_names) - set(sorted_sensor_names)) == 0, \
        "Expect all sensors to exist in topo grid, not existing: {:s}".format(
            str(set(sensor_names) - set(sorted_sensor_names)))
    return sorted_sensor_names
    
def get_sensor_pos(sensor_name, sensor_map=cap_positions):
    sensor_pos = np.where(np.char.lower(np.char.array(sensor_map)) == sensor_name.lower())
    # unpack them: they are 1-dimensional arrays before
    assert len(sensor_pos[0]) == 1, ("there should be a position for the sensor "
        "{:s}".format(sensor_name))
    return sensor_pos[0][0], sensor_pos[1][0]

def get_cap_shape():
    return np.array(cap_positions).shape

def get_C_sensors():
    C_sensors= ['FC5', 'FC1', 'FC2', 'FC6', 'C3', 'Cz', 'C4', 'CP5',
        'CP1', 'CP2', 'CP6', 'FC3', 'FCz', 'FC4', 'C5', 'C1', 'C2', 'C6',
        'CP3', 'CPz', 'CP4', 'FFC5h', 'FFC3h', 'FFC4h', 'FFC6h', 'FCC5h',
        'FCC3h', 'FCC4h', 'FCC6h', 'CCP5h', 'CCP3h', 'CCP4h', 'CCP6h', 'CPP5h',
        'CPP3h', 'CPP4h', 'CPP6h', 'FFC1h', 'FFC2h', 'FCC1h', 'FCC2h', 'CCP1h',
         'CCP2h', 'CPP1h', 'CPP2h']
    return C_sensors

def get_C_sensors_sorted():
    return sort_topologically(get_C_sensors())

def get_EEG_sensors():
    return ['Fp1', 'Fp2', 'Fpz', 'F7', 'F3', 'Fz', 'F4', 'F8',
            'FC5', 'FC1', 'FC2', 'FC6', 'M1', 'T7', 'C3', 'Cz', 'C4', 'T8', 'M2',
            'CP5', 'CP1', 'CP2', 'CP6', 'P7', 'P3', 'Pz', 'P4', 'P8', 'POz', 'O1',
            'Oz', 'O2', 'AF7', 'AF3', 'AF4', 'AF8', 'F5', 'F1', 'F2', 'F6', 'FC3',
            'FCz', 'FC4', 'C5', 'C1', 'C2', 'C6', 'CP3', 'CPz', 'CP4', 'P5', 'P1',
            'P2', 'P6', 'PO5', 'PO3', 'PO4', 'PO6', 'FT7', 'FT8', 'TP7', 'TP8',
            'PO7', 'PO8', 'FT9', 'FT10', 'TPP9h', 'TPP10h', 'PO9', 'PO10', 'P9',
            'P10', 'AFF1', 'AFz', 'AFF2', 'FFC5h', 'FFC3h', 'FFC4h', 'FFC6h', 'FCC5h',
            'FCC3h', 'FCC4h', 'FCC6h', 'CCP5h', 'CCP3h', 'CCP4h', 'CCP6h', 'CPP5h',
            'CPP3h', 'CPP4h', 'CPP6h', 'PPO1', 'PPO2', 'I1', 'Iz', 'I2', 'AFp3h',
            'AFp4h', 'AFF5h', 'AFF6h', 'FFT7h', 'FFC1h', 'FFC2h', 'FFT8h', 'FTT9h',
            'FTT7h', 'FCC1h', 'FCC2h', 'FTT8h', 'FTT10h', 'TTP7h', 'CCP1h', 'CCP2h',
            'TTP8h', 'TPP7h', 'CPP1h', 'CPP2h', 'TPP8h', 'PPO9h', 'PPO5h', 'PPO6h',
            'PPO10h', 'POO9h', 'POO3h', 'POO4h', 'POO10h', 'OI1h', 'OI2h']

def get_EEG_sensors_sorted():
    return sort_topologically(get_EEG_sensors())

def get_bci_competition_iv_2a_sensors():
    return ['Fz','2','3','4','5','6',
    '7','C3','9','Cz','11','C4','13',
    '14','15','16','17','18', '19','Pz','21','22']
    
def get_nico_sensors():
    sensors = ['Fp1', 'Fpz', 'Fp2', 'AF7', 'AF3', 'AF4', 'AF8', 'F7',
         'F5', 'F3', 'F1', 'Fz', 'F2', 'F4', 'F6', 'F8', 'FT7', 'FC5', 'FC3',
         'FC1', 'FCz', 'FC2', 'FC4', 'FC6', 'FT8', 'M1', 'T7', 'C5', 'C3',
         'C1', 'Cz', 'C2', 'C4', 'C6', 'T8', 'M2', 'TP7', 'CP5', 'CP3',
         'CP1', 'CPz', 'CP2', 'CP4', 'CP6', 'TP8', 'P7', 'P5', 'P3', 'P1',
         'Pz', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POz', 'PO4',
         'PO6', 'PO8', 'O1', 'Oz', 'O2']
    assert np.array_equal(sensors, sort_topologically(sensors))
    return sensors

def get_cartesian_sensor_pos_from_bbci(filename):
    from braindevel.datautil.loaders import BBCIDataset
    filename = filename
    with h5py.File(filename, 'r') as h5file:
        sensor_names = BBCIDataset.get_all_sensors(filename, None)
        x_pos = h5file['mnt']['x'][:].squeeze()
        y_pos = h5file['mnt']['y'][:].squeeze()
        xy_pos = tuple(zip(x_pos, y_pos))
        sensor_name_pos = zip(sensor_names, xy_pos)
        sensor_name_pos_cartesian = ('cartesian', ) + tuple(sensor_name_pos)
    return sensor_name_pos_cartesian
