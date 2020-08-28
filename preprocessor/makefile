COMPILER=clang++
EXEC=preprocessor
TESTEXEC=unitTests
COMPILATION_FLAGS=-Werror=vla -Wall -MMD -stdlib=libc++
LINKER_FLAGS=-lc++abi -lc++
#-lstdc++fs
TEST_LINK_FLAGS=-lgtest_main -lgtest -lpthread
CPPSTANDARD=c++17

SRCDIR=./src
OBJDIR=./obj
TEST_OBJDIR=./test_obj
TESTDIR=./test

MAIN_OBJ=main.o
MAIN_PATH=$(call addprefix, ${OBJDIR}/, ${MAIN_OBJ})
OTHER_OBJS=args.o file.o preprocessor.o
OTHER_PATHS=$(call addprefix, ${OBJDIR}/, ${OTHER_OBJS})
TEST_OBJS=preprocessor.test.o
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


debug: COMPILATION_FLAGS+=-g 
debug: ${EXEC}

compile: $(OBJECTPATHS)
	@echo Compiled

link: 
	${COMPILER} ${OBJDIR}/*.o -o ${EXEC} ${LINKER_FLAGS}
	@echo Linking Complete

clean:
	rm -f ${OBJDIR}/* ${EXEC}

test: ${OTHER_PATHS} ${TEST_PATHS}
	${COMPILER} ${OTHER_PATHS} ${TEST_PATHS} -o ${TESTEXEC} ${LINKER_FLAGS} ${TEST_LINK_FLAGS} 

