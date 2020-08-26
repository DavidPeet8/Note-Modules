
#include "../src/preprocessor.h"
#include "gtest/gtest.h"


class PreprocessorTest : public ::testing::Test 
{
protected:
	PreprocessorTest()
	{

	}

	~PreprocessorTest()
	{

	}

	void SetUp() override 
	{

	}

	void TearDown() override
	{

	}

};

TEST_F(PreprocessorTest, ConvertsFromStringToEnum) 
{
	EXPECT_EQ(Preprocessor::strToCmdType("include"), Preprocessor::CmdType::INCLUDE);
	EXPECT_EQ(Preprocessor::strToCmdType("link"), Preprocessor::CmdType::LINK);
	EXPECT_EQ(Preprocessor::strToCmdType("nobuild"), Preprocessor::CmdType::NOBUILD);
}

TEST_F(PreprocessorTest, CmdParsesBasicArgString)
{
	Preprocessor::Cmd cmd(Preprocessor::CmdType::INCLUDE, "arg1 arg2 arg3");
	const auto & targets = cmd.getTargets();
	const std::vector<std::string> expected{"arg1", "arg2", "arg3"};

	if (expected.size() != targets.size()) 
	{
		FAIL() << "Expected " << expected.size() << " Arguments, saw " << targets.size();
	}

	for (int i = 0; i < targets.size(); i++) 
	{
		EXPECT_EQ(targets[i], expected[i]);
	}
}

TEST_F(PreprocessorTest, CmdParsesQuotedArgString)
{
	Preprocessor::Cmd cmd(Preprocessor::CmdType::INCLUDE, "arg1 \"arg2 arg3\" arg4");
	const auto & targets = cmd.getTargets();
	const std::vector<std::string> expected{"arg1", "arg2 arg3", "arg4"};

	if (expected.size() != targets.size()) 
	{
		FAIL() << "Expected " << expected.size() << " Arguments, saw " << targets.size();
	}

	for (int i = 0; i < targets.size(); i++) 
	{
		EXPECT_EQ(targets[i], expected[i]);
	}
}

TEST_F(PreprocessorTest, CmdParsesMultiSpaceArgString)
{
	Preprocessor::Cmd cmd(Preprocessor::CmdType::INCLUDE, " arg1       arg2 arg3  arg4  ");
	const auto & targets = cmd.getTargets();
	const std::vector<std::string> expected{"arg1", "arg2", "arg3", "arg4"};

	if (expected.size() != targets.size()) 
	{
		FAIL() << "Expected " << expected.size() << " Arguments, saw " << targets.size();
	}

	for (int i = 0; i < targets.size(); i++) 
	{
		EXPECT_EQ(targets[i], expected[i]);
	}
}

TEST_F(PreprocessorTest, CmdParsesQuoteStringAtEndArgString)
{
	Preprocessor::Cmd cmd(Preprocessor::CmdType::INCLUDE, " arg1       arg2 \"arg3  arg4  \"");
	const auto & targets = cmd.getTargets();
	const std::vector<std::string> expected{"arg1", "arg2", "arg3  arg4  "};

	if (expected.size() != targets.size()) 
	{
		FAIL() << "Expected " << expected.size() << " Arguments, saw " << targets.size();
	}

	for (int i = 0; i < targets.size(); i++) 
	{
		EXPECT_EQ(targets[i], expected[i]);
	}
}

TEST_F(PreprocessorTest, ParsesRawCommand)
{
	Preprocessor::Cmd cmd = Preprocessor::getCmd("[//]:#(include other arguments \"this is all one arg\")");
	EXPECT_EQ(cmd.getType(), Preprocessor::CmdType::INCLUDE);
	const auto & targets = cmd.getTargets();
	const std::vector<std::string> expected {"other", "arguments", "this is all one arg"};

	if (expected.size() != targets.size()) 
	{
		FAIL() << "Expected " << expected.size() << " Arguments, saw " << targets.size();
	}

	for (int i = 0; i < targets.size(); i++) 
	{
		EXPECT_EQ(targets[i], expected[i]);
	}
}