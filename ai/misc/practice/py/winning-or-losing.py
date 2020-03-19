import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# 0 = O, 1 = X, 0.5 = N/A
data = np.array([

    [
        [0, 0.5, 1],
        [0.5, 0, 0.5],
        [1, 0.5, 0]
    ],
    [
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 1]
    ],
    [
        [0, 1, 1],
        [0, 0, 0],
        [1, 0, 1]
    ],
    [
        [1, 1, 1],
        [1, 0, 0],
        [0, 0, 1]
    ],
    [
        [1, 1, 0],
        [1, 0, 0],
        [1, 0, 1]
    ],
    [
        [0, 1, 0],
        [1, 0, 1],
        [1, 0, 1]
    ],
    [
        [0, 0.5, 1],
        [1, 0, 1],
        [0, 0.5, 1]
    ],
    [
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 1]
    ],

])
# 0 = O, 1 = X, 0.5 = DRAW
expect = np.array([
    0, 2, 0, 1, 1, 2, 1, 2
])

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(3, 3)),
    tf.keras.layers.Dense(9, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
history = model.fit(data, expect, epochs=500, verbose=False)

# plt.xlabel('Iterácia (eopch)')
# plt.ylabel('Chyba (loss)')
# plt.plot(history.history['loss'])
# plt.show()

predictions = model.predict([
    [
        [0, 1, 1],
        [0.5, 0, 0],
        [1, 0.5, 0]
    ],
    [

        [1, 1, 0],
        [0, 0.5, 0],
        [0.5, 0, 0]
    ],
    [
        [1, 1, 1],
        [1, 0, 0],
        [0, 0, 0.5]
    ]
])
print(np.argmax(predictions[0]), predictions[0])
print(np.argmax(predictions[1]), predictions[1])
print(np.argmax(predictions[2]), predictions[2])
