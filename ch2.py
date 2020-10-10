import json
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter, defaultdict


# 数据来源与bit.ly跟美国政府网站usa.gov合作提供的短链接用户那收集来的匿名数据
path = "./datasets/bitly_usagov/example.txt"
print(open(path).readline(), '文件的第一行')

# 读取数据，json库对其格式进行修改生成对象
records = [json.loads(line) for line in open(path)]
print(records[0])

print(records[0]['tz'], '数据的时区字段')

# 对时区进行计数
# 用纯Python代码进行计数
time_zones = [rec['tz'] for rec in records if 'tz' in rec]
print(time_zones[:10], '前十个数据的时区字段')


# 最直观的想法，用字典对出现的key计数
def get_counts(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts


# 在用字典计数的基础上，引入defaultdict初始化字典来简化代码
def get_counts2(sequence):
    counts = defaultdict(int)
    for x in sequence:
        counts[x] += 1
    return counts


counts_dict = get_counts(time_zones)
print(counts_dict['America/New_York'], '字典时区计数', len(time_zones), '时区总数')


# 获得字典计数的前十位时区
def top_counts(count_dict, n=10):
    value_key_pairs = [(count, tz) for tz, count in counts_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]


print(top_counts(counts_dict), '前十位时区')

# 引入collections.Counter简化计数
counts_counter = Counter(time_zones)
print(counts_counter.most_common(10), 'Counter计算出的前十时区')


# 用pandas对时区进行计数
frame = DataFrame(records)
print(frame, 'frame')
print(frame['tz'][:10], 'frame["tz"][:10]')
tz_counts = frame['tz'].value_counts()
print(tz_counts[:10], 'tz_count[:10]')
# 替换缺失值
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()
print(tz_counts[:10])
tz_counts[:10].plot(kind='barh')
# plt.show()
print(frame['a'][1], 'frame["a"][1]')
print(frame['a'][50], 'frame["a"][50]')
print(frame['a'][51], 'frame["a"][51]')
# 分离出用户访问用的浏览器
results = Series([x.split()[0] for x in frame.a.dropna()])
print(results[:5], '浏览器')
print(results.value_counts()[:8], '浏览器计数')
# 分离出用户的操作系统
cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows'),
                            'Windows', 'Not Windows')
print(operating_system[:5], '前五个用户的操作系统')
# 根据时区和操作系统进行分组
by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)
print(agg_counts[:10], '分组计数的前十')
indexer = agg_counts.sum(1).argsort()
print(indexer[:10], '升序排序后的分区计数前十')
count_subset = agg_counts.take(indexer)[-10:]
count_subset.plot(kind='barh', stacked=True)
# plt.show()
# 各行规范化为“总计为1”来观察相对比例
normed_subset = count_subset.div(count_subset.sum(1), axis=0)
normed_subset.plot(kind='barh', stacked=True)
# plt.show()


# MovieLens 1M 数据集 GroupLens Research(http://www.grouplens.org/node/73)
unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('./datasets/movielens/users.dat', sep='::', header=None, names=unames)
rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('./datasets/movielens/ratings.dat', sep='::', header=None, names=rnames)
mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('./datasets/movielens/movies.dat', sep='::', header=None, names=mnames)
print(users[:5], 'users')
print(ratings[:5], 'ratings')
print(movies[:5], 'movies')
# merge函数合并表
data = pd.merge(pd.merge(ratings, users), movies)
print(data, 'data', data.loc[0])
# 按性别计算每部电影的平均得分
mean_ratings = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
print(mean_ratings[:5], 'mean_ratings[:5]')
# 对title分组，利用size()得到一个含有鸽电影分组大小的Series对象
ratings_by_title = data.groupby('title').size()
print(ratings_by_title[:10], 'ratings_by_title[:10]')
active_titles = ratings_by_title.index[ratings_by_title >= 250]
print(active_titles)
# 选取所需行
mean_ratings = mean_ratings.loc[active_titles]
print(mean_ratings, 'mean_ratings')
# 对F列降序排序
top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)
print(top_female_ratings[:10], 'top_female_ratings[:10]')
# 计算评分分歧
# 加上存放平均得分之差的列并排序
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_values(by='diff')
# 正序排序前15， 女性更喜欢的电影
print(sorted_by_diff[:15], 'sorted_by_diff[:15]')
# 反序取出男性更喜欢的电影
print(sorted_by_diff[::-1][:15])
# 计算得分数据的方差或标准差来找出分歧最大的电影
# 根据电影名称分组的得分数据的标准差
rating_std_by_title = data.groupby('title')['rating'].std()
# 根据active_titles进行过滤
rating_std_by_title = rating_std_by_title.loc[active_titles]
# 根据值对Series进行降序排列
print(rating_std_by_title.sort_values(ascending=False)[:10])


# 1880-2010年间全美婴儿姓名
names1880 = pd.read_csv('./datasets/babynames/yob1880.txt', names=['name', 'sex', 'births'])
print(names1880, 'names1880')
# sex分组births小计
print(names1880.groupby('sex').births.sum())
# 按年度被分隔的多个文件，将所有数据都组装到一个DataFrame里
years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']
for year in years:
    path = './datasets/babynames/yob%d.txt' % year
    frame = pd.read_csv(path, names=columns)
    frame['year'] = year
    pieces.append(frame)
names = pd.concat(pieces, ignore_index=True) # 不保留read_csv返回的原始行号
print(names, 'names')
# 在year和sex级别上进行聚合
total_births = names.pivot_table('births', index='year', columns='sex', aggfunc=sum)
print(total_births.tail())
total_births.plot(title='Total births by sex and year')
plt.show()


# 插入prop列，用于存放指定名字的婴儿数相对于总出生数的比例
# 先按year和sex分组再加新列
def add_prop(group):
    births = group.births.astype(float)
    group['prop'] = births / births.sum()
    return group


names = names.groupby(['year', 'sex']).apply(add_prop)
print(names, '加了prop的数据集')
# 有效性检查，如总和是否为1或者总计值是否足够近似于1
print(np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1), '有效性检查')


# 取出该数据的一个子集：每对sex/year组合的前1000个名字
def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]


grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)
print(top1000, '每个sex/year组合的前1000个名字')


# 分析命名趋势
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']
# 按year和name统计的总出生数透视表
total_births = top1000.pivot_table('births', index='year', columns='name', aggfunc=sum)
subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
subset.plot(subplots=True, figsize=(12, 10), grid=False, title="Number of births per year")
plt.show()

# 评估命名多样性的增长
# 方法一.计算最流行的1000鸽名字所占比例
table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
table.plot(title='Sum of table 1000.prop by year and sex', yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))
# 方法二.计算占总出生人数前50%的不同名字的数量
df = boys[boys.year == 2010]
prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
print(prop_cumsum[:10], 'prop_cumsum[:10]')
print(prop_cumsum.searchsorted(0.5))
df = boys[boys.year == 1900]
in1900 = df.sort_values(by='prop', ascending=False).prop.cumsum()
print(in1900.searchsorted(0.5) + 1, 'in1900.searchsorted(0.5) + 1')


def get_quantile_count(group, q=0.5):
    group = group.sort_values(by='prop', ascending=False)
    return group.prop.cumsum().searchsorted(q) + 1


diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
diversity.plot(title='Number of popular names in top 50%')


# "最后一个字母"的变革
# 从name列取出最后一个字母
get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'

table = names.pivot_table('births', index=last_letters, columns=['sex', 'year'], aggfunc=sum)
subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
print(subtable.head(), 'subtable.head()')
print(subtable.sum(), 'subtable.sum()')
letter_prop = subtable / subtable.sum().astype(float)
fig, axes = plt.subplots(2, 1, figsize=(10, 8))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female', legend=False)

letter_prop = table / table.sum().astype(float)
dny_ts = letter_prop.ix[['d', 'n', 'y'], 'M'].T
print(dny_ts.head(), 'dny_ts.head()')
dny_ts.plot()


# 变成女孩名字的男孩名字(以及相反的情况)
# 找出其中以"lesl"开头的一组名字
all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])
lesley_like = all_names[mask]
print(lesley_like, 'lesley_like')
# 利用这个结果过滤其他名字，并按名字分组计算出生数以查看相对频率
filtered = top1000[top1000.name.isin(lesley_like)]
print(filtered.groupby('name').births.sum(), 'filtered.groupby("name").births.sum()')
# 按性别和年度聚合，按年度进行规范化处理
table = filtered.pivot_table('births', index='year', columns='sex', aggfunc='sum')
table = table.div(table.sum(1), axis=0)
print(table.tail(), 'table.tail()')
table.plot(style={'M': 'k-', 'F': 'k--'})
plt.show()
