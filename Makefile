DATE=$(shell date +"%Y年%m月%d日")

all: index.html

clean:
	rm -f index.html

index.html: demo/index.md demo/template.html Makefile
	pandoc -s --css src/reset.css --css src/index.css -Vdate=$(DATE) -i $< -o $@ --template=demo/template.html

.PHONY: all clean
