COMPILER=clang++
EXEC=preprocessor
TESTEXEC=unitTests
COMPILATION_FLAGS=-Werror -Wall -MMD -stdlib=libc++ -I src/include
LINKER_FLAGS=-lc++abi -lc++
CPPSTANDARD=c++17

SRCDIR=./src
OBJDIR=./obj
TEST_OBJDIR=./test_obj
TESTDIR=./test

MAIN_OBJ=main.o
MAIN_PATH=$(call addprefix, ${OBJDIR}/, ${MAIN_OBJ})
OTHER_OBJS=args.o preprocessor.o command.o dfa.o logger.o arg_utils.o arg_parser.o preprocessor_utils.o
OTHER_PATHS=$(call addprefix, ${OBJDIR}/, ${OTHER_OBJS})
TEST_OBJS=preprocessor.test.o
TEST_PATHS=$(call addprefix, ${TEST_OBJDIR}/, ${TEST_OBJS})
PCH_FILES=io.h other.h datastructs.h
PCH_PATHS=$(call addprefix, src/include/, ${PCH_FILES})
PCH_INCL1=$(call addsuffix,.gch, ${PCH_PATHS})
PCH_INCL=$(call addprefix, -include-pch , ${PCH_INCL1})


OBJECTPATHS=${MAIN_PATH} ${OTHER_PATHS}
DEPENDSPATHS=${OBJECTPATHS:.o=.d}

.PHONY: clean debug compile link test warn error silent _silent info symbols gen_pch use_pch

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


symbols: COMPILATION_FLAGS+=-g -D LOGLEVEL=0 -O0
symbols: ${EXEC}

debug: COMPILATION_FLAGS+=-g -fsanitize=address -fno-omit-frame-pointer -fno-optimize-sibling-calls -O0 -D LOGLEVEL=4
debug: LINKER_FLAGS+=-fsanitize=address -fno-omit-frame-pointer -fno-optimize-sibling-calls -O0 
debug: ${EXEC}

info: COMPILATION_FLAGS+=-D LOGLEVEL=3 -O2
info: ${EXEC}

warn: COMPILATION_FLAGS+=-D LOGLEVEL=2 -O2
warn: ${EXEC}

error: COMPILATION_FLAGS+=-D LOGLEVEL=1 -O2
error: ${EXEC}

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

gen_pch:
	${COMPILER} -Wall -stdlib=libc++ -std=${CPPSTANDARD} ${PCH_PATHS}

pch_debug: COMPILATION_FLAGS+=${PCH_INCL} debug
pch_info: COMPILATION_FLAGS+=${PCH_INCL} info
pch_warn: COMPILATION_FLAGS+=${PCH_INCL} warn
pch_error: COMPILATION_FLAGS+=${PCH_INCL} error
pch_silent: COMPILATION_FLAGS+=${PCH_INCL} silent
use_pch: COMPILATION_FLAGS+=${PCH_INCL} 
use_pch: ${EXEC}
