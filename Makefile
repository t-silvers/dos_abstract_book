include config/common.mk

.PHONY: all help clean

all: clean_responses publish_booklet

# Separate publishing final book from cleaning responses
.PHONY: clean_responses
clean_responses: $(OUT)/.published

.PHONY: publish_booklet
publish_booklet: $(BOOK_POSTERS) $(BOOK_TALKS)

help:
	@echo "TODO: Write help message."

# Check executables
EXECUTABLES = $(PYTHON) $(RCLONE)
K := $(foreach exec,$(EXECUTABLES),\
	$(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

# Get form responses from gdrive
$(OUT):
	$(MKDIR) $@

$(COMPLETE_LOCAL): $(OUT)
	$(RCP) $(COMPLETE_ORIG) $@

# Clean responses and re-publish
$(VENV)/.done:
	$(PYTHON) -m venv $(VENV) && $(VENV)/bin/pip install -r $(CFG)/requirements.txt && touch $@

$(PUBLIC_RESPONSES): $(COMPLETE_LOCAL) $(VENV)/.done
	$(VENV)/bin/python $(SCRIPTS)/original_responses.py $< $@ $(CFG)/responses.ini

$(OUT)/.published: $(PUBLIC_RESPONSES)
	$(RCP) $< $(RCLONE_REMOTE):DoS/$(notdir $<) && touch $@

# ------------------
#
# [Via Google Workspace GUI] Convert to Google sheet
# 	Open with > Google Sheets
#
# [Via Google Workspace GUI] Prepare for release
# 	View more row actions > Freeze up to row 1
# 	Text wrapping > Clip

# [Via Google Workspace GUI] Release cleaned responses
#
# ------------------

# Prepare amended responses
.PHONY: cleaned
cleaned: $(OUT)/._published
$(OUT)/._published:
	if [ -f $(OUT)/.published ]; then touch $@; fi

$(AMENDED_LOCAL): $(OUT)/._published
	$(RCP) $(AMENDED_ORIG) $@

$(BOOK_POSTERS) $(BOOK_TALKS): $(AMENDED_LOCAL)
	$(VENV)/bin/python $(SCRIPTS)/make_booklet.py $< $(BOOKDIR)

# ------------------
#
# [Via External Typesetter] Compile booklet as PDF
# 	Open with > Google Sheets
#
# ------------------

clean:
	rm -f $(COMPLETE_LOCAL) $(PUBLIC_RESPONSES) $(OUT)/.published $(OUT)/._published $(AMENDED_LOCAL) $(BOOK_POSTERS) $(BOOK_TALKS)