import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

celsius = np.array([-40, -10, 0, 8, 15, 22, 38], dtype=float)
fahrenheit = np.array([-40, 14, 32, 46, 59, 72, 100], dtype=float)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[1])
])
model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.Adam(0.1))
history = model.fit(celsius, fahrenheit, epochs=500, verbose=False)

plt.xlabel('Iterácia (eopch)')
plt.ylabel('Chyba (loss)')
plt.plot(history.history['loss'])
plt.show()

print(model.predict([0]))
