COMPILER=clang++
EXEC=preprocessor
COMPILATION_FLAGS=-Werror=vla -Wall -MMD 
LINKER_FLAGS=-lstdc++fs
CPPSTANDARD=c++17

SRCDIR=./src
OBJDIR=./obj
OBJECTS=main.o args.o file.o

OBJECTPATHS=$(call addprefix, ${OBJDIR}/, ${OBJECTS})
DEPENDSPATHS=${OBJECTPATHS:.o=.d}

.PHONY: clean debug compile link

${EXEC}: compile link
-include ${DEPENDSPATHS}

# Individual File Compilation Target
${OBJDIR}/%.o: ${SRCDIR}/%.cc
	# $@ --> is the name of the makefile target
	# $< is the name of the first prerequisite
	${COMPILER} $< -std=${CPPSTANDARD} -c -o $@ ${COMPILATION_FLAGS}


debug: COMPILATION_FLAGS+=-g 
debug: ${EXEC}

compile: $(OBJECTPATHS)
	@echo Compiled

link: 
	${COMPILER} ${OBJDIR}/*.o ${COMMON_OBJS_PATHS} -o ${EXEC} ${LINKER_FLAGS}
	@echo Linking Complete

clean:
	rm -f ${OBJDIR}/* ${EXEC}