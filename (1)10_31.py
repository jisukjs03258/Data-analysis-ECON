# -*- coding: utf-8 -*-
"""(1)10/31.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Wx17mrWGMgwYQ6SOIEvAynXXP10e4rUr

#EDA (Exploratory Data Analysis)

1. 문제를 인식
  - ex) 보험료가 바르게 책정되고 있는지를 확인

2. 변수 설명
3. 데이터에 대한 이해
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from google.colab import files

sns.set_style("whitegrid") #옵션임 안해두돼

files.upload()

df=pd.read_csv("insurance.csv")

df.head()

"""- bmi : body mass index
- charges : 개인의 의료 비용 (의료 보험회사에서 청구하는)
"""

df.tail()

df.shape #row-1338,column-7

df.columns #변수

df.describe() #수치형 데이터가 계산되어 나옴 <-> 범주형데이터(글자)
#보고서 과제를 할때, 이걸 활용

df.describe(include="O") #범주형 데이터를 구해줘!
                         #unique : 데이터의 종류
                         #대문자 O(오)

"""- 범주형 데이터(strings)
  - top : 가장 많이 나오는 유형
  - freq : 가장 많이 나오는 유형에 대한 빈도

- Results
  - 성별중에서 가장 많이 도출되는 유형은 male
    - male은 676번 도출됨
  - southeast지역이 가장 많이 도출됨
    - southeast는 364번 도출됨
  - 대부분의 사람들은 비흡연자
    - 1338중에서 1064명이 nonsmoker
"""

df["sex"].unique() # unique 값 확인

df["region"].unique()

"""### 4. Data Cleaning

  (1) missing value

  (2) 중복 데이터 확인
"""

df.isnull() #true-결측치 / false-채워진 값

df.isnull().sum() #true-1,false-0으로 가정해 더해라!

df.info() #결측치는 아니지만, "? 같은 object가 수치형에 있는지를 확인

df.duplicated() #중복 데이터 확인! - true(중복값있음)

df.duplicated().sum() #1개의 중복값이 있다는 것

df[df.duplicated()] #중복값 찾는 명령

df.drop_duplicates(keep="first",inplace=True) #1번째 값은 냅두고, 두번째 값은 영구히(inplace) drop하겠다

"""- drop_duplicates 메소드 사용하여 중복된 행 제거

- keep="first"
  - 중복값 2개 중 첫번째 것은 남겨둠

- inplace=True
  - 영구히 데이터 변경
"""

df.duplicated().sum() #inplace가 반영되어 중복값이 없어짐

"""### 5. 데이터 시각화

####5.1 개별 변수 분석

  - 각 변수별 분포 분석
    - 기초통계량
    - 분포도
    - 차트(boxplot, histogram, barplot, piechart)
"""

df.head()

"""- 변수 charges"""

sns.histplot(df["charges"], color="r",kde=True) # 맨 처음에 whitegrid 스타일을 적용해서 격자무늬가 생긴 것
plt.title("Charges Distribution", size=18)      # kde : 밀도선을 그려줌
plt.xlabel("Charges")
plt.ylabel("Density")
plt.show()

"""- "charges":
  - right skewed (positive skewed)

- 왜도(skewness)
  - 3차 모먼트

$$ \gamma_1=E[(\frac{x-\mu}{\sigma})^3]$$
(식은 시험에 안나옴)
"""

sns.histplot(df["age"], color="k")
plt.title("Age Distribution", size=18)
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()

"""- 의료보험 고객 중 가장 빈번한 나이대는 18-19세임
- 분포는 uniform distribution 형태처럼 나타남
"""

sns.histplot(df["bmi"], color="m", kde=True)
plt.title("BMI Distribution", size=18)
plt.show()

sns.histplot(df["children"], color="c")
plt.title("number of Children", size=18)
plt.show()

sns.boxplot(data=df, x="charges", color="pink")
plt.title("boxplot for charges", size=18)
plt.show()

q1_charges=df["charges"].quantile(0.25)
q3_charges=df["charges"].quantile(0.75)
iqr_charges=q3_charges-q1_charges

print(iqr_charges)

ll=q1_charges-1.5*iqr_charges
ul=q3_charges+1.5*iqr_charges

df[(df["charges"]<ll)|(df["charges"]>ul)] # 대괄호[]안에 해당하는 것들을 df형식으로 나타내줘!
                                          # 여기서 outlier는 139개라는 것

"""### Categorical Features (범주형 데이터)

gender
"""

sns.countplot(x="sex",data=df)
plt.show()

"""children"""

sns.countplot(x="children", data=df, palette="Purples") #범주형 데이터는 아니지만 countplot으로 보는 게 적합함
plt.title("Number of children")
plt.xlabel("children")
plt.ylabel("count")
plt.show()

"""smoker"""

sns.countplot(x="smoker", data=df)
plt.title("smokers vs nonsmokers", size=18)
plt.xlabel("smokers")
plt.ylabel("count")
plt.show()

df["smoker"].value_counts() #df.value_counts() : 카운팅 해줌

"""region"""

sns.countplot(x="region", data=df, palette="BuGn")
plt.title("Region Distriburion", size=18)
plt.xlabel("region")
plt.ylabel("count")
plt.show()

df["region"].value_counts()

"""### Bivariate Analysis

- 두 변수를 함께 분석하는 것을 의미함
- 두 변수간의 관계를 파악하는 것이 목적임

  - boxplot etc

**Age vs Charges** 둘다 수치형인 경우
"""

plt.figure(figsize=(10,3))
sns.scatterplot(x="age", y="charges", color="skyblue", data=df)
plt.title("Age vs Charges", size=18)
plt.xlabel("Age")
plt.ylabel("Charges")
plt.show()

df.corr(numeric_only=True)["age"]["charges"] #둘의 상관관계 알아보기 / corr괄호 안에 numeric_only=True 쓰면 자잘한 거 없이 값만 나옴!

"""**smoker vs charges** 범주형과 수치형 둘 다 있는 경우"""

sns.boxplot(data=df, x="smoker", y="charges", palette="RdPu")
plt.title("smoker vs charges boxplot", size=18)
plt.show()

"""#### Pairplot (수치형 데이터)
- 두개의 수치형 데이터의 관계를 보여주는 시각화 그래프
"""

sns.pairplot(df, diag_kind="kde", kind="reg", markers="+", plot_kws={"line_kws":{"color":"g"}, "scatter_kws":{"color":"pink"}}, corner=True) #일일이 구하지 않아도 matrix form으로 보여줌
#하나씩 넣어보면서 만들어 본 것 / 학습할 땐 df만 넣었다가 하나씩 추가해보기
plt.show()

sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="Purples", vmax=1, vmin=-1) #annot=가운데 숫자
plt.title("Correlation between variables", size=18)
plt.show()

