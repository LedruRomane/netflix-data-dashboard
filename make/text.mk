##########
# Colors #
##########

DASH_COLOR_RESET   := \033[0m
DASH_COLOR_ERROR   := \033[31m
DASH_COLOR_INFO    := \033[32m
DASH_COLOR_WARNING := \033[33m
DASH_COLOR_COMMENT := \033[36m

######################
# Special Characters #
######################

# Usage:
#   $(call dash_message, Foo$(,) bar) = Foo, bar
#   $(call dash_message, $(lp)Foo bar) = (Foo bar
#   $(call dash_message, Foo$(rp) bar) = Foo) bar

, := ,
lp := (
rp := )

########
# Time #
########

# Usage:
#   $(call dash_time) = 11:06:20

define dash_time
`date -u +%T`
endef

###########
# Message #
###########

# Usage:
#   $(call dash_message, Foo bar)         = Foo bar
#   $(call dash_message_success, Foo bar) = (っ◕‿◕)っ Foo bar
#   $(call dash_message_warning, Foo bar) = ¯\_(ツ)_/¯ Foo bar
#   $(call dash_message_error, Foo bar)   = (╯°□°)╯︵ ┻━┻ Foo bar

define dash_message
	printf "$(DASH_COLOR_INFO)$(strip $(1))$(DASH_COLOR_RESET)\n"
endef

define dash_message_success
	printf "$(DASH_COLOR_INFO)(っ◕‿◕)っ $(strip $(1))$(DASH_COLOR_RESET)\n"
endef

define dash_message_warning
	printf "$(DASH_COLOR_WARNING)¯\_(ツ)_/¯ $(strip $(1))$(DASH_COLOR_RESET)\n"
endef

define dash_message_error
	printf "$(DASH_COLOR_ERROR)(╯°□°)╯︵ ┻━┻ $(strip $(1))$(DASH_COLOR_RESET)\n"
endef

#######
# Log #
#######

# Usage:
#   $(call dash_log, Foo bar)         = [11:06:20] [target] Foo bar
#   $(call dash_log_warning, Foo bar) = [11:06:20] [target] ¯\_(ツ)_/¯ Foo bar
#   $(call dash_log_error, Foo bar)   = [11:06:20] [target] (╯°□°)╯︵ ┻━┻ Foo bar

define dash_log
	printf "[$(DASH_COLOR_COMMENT)$(call dash_time)$(DASH_COLOR_RESET)] [$(DASH_COLOR_COMMENT)$(@)$(DASH_COLOR_RESET)] " ; $(call dash_message, $(1))
endef

define dash_log_warning
	printf "[$(DASH_COLOR_COMMENT)$(call dash_time)$(DASH_COLOR_RESET)] [$(DASHCOLOR_COMMENT)$(@)$(DASH_COLOR_RESET)] "  ; $(call dash_message_warning, $(1))
endef

define dash_log_error
	printf "[$(DASH_COLOR_COMMENT)$(call dash_time)$(DASH_COLOR_RESET)] [$(DASHCOLOR_COMMENT)$(@)$(DASH_COLOR_RESET)] " ;  $(call dash_message_error, $(1))
endef

###########
# Confirm #
###########

# Usage:
#   $(call dash_confirm, Foo bar) = ༼ つ ◕_◕ ༽つ Foo bar (y/N):
#   $(call dash_confirm, Bar foo, y) = ༼ つ ◕_◕ ༽つ Foo bar (Y/n):

define dash_confirm
	$(if $(CONFIRM),, \
		printf "$(DASH_COLOR_INFO) ༼ つ ◕_◕ ༽つ $(DASH_COLOR_WARNING)$(strip $(1)) $(DASH_COLOR_RESET)$(DASH_COLOR_WARNING)$(if $(filter y,$(2)),(Y/n),(y/N))$(DASH_COLOR_RESET): " ; \
		read CONFIRM ; \
		case $$CONFIRM in $(if $(filter y,$(2)), \
			[nN]$(rp) printf "\n" ; exit 1 ;; *$(rp) ;;, \
			[yY]$(rp) ;; *$(rp) printf "\n" ; exit 1 ;; \
		) esac \
	)
endef

################
# Conditionals #
################

# Usage:
#   $(call dash_error_if_not, $(FOO), FOO has not been specified) = (╯°□°)╯︵ ┻━┻ FOO has not been specified

define dash_error_if_not
	$(if $(strip $(1)),, \
		$(call dash_message_error, $(strip $(2))) ; exit 1 \
	)
endef

# Usage:
#   $(call dash_confirm_if, $(FOO), Foo bar) = ༼ つ ◕_◕ ༽つ Foo bar (y/N):

define dash_confirm_if
	$(if $(strip $(1)), \
		$(call dash_confirm, $(strip $(2)))
	)
endef

# Usage:
#   $(call dash_confirm_if_not, $(FOO), Foo bar) = ༼ つ ◕_◕ ༽つ Foo bar (y/N):

define dash_confirm_if_not
	$(if $(strip $(1)),, \
		$(call dash_confirm, $(strip $(2)))
	)
endef

##########
# Random #
##########

# Usage:
#   $(call dash_rand, 8) = 8th56zp2

define dash_rand
`cat /dev/urandom | LC_ALL=C tr -dc 'a-z0-9' | fold -w $(strip $(1)) | head -n 1`
endef
