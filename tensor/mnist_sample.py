import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D


def get_preprocessed_data():
    # Get mnist data
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    # Reshape data for keras API
    x_train = x_train.reshape(x_train.shape[0], 28, 28, 1).astype('float32')
    x_test = x_test.reshape(x_test.shape[0], 28, 28, 1).astype('float32')
    # Normalize input ([0,1])
    x_train /= 255
    x_test /= 255
    return (x_train, y_train), (x_test, y_test)


def setup_network():
    input_shape = (28, 28, 1)
    # Set up basic NN model
    model = Sequential()
    model.add(Conv2D(28, kernel_size=(3, 3), input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())  # Flattening the 2D arrays for fully connected layers
    model.add(Dense(128, activation=tf.nn.relu))
    model.add(Dropout(0.2))
    model.add(Dense(10, activation=tf.nn.softmax))
    # Compile graph with optimizer/loss/metrics
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


def do_tf_work():
    (x_train, y_train), (x_test, y_test) = get_preprocessed_data()
    model = setup_network()
    # Fit model to dataset
    model.fit(x=x_train, y=y_train, epochs=1)

    # Evaluate model on test set
    model.evaluate(x_test, y_test)

    # Select id 4444 of the test data and run prediction, gt=9
    image_index = 4444
    pred = model.predict(x_test[image_index].reshape(1, 28, 28, 1))
    print(pred.argmax())
