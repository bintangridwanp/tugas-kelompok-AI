import os
import librosa
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Konfigurasi awal
DATA_PATH = "ravdess/"  # ganti sesuai folder dataset
SAVED_MODEL_NAME = "model_ravdess_cnn.h5"
EMOTIONS = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

def extract_features(file_path, max_pad_len=216):  # Panjang 216 tergantung pada sampling
    try:
        audio, sample_rate = librosa.load(file_path, res_type='kaiser_fast', duration=3, sr=22050, offset=0.5)
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        pad_width = max_pad_len - mfccs.shape[1]
        if pad_width > 0:
            mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
        else:
            mfccs = mfccs[:, :max_pad_len]
        return mfccs
    except Exception as e:
        print("Error processing {}: {}".format(file_path, e))
        return None

def load_data():
    x_data, y_data = [], []
    for root, _, files in os.walk(DATA_PATH):
        for file in files:
            if file.endswith(".wav"):
                file_path = os.path.join(root, file)
                emotion = EMOTIONS[file.split("-")[2]]
                label = list(EMOTIONS.values()).index(emotion)
                mfcc = extract_features(file_path)
                if mfcc is not None:
                    x_data.append(mfcc)
                    y_data.append(label)
    return np.array(x_data), np.array(y_data)

# Load dan preprocess data
print("Loading data...")
X, y = load_data()
X = X[..., np.newaxis]  # Tambahkan channel untuk CNN: (samples, 40, 216, 1)
X = X.astype('float32')
y = to_categorical(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Arsitektur CNN
model = Sequential()
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=(40, 216, 1)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.3))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.3))

model.add(Conv2D(256, kernel_size=(3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.3))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(len(EMOTIONS), activation='softmax'))

# Kompilasi
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Training
print("Training model...")
model.fit(X_train, y_train, batch_size=32, epochs=1, validation_data=(X_test, y_test))

# Simpan model
# Simpan model
model.save("model_ravdess_cnn.h5")
print("Model saved to model_ravdess_cnn.h5")

