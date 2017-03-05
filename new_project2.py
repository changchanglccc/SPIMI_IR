import glob
import time
import nltk
import collections
import sys
from math import *
import json

#n terms in query, we need to iterate n times
#ranking = 0
#ranking = ranking + prepareforRSV(term)

#for every term in query,find doclen,avgdoclen,docfreq,termfreqindoc and then, calculate the formula,
#add them all as the ranking score and bound it with the doc

def calculate_RSVd(query_list,final_result):#for docs in final_result
        
	#print 'entered in calculate_RSVd'
	match = []
	RSVd = 0
	for docid in final_result:
		#print '========docid : ',docid
		for word in query_list:
		#prepare the reference
			if word == 'and':
				pass
			else:
				#print 'word is ',word
				match = calculate_queryword_refrence(word,docid)
				doclen = match[0]
				termfreqindoc = match[1]
				docfreq = match[2]
				del match[:]
				step1 = (1-b)+b*(doclen/avgdoclen)
				step2 = (k+1)*termfreqindoc/(k*step1 + termfreqindoc)
				RSVdq = log(float(docCounter/docfreq)) * step2   #N need to be record

				RSVd = RSVd + RSVdq #just a RSVd for a specific doc
				doc_ranking[docid] = RSVd

	return doc_ranking

def calculate_queryword_refrence(key,docid):#prepare the reference,need to get the dictionary of key from the final dictionary!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	#print 'entered in calculate_queryword_refrence'
	match = []
	dict_aid = {}
	filename = "final_dict.json"
	termfreqindoc = 0
	docfreq = 0
	key = key.lower()
	with open(filename,'r') as json_file: #bow open the file0.json; later need to open final_dict
		final_dict = json.load(json_file) # json_dicttaiwadoclen = docLenStore[docid]
		dict_aid = final_dict.get(key)
		if final_dict.has_key(key):
			termfreqindoc = dict_aid.get(docid)
		#termfreqindoc = int(final_dict[key][docid])
			docfreq = len(dict_aid)
		#test doclen+termfreq+docfreq
		#print 'doclen :',docLen
		#print 'termfreqindoc:',termfreqindoc
		#print 'docfreq:',docfreq

		match.append(doclen)
		match.append(termfreqindoc)
		match.append(docfreq)#(int(docfreq))
	json_file.close()

	return match

def findMatch(key): #open the json file and do the single query
        match = []
        filename = "final_dict.json"
        #convert the key into lowercase1115#case folding 
        key = key.lower()
        with open(filename,'r') as json_file: #bow open the file0.json; later need to open fianl_dict
                json_dict = json.load(json_file) # json_dict
                #add if statement
                if json_dict.has_key(key): #check wether there is the key in our dictionary
                        for docid in json_dict[key].keys():
                                match.append(docid)
                else:
                        print 'There is no key named',key
        #print type(json_dict[key].keys())
        json_file.close()
        #match.qsort(match)
        #match1 = sortMatch(match)
        match.sort()
        return match
		
def sortMatch(mylist):#remove space from the decoded json file and do the sort operation
        mylist2 = []
        for word in mylist:
              word = int(word)
              mylist2.append(word)
        mylist2.sort()
        for word in mylist2:
              word = "u'   "+ str(word)+"   '"
        print 'mylist is',mylist2
        return mylist2

def singleWordQuery(query_list):
	match1 ={}
	result_and = []
	#result_or = []
	for key in query_list:
		match = findMatch(key) # match = ['',''...]
		match1[key] = sorted(match[key])
		print key,'exists in :',match1[key],'docs'

def stopwords_30 (word):
	words30= ['',' ','a', 'about', 'above', 'across', 'after', 'again', 'against','all','almost','alone','along','already','also','although','always','among','an','and','another','any','anybody','anyone','anything','anywhere','are',' ','areas','around','as','\n']
	if word in words30:
		x = True
		return x;
	else:
		x = False
		return x

def stopwords_150(word):
	words150 = ['',' ','\n','a', 'about', 'above', 'after', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'an', 'and', 'another', 'any', 'anybody', 'anyone', 'anything', 'anywhere', 'around', 'as', 'at', 'away', 'been', 'but', 'even', 'evenly', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'for', 'had', 'has', 'have', 'he', 'her', 'here', 'herself', 'higher', 'highest', 'him', 'himself', 'his', 'how', 'however', 'if', 'in', 'interests', 'interesting', 'into', 'is', 'it', 'its', 'itself', 'just', 'last', 'me', 'might', 'more', 'most', 'mostly', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'of', 'off', 'often', 'on', 'once', 'only', 'or', 'other', 'others', 'our', 'out', 'over', 'second', 'seconds', 'seem', 'seemed', 'seeming', 'seems', 'sees', 'several', 'shall', 'she', 'should', 'since', 'so', 'some', 'somebody', 'someone', 'something', 'somewhere', 'still', 'such', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'therefore', 'these', 'they', 'things', 'this', 'those', 'though', 'thoughts', 'through', 'thus', 'to', 'too', 'until', 'us', 'very', 'was', 'ways', 'we', 'were', 'what', 'when', 'where', 'whether', 'which', 'while', 'who', 'whole', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours']
	if word in words150:
		x = True
		return x;
	else:
		x = False
		return x

def merge_tokenDicts(dict1, dict2):
	for key in dict2.keys():
		if key in dict1.keys():
			for docid in dict2[key].keys():
				if docid in dict1[key].keys():
					dict1[key][docid] += dict2[key][docid]
				else:
					dict1[key][docid] = dict2[key][docid]
		else:
			dict1[key] = dict2[key]
	return dict1

def Ranking(query_list,final_result):
	if(len(final_result) > 0):
		doc_ranking = calculate_RSVd(query_list,final_result)
		if len(doc_ranking) == 1:
			print doc_ranking
		else:
			#sort based on ranking
			print sorted(doc_ranking.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
		doc_ranking.clear()

#----------------------------------start the program------------------------------------
print '----------------------------Start the program-------------------------------'

tokendict = {}
docLenStore = {} #store the docLen of each doc
doc_ranking = {} #store docid:rankingScore
fileCounter =0
#filename = 'file' + str(fileCounter) + '.txt'
path = 'F:/Pythongithub/python_project/COMP6791_project2/reuters21578/'
#path = 'E:/COMP6791/COMP6791Project2/reuters21578/'
delimite = ' '
sgmfiles = glob.glob(path + 'reut2-*.sgm')
memorylimit = 1024 *3
k = 1.2
b = 0.75
start = time.clock()
docCounter = 0  # count the number of doc
doclenCounterList = [];#store every doclen, in order to calculate the avgdoclen in convience

#---------------------------------spimi------------------------------------------------
print '---Open the files---'
print '---Split the files---'
filename = 'file' + str(fileCounter) + '.json' #change to json file to store the dictionary
#filename = 'final_dict.json'
target = open(filename,'w')
target.truncate()
stopwords = 0
numbers = 0
word_flag = True;
for i in range(len(sgmfiles)):
	with open(sgmfiles[i],'r') as f:
		totalDocLen = 0;
		flag = False
		doclen = 0
		for line in f:
			line = line.replace('<', ' <');
			line = line.replace('>', '> ');
			line = line.replace('\n', ' ');
			line = line.replace('\t', ' ');
			line = line.replace('.','');
			line = line.replace(',',' ')
			line = line.replace('.',' ')
			line = line.replace('}',' ')
			line = line.replace('{',' ')
			line = line.replace('&',' ')
			line = line.replace('-',' ')
			line = line.replace('"',' ')
			line = line.replace(';',' ')
			line = line.replace("(",' ')
			line = line.replace(")",' ')
			line = line.replace('*','')
			line = line.replace(':',' ')
			line = line.replace('+',' ')
			line = line.replace('$',' ')
			line = line.replace("'",'')
			line = line.replace("=",' ')
			if('<REUTERS' in line):
				docid_previousone = 0 #the first docid must be 0,in order to make difference with later docid

				docid = line[line.find('NEWID'): ]
				docid = docid.replace('"','')
				docid = docid.replace('>','')
				docid = docid.replace('NEWID','')
				docid = docid.replace('=','')

				if(docid != docid_previousone):
					docCounter += 1 #calculate the total number of docs = (N)
					#store the totalDocLen in the docLenStore
					docLenStore[docid] = totalDocLen
					totalDocLen = 0
					#reset totalDocLen

			for word in line.split(' '):
				word = word.strip()
				if(word.lower() == '<body>' or word.lower() == '<title>'):
					flag = True
					pass
				elif(word.lower() == '</body>' or word.lower() == '</title>'):
					flag = False
					pass
				elif flag:
					if(word==' ' or word == '' or '&#' in word or '/' in word or '[' in word or ']' in word or '@' in word or '=' in word or '?' in word or '#' in word or '&' in word ):
						pass
					elif(word.isdigit()): #remove numbers
						numbers += 1
						pass
					elif stopwords_150(word): #remove 150 stopwords
						stopwords += 1
						pass
					# elif(word.isupper()): # case folding
					# 	word = word.lower()
					# 	pass
					else:
						word = word.replace('<','')
						word = word.replace('>','')
						word = word.lower()#case folding
						totalDocLen += 1
						if word in tokendict:
							#check whether has the same docid
							if tokendict[word].has_key(docid):
								tokendict[word][docid] += 1
							else:
								tokendict[word][docid] = 1
						else:
							tokendict[word] = {}
							tokendict[word][docid] = 1

#---------------------checking size memory, if full(sort them) , write into a file as a block file and free the memory----------

				if ((sys.getsizeof(tokendict)/1024) >= memorylimit):
					fileCounter = fileCounter + 1
					tokendict = collections.OrderedDict(sorted(tokendict.items()))
					#filename = 'final_dict.json'
					filename = "file" + str(fileCounter) +".json"
					data_string = json.dumps(tokendict,encoding = 'latin-1')
					target = open(filename,'w')
					target.write(data_string)
					target.close()
					tokendict.clear()
					filename_doclenStore = "doclenStore.json"
					data_string1 = json.dumps(docLenStore)
					target1 = open(filename_doclenStore,'w')
					target1.write(data_string1)
					target1.close()
#if the block is not fulled in final,we need to get this part too
tokendict = collections.OrderedDict(sorted(tokendict.items()))

#calculate avgdoclen
totalLen = 0
for docid, docLen in docLenStore.items():
	totalLen += docLen
avgdoclen = totalLen/len(docLenStore)
print avgdoclen

#data_string = unicode(json.dumps(tokendict),errors = 'ignore')
data_string = json.dumps(tokendict,encoding = 'latin-1')
target = open(filename,'w')
target.write(data_string)
target.close()
filename_doclenStore = "doclenStore.json"
data_string1 = json.dumps(docLenStore)
target1 = open(filename_doclenStore,'w')
target1.write(data_string1)
target1.close()
#---------------------merge blocks----------------------------------------------------------------------
#pay attention that when merge them ,need to check the term part
mergeCounter = 0
final_dict={}
#print '-------------file counter: ',fileCounter~~~
#merge each small dictionary(merge those json file)
for mergeCounter in range(fileCounter + 1):
	filename = "file"+str(mergeCounter)+".json"
	with open(filename,'r') as dict2:
		dict2 = json.load(dict2)
		final_dict = merge_tokenDicts(final_dict,dict2)
#merge this dictionary docLenStore-->ignore
filename = "final_dict.json"
data_string = json.dumps(final_dict)
target = open(filename,'w')
target.write(data_string)
target.close()

print '# of numbers deleted = ', numbers
print '# of stopwords deleted = ', stopwords
#---------------------Quary part------------------------------
match1 = {}
query_resluts = {}

final_result=[]# an empty smallList, in order to do the insection operation,and store the final_result in final
andFlag = False
orFlag = False
queryFlag = True
query_list=[] # store the query words

while queryFlag:
	query = raw_input("--------Please enter your Query-----------\n\n")
	singleResultList = []
	query_list = query.split(' ')
	print query_list
	#single word query
	if len(query_list) == 1:
		#query_resluts = findMatch(query)
		final_result = findMatch(query)
		print 'The result of',query,'is',final_result#query_resluts
		Ranking(query_list,final_result)
		# if(len(final_result) > 0):
		# 	doc_ranking = calculate_RSVd(query_list,final_result)
		# 	if len(doc_ranking) == 1:
		# 		print doc_ranking
		# 	else:
		# 	#sort based on ranking
		# 		print sorted(doc_ranking.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)# decrese ordering
		# 	doc_ranking.clear()

	#multiple word query
	else:#and operation (multiple and)
		#if 'and' in query_list:
		for word in query_list:
				#do single query for each word and get the interaction of their results
			if (word == 'and' or word == 'or'):
					#query_list.remove('and')
				pass
			else: #do single query for each word
				list_of_matchedItems = findMatch(word)
				singleResultList.append(list_of_matchedItems)
				print('word is:',word,findMatch(word))   #('word is: ', {'textile': [354, 429, 867, 891, 956, 1002, 1197, 1226, 1509, 1594, 1809, 1955]})
					#have multiple singleQuery results,
		print 'Consumed time =',time.clock()-start,'ms'
			#do interaction
		p = 0
		final_result = singleResultList[0]
		for index in xrange(1, len(singleResultList)):

			final_result = list(set(final_result) & set(singleResultList[index]))
		print 'The final result is:',final_result
		Ranking(query_list,final_result)

#---------------------------for the Ranking part------------------------------
#just use Ranking function() to simplify!!!
#for each doc in final_result, do the RSVd ranking, and bound rankingscore with docid
		# if(len(final_result) > 0):
		# 	doc_ranking = calculate_RSVd(query_list,final_result)
		# 	if len(doc_ranking) == 1:
		# 		print doc_ranking
		# 	else:
		# 	#sort based on ranking
		# 		print sorted(doc_ranking.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)# decrese ordering
		# 	doc_ranking.clear()






#tokenize--->spimi---->(inverted index)//check size,sort,wirte into q block file

#remove stop word,ask alaa (check)

#open block files,merge them into a big dictionary(consider the data structure(use dictionary{,dictinary{, tuple}} & which part need to be recorded)
#using the dictionary,realize the query(single word, and,or),print the result out

#and operation,do the insection operation or two lists
#or operation, just add them together




#calculate the formula,print the result out


#lengthCouter if docid changes, record the len of the doc,and record it into dictionary
