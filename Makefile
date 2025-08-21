DATE=$(shell date +"%Y年%m月%d日")
NEW_GRAPH_FILE=content/generated/new.txt
REVIEW_GRAPH_FILE=content/generated/revs.txt
NEW_GRAPH=$(cat NEW_GRAPH_FILE)
REVIEW_GRAPH=$(cat REVIEW_GRAPH_FILE)
TMP_MD := content/tmp_index.md
all: index.html jlpt.html

clean:
	rm -f index.html

graph:
	python graph.py

index.html: content/index.md content/template.html Makefile
	pandoc -s --css src/reset.css --css src/index.css -Vdate=$(DATE) -V -i $< -o $@ --template=content/template.html
jlpt.html: content/jlpt.md content/template.html Makefile $(NEW_GRAPH_FILE) $(REVIEW_GRAPH_FILE)
	awk 'BEGIN { \
	    while ((getline line < "content/generated/new.txt") > 0) new_graph = new_graph line "\n"; \
	    close("content/generated/new.txt"); \
	    while ((getline line < "content/generated/revs.txt") > 0) review_graph = review_graph line "\n"; \
	    close("content/generated/revs.txt"); \
	} \
	{ \
	    gsub("<!--NEW_GRAPH-->", new_graph); \
	    gsub("<!--REVIEW_GRAPH-->", review_graph); \
	    print; \
	}' content/jlpt.md > $(TMP_MD)
	pandoc -s --css src/reset.css --css src/index.css -Vdate="$(DATE)" -i $(TMP_MD) -o $@ --template=content/template.html
	rm $(TMP_MD)
	
.PHONY: all clean
