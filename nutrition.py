carbon_per_kilo = 3.6
protein_per_kilo = 1.6
fat_per_kilo = 1
bodyweight = 70

cday = carbon_per_kilo * bodyweight
pday = protein_per_kilo * bodyweight
fday = fat_per_kilo * bodyweight

# 碳水日内分配
# 早饭：全天碳水的30%，GI无所谓
breakfast_carbon_ratio = .3
breakfast_carbon_GI = 'ALL'

# 训练前：全天碳水的20%，中等GI，蛋白质可吃可不吃
# 练前一刻钟
before_training_carbon_ratio = .2

# 训后：全天碳水的50%,高GI碳水
# 训后立刻，最迟半小时能吃上
after_training_carbon_ratio = .5

carbon_breakfast = cday * breakfast_carbon_ratio
carbon_before_training = cday * before_training_carbon_ratio
carbon_after_training = cday * after_training_carbon_ratio

# 其他餐
# 不吃碳水
# 吃少量脂肪，瘦肉，蔬菜

# 休息日，碳水不讲究

# 碳水分配如果晚上训练
# 早饭30% 午饭 晚饭 训前餐20% 训练  训后餐50%

# 碳水动态配比
# 腿/背 > 胸 > 肩/手臂 > 休息日
carbon_train_fit_ratio = {
    'back': 1.05,
    'chest': 1.03,
    'shoulder': 1.03,
    'rest': 1,
}

# kcalCalc
carbon_kcal_ratio = 4.1
protein_kcal_ratio = 4.1
fat_kcal_ratio = 9.3
# 消耗很难精确计算

# 热量平衡：体重不变，
# 干净增肌 热量盈余10-20%
good_gain_ratio = 1.15
# 持续减脂 热量缺口10-20%
good_lose_ratio = .85

kcal_perday_ate = cday * carbon_kcal_ratio + \
                  pday * protein_kcal_ratio + \
                  fday * fat_kcal_ratio

# 看体重变化
# 增肌月增1-3斤就合适
# 减脂月减2-5斤就合适
# 碳水调整尺度 .3-.5g

protein_times = 4
protein_each = pday / protein_times
# 训后一定要有一次蛋白质

# 脂肪 总量符合要求就行
# 训后餐尽量低脂

protein_breakfast = protein_each
fat_breakfast = 20
takein_breakfast = {'carbon': carbon_breakfast,
                    'protein': protein_breakfast,
                    'fat': fat_breakfast}

# 训前餐,蛋白质随意,脂肪一般不吃
protein_before_training = protein_each
fat_before_training = 0
takein_before_training = {'carbon': carbon_before_training,
                          'protein': protein_before_training,
                          'fat': fat_before_training}

# 训后餐,高碳水,蛋白质一次,低脂
protein_after_training = protein_each
fat_after_training = 10
takein_after_training = {'carbon': carbon_after_training,
                         'protein': protein_after_training,
                         'fat': fat_after_training}

takein_rest = {
    'carbon': cday - carbon_breakfast - carbon_before_training - carbon_after_training,
    'protein': pday - protein_breakfast - protein_before_training - protein_after_training,
    'fat': fday - fat_breakfast - fat_before_training - fat_after_training
}

print('takein_breakfast', takein_breakfast)
print('takein_before_training', takein_before_training)
print('takein_after_training', takein_after_training)
print('takein_rest', takein_rest)
# nutrition
# 每餐食谱生成，问chat
# 一个鸡蛋：6g 蛋白质，5g脂肪
# 一盒牛奶： 6g 碳水 9g脂肪 9g蛋白质
