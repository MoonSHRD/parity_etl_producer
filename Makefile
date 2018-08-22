UNAME_S := $(shell uname -s)
CURRENT_DIRECTORY = $(shell pwd)

ifeq ($(UNAME_S),Linux)
	PLATFORM = linux
endif


.PHONY: all clean

all: build


build:
	mkdir -p build/contracts
	go build -o build/contracts/token_factory:0.1.0 contracts/token_factory/factory.go


clean:
	go clean
	rm -rf build

