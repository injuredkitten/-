import pandas as pd
import numpy as np
import tensorflow as tf

# 设置GPU设备
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)  # 启用内存增长
    print(f"Using GPU: {gpus[0]}")  # 默认选择第一个 GPU
else:
    print("No GPU available.")

# 数据加载
Book = pd.read_csv('data/BX-Books.csv', sep=None, on_bad_lines='skip', engine='python', encoding='ISO-8859-1')
Book = Book[['ISBN', 'Book-Title']]
Book['index'] = Book.index

Rating = pd.read_csv('data/BX-Book-Ratings.csv', sep=None, on_bad_lines='skip', engine='python', encoding='ISO-8859-1')
Rating = Rating[:10000]

i = 0
for x in set(Rating['User-ID']):
    Rating.loc[Rating['User-ID'] == x, 'userId'] = i
    i += 1

Rating['userId'] = Rating['userId'].astype(int)

Rating.columns = ['User-ID', 'ISBN', 'rating', 'userId']
ratings_df = pd.merge(Rating, Book, on='ISBN')

ratings_df = ratings_df[['userId', 'index', 'rating']]

userNo = ratings_df['userId'].max() + 1
bookNo = ratings_df['index'].max() + 1

rating = np.zeros((bookNo, userNo))
flag = 0
ratings_df_length = np.shape(ratings_df)[0]
for index, row in ratings_df.iterrows():
    rating[int(row['index']), int(row['userId'])] = row['rating']
    flag += 1
    print('processed %d, %d left' % (flag, ratings_df_length - flag))

record = rating > 0
record = np.array(record, dtype=int)


def normalizeRatings(rating, record):
    m, n = rating.shape
    rating_mean = np.zeros((m, 1))
    rating_norm = np.zeros((m, n))
    for i in range(m):
        idx = record[i, :] != 0
        rating_mean[i] = np.mean(rating[i, idx])
        rating_norm[i, idx] -= rating_mean[i]
    return rating_norm, rating_mean


rating_norm, rating_mean = normalizeRatings(rating, record)

rating_norm = np.nan_to_num(rating_norm)
rating_mean = np.nan_to_num(rating_mean)

num_features = 10

X_parameters = tf.Variable(tf.random.normal([bookNo, num_features], stddev=0.35))
Theta_parameters = tf.Variable(tf.random.normal([userNo, num_features], stddev=0.35))

optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)

# 使用 GradientTape 计算梯度
for i in range(4000):
    print(f'Epoch {i}')
    with tf.GradientTape() as tape:
        loss_value = 1 / 2 * tf.reduce_sum(
            ((tf.matmul(X_parameters, Theta_parameters, transpose_b=True) - rating_norm) * record) ** 2) + 1 / 2 * (
                                 tf.reduce_sum(X_parameters ** 2) + tf.reduce_sum(Theta_parameters ** 2))

    gradients = tape.gradient(loss_value, [X_parameters, Theta_parameters])
    optimizer.apply_gradients(zip(gradients, [X_parameters, Theta_parameters]))

    # 记录 loss 值
    with tf.summary.create_file_writer('./result').as_default():
        tf.summary.scalar('loss', loss_value, step=i)

# 保存模型
model = tf.keras.Model(inputs=[X_parameters, Theta_parameters], outputs=loss_value)
model.save('./model/BookModel')

# 加载模型
model = tf.keras.models.load_model('./model/BookModel')

# 预测
Current_X_parameters, Current_Theta_parameters = X_parameters.numpy(), Theta_parameters.numpy()
predicts = np.dot(Current_X_parameters, Current_Theta_parameters.T) + rating_mean
errors = np.sqrt(np.sum((predicts - rating) ** 2))

# 推荐
userId = 666
sortedResult = predicts[:, int(userId)].argsort()[::-1]
idx = 0
print('为该用户推荐的评分最高的20部书籍是：'.center(80, '='))
for i in sortedResult:
    print(f'score: {predicts[i, int(userId)]:.3f}, book name: {Book.iloc[i]["Book-Title"]}')
    idx += 1
    if idx == 20:
        break
