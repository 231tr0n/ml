import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Input

(X, Y) = load_digits(return_X_y=True)

plt.gray()
plt.matshow(X[0].reshape(8, 8))
plt.show()

x_train, x_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.20, random_state=4
)

x_train_cnn = np.array(x_train).reshape(len(x_train), 8, 8, 1)
x_test_cnn = np.array(x_test).reshape(len(x_test), 8, 8, 1)

accuracy = {}

model = Sequential()
model.add(Dense(64, activation="relu"))
model.add(Dense(68, activation="relu"))
model.add(Dense(40, activation="relu"))
model.add(Dense(1, activation="linear"))
model.compile(optimizer="adam", loss="mean_squared_error", metrics=["accuracy"])
history = model.fit(x_train, y_train, epochs=20, verbose=1)
accuracy["nn"] = max(history.history["accuracy"])


model = Sequential()
model.add(Input(shape=(8, 8, 1)))
model.add(Conv2D(32, kernel_size=2, activation="relu"))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(64, activation="relu"))
model.add(Dense(1, activation="linear"))
model.compile(optimizer="adam", loss="mean_squared_error", metrics=["accuracy"])
model.fit(x_train_cnn, y_train, epochs=20, verbose=1)
accuracy["cnn"] = max(history.history["accuracy"])

plt.bar(list(accuracy.keys()), list(accuracy.values()), color="green")
plt.show()
