if [ $1 == '' -o $1 == 'en' ]
then 
	make clean
	make html
elif [ $1 == 'zh' ]
then
	make clean
	make gettext
	sphinx-intl update -l zh_CN
	make -e SPHINXOPTS="-D language='zh_CN, en'" html
fi
