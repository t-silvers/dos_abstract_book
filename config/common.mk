DIR ?= /Users/thomassilvers/dev/projects/booklet_maker

CFG := $(DIR)/config
OUT := $(DIR)/results
SCRIPTS := $(DIR)/scripts
VENV := $(DIR)/venv

BOOKDIR := $(OUT)/dos_booklet

MKDIR := mkdir -p
PYTHON ?= /Users/thomassilvers/mambaforge/bin/python
# PYTHON ?= /usr/bin/python
RCLONE ?= /usr/local/bin/rclone
RCLONE_REMOTE ?= mpg_gdrive
RCP := rclone copyto

HOST := $(RCLONE_REMOTE):DoS
# Note: Must use extension for rclone copyto to work
AMENDED_ORIG := "$(HOST)/registration_responses.xlsx"
COMPLETE_ORIG := "$(HOST)/DoS2023Registration (Responses).xlsx"

AMENDED_LOCAL := $(OUT)/amended_registration_responses.xlsx
COMPLETE_LOCAL := $(OUT)/raw_registration_responses.xlsx
PUBLIC_RESPONSES := $(OUT)/registration_responses.csv
BOOK_POSTERS := $(BOOKDIR)/posters.tex
BOOK_TALKS := $(BOOKDIR)/talks.tex

SMOKE_TEST ?= 0
export SMOKE_TEST

.SHELLFLAGS := -eu -o pipefail -c
.ONESHELL:
.DELETE_ON_ERROR: