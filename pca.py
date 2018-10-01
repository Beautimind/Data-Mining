import numpy as np;
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import seaborn as seab
#first part, pca dimension reduction
rawdata=np.genfromtxt('/Users/haochengtang/cse601/pca_demo.txt',delimiter='\t',dtype=None);
length=len(rawdata);
width=len(rawdata[1]);
print(rawdata[1][0])
print(type(rawdata[1][-1]))
data=np.zeros([length,width-1]);
category=dict();
colors=np.zeros([length,])
num=0;
labels=np.zeros([length,],dtype=object);
for i in range(0,length):
    labels[i]=rawdata[i][-1].decode("UTF-8")
    if not rawdata[i][-1] in category:
        category[rawdata[i][-1]]=num;
        colors[i]=num;
        num+=1
    else:
        colors[i]=category[rawdata[i][-1]]
    for j in range(0,width-1):
        data[i][j]=rawdata[i][j];

# print(data)
# print(type(data))
# category=data[:][-1]
# data=np.delete(data,data.shape[1]-1,1);

mean=data.mean(0);
centered=np.zeros(data.shape)
for row in range(data.shape[0]):
    centered[row,:]=data[row,:]-mean;
coef=np.dot(np.transpose(centered),centered)/(centered.shape[0]-1);
Eigvalues,Eigvectors=np.linalg.eig(coef)
idx=Eigvalues.argsort()[::-1]
Eigvalues = Eigvalues[idx]
Eigvectors = Eigvectors[:,idx]
top2=Eigvectors[:,0:2]
pca_result1=np.dot(data,top2)

visual1={'x':pca_result1[:,0],'y':pca_result1[:,1],'label':labels}
seab.scatterplot(x='x',y='y',hue='label',data=visual1).set_title("pca-pca_c.txt")
plt.show()
# plt.scatter(pca_result1[:,0],pca_result1[:,1],c=colors)
# plt.title("pca-data1")
# plt.legend()
# plt.show()
#svd
from sklearn.decomposition import TruncatedSVD
svd=TruncatedSVD(2);
svd.fit(data);
svd_result1=svd.transform(data);
visual2={'x':svd_result1[:,0],'y':svd_result1[:,1],'label':labels}
seab.scatterplot(x='x',y='y',hue='label',data=visual2).set_title("svd-pca_c.txt")
plt.show()
# plt.scatter(svd_result1[:,0],svd_result1[:,1],c=colors)
# plt.title("svd-data1")
# plt.show();

# print(svd.trdansform(data));

#t-SNE
from sklearn.manifold import TSNE
tsne=TSNE(2);
tsne_result1=tsne.fit_transform(data);
visual3={'x':tsne_result1[:,0],'y':tsne_result1[:,1],'label':labels}
seab.scatterplot(x='x',y='y',hue='label',data=visual3).set_title("tsne-pca_c.txt")
plt.show()
# plt.scatter(tsne_result1[:,0],tsne_result1[:,1],c=colors)
# plt.title("tsne-data1")
# plt.show()
# print(tsne.fit_transform(data))
