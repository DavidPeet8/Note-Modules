COMPILER=clang++
EXEC=preprocessor
TESTEXEC=unitTests
COMPILATION_FLAGS=-Werror -Wall -MMD -stdlib=libc++
LINKER_FLAGS=-lc++abi -lc++
CPPSTANDARD=c++17

SRCDIR=./src
OBJDIR=./obj
TEST_OBJDIR=./test_obj
TESTDIR=./test

MAIN_OBJ=main.o
MAIN_PATH=$(call addprefix, ${OBJDIR}/, ${MAIN_OBJ})
OTHER_OBJS=args.o preprocessor.o command.o dfa.o logger.o
OTHER_PATHS=$(call addprefix, ${OBJDIR}/, ${OTHER_OBJS})
TEST_OBJS=preprocessor.test.o
TEST_PATHS=$(call addprefix, ${TEST_OBJDIR}/, ${TEST_OBJS})

OBJECTPATHS=${MAIN_PATH} ${OTHER_PATHS}
DEPENDSPATHS=${OBJECTPATHS:.o=.d}

.PHONY: clean debug compile link test warn error silent _silent info

${EXEC}: compile link
-include ${DEPENDSPATHS}

# Individual File Compilation Target
${OBJDIR}/%.o: ${SRCDIR}/%.cc
	# $@ --> is the name of the makefile target
	# $< is the name of the first prerequisite
	${COMPILER} $< -std=${CPPSTANDARD} -c -o $@ ${COMPILATION_FLAGS}

# Individual File Compilation Target
${TEST_OBJDIR}/%.o: ${TESTDIR}/%.cc
	# $@ --> is the name of the makefile target
	# $< is the name of the first prerequisite
	${COMPILER} $< -std=${CPPSTANDARD} -c -o $@ ${COMPILATION_FLAGS}


debug: COMPILATION_FLAGS+=-g -fsanitize=address -fno-omit-frame-pointer -fno-optimize-sibling-calls -O0 -D LOGLEVEL=4
debug: LINKER_FLAGS+=-fsanitize=address -fno-omit-frame-pointer -fno-optimize-sibling-calls -O0 
debug: ${EXEC}

info: COMPILATION_FLAGS+=-D LOGLEVEL=3 -O2
info: ${EXEC}

warn: COMPILATION_FLAGS+=-D LOGLEVEL=2 -O2
warn: ${EXEC}

error: COMPILATION_FLAGS+=-D LOGLEVEL=1 -O2
warn: ${EXEC}

silent: COMPILATION_FLAGS+=-O2
silent: _silent

_silent: COMPILATION_FLAGS+=-D LOGLEVEL=0
_silent: ${EXEC}

prod: COMPILATION_FLAGS+=-Ofast
prod: _silent

compile: $(OBJECTPATHS)
	@echo Compiled

link: 
	${COMPILER} ${OBJDIR}/*.o -o ${EXEC} ${LINKER_FLAGS}
	@echo Linking Complete

clean:
	rm -f ${OBJDIR}/* ${EXEC}

test: LINKER_FLAGS+=-lgtest_main -lgtest -lpthread
test: ${OTHER_PATHS} ${TEST_PATHS}
	${COMPILER} ${OTHER_PATHS} ${TEST_PATHS} -o ${TESTEXEC} ${LINKER_FLAGS}

