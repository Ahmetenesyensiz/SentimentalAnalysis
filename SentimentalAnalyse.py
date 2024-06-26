# -*- coding: utf-8 -*-
"""NLP.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17ScOJXCoCnhu9_qUWMeTNwQUqHGiUDrs
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# import warnings
# warnings.filterwarnings('ignore')

data = pd.read_csv("data.csv" , encoding = "utf-16")

data.head(10)

data.info

data = data.dropna() #eksik değerleri(NaN,None gibi) içeren satırları kaldırır.

print(data)

data = data.rename({'Görüş': 'Gorus'}, axis=1) #manuel duzenleme

data.head()

print(data.columns)

data["Durum"].value_counts() #durum sayısı

sns.countplot(data["Durum"]) #seaborn ile sütun grafiği , kategorik değerlerin frekansı
print(data.Durum.value_counts())

data['Durum'] = data.loc[:, 'Durum'].map({'Olumlu' : 0 , 'Olumsuz' :1 , 'Tarafsız' :2}) #seçenekleri integer olarak işaretledik.Daha sonra kullanmak için

print(data)

print(data["Gorus"])

print(data["Durum"])

#verisetindeki yorumların ilk ucunun gorunumu
print(data["Gorus"][0] + "\n")
print(data["Gorus"][1] + "\n")
print(data["Gorus"][2] + "\n")

"""DATASETIN HAZIRLANMASI ASAMASI"""

print(data)

import re    #re kutuphanesi duzenli ifadelerle calismamizi saglar

import nltk
# nltk.download('punkt', download_dir='/content/')

import nltk.data
# nltk.data.path.append('/content/')

from nltk.corpus import stopwords
nltk.download('stopwords')

print(stopwords.words("turkish"))
silinecek =  stopwords.words("turkish")
print(len(silinecek))

"""## Tüm verisetinin üstünde gezinerek makine öğrenme modelinde kullanılacak formata dönüştüren fonksiyon"""

def harf_degistir_ve_temizle(cumle):
    turkce_degisim = {
        "ü": "u", "Ü": "U",
        "ö": "o", "Ö": "O",
        "ç": "c", "Ç": "C",
        "ş": "s", "Ş": "S",
        "ı": "i", "İ": "I",
        "ğ": "g", "Ğ": "G"
    }

    # Türkçe karakterleri değiştirme
    for turkce, ingilizce in turkce_degisim.items():
        cumle = cumle.replace(turkce, ingilizce)

    # Sadece harf karakterlerini tutma
    cumle = re.sub("[^a-zA-Z]", " ", cumle)

    # Küçük harfe dönüştürme
    cumle = cumle.lower()

    # Türkçe stopwords'leri kaldırma
    stopwords_turkish = set(stopwords.words("turkish"))
    cumle_kelimeleri = nltk.word_tokenize(cumle)
    cumle_kelimeleri = [word for word in cumle_kelimeleri if word not in stopwords_turkish]

    # Temizlenmiş cümleyi birleştirme
    temizlenmis_cumle = " ".join(cumle_kelimeleri)

    return temizlenmis_cumle

print(data["Gorus"])

X = data["Gorus"].values
print("Veri setinin uzunlugu: ",len(X))

X[777]

fixed_X = []
for i in range(0 , len(X)):
    X_ = harf_degistir_ve_temizle(X[i])
    fixed_X.append(X_)

fixed_X[777]

print("Düzeltilmemiş örnek bir yorum:\n" + X[300] + "\n--------------------------------------------------------------------")

print("Düzeltilmiş örnek bir yorum:\n",fixed_X[300])

"""## Düzeltilmiş birkaç yorum örneği :"""

print(fixed_X[0] + "\n")
print(fixed_X[4588] + "\n")
print(fixed_X[4000] + "\n")

"""# Metin verilerini sayısal vektörlere çevirmek.Amaç: verileri analiz ediebilir bir forma getirme ve makine öğrenmesi modelleri tarafından işlenebilir hale getirmek."""

from sklearn.feature_extraction.text import CountVectorizer
max_feature = 2000 #Vektörleştirme işleminde en fazla kaç özellik kullanılacak

cv = CountVectorizer(max_features = max_feature , stop_words = silinecek)

space_matrix = cv.fit_transform(fixed_X).toarray() #fit_transform()->text to vector.  toarray()->?

print("En sık kullanılan {} kelimeler {}".format(max_feature , cv.get_feature_names_out()))
print(space_matrix)
print(space_matrix.shape)

from wordcloud import WordCloud

encok_kullanilan_kelimeler = cv.get_feature_names_out()

plt.subplots(figsize=(8,8)) #altcizim ile grafik boyutu ayarla
wordcloud = WordCloud(background_color = "white", width = 512, height = 512).generate(" ".join(list(encok_kullanilan_kelimeler))) #word cloud objesi oluştur.
plt.imshow(wordcloud)
plt.axis("off") #eksenleri kapatır "on"
plt.show()

"""ML"""

X = space_matrix #metin verilerinin sayısal özelliklere vektörleştirilmiş hali.Modelin girdisi bu.
y = data.iloc[: , -1].values #Modelin çıkış verisi. Olumlu(0)/Olumusuz(1)/Tarafsız(2)
print(X)
print(X.shape)
print("s")
print(y)

from sklearn.model_selection import train_test_split , cross_val_score #train_test_split fonk kullanmak için
x_train , x_test , y_train , y_test = train_test_split(X , y , test_size = 0.25 , random_state = 0) #Burda eğitim_setini(X) ve test_setinden(y) ayırdık. Ve test setini tüm veri setinin %25'inden random olarak ayırdık.
print("Eğitim setininin uzunluğu : ",len(x_train))
print("Test setinin uzunluğu : ",len(y_test))

"""# MAKİNE ÖĞRENİM MODELLERİ"""

from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score , confusion_matrix, classification_report


"""## Navie Bayes Classification

1.   Gaussian Navie Bayes
2.   Bernoulli Navie Bayes
3.   Multinomial Navie Bayes

## 1. Gaussian Navie Bayes
"""

gnb = GaussianNB()
gnb.fit(x_train , y_train) #veri : x_train , özellik matrisi : y_train
y_pred = gnb.predict(x_test)

gnb_csv = cross_val_score(estimator=gnb , X=x_train , y=y_train , cv=5)

print("GaussianNB Accuary : ",accuracy_score(y_pred , y_test)) #Tahminlerin doğruluğunu hesaplar.Gerçek durumlarla(y_test) yapılan tahminlerin doğruluğunu ölçer.

print("GaussianNB Test Score: ", gnb.score(x_test, y_test)) #Test seti üzerinde modelin doğruluk skorunu hesaplama
print("GaussianNB Train Score: ", gnb.score(x_train, y_train)) #Eğitim seti üzerinde modelin doğruluk skorunu hesaplama

print("GaussianNB Cross Validation Mean: ", gnb_csv.mean())
print("GaussianNB Cross Validation Std: ", gnb_csv.std())

# GaussianNB için
y_pred_gnb = gnb.predict(x_test)
print("GaussianNB Confusion Matrix:")
conf_matrix_gnb = confusion_matrix(y_test, y_pred_gnb)
sns.heatmap(conf_matrix_gnb, annot=True, fmt='d', cmap='Blues', xticklabels=['Olumlu', 'Olumsuz', 'Tarafsız'], yticklabels=['Olumlu', 'Olumsuz', 'Tarafsız'])
plt.xlabel('Tahmin')
plt.ylabel('Gerçek')
plt.title('GaussianNB Confusion Matrix')
plt.show()
print("GaussianNB Accuracy:", accuracy_score(y_test, y_pred_gnb))
print("GaussianNB Classification Report:\n", classification_report(y_test, y_pred_gnb))

"""# 2. Bernoulli Navie Bayes"""

bnb= BernoulliNB()
bnb.fit(x_train,y_train)
y_pred_bnb=bnb.predict(x_test)

bnb_cvs = cross_val_score(estimator=bnb, X = x_train, y = y_train, cv = 5)

print("BernoulliNB Accuracy:              ", accuracy_score(y_pred_bnb,y_test))

print("BernoulliNB Test Score:            ", bnb.score(x_test, y_test))
print("BernoulliNB Train Score:           ", bnb.score(x_train, y_train))

print("BernoulliNB Cross Validation Mean: ", bnb_cvs.mean())
print("BernoulliNB Cross Validation Std:  ", bnb_cvs.std())

# BernoulliNB için
y_pred_bnb = bnb.predict(x_test)
print("BernoulliNB Confusion Matrix:")
conf_matrix_bnb = confusion_matrix(y_test, y_pred_bnb)
sns.heatmap(conf_matrix_bnb, annot=True, fmt='d', cmap='Blues', xticklabels=['Olumlu', 'Olumsuz', 'Tarafsız'], yticklabels=['Olumlu', 'Olumsuz', 'Tarafsız'])
plt.xlabel('Tahmin')
plt.ylabel('Gerçek')
plt.title('BernoulliNB Confusion Matrix')
plt.show()
print("BernoulliNB Accuracy    ------->    ", accuracy_score(y_test, y_pred_bnb))
print("BernoulliNB Classification Report:\n", classification_report(y_test, y_pred_bnb))

"""## 3. Multinomial Navie Bayes"""

mnb = MultinomialNB()

mnb.fit(x_train,y_train)

y_pred_mnb = mnb.predict(x_test)

mnb_cvs = cross_val_score(estimator=mnb, X = x_train, y = y_train, cv = 10)

print("MultinomialNB Accuracy:               ", accuracy_score(y_pred_mnb, y_test))

print("MultinomialNB Test Score:             ", mnb.score(x_test, y_test))
print("MultinomialNB Train Score:            ", mnb.score(x_train, y_train))

print("MultinomialNB Cross Validation Mean:  ", mnb_cvs.mean())
print("MultinomialNB Cross Validation Std:   ", mnb_cvs.std())

# MultinomialNB için
y_pred_mnb = mnb.predict(x_test)
print("MultinomialNB Confusion Matrix:")
conf_matrix_mnb = confusion_matrix(y_test, y_pred_mnb)
sns.heatmap(conf_matrix_mnb, annot=True, fmt='d', cmap='Blues', xticklabels=['Olumlu', 'Olumsuz', 'Tarafsız'], yticklabels=['Olumlu', 'Olumsuz', 'Tarafsız'])
plt.xlabel('Tahmin')
plt.ylabel('Gerçek')
plt.title('MultinomialNB Confusion Matrix')
plt.show()
print("MultinomialNB Accuracy    ------->    ", accuracy_score(y_test, y_pred_mnb))
print("MultinomialNB Classification Report:\n", classification_report(y_test, y_pred_mnb))

"""## Logistic Regression Classification"""

logr = LogisticRegression(random_state = 0)
logr.fit(x_train, y_train)

y_pred_logr = logr.predict(x_test)

bas_log = cross_val_score(estimator = logr, X = x_test, y = y_test, cv = 4)

print("Logistic Regression Accuracy:            ", accuracy_score(y_pred_logr, y_test))

print("Logistic Regression Test accuracy        ", (logr.score(x_test,y_test)))
print("Logistic Regression Train accuracy       ", (logr.score(x_train, y_train)))

print("Logistic ile SVC Cross Validation Mean:  ", bas_log.mean())
print("Logistic ile SVC Cross Validation Std:   ", bas_log.std())

y_pred_logr = logr.predict(x_test)
print("Logistic Regression Confusion Matrix:")
conf_matrix_logr = confusion_matrix(y_test, y_pred_logr)
sns.heatmap(conf_matrix_logr, annot=True, fmt='d', cmap='Blues', xticklabels=['Olumlu', 'Olumsuz', 'Tarafsız'], yticklabels=['Olumlu', 'Olumsuz', 'Tarafsız'])
plt.xlabel('Tahmin')
plt.ylabel('Gerçek')
plt.title('Logistic Regression Confusion Matrix')
plt.show()
print("Logistic Regression Accuracy    ------->    ", accuracy_score(y_test, y_pred_logr))
print("Logistic Regression Classification Report:\n", classification_report(y_test, y_pred_logr))

"""## Support Vector Machine (SVM) Classification"""

# svc = SVC(random_state = 1, kernel = "rbf")
# svc.fit(x_train, y_train)

# y_pred_svc = svc.predict(x_test)

# svc_cvs = cross_val_score(estimator= svc, X = x_train, y = y_train, cv = 5)

# print("Rbf ile SVC Accuracy: ", accuracy_score(y_pred_svc, y_test))

# print("Rbf ile SVC Test accuracy: {}".format(svc.score(x_test,y_test)))
# print("Rbf ile SVC Train accuracy: {}".format(svc.score(x_train, y_train)))

# print("Rbf ile SVC Cross Validation Mean: ", svc_cvs.mean())
# print("Rbf ile SVC Cross Validation Std: ", svc_cvs.std())

# y_pred_svc = svc.predict(x_test)
# print("SVM Confusion Matrix:")
# conf_matrix_svc = confusion_matrix(y_test, y_pred_svc)
# sns.heatmap(conf_matrix_svc, annot=True, fmt='d', cmap='Blues', xticklabels=['Olumlu', 'Olumsuz', 'Tarafsız'], yticklabels=['Olumlu', 'Olumsuz', 'Tarafsız'])
# plt.xlabel('Tahmin')
# plt.ylabel('Gerçek')
# plt.title('SVM Confusion Matrix')
# plt.show()
# print("SVM Accuracy    ------->    ", accuracy_score(y_test, y_pred_svc))
# print("SVM Classification Report:\n", classification_report(y_test, y_pred_svc))

"""## Bir GUI yardımıyla modelimiz üzerinde manuel denemeler yapmak :"""

import tkinter as tk
from tkinter import ttk

# GUI oluşturma
def analiz_et():
    metin = entry.get("1.0", tk.END)
    temiz_metin = harf_degistir_ve_temizle(metin)
    metin_vector = cv.transform([temiz_metin]).toarray()
    tahmin = mnb.predict(metin_vector)
    if tahmin == 0:
        sonuc.set("Sonuç: Olumlu")
    elif tahmin == 1:
        sonuc.set("Sonuç: Olumsuz")
    else:
        sonuc.set("Sonuç: Tarafsız")

# Tkinter ana penceresi
root = tk.Tk()
root.title("Duygu Durum Analizi")

# Kullanıcıdan metin alımı
ttk.Label(root, text="Metin:").grid(row=0, column=0, padx=10, pady=10)
entry = tk.Text(root, height=10, width=50)
entry.grid(row=0, column=1, padx=10, pady=10)

# Analiz butonu
analiz_button = ttk.Button(root, text="Analiz Et", command=analiz_et)
analiz_button.grid(row=1, column=1, padx=10, pady=10)

# Sonuç etiketi
sonuc = tk.StringVar()
sonuc.set("Sonuç: ")
ttk.Label(root, textvariable=sonuc).grid(row=2, column=1, padx=10, pady=10)

# GUI çalıştırma
root.mainloop()