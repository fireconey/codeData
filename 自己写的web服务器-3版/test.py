import copy

html="""
<html>
	<body>
		
	</body>
</html>

"""
class  RenderTemplate():
	# var用于接收代码执行后的数据
	var=""
	#splitStart:文本中代码开始的标记
	#splitEnd:文本中代码结束的标记
	def __init__(self,splitStart="py:",splitEnd=":py"):
		self.splitStart=splitStart
		self.splitEnd=splitEnd

	def write(self,text):
		self.var+=str(text)+"\n"

	#使代码左对齐
	#code:文本得到中的代码
	def deletTable(self,code):
		code=code
		table=""
		ttemp=""
		newcde=""
		startTableCount=0
		#由于代码前面有一定数量的\t所有要计算
		#总共有多少个\t便于所有所有多于这个数
		#量的\t处减去这么多的\t
		for i in code:
			if i=="\t":
				startTableCount+=1
			elif i=="\n":
				#解决\t\t\t\n\t\t\t代码处
				#如果在前面\t后遇到\n就从
				#新计数。如果\t后遇到代码
				#就表示计算结束
				startTableCount=0
				continue
			else:
			 break
		# 通过循环查看连续的\t有几个：
		# 通过循环计算连续的\t个数，当
		# 遇到其它字符后就开始比较是否
		# 多于指定的个数，如果多就去除
		# 指定数量的\t剩下的保留，同时
		# 计算器置零从新计算连续的\t个
		# 数
		for i in code:
			if i=="\t":
				table+=i
			else:
				if len(table)>=startTableCount:
					newcde+=table[startTableCount:]+i
					table=""
				else:
					newcde+=table+i	
					table=""
		return newcde

	#html:文本
	#args：传入到文本中的参数是字典形式的
	def getHtmlResult(self,html,args):
		result=""
		html=html
		args=args
		splitStart=self.splitStart
		splitEnd=self.splitEnd
		codeListOne=html.split(splitStart)
		if len(codeListOne)<2:
			print("在类RenderTemplate 方法getHtmlResult 中错误:")
			print("\t你的划分方法是'%s'和'%s',在html文件中没有这个标记" %(splitStart,splitEnd))
			print("\t将给你返回原始文本")
			return html
		codeListTwo=[]
		result=""
		codeArgs={"write":self.write}
		codeArgs.update(args)
		for i in codeListOne:
			if  splitEnd in i:
				splitEndPy=i.split(splitEnd)
				#由于执行一次代码是可以多次写入self.var
				#(使用self.var+=)所有要在下一次执行时清
				#空数据
				self.var=""
				exec(self.deletTable(splitEndPy[0]),{},codeArgs)
				result+=str(self.var)+splitEndPy[1]
			else:
				result+=i
		return result

rend=RenderTemplate("{","}")
print(rend.getHtmlResult(html,{"var":10}))

