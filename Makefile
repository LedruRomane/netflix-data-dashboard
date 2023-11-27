# --------------------------------#
# "make" command
# --------------------------------#

-include ./make/text.mk
-include ./make/help.mk
-include ./make/url.mk

###########
#   Run   #
###########

## Run the server
run:
	python3 ./Dash/index.py