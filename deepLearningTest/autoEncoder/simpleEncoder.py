# -*- coding: UTF-8 -*-

"""
对于自编码器的简单使用。
"""

import numpy as np
import sklearn.preprocessing as prep
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


class AdditiveAutoEncoder(object):
    def __init__(self, n_input, n_hidden, transfer_function=tf.nn.softplus, optimizer=tf.train.AdamOptimizer(),
                 scale=0.1):
        self.n_input = n_input
        self.n_hidden = n_hidden
        self.transfer = transfer_function
        self.scale = tf.placeholder(tf.float32)
        self.training_scale = scale
        network_weights = self._initialize_weights()
        self.weights = network_weights
        # 为输入x创建一个维度为n_input的placeholder
        self.x = tf.placeholder(tf.float32, [None, self.n_input])
        # 建立隐含层
        self.hidden = self.transfer(tf.add(tf.matmul(
            self.x + scale * tf.random_normal((n_input,)),
            self.weights['w1']), self.weights['b1']))
        # 建立还原层
        self.reconstruction = tf.add(tf.matmul(self.hidden, self.weights['w2']), self.weights['b2'])
        # 定义自编码器的损失函数
        self.cost = 0.5 * tf.reduce_sum(tf.pow(tf.subtract(self.reconstruction, self.x), 2.0))
        self.optimizer = optimizer.minimize(self.cost)
        init = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(init)

    # 初始化参数
    def _initialize_weights(self):
        """
        参数初始化
        :return:
        """
        all_weights = dict()
        all_weights['w1'] = tf.Variable(xavier_init(self.n_input, self.n_hidden))
        all_weights['b1'] = tf.Variable(tf.zeros([self.n_hidden], dtype=tf.float32))
        all_weights['w2'] = tf.Variable(tf.zeros([self.n_hidden, self.n_input], dtype=tf.float32))
        all_weights['b2'] = tf.Variable(tf.zeros([self.n_input], dtype=tf.float32))
        return all_weights

    # 定义计算损失cost
    def partial_fit(self, X):
        cost, opt = self.sess.run((self.cost, self.optimizer), feed_dict={self.x: X, self.scale: self.training_scale})
        return cost

    # 只求损失cost的函数
    def calc_total_cost(self, X):
        return self.sess.run(self.cost, feed_dict={self.x: X, self.scale: self.training_scale})

    # 返回自编码器隐含层的输出结果
    def transform(self, X):
        return self.sess.run(self.hidden, feed_dict={self.x: X, self.scale: self.training_scale})

    # 将隐含层的输出结果作为输入，复原为原始数据
    def generate(self, hidden=None):
        if hidden is None:
            hidden = np.random.normal(size=self.weights['b1'])
        return self.sess.run(self.reconstruction, feed_dict={self.hidden: hidden})

    # 整体运行一边复原函数
    def reconstruct(self, X):
        return self.sess.run(self.reconstruction, feed_dict={self.x: X, self.scale: self.training_scale})

    # 获取隐含层的权重w1
    def getWeights(self):
        return self.sess.run(self.weights['w1'])

    # 获取隐含层的偏置系数b1
    def getBiases(self):
        return self.sess.run(self.weights['b1'])


def xavier_init(fan_in, fan_out, constant=1):
    """
    让权重被初始化的正好，满足均值为0，方差为2/(nin+nout)
    :param fan_in: 输入节点的数量
    :param fan_out: 输出节点的数量
    :param constant:
    :return:
    """
    low = -constant * np.sqrt(6.0 / (fan_in + fan_out))
    high = constant * np.sqrt(6.0 / (fan_in + fan_out))
    return tf.random_uniform((fan_in, fan_out), minval=low, maxval=high, dtype=tf.float32)


def standard_scale(X_train, X_test):
    """
    对训练集和测试集进行标准化
    :param X_train: 训练集
    :param X_test: 测试集
    :return:
    """
    preprocessor = prep.StandardScaler().fit(X_train)
    X_train = preprocessor.transform(X_train)
    X_test = preprocessor.transform(X_test)
    return X_train, X_test


def get_random_block_from_data(data, batch_size):
    """
    获取一个随机block数据，初始位置随机，长度为batch_size
    :param data: 数据集
    :param batch_size:一组数据的大小
    :return:
    """
    start_index = np.random.randint(0, len(data) - batch_size)
    return data[start_index:(start_index + batch_size)]


# 获取数据集
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
# 数据初始化
X_train, X_test = standard_scale(mnist.train.images, mnist.test.images)

# 训练数据集的大小
n_samples = int(mnist.train.num_examples)

# 训练轮数
train_epochs = 2000
# 一组数据的大小
batch_size = 128
display_step = 1

# 创建一个自编码器的实例
autoencoder = AdditiveAutoEncoder(n_input=784, n_hidden=200, transfer_function=tf.nn.softplus,
                                  optimizer=tf.train.AdamOptimizer(learning_rate=0.001), scale=0.01)

for epoch in range(train_epochs):
    avg_cost = 0.
    # 单次训练次数
    total_batch = int(n_samples / batch_size)
    for i in range(total_batch):
        batch_xs = get_random_block_from_data(X_train, batch_size)

        # 计算总损失值
        cost = autoencoder.partial_fit(batch_xs)
        # 计算平均损失值
        avg_cost += cost / n_samples * batch_size

    if epoch % display_step == 0:
        print("Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(avg_cost))

print("Total cost:" + str(autoencoder.calc_total_cost(X_test)))
