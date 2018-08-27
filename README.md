
# imgClassification
남녀 얼굴사진을 학습시켜 구분 (tensorflow)
<br>
ImgScrapy.py => data 수집  
FaceDetection.py => 수집된 데이터 얼굴부분만 crop, resize (feat. openCV)  

## requirements
    cv2
    tensorflow
    numpy
    pandas
    urllib
    bs4
    selenium
    
## how to run
    1) image scrap
        python3 ImgScrapy.py searchWord_1 [searchWord_2] ... [searchWord_N]
        
    2) image preprocessing
        python3 FaceDetection.py
<br>

## model graph
<br>

![1_uuyc126ru4mntwwckebctw 2x](https://user-images.githubusercontent.com/35649392/43726611-9839f3ae-99da-11e8-8d91-49774e1878ea.png)

![gender_cnn](https://user-images.githubusercontent.com/35649392/43726804-15f8bb86-99db-11e8-990e-5fccadd3cdce.png)


## model code
특이사항: one by one convolution (is used in Google Inception Module)

    X = tf.placeholder(tf.float32, [None, 80 * 80])
    X_img = tf.reshape(X, [-1, 80, 80, 1])
    Y = tf.placeholder(tf.float32, [None, 1])

    with tf.name_scope('L1') as scope:
        W1 = tf.Variable(tf.random_normal([3, 3, 1, 32], stddev=0.01))
        L1 = tf.nn.conv2d(X_img, W1, strides=[1, 1, 1, 1], padding='SAME')
        L1 = tf.nn.relu6(L1)
        L1 = tf.nn.max_pool(L1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    with tf.name_scope('L2') as scope:
        # one by one convolution for dimensionality reduction
        _W2 = tf.Variable(tf.random_normal([1, 1, 32, 5]))
        _L2 = tf.nn.conv2d(L1, _W2, strides=[1, 1, 1, 1], padding='SAME')

        W2 = tf.Variable(tf.random_normal([3, 3, 5, 64], stddev=0.01))
        L2 = tf.nn.conv2d(_L2, W2, strides=[1, 1, 1, 1], padding='SAME')
        L2 = tf.nn.relu6(L2)
        L2 = tf.nn.max_pool(L2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    with tf.name_scope('L3') as scope:
        # one by one convolution for dimensionality reduction
        _W3 = tf.Variable(tf.random_normal([1, 1, 64, 5]))
        _L3 = tf.nn.conv2d(L2, _W3, strides=[1, 1, 1, 1], padding='SAME')

        W3 = tf.Variable(tf.random_normal([3, 3, 5, 128], stddev=0.01))
        L3 = tf.nn.conv2d(_L3, W3, strides=[1, 1, 1, 1], padding='SAME')
        L3 = tf.nn.relu6(L3)
        L3 = tf.nn.max_pool(L3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    with tf.name_scope('L4') as scope:
        # one by one convolution for dimensionality reduction
        _W4 = tf.Variable(tf.random_normal([1, 1, 128, 5]))
        _L4 = tf.nn.conv2d(L3, _W4, strides=[1, 1, 1, 1], padding='SAME')

        W4 = tf.Variable(tf.random_normal([3, 3, 5, 256], stddev=0.01))
        L4 = tf.nn.conv2d(_L4, W4, strides=[1, 1, 1, 1], padding='SAME')
        L4 = tf.nn.relu6(L4)
        L4 = tf.nn.max_pool(L4, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    with tf.name_scope('L5_FC') as scope:
        L4_flat = tf.reshape(L4, [-1, 5 * 5 * 256])
        W5 = tf.get_variable("W5", shape=[5 * 5 * 256, 5 * 5 * 128], initializer=tf.contrib.layers.xavier_initializer())
        b5 = tf.Variable(tf.random_normal([5 * 5 * 128]))
        L5 = tf.nn.relu6(tf.matmul(L4_flat, W5) + b5)
        L5 = tf.nn.dropout(L5, keep_prob=keep_prob)

    with tf.name_scope('L6_FC') as scope:
        W6 = tf.get_variable("W6", shape=[5 * 5 * 128, 1], initializer=tf.contrib.layers.xavier_initializer())
        b6 = tf.Variable(tf.random_normal([1]))
        logits = tf.matmul(L5, W6) + b6
        hypothesis = tf.sigmoid(logits)

## accuracy & cost (tensorBoard)
<br>

![accuracy_cost](https://user-images.githubusercontent.com/35649392/43726947-94badb5c-99db-11e8-8ba1-b43bd7ba3e91.png)

epoch 40 부터 오버피팅 되는 것 같음.
