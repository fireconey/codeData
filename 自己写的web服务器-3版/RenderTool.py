import copy


html="""
<html>
	<body>
	#如果要在文本对应代码处写入运行后的
	#值,则要使用文本写入功能函数,要在
	#函数中使用参数默认。运行函数时默认
	#的传递参数是write：注意一定不能修
	#改。其他的参数可以修改。
	{
	def function(var):
		write("<div>hello world</div>")
		print(var,"5555555")
	function(var)
	
	}
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
	def getHtmlResult(self,html,args={}):
		result=""
		html=html
		args=args
		splitStart=self.splitStart
		splitEnd=self.splitEnd
		codeListTwo=[]
		result=""
		codeListOne=html.split(splitStart)
		if len(codeListOne)<2:
			print("\n在类RenderTemplate 方法getHtmlResult 中错误:")
			print("\t你的划分方法是'%s'和'%s',在html文件中没有这个标记" %(splitStart,splitEnd))
			print("\t将给你返回原始文本\n")
			return html
		for i in codeListOne:
			if  splitEnd in i:
				splitEndPy=i.split(splitEnd)
				#由于执行一次代码是可以多次写入self.var
				#(使用self.var+=)所有要在下一次执行时清
				#空数据
				self.var=""
				try:
					exec(self.deletTable(splitEndPy[0]),{"write":self.write},args)
				except:
					print("\n在类RenderTemplate 方法getHtmlResult 中错误:")
					print("\t在html中有的参数没有获取值或表达式错误\n")
					return  "None"
				result+=str(self.var)+splitEndPy[1]
			else:
				result+=i
		return result


#使用方法：
#1、初始化时可以指定代码中的开始标记和结束标记，
#如果不指定默认是py:和:py。
#2、getHtmlResult第一个参数是要渲染的文本第二个
#参数是要传入到文本中的变量是字典形式。在使用的
#时候使用字典获取
# rend=RenderTemplate("{","}")
# print(rend.getHtmlResult(html,{"var":10}))

