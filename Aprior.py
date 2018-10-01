import numpy as np;
from bisect import bisect


class AsoRules:

    def load_trans(self,fname):
        raw_data = np.genfromtxt(fname, dtype=str, delimiter='\t')
        rules=dict()
        numr = raw_data.shape[0]
        numc = raw_data.shape[1]
        category = (numc - 1) * 2
        data = [set() for i in range(numr)]
        for i in range(numr):
            for j in range(numc - 1):
                s="G"
                if raw_data[i][j] == 'Up':
                    data[i].add(j * 2)
                    s+=str(j+1)+"_Up"
                    self.dic[j*2]=s;
                else:
                    data[i].add(j * 2 + 1);
                    s += str(j + 1) + "_Down"
                    self.dic[j*2+1]=s;
            if raw_data[i][-1] not in self.dic:
                self.dic[category] = raw_data[i][-1];
                data[i].add(category);
                category += 1
            else:
                data[i].add(self.dic[raw_data[i][-1]]);
        return data, category;

    def __init__(self,support,confidence,fname):
        self.support = support;
        self.confidence = confidence;
        self.dic = dict();
        self.data,self.category = self.load_trans(fname);
        self.freqs = list();
        self.infreq = set();
        self.rules= list();
        self.freqsfinal=list()
        self.rulesfinal=list();


    # the first part is for frequent ItemSet Generation
    def contain(self,n):
        # print('contain start')
        for i in self.infreq:
            if i.issubset(n):
                return True;
        # print('contain end')
        return False;

    def count(self, n):
        # print('count start')
        result = 0;
        for record in self.data:
            if n.issubset(record):
                result += 1
        # print('count end')
        return result

    def genK(self,pre):
        # print(len(infreq))
        self.freqs.append(dict());
        result = set()
        elems = set()
        for l in pre:
            elems = elems.union(l);
        elems = list(elems);
        elems.sort()
        for l in pre:
            cur = list(l);
            start = bisect(elems, l[-1])
            for i in range(start, len(elems)):
                cur.append(elems[i]);
                n = frozenset(cur)
                # if not self.contain(n):
                    # print("need to count")
                times = self.count(n)
                if times >= len(self.data) * self.support:
                    # print(n)
                    self.freqs[-1][n] = times;
                    result.add(tuple(cur))
                else:
                    self.infreq.add(n);
                cur.pop();
        return result

    def genfrequent(self):
        pre = set()
        self.freqs.append(dict())
        for i in range(self.category):
            times = self.count({i})
            if times / len(self.data) >= self.support:
                self.freqs[0][frozenset([i])] = times
                pre.add((i,))
            else:
                self.infreq.add(frozenset([i]))
        while pre:
            pre = self.genK(pre)
        self.freqs.pop();




#code to find rules
    def genfromset(self,fset,time,pre):
        # print("here1")
        if not pre:
            return;
        npre=list()
        for s in pre:
            for i in fset:
                if i > s[-1]:
                    s.append(i);
                    n = frozenset(fset - set(s));
                    # print("judging")
                    # print(n,s);
                    # print(n,s)
                    if not n:
                        return
                    if time / self.freqs[len(n) - 1][n] >= self.confidence:
                        # self.rules[n] = set(s);
                        self.rules.append((n,set(s)))
                        npre.append(list(s));
                    s.pop()
        # print("here2")
        self.genfromset(fset,time,npre)


    def genrule(self):
        for freq in self.freqs:
            for fset,count in freq.items():
                # print("begin to generate rules for:")
                # print(fset)
                time=self.freqs[len(fset)-1][fset]
                pre=list()
                if len(fset)>1:
                    for i in fset:
                        n=frozenset(fset-{i});
                        if time/self.freqs[len(n)-1][n]>=self.confidence:
                            # print(n,i)
                            pre.append([i]);
                            # self.rules[frozenset(n)]={i};
                            self.rules.append((n,{i}))
                self.genfromset(fset, time, pre);

    def template1(self,pos,num,elems):

        #will this convert maintain corresponding order of our key value pairs?
        result=set();
        if num=="ANY":
            if pos=="HEAD":
                for rule in self.rulesfinal:
                    for e in elems:
                        if e in rule[0]:
                            result.add((tuple(rule[0]),tuple(rule[1])));
                            break;
            elif pos=="BODY":
                for rule in self.rulesfinal:
                    for e in elems:
                        if e in rule[1]:
                            result.add((tuple(rule[0]),tuple(rule[1])));
                            break;
            elif pos=="RULE":
                for rule in self.rulesfinal:
                    for e in elems:
                        # print(rule)
                        # print(e)
                        if e in rule[0] or e in rule[1]:
                            # print("select")
                            result.add((tuple(rule[0]), tuple(rule[1])));
                            break;
        if num=="NONE":
            if pos=="HEAD":
                for rule in self.rulesfinal:
                    def inner():
                        for e in elems:
                            if e in rule[0]:
                                return False;
                        return True
                    if inner():
                        result.add((tuple(rule[0]), tuple(rule[1])));
            elif pos=="BODY":
                for rule in self.rulesfinal:
                    def inner():
                        for e in elems:
                            if e in rule[1]:
                                return False;
                        return True
                    if inner():
                        result.add((tuple(rule[0]), tuple(rule[1])));
            elif pos=="RULE":
                for rule in self.rulesfinal:
                    def inner():
                        for e in elems:
                            if e in rule[0] or e in rule[1]:
                                return False;
                        return True
                    if inner():
                        result.add((tuple(rule[0]), tuple(rule[1])));

        else:
            if pos=="HEAD":
                for rule in self.rulesfinal:
                    count=0;
                    for e in elems:
                        if e in rule[0]:
                            count+=1;
                    if count == num:
                        result.add((tuple(rule[0]), tuple(rule[1])));
            elif pos=="BODY":
                for rule in self.rulesfinal:
                    count=0;
                    for e in elems:
                        if e in rule[1]:
                            count+=1;
                    if count == num:
                        result.add((tuple(rule[0]), tuple(rule[1])));
            elif pos=="RULE":
                for rule in self.rulesfinal:
                    count=0;
                    for e in elems:
                        if e in rule[0] or e in rule[1]:
                            count+=1;
                    # print(rule)
                    # print(count,num)
                    if count == num:
                        result.add((tuple(rule[0]), tuple(rule[1])));
        return result

    def template2(self,pos,length):
        result = set();
        if pos=="HEAD":
            for rule in self.rulesfinal:
                if len(rule[0])>=length:
                    result.add((tuple(rule[0]), tuple(rule[1])));
        elif pos=="BODY":
            for rule in self.rulesfinal:
                if len(rule[1])>=length:
                    result.add((tuple(rule[0]), tuple(rule[1])));
        else:
            for rule in self.rulesfinal:
                if len(rule[0])+len(rule[1])>=length:
                    result.add((tuple(rule[0]), tuple(rule[1])));
        return result;

    def template3(self,*args):
        a=args[0];
        result1=set();
        result2=set();
        result=set();
        if a[0]=='1':
            result1=self.template1(args[1],args[2],args[3])
            if a[-1]=='1':
                result2=self.template1(args[4],args[5],args[6])
            else:
                result2=self.template2(args[4],args[5])
        else:
            result1=self.template2(args[1],args[2])
            if a[-1]=='1':
                result2=self.template1(args[3],args[4],args[5])
            else:
                result2=self.template2(args[3],args[4])
        if a[1:-1] == 'and':
            result=result1.intersection(result2);
        else:
            result=result1.union(result2);
        return result

    def Transback(self):
        for ksets in self.freqs:
            ls=list()
            for kset in ksets:
                l=list()
                for elem in kset:
                    l.append(self.dic[elem])
                ls.append(l)
            self.freqsfinal.append(ls)

        for rule in self.rules:
            h=list()
            b=list()
            for elem in rule[0]:
                h.append(self.dic[elem])
            for elem in rule[1]:
                b.append(self.dic[elem])
            self.rulesfinal.append((h,b))

ar=AsoRules(0.3,0.7,'/Users/haochengtang/cse601/associationruletestdata.txt');
ar.genfrequent();
ar.genrule();
ar.Transback();
# result=ar.template1("RULE","ANY",['G59_Up'])
# sum=0;
# for i in ar.freqs:
#     sum+=len(i)
#     print(len(i))
# print(sum)
result=ar.template1("RULE", "ANY", ['G59_Up'])
print(len(result))
result=ar.template1("RULE", "NONE", ['G59_Up'])
print(len(result))
result=ar.template1("RULE", 1, ['G59_Up', 'G10_Down'])
print(len(result))
result=ar.template1("HEAD", "ANY", ['G59_Up'])
print(len(result))
result=ar.template1("HEAD", "NONE", ['G59_Up'])
print(len(result))
result=ar.template1("HEAD", 1, ['G59_Up', 'G10_Down'])
print(len(result))
result=ar.template1("BODY", "ANY", ['G59_Up'])
print(len(result))
result=ar.template1("BODY", "NONE", ['G59_Up'])
print(len(result))
result=ar.template1("BODY", 1, ['G59_Up', 'G10_Down'])
print(len(result))

result=ar.template2("RULE", 3);
print(len(result));
result=ar.template2("HEAD", 2);
print(len(result))
result=ar.template2("BODY", 1)
print(len(result))

result=ar.template3("1or1", "HEAD", "ANY", ['G10_Down'], "BODY", 1, ['G59_Up'])
print(len(result))
result=ar.template3("1and1", "HEAD", "ANY", ['G10_Down'], "BODY", 1, ['G59_Up'])
print(len(result))
result=ar.template3("1or2", "HEAD", "ANY", ['G10_Down'], "BODY", 2)
print(len(result))
result=ar.template3("1and2", "HEAD", "ANY", ['G10_Down'], "BODY", 2)
print(len(result));
result=ar.template3("2or2", "HEAD", 1, "BODY", 2)
print(len(result))
result=ar.template3("2and2", "HEAD", 1, "BODY", 2)
print(len(result))
# result=ar.template3("1and1", "BODY", "ANY", ['G10_Down'], "HEAD", 1, ['G59_Up'])
# result=ar.template1("BODY", "ANY", ['G10_Down'])
# result=ar.template1("HEAD", 1, ['G59_Up'])
# for i in result:
#     print(i)
# print(len(result))
import cProfile
#
# pr = cProfile.Profile()
# pr.enable()
# main()
# pr.disable()
# # after your program ends
# pr.print_stats(sort="calls")
#The second part is for rule generation based on result of result of first part.
# for freqset,count in freq.items():
#     right=list()
#     left=list()
#     for elem in freqset:
#         single=elem.



