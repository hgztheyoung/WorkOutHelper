# splitting
import warnings
import pandas as pd
import io
import random

warnings.simplefilter(action='ignore', category=FutureWarning)

splits = {
    '五分化': '背 胸 肩 手 腿腹'.split(' '),
    '四分化': '背肩后束 胸肩前中束 手 腿腹'.split(' '),
    '三分化': '背肩后束肱二头 胸肩前中束肱三头  腿腹'.split(' '),
}

# 每周应该练3~5次
# 矢状面 水平面 额状面=冠状面


moves_csv = f'''index,部位,训练类型,动作,index2,Muscle Group,Exercise Type,Exercise
0,胸,推胸,杠铃卧推,0,Chest,Pushing,Barbell Bench Press
1,胸,推胸,哑铃卧推,1,Chest,Pushing,Dumbbell Bench Press
2,胸,推胸,史密斯卧推,2,Chest,Pushing,Smith Machine Bench Press
3,胸,推胸,器械推胸,3,Chest,Pushing,Machine Chest Press
4,胸,推胸,俯卧撑,4,Chest,Pushing,Push-Up
5,胸,推胸,双杠臂屈伸,5,Chest,Pushing,Dip
6,胸,夹胸,蝴蝶机夹胸,6,Chest,Flyes,Butterfly Machine Flyes
7,胸,夹胸,龙门架夹胸,7,Chest,Flyes,Pec Deck Machine Flyes
8,胸,夹胸,仰卧哑铃飞鸟,8,Chest,Flyes,Incline Dumbbell Flyes
9,胸,夹胸,仰卧龙门架飞鸟,9,Chest,Flyes,Incline Pec Deck Machine Flyes
10,肩前束,推举,哑铃推举,10,Front Deltoid,Press,Dumbbell Shoulder Press
11,肩前束,推举,杠铃推举,11,Front Deltoid,Press,Barbell Shoulder Press
12,肩前束,推举,器械推举,12,Front Deltoid,Press,Machine Shoulder Press
13,肩前束,推举,史密斯推举,13,Front Deltoid,Press,Smith Machine Shoulder Press
14,肩前束,前平举,哑铃前平举,14,Front Deltoid,Raise,Dumbbell Front Raise
15,肩前束,前平举,龙门架前平举,15,Front Deltoid,Raise,Pec Deck Machine Front Raise
16,肩前束,前平举,杠铃前平举,16,Front Deltoid,Raise,Barbell Front Raise
17,肩前束,前平举,杠铃片前平举,17,Front Deltoid,Raise,Plate Front Raise
18,股四头,膝关节伸,杠铃深蹲,18,Quadriceps,Extension,Barbell Squat
19,股四头,膝关节伸,哈克机,19,Quadriceps,Extension,Hack Squat Machine
20,股四头,膝关节伸,倒蹬机,20,Quadriceps,Extension,Seated Leg Press Machine
21,股四头,膝关节伸,箭步蹲,21,Quadriceps,Extension,Lunge
22,股四头,膝关节伸,器械腿屈伸,22,Quadriceps,Extension,Leg Extension Machine
23,股二头,膝关节屈,器械腿弯举,23,Hamstrings,Flexion,Seated Leg Curl Machine
24,股二头,膝关节屈,北欧挺,24,Hamstrings,Flexion,Nordic Hamstring Curl
25,股二头,髋关节伸,硬拉,25,Glutes,Extension,Straight Leg Deadlift
26,股二头,髋关节伸,哈克机,26,Glutes,Extension,Hip Thrust Machine
27,股二头,髋关节伸,倒蹬机,27,Glutes,Extension,Seated Leg Press Machine
28,背,划船,杠铃划船,28,Back,Row,Barbell Bent-Over Row
29,背,划船,哑铃划船,29,Back,Row,Dumbbell Bent-Over Row
30,背,划船,器械划船,30,Back,Row,Machine Row
31,背,划船,直臂下压,31,Back,Row,Straight-Arm Pulldown
32,背,划船,T杆划船,32,Back,Row,T-Bar Row
33,背,划船,坐姿钢线划船,33,Back,Row,Seated Cable Row
34,背,下拉,引体向上,34,Back,Pull-Up,Pull-Up
35,背,下拉,高位下拉,35,Back,Pull-Down,Lat Pulldown
36,背,下拉,器械下拉,36,Back,Pull-Down,Machine Pulldown
37,肩中束,侧平举,哑铃侧平举,37,Middle Deltoid,Side Raise,Dumbbell Side Raise
38,肩中束,侧平举,龙门架侧平举,38,Middle Deltoid,Side Raise,Pec Deck Machine Side Raise
39,肩中束,侧平举,器械侧平举,39,Middle Deltoid,Side Raise,Machine Side Raise
40,肩中束,侧平举,杠铃片侧平举,40,Middle Deltoid,Side Raise,Plate Side Raise
41,肩中束,提拉,杠铃提拉,41,Middle Deltoid,Rear Delt Flye,Barbell Rear Delt Flye
42,肩中束,提拉,龙门架提拉,42,Middle Deltoid,Rear Delt Flye,Cable Rear Delt Flye
43,臀,髋关节伸,屯冲,43,Glutes,Extension,Glute Bridge
44,臀,髋关节伸,臀桥,44,Glutes,Extension,Barbell Hip Thrust
45,臀,髋关节伸,后踢,45,Glutes,Extension,Donkey Kick
46,臀,髋关节伸,硬拉,46,Glutes,Extension,Straight Leg Deadlift
47,臀,髋关节伸,哈克机,47,Glutes,Extension,Hip Thrust Machine
48,臀,髋关节伸,倒蹬机,48,Glutes,Extension,Seated Leg Press Machine
49,臀,髋关节外展,器械髋外展,49,Glutes,Abduction,Machine Hip Abduction
50,臀,髋关节外展,龙门架髋外展,50,Glutes,Abduction,Pec Deck Machine Hip Abduction
51,肱三头,臂屈伸,龙门架绳索臂屈伸,51,Triceps,Extension,Cable Tricep Extension
52,肱三头,臂屈伸,过顶臂屈伸,52,Triceps,Extension,Overhead Tricep Extension
53,肱三头,臂屈伸,反手臂屈伸,53,Triceps,Extension,Reverse Grip Tricep Extension
54,肱三头,臂屈伸,直杆下压,54,Triceps,Extension,Lying Tricep Extension
55,肱三头,臂屈伸,杠铃仰卧臂屈伸,55,Triceps,Extension,Barbell Skull Crusher
56,肱三头,臂屈伸,哑铃颈后臂屈伸,56,Triceps,Extension,Dumbbell Overhead Tricep Extension
57,肱二头,弯举,哑铃弯举,57,Biceps,Curl,Dumbbell Curl
58,肱二头,弯举,杠铃弯举,58,Biceps,Curl,Barbell Curl
59,肱二头,弯举,器械弯举,59,Biceps,Curl,Machine Curl
60,肱二头,弯举,集中弯举,60,Biceps,Curl,Concentration Curl
61,肱二头,弯举,牧师椅弯举,61,Biceps,Curl,Preacher Curl
62,肱二头,弯举,龙门架弯举,62,Biceps,Curl,Cable Curl
63,肩后束,反向飞鸟,哑铃俯身飞鸟,63,Rear Deltoid,Reverse Flye,Dumbbell Rear Delt Flye
64,肩后束,反向飞鸟,蝴蝶机反向飞鸟,64,Rear Deltoid,Reverse Flye,Butterfly Machine Reverse Flye
65,肩后束,反向飞鸟,面拉,65,Rear Deltoid,Reverse Flye,Face Pull
66,肩后束,反向飞鸟,龙门架俯身飞鸟,66,Rear Deltoid,Reverse Flye,Cable Rear Delt Flye
67,肩后束,反向飞鸟,龙门架反向飞鸟,67,Rear Deltoid,Reverse Flye,Machine Rear Delt Flye
68,肩后束,上背划船,开肘打宽握距拉向胸口偏上的划船,68,Upper Back,High Row,Wide-Grip Cable Row
69,腹,卷腹,器械卷腹,69,Abdominals,Crunch,Machine Crunch
70,腹,卷腹,仰卧平板卷腹,70,Abdominals,Crunch,Incline Bench Crunch
71,腹,卷腹,龙门架跪姿卷腹,71,Abdominals,Crunch,Cable Kneeling Crunch
72,腹,举腿,悬垂举腿,72,Abdominals,Leg Raise,Hanging Leg Raise
73,腹,举腿,仰卧平板举腿,73,Abdominals,Leg Raise,Seated Leg Raise
74,背,脊柱伸,山羊挺身,74,Back,Spinal Extension,goat stand up'''

df = pd.read_csv(io.StringIO(moves_csv))

move_details = \
    {'上背划船': ['肩关节伸', '肩关节水平外展'],
     '下拉': ['肩关节内收'],
     '举腿': ['骶椎脊柱屈'],
     '侧平举': ['肩关节外展'],
     '划船': ['肩关节伸'],
     '前平举': ['肩关节屈'],
     '卷腹': ['胸椎腰椎脊柱屈'],
     '反向飞鸟': ['肩关节水平外展'],
     '夹胸': ['肩关节水平内收'],
     '弯举': ['肘关节屈'],
     '推举': ['肩关节屈', '肩关节外展'],
     '推胸': ['肩关节水平内收', '肩关节屈', '肘关节伸'],
     '提拉': ['肩关节外展', '肘关节屈'],
     '膝关节伸': ['膝关节伸'],
     '膝关节屈': ['膝关节屈'],
     '臂屈伸': ['肘关节伸'],
     '髋关节伸': ['髋关节伸'],
     '髋关节外展': ['髋关节外展'],
     '脊柱伸': ['脊柱伸']}
detail_defs = {
    '肩关节水平内收': '胸大肌+肩前束 水平面上大臂从外向内运动',
    '肩关节屈': '胸大肌+肩前束 矢状面上大臂从后向前运动',
    '肘关节伸': '肱三头肌 肘关节从折叠变为打直的运动',
    '肘关节屈': '肱二头肌 肘关节从打直变为折叠的运动',
    '肩关节伸': '背阔肌+大圆肌+肱三头肌长头+肩后束 矢状面上大臂从前往后的运动',
    '肩关节水平外展': '肩后束+冈下肌 水平面上大臂从内向外运动',
    '肩关节内收': '背阔肌+大圆肌 额状面上大臂从外向内运动',
    '肩关节外展': '肩中束+冈下肌 额状面上大臂从内往外的运动',
    '膝关节伸': '股四头肌 膝关节从折叠变为打直的运动',
    '膝关节屈': '股二头肌 膝关节从打直变为折叠的运动',
    '髋关节伸': '股二头肌+臀大肌 矢状面上大腿从前往后运动',
    '髋关节外展': '臀大肌+臀中肌+阔筋膜张肌 额状面上大腿从内往外运动',
    '胸椎腰椎脊柱屈': '腹直肌 胸椎腰椎脊柱弯曲的运动',
    '骶椎脊柱屈': '腹直肌 骶椎脊柱弯曲的运动',
    '脊柱伸': '竖脊肌 脊柱从弯曲到伸展的运动'
}


def select_one_move_by_type(t, df=df):
    return random.choice(list(df[df['训练类型'] == t]['动作']))


split3_training_pain = \
    [
        [[{'部位': '背',
           '动作数': 3,
           '组数': 3,
           '动作选择': [['下拉', '下拉', '划船'], ['下拉', '划船', '划船']]}],
         [{'部位': '肩后束',
           '动作数': 2,
           '组数': 3,
           '动作选择': [['反向飞鸟', '上背划船'], ['反向飞鸟', '反向飞鸟']]}],
         [{'部位': '肱二头',
           '动作数': 2,
           '组数': 3,
           '动作选择': [['弯举', '弯举'], ['弯举', '弯举']]}], ],
        [[{'部位': '胸',
           '动作数': 3,
           '组数': 3,
           '动作选择': [['推胸', '推胸', '推胸']]}],
         [{'部位': '肩前束',
           '动作数': 1,
           '组数': 3,
           '动作选择': [['推举'], ['前平举']]}],
         [{'部位': '肩中束',
           '动作数': 1,
           '组数': 3,
           '动作选择': [['侧平举']]}],
         [{'部位': '肱三头',
           '动作数': 2,
           '组数': 3,
           '动作选择': [['臂屈伸', '臂屈伸']]}]
         ],
        [[{'部位': '腿',
           '动作数': 3,
           '组数': 4,
           '动作选择': [['髋关节伸', '髋关节伸', '髋关节外展'], ['髋关节伸', '髋关节伸', '髋关节外展']]}],
         [{'部位': '腹',
           '动作数': 5,
           '组数': 2,
           '动作选择': [['卷腹', '卷腹', '卷腹', '举腿', '举腿']]}]]
    ]

for e in split3_training_pain:
    print(f'''训练日：{str([p['部位'] for t in e for p in t])}''')
    for t in e:
        for p in t:
            move = random.choice(p['动作选择'])
            l = [select_one_move_by_type(m) for m in move]
            sl = set(l)
            while len(sl) < len(l):
                l = [select_one_move_by_type(m) for m in move]
                sl = set(l)
            print(f'''{move}:{[select_one_move_by_type(m) for m in move]}''')
    print('--------------------------------')
# 组间休息：胸背腿 3 肩手2 腿4

# 每组8个，做到力竭
