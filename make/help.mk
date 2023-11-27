########
# Help #
########

.DEFAULT_GOAL := help

DASH_HELP = \
	Usage: make [$(DASH_COLOR_INFO)command$(DASH_COLOR_RESET)] \
	$(call dash_help_section, Help) \
	$(call dash_help,help,This help)

define dash_help_section
	\n\n$(DASH_COLOR_COMMENT)$(strip $(1)):$(DASH_COLOR_RESET)
endef

define dash_help
  \n  $(DASH_COLOR_INFO)$(1)$(DASH_COLOR_RESET) $(2)
endef

help:
	@printf "\n$(DASH_HELP)"
	@awk ' \
		BEGIN { \
			sectionsName[1] = "Commands" ; \
			sectionsCount = 1 ; \
		} \
		/^[-a-zA-Z0-9_.@%\/+]+:/ { \
			if (match(lastLine, /^## (.*)/)) { \
				command = substr($$1, 1, index($$1, ":") - 1) ; \
				section = substr(lastLine, RSTART + 3, index(lastLine, " - ") - 4) ; \
				if (section) { \
					message = substr(lastLine, index(lastLine, " - ") + 3, RLENGTH) ; \
					sectionIndex = 0 ; \
					for (i = 1; i <= sectionsCount; i++) { \
						if (sectionsName[i] == section) { \
							sectionIndex = i ; \
						} \
					} \
					if (!sectionIndex) { \
						sectionIndex = sectionsCount++ + 1 ; \
						sectionsName[sectionIndex] = section ; \
					} \
				} else { \
					message = substr(lastLine, RSTART + 3, RLENGTH) ; \
					sectionIndex = 1 ; \
				} \
				if (length(command) > sectionsCommandLength[sectionIndex]) { \
					sectionsCommandLength[sectionIndex] = length(command) ; \
				} \
				sectionCommandIndex = sectionsCommandCount[sectionIndex]++ + 1; \
				helpsCommand[sectionIndex, sectionCommandIndex] = command ; \
				helpsMessage[sectionIndex, sectionCommandIndex] = message ; \
			} \
		} \
		{ lastLine = $$0 } \
		END { \
			for (i = 1; i <= sectionsCount; i++) { \
				if (sectionsCommandCount[i]) { \
					printf "\n\n$(DASH_COLOR_COMMENT)%s:$(DASH_COLOR_RESET)", sectionsName[i] ; \
					for (j = 1; j <= sectionsCommandCount[i]; j++) { \
						printf "\n  $(DASH_COLOR_INFO)%-" sectionsCommandLength[i] "s$(DASH_COLOR_RESET) %s", helpsCommand[i, j], helpsMessage[i, j] ; \
					} \
				} \
			} \
		} \
	' $(MAKEFILE_LIST)
	@printf "\n\n"
	@printf "$(if $(DASH_HELP_PROJECT),$(DASH_HELP_PROJECT)\n\n)"
.PHONY: help

help.project:
	@printf "$(if $(DASH_HELP_PROJECT),\n$(DASH_HELP_PROJECT)\n\n)"
