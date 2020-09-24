COMPILER=clang++
EXEC=searchEngine
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
OTHER_OBJS=
OTHER_PATHS=$(call addprefix, ${OBJDIR}/, ${OTHER_OBJS})
TEST_OBJS=
TEST_PATHS=$(call addprefix, ${TEST_OBJDIR}/, ${TEST_OBJS})

OBJECTPATHS=${MAIN_PATH} ${OTHER_PATHS}
DEPENDSPATHS=${OBJECTPATHS:.o=.d}

.PHONY: clean debug compile link test

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


debug: COMPILATION_FLAGS+=-g -fsanitize=address -fno-omit-frame-pointer -fno-optimize-sibling-calls -O1 
debug: LINKER_FLAGS+=-fsanitize=address -fno-omit-frame-pointer -fno-optimize-sibling-calls -O1 
debug: ${EXEC}

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

