# -*- coding: utf-8 -*-
"""
实验一些TensorFlow的一些例子
"""

from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf


def soft_max():
    """
    y = softmax(Wx+b)
    :return:
    """
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
    sess = tf.InteractiveSession()
    x = tf.placeholder(tf.float32, [None, 784])
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))
    y = tf.nn.softmax(tf.matmul(x, W) + b)

    # 损失函数计算
    y_ = tf.placeholder(tf.float32, [None, 10])
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

    # 优化算法, 学习速率为0.5, 损失函数为cross_entropy
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
    # 全局参数初始化器
    tf.global_variables_initializer().run()

    for i in range(1000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        train_step.run({x: batch_xs, y_: batch_ys})
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print(accracy.eval({x: mnist.test.images, y_: mnist.test.labels}))


def main():
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

    print(mnist.train.images, mnist.train.labels.shape)
    print(mnist.test.images.shape, mnist.test.labels.shape)
    print(mnist.validation.images.shape, mnist.validation.labels.shape)


if __name__ == '__main__':
    soft_max()
