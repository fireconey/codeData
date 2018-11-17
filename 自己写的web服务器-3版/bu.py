import copy

html="""
<html>
	<body>
			py:									
			def yu(write):
			  	write("9")
			yu(write)
			:py
			
	</body>
</html>

"""
class  RenderTemplate():
	var=""
	result=""
	def __init__(self,html):
		self.html=html
		self.result=self.getHtmlResult(self.html)

	

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
	def write(self,text):
			self.var=text
	def getHtmlResult(self,html):
		html=html
		codeListOne=html.split("py:")
		codeListTwo=[]
		html=""
		
		for i in codeListOne:
			if ":py" in i:
				splitEndPy=i.split(":py")
				exec(self.deletTable(splitEndPy[0]),{},{"write":self.write})
				html+=self.var+splitEndPy[1]
			else:
				html+=i
		print(html)
		return html

print(RenderTemplate(html))




