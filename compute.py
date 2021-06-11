import sys
import re
import subprocess
from statistics import mode
#pycファイルを作成しない設定
sys.dont_write_bytecode = True

#アミノ酸配列の１文字表記と3文字表記のリストを所得
import amino_dic

class Compute(amino_dic.Aminodic):
    def __init__(self,info,index,script_dir,snpPath,ref,toolPath,excelPrefix,tmp_dir):
        super().__init__()
        self.info = info
        self.index = index
        self.varLists = []
        self.resultList = []
        self.result = {}
        self.script_dir = script_dir
        self.snpPath = snpPath
        self.reference = ref
        self.toolPath = toolPath
        self.err_msg_provean = 'provean Failed'
        self.excelPrefix = excelPrefix
        self.tmp_dir = tmp_dir
    #変異のリストを取得
    def varListAquire(self):
        ls1=self.info.split('|protein_coding|')
        for j in range(1,len(ls1)):
            ls2=ls1[j].split('|')
            ls3=ls1[j-1].split('|')
            ls2[2]=ls2[2].replace('p.','')
            str1=''
            while str1!=ls2[2]:
                str1=ls2[2]
                for key in self.aminokey:
                    ls2[2]=ls2[2].replace(key,self.aminodic[key])
            if ls3[-5]=='HIGH' or ls3[-5]=='MODERATE':
                if self.reference == "hg38":
                  ID=re.search(r'NM.{0,}',ls3[-1])
                  ls3[-1]=ID.group(0)
                ls4=[ls3[-1],ls3[-6],ls3[-5],ls2[1],ls2[2]]
                self.varLists.append(ls4)
            else:
                pass
    #変異の種類で振り分け
    def varCheck(self):
        if self.varLists == []:
            print('pseudogene')
            return
        for varList in self.varLists:
            print(varList)
            resA = self.queryAquire(varList[0])
            if varList[4]=='':
                self.spliceCompute(varList,resA)
            else:
                if 'fs' in varList[4] or '*' in varList[4]:
                    self.fsStopCompute(varList,resA)
                elif varList[1] == 'start_lost':
                    self.startLostCompute(varList,resA) 
                elif 'inframe' in varList[1]:
                    self.inframeCompute(varList,resA)
                else:
                    self.pointMutationCompute(varList,resA)
    #snpEffで配列を取得
    def queryAquire(self, ID):
        argsA=['bash', self.script_dir + '/query_Aquire.sh', ID, self.tmp_dir, self.snpPath, self.reference]
        try:
            resA = subprocess.check_output(argsA)
            resA = resA.decode()
            return resA
        except:
            print('snp failed')
            return ''
    #splicing variantの処理
    def spliceCompute(self,varList,resA):
        geneVar = varList[3].replace('c.','')
        if '*' in geneVar or varList[1]=='sequence_feature':
            print('sequence feature or variant after stopcodon')
            return
        if resA == '':
            return
        self.spliceCompute_provean(varList,resA,geneVar)
    #frameshift, stopgainの処理
    def fsStopCompute(self,varList,resA):
        if varList[1] == 'stop_lost':
            print('stop_lost')
            return
        if resA == '':
            return
        self.fsStopCompute_provean(varList,resA)
    #startlostの処理
    def startLostCompute(self,varList,resA):
        if resA == '':
            return
        self.startLostCompute_provean(varList,resA)
    #inframeのindelの処理
    def inframeCompute(self,varList,resA):
        if resA == '':
            return
        self.pointMutation_inframeCompute_provean(varList)
    #pointmutationの処理
    def pointMutationCompute(self,varList,resA):
        if resA == '':
            return
        self.pointMutation_inframeCompute_provean(varList)
    #frameshift, stopgain, splicevariantのprovean実行
    def runProvean_fsStopSplice(self,varList):
        try:
            argsB = ['bash', self.script_dir + '/fsStopCompute_provean.sh', varList[0], self.tmp_dir, self.toolPath, self.excelPrefix]
            resB = subprocess.check_output(argsB)
            resB = resB.decode()
            self.resultCompute_fsStopSplice(resB)
        except:
            print(self.err_msg_provean)
            return
    #pointmutation,inframeのindelのprovean実行
    def runProvean(self,varList):
        try:
            argsB = ['bash', self.script_dir + '/pointmutationCompute_provean.sh', varList[0], self.tmp_dir, self.toolPath, self.excelPrefix]
            resB = subprocess.check_output(argsB)
            resB = resB.decode()
            self.resultCompute(resB)
        except:
            print(self.err_msg_provean)
            return
    #provean用に変異の情報を処理(splice variant)
    def spliceCompute_provean(self,varList,resA,geneVar):
        if re.match('-',geneVar):
            m = 1
        else:
            M = re.search('\d+',geneVar)
            m = int(M.group())
            m = m//3
        if m + 1 > len(resA) - 1:
            return
        f = open(self.tmp_dir + self.excelPrefix  +  '.var','w')
        for j in range(m + 1, len(resA) - 1):
            for amino in self.aminovalues:
                f.write(resA[j-1] + str(j) + amino + '\n')
        f.close()
        self.runProvean_fsStopSplice(varList)
    #provean用に変異の情報を処理(frameshift)
    def fsStopCompute_provean(self,varList,resA):
        aminoVar = re.sub('[A-Z]','',varList[4])
        aminoVar = aminoVar.replace('fs','')
        aminoVar = aminoVar.replace('*','')
        m = int(aminoVar)
        if m + 1 > len(resA) - 1:
            return
        f = open(self.tmp_dir + self.excelPrefix + '.var', 'w')
        for j in range(m + 1,len(resA) - 1):
            for amino in self.aminovalues:    
                f.write(resA[j-1] + str(j) + amino + '\n')
        f.close()
        self.runProvean_fsStopSplice(varList)
    #provean用に変異の情報を処理(startlost)
    def startLostCompute_provean(self,varList,resA):
        f = open(self.tmp_dir + self.excelPrefix + '.var', 'w')
        for j in range(2,len(resA)):
            if resA[j-1] == 'M':
                break
            for amino in self.aminovalues:
                f.write(resA[j-1] + str(j) + amino + '\n')
        f.close()
        self.runProvean_fsStopSplice(varList)
    #provean用に変異の情報を処理(pointmutation)
    def pointMutation_inframeCompute_provean(self,varList):
        f = open(self.tmp_dir + self.excelPrefix + '.var', 'w')
        f.write(varList[4] + '\n')
        f.close()
        self.runProvean(varList)
    #frameshift等の結果処理
    def resultCompute_fsStopSplice(self,resB):
        results = resB.split()
        results = map(float,results)
        results = list(zip(*[iter(results)]*20))
        tmpResultList = []
        for position in results:
            avg = sum(position) / 20
            tmpResultList.append(avg)
        self.resultList.append(min(tmpResultList))
    #pointmutation等の結果処理
    def resultCompute(self,resB):
        self.resultList.append(float(resB))
    #結果のチェック
    def resultCheck(self):
        if self.resultList == []:
            self.result['resultValue'] = ''
            self.result['resultPred'] = ''
        else:
            resultValue = min(self.resultList)
            if resultValue > -2.5:
                resultPred = 'N'
            else:
                resultPred = 'D'
            self.result['resultValue'] = resultValue
            self.result['resultPred'] = resultPred
    def run(self):
        self.varListAquire()
        self.varCheck()
        self.resultCheck()
        print(self.result['resultValue'], self.result['resultPred'])
        return self.result
