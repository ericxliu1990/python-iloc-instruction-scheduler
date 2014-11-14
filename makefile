# If the first argument is "run"...
ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

ifeq (sim,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

run:
	@scheduler $(RUN_ARGS)
INPUT = $(shell cat $(RUN_ARGS) | egrep INPUT | awk '{for(i = 3; i <= NF; i++){printf "%s ",$$i}}')
OUTPUT = $(shell cat $(RUN_ARGS) | egrep OUTPUT | awk '{for(i = 2; i <= NF; i++){printf "%s ",$$i}}')
sim:
	@scheduler $(RUN_ARGS) > a.i
	@echo "The origin result" $(OUTPUT)
	@lab3sim/sim < $(RUN_ARGS) $(INPUT)
	@echo "My result" $(OUTPUT)
	@lab3sim/sim < a.i $(INPUT)
	@rm -f a.i
profile:
	python -m cProfile -s 'tottime' source/iloc_instruction_scheduler.py timing/T8k.i | head -15