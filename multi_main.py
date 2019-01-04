import sys
import csv
import os
#import pickle
import gc
from pkg.CaseScene import CaseSceneIns
import pandas as pd
from IPython.display import display, HTML


gc.enable()

def runCase(nLoop):

	# create "mast_achor_conf.csv" for different mast combination height and collar combination, "mast_achor_conf.csv" will be read by calcsolve.case_reader
	csv_WriteConf=path_text+'mast_achor_conf.csv'
	l_write=list()
	l_write.append(ma_conf[0])
	l_write.append(ma_conf[1])
	# join title to list
	l_TitleMastType=['each mast no']+l_mastType[nLoop+1]
	l_write.append(l_TitleMastType)
	l_TitleAnchor=['collar height']+lm_anchor[nLoop]
	l_write.append(l_TitleAnchor)

	with open(csv_WriteConf,'w') as c_WriteConf:
		confWriter=csv.writer(c_WriteConf,delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
		for ll in l_write:
			confWriter.writerow(ll)


	cs=CaseSceneIns(path_text)

	mastHeight,rList=cs.get_result()

	# rList=[rInTighten,rOutTighten,rInReleased,rOutReleased]
	lInTighten=[mastHeight,rList[0]]
	lOutTighten=[mastHeight,rList[1]]
	lInReleased=[mastHeight,rList[2]]
	lOutReleased=[mastHeight,rList[3]]

	alst000=list(map(lambda i0: i0 + [''],rList[0]))
	alst001=list(map(lambda i0: i0 + [''],rList[1]))
	alst002=list(map(lambda i0: i0 + [''],rList[2]))
	alst003=list(map(lambda i0: i0 + [''],rList[3]))


	alst00.append(alst000)
	alst01.append(alst001)
	alst02.append(alst002)
	alst03.append(alst003)


	nLoop+=1

def output():


	lststr=[['Stage '+str(i),'',''] for i in range(2,nS+2)]

	lststr1=list()
	for li in lststr:
		lststr1.extend(li)


	alst0=[lststr1]+format_list(alst00)
	alst1=[lststr1]+format_list(alst01)
	alst2=[lststr1]+format_list(alst02)
	alst3=[lststr1]+format_list(alst03)

	df0=pd.DataFrame(alst0)
	display(df0)

	c_out0=path_text+'0 In service -all tighten.csv'
	c_out1=path_text+'0 Out service -all tighten.csv'
	c_out2=path_text+'0 In service -alt released.csv'
	c_out3=path_text+'0 Out service -alt released.csv'
	with open(c_out0,'w') as c_in_tighten:
		writer=csv.writer(c_in_tighten)
		for rows in alst0:
			writer.writerow(rows)
	with open(c_out1,'w') as c_out_tighten:
		writer=csv.writer(c_out_tighten)
		for rows in alst1:
			writer.writerow(rows)
	with open(c_out2,'w') as c_in_released:
		writer=csv.writer(c_in_released)
		for rows in alst2:
			writer.writerow(rows)
	with open(c_out3,'w') as c_out_released:
		writer=csv.writer(c_out_released)
		for rows in alst3:
			writer.writerow(rows)




def format_list(lst):
	arr0=list()
	for n0 in range(0,nS):
		arr=lst[n0]
		for n1 in range(0,nS):
			if(len(arr)<n1+1):
				arr.append('')
		arr0.append(arr)

	arr1=list(map(list,zip(*arr0)))
	arr1.reverse()
	arr1=list(map(lambda l0:l0[::-1],arr1))
	al0=list()
	al1=list()
	for l0 in arr1:

		for e in l0:
			if e=='':
				al0.extend(['','',''])
			else:
				al0.extend(e)
		al1.append(list(al0))
		al0=list()
	return al1

def is_kernel():
	"""
	This function check this file is execute for kernel(Jupyter Note, Ipython)
	Return True is execute from kernel
	"""
	if 'IPython' not in sys.modules:
		# IPython hasn't been imported, definitely not
		return False
	from IPython import get_ipython
	# check for `kernel` attribute on the IPython instance
	return getattr(get_ipython(), 'kernel', None) is not None

if __name__=='__main__':

	run_from_kernel=is_kernel()

	if run_from_kernel:
		path=input('Please key in file location (Folder)')
	else:
		path=str(os.path.dirname(os.path.abspath(__file__)))
	path_text=path.replace('\\','/')+'/'
	# path_text='D:/TYS/Project/python solver 1.1/'
	csv_multi=path_text+'MultipleInput.csv'


	with open(csv_multi) as c_multi:
		l_main=filter(bool,list(csv.reader(c_multi)))

	#lm  : list multi

	lm=list(l_main)

	n=0
	for line in lm:
		if (line[0]=='Note:'):
			break
		n+=1

	noOfStage=len(list(filter(bool,lm[2])))-1
	noMastType=len(list(filter(bool,lm[1])))-1

	l_mastType0=list()
	l_mastType0=lm[2:n-1]

	l_mastType00=list(map(lambda aL: list(filter(bool,aL[1:])),l_mastType0))
	l_mastType=list(map(list,zip(*list(filter(bool,l_mastType00)))))
	#print(l_mastType)

	# l_mastType0=list()
	# for c1 in range(2,n):
	# 	l_mastType0.append(lm[c1][1:noOfStage-1])
	# 	c1+=1
	#
	# l_mastType1=list(map(list,zip(*l_mastType0)))
	# l_mastType2=l_mastType1[1:]
	# l_mastType=list(map(lambda a0: list(filter(bool,a0)),l_mastType2))

	lm_anchor00=list()
	for l1 in lm[n+2:]:
		lm_anchor00.append(l1[2:noOfStage+1])



	lm_anchor0=list(map(lambda x0: x0[::-1],list(map(list, zip(*lm_anchor00)))))

	## remove all empty in each element in lm_anchor0, lm_anchor is a list of list
	lm_anchor=list(map(lambda aList: list(filter(bool,aList)),lm_anchor0))
	# for li in lm_anchor:
	# 	print(li)
	# read mast type and quantity
	# mast and anchorage data

	ma_conf=list(map(lambda bList: list(filter(bool,bList)),lm[:2]))


	# clear 'OutputResult.csv' content
	csv_out=path_text+'OutputResult.csv'
	with open(csv_out,'w+') as c_out:
		c_out.truncate()

	alst00=list()
	alst01=list()
	alst02=list()
	alst03=list()


	for nLoop in range(0,noOfStage-1):
		runCase(nLoop)

	nS=noOfStage-1

	alst00.reverse()
	alst01.reverse()
	alst02.reverse()
	alst03.reverse()

	output()

gc.collect()
sys.exit()
